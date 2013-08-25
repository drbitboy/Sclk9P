"""
Usage:

  python ttmodel.py all_scutemp.txt \\
    [--sf=#samples/smoothingFactor, default=150] \\
    [--k=initial time slope as a multiple of net slope, default=-.01383] \\
    [--p1=dRate/dTemperature, ppm/degC, default=-.65] \\
   

"""
import os
import sys
import numpy
import matplotlib.pyplot as plt
import smoothtemps
import timediffs
import spice


########################################################################
def setupTemperatures(lotime=None,verbose='verbose' in sys.argv[1:]):

  ### Use smoothtmeps.SmoothDiTemps class to get temperature data
  smoothditemps = smoothtemps.SmoothDiTemps(verbose=verbose)

  ### Get DII and DIF smoothed temperatures at 60s intervals
  smoothTimes, diiSmooth, difSmooth = smoothditemps.smoothedTTs(60.,lotime=lotime)

  ### Return those, plus DII-DIF differences between smoothed data

  return smoothTimes, diiSmooth, difSmooth, diiSmooth - difSmooth, smoothditemps


########################################################################
def setupTimeDiffs():

  ### Get DII & DIF time correlation data for approach, suspect point,
  ### and TOI times
  diDiffs,diBadDiffs, diTOIDiff = timediffs.parsedoclines()

  ### Build good and supect arrays of DII-DIF time differences
  ### - append 1.0 to prep goods for least-squares fit to remove slope
  goods = numpy.array( [ [i.imFbDiff,i.imFracSec,1.0] for i in diDiffs ] )
  bads = numpy.array( [ [i.imFbDiff,i.imFracSec] for i in diBadDiffs ] )

  ### Do least squares fit to good data
  A = goods[:,1:3].copy()             ### A i.e. [[t0,1],[t1,1],...]
  y = goods[:,0].copy()               ### y
  nll = numpy.linalg.lstsq( A, y )    ### ... do fit ...
  m,c = nll[0]                        ### x  i.e. y =  Ax

  ### Subtract fit from data, so mX+b becomes y=0; enhances deviations visually
  goods[:,0] = goods[:,0] - (m * goods[:,1] + c)
  bads[:,0] = bads[:,0] - (m * bads[:,1] + c)
  diTOIDiff.imFbDiff -= m * diTOIDiff.imFracSec + c

  ### Flatten data
  diffsAbstimes, diffsNets = goods[:,1].flatten(), goods[:,0].flatten()

  ### Select first data group i.e. within ~1h of first point
  iw = numpy.where( (diffsAbstimes-diffsAbstimes[0]) < 3610 )

  diffsGroup0 = numpy.mean( diffsAbstimes[iw] ), numpy.mean( diffsNets[iw] )
  
  return diffsAbstimes, diffsNets, diffsGroup0, m, bads, diTOIDiff


########################################################################
def model2par( paramDeltaRateppm0, paramPpmPerDegC, deltaTime0, smoothTimes, deltaDegC):
  """
  Two-parameter model:

    Part 1:  at each time T=t, calculate differential rate DII-DIF SCUs

      deltaRateppm(T=t) = deltaRateppm(T=0) + ppmPerDegC * ( deltaDegC(T=t) - deltaDegC(T=0) )

      - function only of delta-temperature DII-DIF SCUs

        - Assumes thermal rate change with temperature is same for both DII and DIF SCUs

        - Uses measured delta-temperature and assumed rate (arg paramDeltaRateppm0) at t=0

    Part 2:  integrate differential rate over time period deltaT

      deltaTime(T=t+deltaT) = deltaTime(T=t) + deltaRateppm(T=t) * 1E-6 * deltaT

  """

  ### Assume time steps are constant
  constantTimeDelta = (smoothTimes[1]-smoothTimes[0])

  ### Simplification:  separate paramDeltaRateppm0 (initial drift rate)
  ### from dRate/dTemperature
  deltaTimes = deltaTime0 + (paramDeltaRateppm0 * 1e6) * (smoothTimes - smoothTimes[0])

  ### Integrate delta-temperatures after subtracting initial delta-temperature
  cumDegC = numpy.cumsum( deltaDegC - deltaDegC[0] )

  ### Scale integrated delta-temperatures by frequency temperature
  ### dependence, ppm/degC to get integrated delta-times
  cumDeltaTimes = cumDegC * (paramPpmPerDegC * 1e-6) * constantTimeDelta

  ### add integrated delta-times to linear delta times to get total delta-times
  deltaTimes = deltaTimes + cumDeltaTimes

  return deltaTimes


########################################################################
class DITwoParamModel:
  """
  DI (DII-DIF) SCLK differences two-parameter model

  Attributes:

  (DII-DIF) SCLK differences as a function of DII SCLK

    .diffsAbstimes  - DII SCLK times of diffsNets, good groups flattened and appended
    .diffsNets      - (DII-DIF) SCLK differences at diffsAbstimes, good groups
    .diffsGroup0    - mean (DII SCLK, (DII-DIF) SCLK difference) of first group
    .m              - Average slope of diffAbstimes vs. diffsNets
    .bads           - suspect SCLK difference point(s)
      .bads[:,0]      - DII Times
      .bads[:,1]      - (DII-DIF) SCLK Differences ad bads[:,0]
    .diTOIDiff      - Object with TOI info
      ".imFracSec     - DII SCLK at TOI
      ".imFbDiff      - (DII-DIF) SCLK difference at TOI


  Smoothed temperature as a function of time

    .smoothTimes    - Times of smoothed DI temperature
    .diiSmooth      - Smoothed DII temperatures at smoothTimes
    .difSmooth      - Smoothed DIF temperatures at smoothTimes
    .diffSmooth     - Smoothed DI temperature differences, diiSmooth - difSmooth
    .smoothditemps  - smoothtemps.SmoothDiTemps object with DI temperatures
      ".diitimes()    - Raw input DII times
      ".diitemps()    - Raw input DII temperatures
      ".diftimes()    - Raw input DIF times
      ".diftemps()    - Raw input DIF temperatures

  .model2parNets    - Modeled (DII-DIFF) SCLK differences at smoothTimes

  """

  ######################################################################
  def __init__(self):
    """
    k = initial slope as multiple of mean slope
    p1 = rate temperature dependence, ppm/degC
    """

    ### Get times, time differences, mean slope, suspect points, TOI point
    self.diffsAbstimes, self.diffsNets, self.diffsGroup0, self.m, self.bads, self.diTOIDiff =  setupTimeDiffs()

    ### Read temperatures from filename sys.argv[1], smooth them on 60s interval
    self.smoothTimes, self.diiSmooth, self.difSmooth, self.diffSmooth, self.smoothditemps = setupTemperatures(lotime=self.diffsGroup0[0])


  ######################################################################
  def sumofsquaredErrors(self):
    diffErrors = numpy.interp( self.diffsAbstimes, self.smoothTimes, self.model2parNets ) - self.diffsNets
    return numpy.sum( diffErrors * diffErrors )


  def makemodel( self, k, p1 ):
    ### Set initial slope of model
    self.k, self.p0, self.p1 = k, self.m * k * 1e-6, p1

    ### Modeled (DII-DIFF) SCLK differences at smoothTimes
    self.model2parNets = model2par( self.p0, self.p1, self.diffsGroup0[1], self.smoothTimes, self.diffSmooth )

    self.sose = self.sumofsquaredErrors()

    return self.sose


  ######################################################################
  def doplot(self):

    T0 = 1.73728e8

    tDays = (self.smoothTimes - T0) / 864e2

    title = """
Two-parameter Modeled DII-DIF time difference
with mean slope (mBar) removed
Param0[slope at T=0] = %f ppm (%e * mBar)
Param1 = dFreq/dTemperature = %f ppm/degC
""".strip() % (self.p0,self.k,self.p1,)

    f,(timePlt,tempPlt) = plt.subplots( 2, 1, sharex=True)
    timePlt.title.set_text( title )
    tempPlt.title.set_text( 'Smoothed Temperatures' )
    tempPlt.set_xlabel( 'TOI - T, d' )


    ### Plot DII and DIF raw data as points
    ### Plot smoothed DII and DIF data as lines
    tempPlt.plot( (self.smoothditemps.diitimes()-T0)/864e2,self.smoothditemps.diitemps(), '.', label='DII' )
    tempPlt.plot( tDays,self.diiSmooth,label='DII smooth')

    tempPlt.plot( (self.smoothditemps.diftimes()-T0)/864e2, self.smoothditemps.diftemps(), '.', label='DIF' )
    tempPlt.plot( tDays,self.difSmooth,label='DIF smooth')

    ### Plot DII-DIF differences, offset +10C
    tempPlt.plot( tDays,10+self.diffSmooth,label='Smooth diff (DII-DIF) + 10')

    tempPlt.legend(loc='center left')

    timePlt.plot( (self.diffsGroup0[0]-T0)/864e2, self.diffsGroup0[1], 'o', label='GoodAvg' )
    timePlt.plot( (self.diffsAbstimes-T0)/864e2, self.diffsNets, '.', label='Good' )
    timePlt.plot( (self.bads[:,1]-T0)/864e2, self.bads[:,0], 'o', label='Suspect' )
    timePlt.plot( (self.diTOIDiff.imFracSec-T0)/864e2, self.diTOIDiff.imFbDiff, 'o', label='TOI' )

    timePlt.plot( tDays, self.model2parNets, label='Predict' )

    timePlt.legend( loc='lower left' )

    plt.show()

### End of class DITwoParamModel
########################################################################


########################################################################
if __name__=="__main__" or "ttmodelmain" in sys.argv[1:]:

  ### Parse arguments
  k  = ([-1.383e-2] + [float(i[4:]) for i in sys.argv[1:] if i[:4]=='--k='])[-1]
  p1s = ([-.65]      + [eval(i[5:]) for i in sys.argv[1:] if i[:5]=='--p1='])[-1]

  if not type(p1s) is list: p1s = [p1s]

  dimodel = DITwoParamModel()

  import scipy.optimize as so

  for p1 in p1s:
    if 'ksolve' in sys.argv[1:]:

      k0 = numpy.array( [k] )
      res = so.minimize( dimodel.makemodel
                       , k0
                       , args=(p1,)
                       , method='nelder-mead'
                       , tol=1e-7
                       , options=dict(maxiter=100000)
                       )
      print( 'p1,k,SoSE = %7.2f, %12.4e, %12.4e' % ( p1, res.x[0], dimodel.sose, ) )
    else:

      ### Create model, print out Sum of Squared Errors
      print( "Sum of Squared Errors[p1=%.4e]=%.4e" % (p1,dimodel.makemodel( k, p1),) )

      ### Plot
    if 'doplot' in sys.argv[1:]: dimodel.doplot()

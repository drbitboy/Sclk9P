"""
Usage:

  python smoothtemps.py all_scutemp.txt [--sf=#samples/smoothingFactor, default=150]

"""
import os
import sys
import numpy
import matplotlib.pyplot as plt
import smoothtemps
import timediffs
import spice


########################################################################
def setupTemperatures(lotime=None):

  ### Use smoothtmeps.SmoothDiTemps class to get temperature data
  smoothditemps = smoothtemps.SmoothDiTemps()

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
  ### - append1.0 to prep goods for least-squares fit to remove slope
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

  ### Simplification:  separate paramDeltaRateppm0 from dRate/dTemperature
  deltaTimes = deltaTime0 + paramDeltaRateppm0 * (smoothTimes - smoothTimes[0]) * 1e-6

  ### Assume time steps are constant
  cumDegC = numpy.cumsum( deltaDegC - deltaDegC[0] )

  cumDeltaTimes = cumDegC * paramPpmPerDegC * 1e-6 * (smoothTimes[1]-smoothTimes[0])

  deltaTimes = deltaTimes + cumDeltaTimes

  ###plt.plot( cumDeltaTimes )
  ###plt.show()

  return deltaTimes

########################################################################
if __name__=="__main__":

  diffsAbstimes, diffsNets, diffsGroup0, m, bads, diTOIDiff = setupTimeDiffs()

  smoothTimes, diiSmooth, difSmooth, diffSmooth, smoothditemps = setupTemperatures(lotime=diffsGroup0[0])

  k = -1e-2
  p0,p1 = m * k * 1e6, -.20

  title = '%f ppm (%em) at T=0; %f ppm/degC' % (p0,k,p1,)

  model2parNets = model2par( p0, p1, diffsGroup0[1], smoothTimes, diffSmooth )

  T0 = 1.724e8

  f,(timePlt,tempPlt) = plt.subplots( 2, 1, sharex=True)
  plt.title( title )

  ### Plot DII and DIF raw data as points
  tempPlt.plot( smoothditemps.diitimes()-T0,smoothditemps.diitemps(), '.', label='DII' )
  tempPlt.plot( smoothditemps.diftimes()-T0, smoothditemps.diftemps(), '.', label='DIF' )

  ### Plot smoothed DII and DIF data as lines
  tempPlt.plot( smoothTimes-T0,diiSmooth,label='DII smooth')
  tempPlt.plot( smoothTimes-T0,difSmooth,label='DIF smooth')

  ### Plot DII-DIF differences, offset +10C
  tempPlt.plot(smoothTimes-T0,10+diffSmooth,label='Smooth diff + 10')

  tempPlt.legend(loc='center left')

  timePlt.plot( diffsGroup0[0]-T0, diffsGroup0[1], 'o', label='GoodAvg' )
  timePlt.plot( diffsAbstimes-T0, diffsNets, '.', label='Good' )
  timePlt.plot( bads[:,1]-T0, bads[:,0], 'o', label='Suspect' )
  timePlt.plot( diTOIDiff.imFracSec-T0, diTOIDiff.imFbDiff, 'o', label='TOI' )

  timePlt.plot( smoothTimes-T0, model2parNets, label='Predict' )

  timePlt.legend( loc='lower left' )

  plt.show()


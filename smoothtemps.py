"""
Usage:

  python smoothtemps.py all_scutemp.txt [--sf=#samples/smoothingFactor, default=150]

"""
import os
import sys
import numpy
import xalglib as xa
from scipy import interpolate
import matplotlib.pyplot as plt
import readtemps
import spice

########################################################################
class AllDiTemps:
  """
  Class that reads a SCU time vs. temperatures file, per readtemps.py,
  and splits the data into DII and DIF instances of class DiScuTemps

  Read from argv[0] if it is the path of a regular file, else read from
  STDIN

  Usage:  ditemps = AllDiTemps(sys.argv[1:])

  """

  def __init__(self,argv=None):

    rf = readtemps.__file__
    if rf[-4:-1]=='.py': rf = rf[:-1]
    spice.furnsh( rf )   ### metakernel

    if argv and os.path.isfile(argv[0]):
      fArg = argv[0]
      fName = fArg
    else:
      fArg = sys.stdin
      fName = 'STDIN'

    print( "Reading DI temperature data from %s ..."%(fName,) )

    tts = readtemps.readtemps( fArg )

    self.dii = readtemps.DiScuTemps( tts, which=-70 )
    self.dif = readtemps.DiScuTemps( tts, which=-140 )


########################################################################
class SmoothDiTemps:
  """
  Class that smooths DII and DIF data in instance of class AllDiTemps

  Usage:  ditemps = AllDiTemps(sys.argv[1:])

  """

  def __init__(self,ditemps=None):

    ### .ditemps.dii and .ditemps.dif are DiScuTemps:
    self.ditemps = ditemps or AllDiTemps(sys.argv[1:])

    self.sf = ([150.] + [i[5:] for i in sys.argv[1:] if i[:5]=='--sf='])[-1]

    self.diicount = self.ditemps.dii.tts.shape[0]
    self.difcount = self.ditemps.dif.tts.shape[0]

    ### Interpolation functions for DII and DIF temperatures = f(time)
    self.fSmoothDii = interpolate.UnivariateSpline( self.diitimes(), self.diitemps(), s = self.diicount/self.sf )
    self.fSmoothDif = interpolate.UnivariateSpline( self.diftimes(), self.diftemps(), s = self.difcount/self.sf )

    self.time_limits = ( numpy.min(self.ditemps.dii.tts[:,0]), numpy.max(self.ditemps.dii.tts[:,0]) )

  ### Return times for DII or DIF
  def diitimes(self): return self.ditemps.dii.tts[:,0].T
  def diftimes(self): return self.ditemps.dif.tts[:,0].T

  ### Return temperatures for DII or DIF
  def diitemps(self): return self.ditemps.dii.tts[:,1].T
  def diftemps(self): return self.ditemps.dif.tts[:,1].T

  ### Return smoothed temperatures at times for DII or DIF
  def diiSmoothTemps(self,smoothtimes): return self.fSmoothDii(smoothtimes)
  def difSmoothTemps(self,smoothtimes): return self.fSmoothDif(smoothtimes)

  ### Return smoothed temperatures at range of times for DII and DIF
  def smoothedTTs(self,step):
    times = numpy.arange( self.time_limits[0], self.time_limits[1] )
    return times, self.diiSmoothTemps(times), self.difSmoothTemps(times)


########################################################################
def ditempsPlot():

  ### Use classes above to get data
  smoothditemps = SmoothDiTemps()

  ### Get DII and DIF smoothed temperatures at .01d intervals
  smoothTimes, diiSmooth, difSmooth = smoothditemps.smoothedTTs(864.)

  ### DII-DIF differences between smoothed data
  smoothDiffs = diiSmooth - difSmooth

  ### Plot DII and DIF raw data as points
  plt.plot( smoothditemps.diitimes(),smoothditemps.diitemps(), '.', label='DII' )
  plt.plot( smoothditemps.diftimes(), smoothditemps.diftemps(), '.', label='DIF' )

  ### Plot smoothed DII and DIF data as lines
  plt.plot( smoothTimes,diiSmooth,label='DII smooth')
  plt.plot( smoothTimes,difSmooth,label='DIF smooth')

  ### Plot DII-DIF differences, offset +10C
  plt.plot(smoothTimes,10+smoothDiffs,label='Smooth diff + 10')

  plt.legend(loc='center left')
  plt.show()


########################################################################
if __name__=="__main__":
  ditempsPlot()


########################################################################
### Obsolete test code
########################################################################
def example():
  xs = numpy.sort( numpy.hstack( (numpy.array([0.,100.]),numpy.random.random(48)*100,) ) )
  ynoises = numpy.random.random(xs.shape[0])
  ys = numpy.round( ynoises + xs/200 - 0.5, 1)

  f = interpolate.UnivariateSpline(xs,ys)
  g = interpolate.interp1d(xs,ys)

  c = xa.spline1dbuildakima(list(xs),list(ys))

  xnews = numpy.arange(1.,99.,.1)

  print( [i.shape for i in (xs,ys,xnews,)] )
  cys = numpy.array( [xa.spline1dcalc(c,x) for x in xnews] )

  plt.plot(xs,ys,'ro')
  plt.plot(xnews,cys,label='akima')
  plt.plot(xnews,f(xnews),label='Univariate')
  plt.plot(xnews,g(xnews),label='interp1d')

  plt.legend(loc='upper left')
  plt.show()

#example()

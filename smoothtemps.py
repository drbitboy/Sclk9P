"""
Usage:

  python in.py --date=all_scutemp.txt [--sf=#samples/smoothingFactor, default=150]
"""
import sys
import numpy
import xalglib as xa
from scipy import interpolate
import matplotlib.pyplot as plt
import readtemps
import spice

########################################################################
class AllDiTemps:

  def __init__(self):

    rf = readtemps.__file__
    if rf[-4:-1]=='.py': rf = rf[:-1]
    spice.furnsh( rf )   ### metakernel

    self.tts = readtemps.readtemps( sys.stdin if not sys.argv[1:] else sys.argv[1] )

    self.dii = readtemps.DiScuTemps( self.tts, which=-70 )
    self.dif = readtemps.DiScuTemps( self.tts, which=-140 )

class SmoothDiTemps:

  def __init__(self,ditemps=None):

    ### .ditemps.dii and .ditemps.dif are DiScuTemps:
    self.ditemps = ditemps or AllDiTemps()

    self.sf = ([150.] + [i[5:] for i in sys.argv[1:] if i[:5]=='--sf='])[-1]

    self.diicount = self.ditemps.dii.tts.shape[0]
    self.difcount = self.ditemps.dif.tts.shape[0]

    ### Interpolation functions for DII and DIF temperatures = f(time)
    self.fSmoothDii = interpolate.UnivariateSpline( self.diitimes(), self.diitemps(), s = self.diicount/self.sf )
    self.fSmoothDif = interpolate.UnivariateSpline( self.diftimes(), self.diftemps(), s = self.difcount/self.sf )

    self.time_limits = ( numpy.min(self.ditemps.dii.tts[:,0]), numpy.max(self.ditemps.dii.tts[:,0]) )

  def diitimes(self): return self.ditemps.dii.tts[:,0].T
  def diftimes(self): return self.ditemps.dif.tts[:,0].T

  def diitemps(self): return self.ditemps.dii.tts[:,1].T
  def diftemps(self): return self.ditemps.dif.tts[:,1].T

  def diiSmoothTemps(self,times): return self.fSmoothDii(times)
  def difSmoothTemps(self,times): return self.fSmoothDif(times)

  def smoothedTTs(self,step):
    times = numpy.arange( self.time_limits[0], self.time_limits[1] )
    return times, self.diiSmoothTemps(times), self.difSmoothTemps(times)


def ditempsPlot():

  smoothditemps = SmoothDiTemps()

  xnews, diiSmooth, difSmooth = smoothditemps.smoothedTTs(864.)

  smoothDiffs = 10 + diiSmooth - difSmooth

  plt.plot( smoothditemps.diitimes(),smoothditemps.diitemps(), '.', label='DII' )

  plt.plot( smoothditemps.diftimes(), smoothditemps.diftemps(), '.', label='DIF' )

  plt.plot( xnews,diiSmooth,label='DII smooth')
  plt.plot( xnews,difSmooth,label='DIF smooth')

  plt.plot(xnews,smoothDiffs,label='Smooth diff + 10')

  plt.legend(loc='center left')
  plt.show()

########################################################################
if __name__=="__main__":
  ditempsPlot()

########################################################################
########################################################################
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

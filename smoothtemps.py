"""
Usage:

  python in.py all_scutemp.txt [#samples/smoothingFactor, default=150]
"""
import sys
import numpy
import xalglib as xa
from scipy import interpolate
import matplotlib.pyplot as plt
import readtemps
import spice

########################################################################
def ditemps():

  rf = readtemps.__file__
  if rf[-4:-1]=='.py': rf = rf[:-1]
  spice.furnsh( rf )   ### metakernel

  print( rf )

  tts = readtemps.readtemps( sys.stdin if not sys.argv[1:] else sys.argv[1] )

  sf = 150. if not sys.argv[2:] else float(sys.argv[2])

  dii = readtemps.DiScuTemps( tts, which=-70 )
  dif = readtemps.DiScuTemps( tts, which=-140 )

  diitimes = dii.tts[:,0]
  diitemps = dii.tts[:,1]

  diftimes = dif.tts[:,0]
  diftemps = dif.tts[:,1]

  fDii = interpolate.UnivariateSpline( diitimes, diitemps, s = diitimes.shape[0]/sf )
  fDif = interpolate.UnivariateSpline( diftimes, diftemps, s = diftimes.shape[0]/sf )

  xnews = numpy.arange( numpy.min(diitimes), numpy.max(diitimes), 864 )

  diiSmooth = fDii(xnews)
  difSmooth = fDif(xnews)

  smoothDiffs = 10 + diiSmooth - difSmooth

  plt.plot( diitimes,diitemps, '.', label='DII' )
  plt.plot(xnews,diiSmooth,label='DII smooth')

  plt.plot( diftimes,diftemps, '.', label='DIF' )
  plt.plot(xnews,difSmooth,label='DIF smooth')

  plt.plot(xnews,smoothDiffs,label='Smooth diff + 10')

  plt.legend(loc='center left')
  plt.show()

########################################################################
if __name__=="__main__":
  ditemps()

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

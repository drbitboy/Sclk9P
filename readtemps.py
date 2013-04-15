import sys
import spice
import numpy

def readtemps( fArg ):
  if type(fArg) is str:
    f = open(fArg,'rb')
  else:
    f = fArg

  f.readline()   ### ignore header

  tts = [ [spice.utc2et('20'+tim),float(tem)] for tim,tem in [lin.split()[:2] for lin in f.readlines()] ]

  if type(fArg) is str: f.close( )

  return numpy.array(tts)


if __name__=='__main__':
  spice.furnsh( __file__ )
  tts = readtemps( sys.stdin if len(sys.argv)<2 else sys.argv[1] )
  print( tts )

"""
\begindata
KERNELS_TO_LOAD = (
'../kernels/naif0010.tls'
'../kernels/dif_sclkscet_00015_science.tsc'
'../kernels/dii_sclkscet_00008_science.tsc'
)
\begintext
"""

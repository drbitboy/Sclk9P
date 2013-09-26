"""
Usage:  python fit2png.ppy mrivis/*.fit

"""
import os
import sys
import numpy
import pyfits
import matplotlib.pyplot as plt

s = ""
for arg in sys.argv[1:]:
  h0 = pyfits.open(arg)[0]
  d = h0.data
  plt.plot( numpy.max(d,axis=-1), label=arg[-10:-7] )
  s += '\n%s' % (os.path.basename(h0.header["filenamr"]),)
plt.title("Locating the DII flash in DIF MRIVIS encounter images:" + s)
plt.xlabel("MRIVIS column (0-63)")
plt.ylabel("Sum of Column brightness, DN")
plt.legend()
plt.show()

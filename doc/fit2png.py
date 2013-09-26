"""
Usage:  python fit2png.py mrivis/*.fit

Takes Deep Impact Flyby (DIF) spacecraft MRIVIS FITS images, finds the
maximum brightness along each column, and plots them on a single plot.

The Deep Impact Impactor (DII) spacecraft impact flash is apparent in
images (_064 and above) by the spike in that plot near the center
columns.

The SCLKs of the FITS images in the mrivis/ subdirectary are

- mv0173727702_9000910_062.fit    SCLK = '1/0173727702.188'
- mv0173727702_9000910_063.fit    SCLK = '1/0173727702.203'
- mv0173727702_9000910_064.fit    SCLK = '1/0173727702.218'
- mv0173727702_9000910_065.fit    SCLK = '1/0173727702.233'
- mv0173727703_9000910_066.fit    SCLK = '1/0173727703.004'
- mv0173727703_9000910_067.fit    SCLK = '1/0173727703.019'

"""
import os
import sys
import numpy
import pyfits
import matplotlib.pyplot as plt

s = ""

### Loop over command line arguments (FITS file paths)
for arg in sys.argv[1:]:

  ### Open FITS images, extract the data, plot column brightness maxima
  h0 = pyfits.open(arg)[0]
  d = h0.data
  plt.plot( numpy.max(d,axis=-1), label=arg[-10:-7] )

  ### Add the file basename to the string s
  s += '\n%s' % (os.path.basename(h0.header["filenamr"]),)

### Plot title, axis labels and legend
plt.title("Locating the DII flash in DIF MRIVIS encounter images:" + s)
plt.xlabel("MRIVIS column (0-63)")
plt.ylabel("Sum of Column brightness, DN")
plt.legend()

### Show the plot
plt.show()

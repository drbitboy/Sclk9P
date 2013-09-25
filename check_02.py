
"""
========================================================================
Usage:  python check_02.py

Plot differences between ET, DIF SCLK (VTCf) and DII SCLK (VTCi), all
three of which represent some form of s past J2000 epoch

DII temperature sensor is FM003; oscillator is #8309 from vendor
DIF temperature sensor is FM001; oscillator is #8306 from vendor

\begindata
PATH_SYMBOLS = ( 'K' )
PATH_VALUES = ( 'kernels' )
KERNELS_TO_LOAD = (
'$K/naif0010.tls'
'$K/dif_sclkscet_00015_science.tsc'
'$K/dii_sclkscet_00008_science_btc.tsc'
)
ETTOI-108d = @2005-03-18T05:45:38.384
\begintext
ETTOI-108d is TOI(tparse('2005-07-04T05:44:34.2')) + 64.184s - 108d
Alternate DII SCLK kernels:
'$K/dii_sclkscet_00008_science.tsc'
'$K/dii_sclkscet_00008.tsc'
========================================================================
"""

import os
import sys
import spice
import pprint
import matplotlib.pyplot as plt

### Load meta-kernel, get start time ETTOI-108d
spice.furnsh(__file__)

### Override any kernels with sys.argv[1:]
for sclkk in sys.argv[1:]: spice.furnsh(sclkk)


### Get TEXT kernel list
ks = '\n'.join([os.path.basename(spice.kdata(i,'text')[0]) for i in range(spice.ktotal('TEXT'))])

### Get TOI-108d, set up for one point per day for 108d
et = spice.gdpool( 'ETTOI-108d', 0, 1 )[1]
spanDays = 108
diffs = range(spanDays+1)
doys = [ i+185-spanDays for i in diffs ]

### Spacecraft IDs to plot
scids = [-70,-140]
n = len(scids)
scidrn = range(n)
f3 = lambda k : ('%.3f '* k).strip()

### Loop over 108d
for iDay in diffs:
  ### Convert ET to SCLKs and Vehicle Time Codes (=Encoded SCLK/256)
  sclks = [ spice.sce2s(scids[i],et) for i in scidrn ]
  vtcs = [ spice.scencd(scids[i],sclks[i])/256e0 for i in scidrn ]
  ### Calculate differences
  diffs[iDay] = [vtcs[0] - vtcs[1]] + [ et-vtcs[i] for i in scidrn ]
  ### Output UTCs, SCLKs, and ET-SCLK differences for every ninth day
  if (iDay%9) == 0:
    utcs = [spice.et2utc( et, 'isoc', 3), spice.et2utc( et, 'isod', 3)]
    svtcs = f3(n) % tuple([ spice.scencd(scids[i],sclks[i])/256e0
                            for i in scidrn
                          ])
    sdiffs = f3(n+1) % tuple( diffs[iDay] )
    print( (utcs,sclks,svtcs,sdiffs,) )

  ### Increment ET by 1d
  et += spice.spd()

print(__doc__.strip().replace('\b','\\b'))


### Plot differences
labels = '(VTCi,FM003,8309)-(VTCf,FM001,8306) ET-(VTCi,FM003,8309) ET-(VTCf,FM001,8306)'.split()
for i in range(3):
  label = labels.pop(0)
  plt.plot( doys, [diff3[i] for diff3 in diffs], '.' if label[:1]=='E' else '', label=label )
plt.legend( loc='upper left' )
plt.xlabel("2005 DOY")
plt.ylabel("Clock differences from SCLK kernels, s")
plt.title( ks + """
DII:  VTCi; Temperature sensor FM003; Vendor oscillator 8309
DIF:  VTCf; Temperature sensor FM001; Vendor oscillator 8306
""".rstrip() )
plt.show()

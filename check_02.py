
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
'$K/dii_sclkscet_00008_science.tsc'
)
ETSTART = @2005-03-18T05:45:38.384
\begintext
ETSTART is TOI(tparse('2005-07-04T05:44:34.2')) + 64.184s - 108d
Alternate DII SCLK kernels:
'$K/dii_sclkscet_00008_science_btc.tsc'
'$K/dii_sclkscet_00008_science.tsc'
'$K/dii_sclkscet_00008.tsc'
========================================================================
"""

import spice
import pprint
import matplotlib.pyplot as plt

### Load meta-kernel, get start time ETSTART
spice.furnsh(__file__)
et = spice.gdpool( 'ETSTART', 0, 1 )[1]

### Set up for 108 days
spanDays = 108
diffs = range(spanDays+1)
doys = [ i+185-spanDays for i in diffs ]
scids = [-70,-140]
n = len(scids)
rn = range(n)

for iDay in diffs:
  utcs= [ spice.et2utc( et, 'isoc', 3), spice.et2utc( et, 'isod', 3) ]
  sclks = [ spice.sce2s(scids[i],et) for i in rn ]
  encds = [ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ]
  sencds = '%.3f  %.3f' % tuple([ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ])
  diffs[iDay] = [encds[0] - encds[1]] + [ et-encds[i] for i in rn ]
  diff3 = '%.3f  %.3f  %.3f' % tuple( diffs[iDay] )
  print( (utcs,sclks,sencds,diff3,) )
  et += spice.spd()

print(__doc__.strip().replace('\b','\\b'))


labels = '(VTCi,FM003,8309)-(VTCf,FM001,8306) ET-(VTCi,FM003,8309) ET-(VTCf,FM001,8306)'.split()
for i in range(3):
  label = labels.pop(0)
  plt.plot( doys, [diff3[i] for diff3 in diffs], '.' if label[:1]=='E' else '', label=label )
plt.legend( loc='upper left' )
plt.xlabel("2005 DOY")
plt.ylabel("Clock differences from SCLK kernels, s")
plt.title( """
DII:  VTCi; Temperature sensor FM003; Vendor oscillator 8309
DIF:  VTCf; Temperature sensor FM001; Vendor oscillator 8306
""".strip() )
plt.show()


"""
\begindata
KERNELS_TO_LOAD = (
'kernels/naif0010.tls'
'kernels/dif_sclkscet_00015_science.tsc'
'kernels/dii_sclkscet_00008_science_btc.tsc'
)
ETSTART = @2005-03-18T05:45:38.384
\begintext

ETSTART is TOI(tparse('2005-07-04T05:44:34.2')) + 64.184s - 108

'kernels/dif_sclkscet_00015_science.tsc'

'kernels/dii_sclkscet_00008_science_btc.tsc'
'kernels/dii_sclkscet_00008_science.tsc'
'kernels/dii_sclkscet_00008.tsc'

"""

import spice
import pprint
import matplotlib.pyplot as plt

spice.furnsh(__file__)

et = spice.gdpool( 'ETSTART', 0, 1 )[1]

spanDays = 108

diffs = range(spanDays+1)
doys = [ i+185-spanDays for i in diffs ]

for iDay in range(spanDays+1):
  utcs= [ spice.et2utc( et, 'isoc', 3), spice.et2utc( et, 'isod', 3) ]
  scids = [-70,-140]
  rn = range(len(scids))
  sclks = [ spice.sce2s(scids[i],et) for i in rn ]
  encds = [ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ]
  sencds = '%.3f  %.3f' % tuple([ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ])
  diffs[iDay] = [encds[0] - encds[1]] + [ et-encds[i] for i in rn ]
  diff3 = '%.3f  %.3f  %.3f' % tuple( diffs[iDay] )
  print( (utcs,sclks,sencds,diff3,) )
  et += spice.spd()


labels = '(VTCi,FM003,8309)-(VTCf,FM001,8306) ET-(VTCi,FM003,8309) ET-(VTCf,FM001,8306)'.split()
for i in range(3):
  label = labels.pop(0)
  plt.plot( doys, [diff3[i] for diff3 in diffs], '.' if label[:1]=='E' else '', label=label )
plt.legend( loc='upper left' )
plt.show()

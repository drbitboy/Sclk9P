
"""
\begindata
KERNELS_TO_LOAD = (
'../kernels/naif0010.tls'
'../kernels/dif_sclkscet_00015_science.tsc'
'../kernels/dii_sclkscet_00008_science_btc.tsc'
)
ETSTART = @2005-06-19T05:45:38.384
\begintext

ETSTART is TOI(tparse('2005-07-04T05:44:34.2')) + 64.184s - 15d

"""

import spice
import pprint

print( __file__)
spice.furnsh(__file__)

et = spice.gdpool( 'ETSTART', 0, 1 )[1]

for i in range(16):
  utcs= [ spice.et2utc( et, 'isoc', 3), spice.et2utc( et, 'isod', 3) ]
  scids = [-70,-140]
  rn = range(len(scids))
  sclks = [ spice.sce2s(scids[i],et) for i in rn ]
  encds = [ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ]
  sencds = '%.3f  %.3f' % tuple([ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ])
  diff3 = '%.3f  %.3f  %.3f' % tuple( [encds[0] - encds[1]] + [ et-encds[i] for i in rn ])
  print( (utcs,sclks,sencds,diff3,) )
  et += spice.spd()

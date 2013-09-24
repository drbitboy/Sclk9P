
"""
========================================================================
Usage:  python check_01.py

Load SCLK and LEAPSECOND SPICE Kernels from this __file__, parsed as
a SPICE meta-kernel; see \begindata and \begintext later in this __doc__
string.

Bet, from kernel pool, ET of DI TOI (Deep Impact; Time Of Impact) minus
15 days.

Print UTC, DII SCLK, DIF SCLK, and, since all of those times express
some form of seconds past the J2000 epoch, their differences, for 15
days up to TOI.

\begindata
PATH_SYMBOLS += ( 'K' )
PATH_VALUES  += ( 'kernels' )
KERNELS_TO_LOAD = (
'$K/naif0010.tls'
'$K/dif_sclkscet_00015_science.tsc'
'$K/dii_sclkscet_00008_science_btc.tsc'
)
ETSTART = @2005-06-19T05:45:38.384
\begintext
N.B. ETSTART is TOI(tparse('2005-07-04T05:44:34.2')) + 64.184s - 15d
========================================================================
"""

import spice
import pprint


print(__doc__.replace('\b','\\b'))
spice.furnsh(__file__)

### ET of TOI-15d
found,et = spice.gdpool( 'ETSTART', 0, 1 )

### S/C IDs
scids = [-70,-140]
n = len(scids)
rn = range(len(scids))

### for 15 days leading up to TOI
for i in range(16):
  ### Convert
  ### - ET to ISO Calendar and DOY UTCs
  ### - ET to DII and DIF SCLKs
  ### - SCLKs to encoded SCLK, scale by 1/256 to get s past J2k epoch
  utcs = [ spice.et2utc( et, 'isoc', 3), spice.et2utc( et, 'isod', 3) ]
  sclks = [ spice.sce2s(scids[i],et) for i in rn ]
  encds = [ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ]
  ### Build and print output
  f3 = ' %.3f'
  sencds = (f3*n).strip() % tuple([ spice.scencd(scids[i],sclks[i])/256e0 for i in rn ])
  diff3 = (f3*(n+1)).strip() % tuple( [encds[0] - encds[1]] + [ et-encds[i] for i in rn ])
  print( (utcs,sclks,sencds,diff3,) )
  ### Increment ET by 1d (spice.spd() = seconds/day)
  et += spice.spd()

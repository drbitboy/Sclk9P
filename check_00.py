
"""
========================================================================
Usage:  python check_00.py

- Load SCLK and LEAPSECOND SPICE Kernels, which are part of this
  __doc__ string

- Set character TOIs (Times Of Impact) from three sources
  - UTC TOI  = 2005-07-04T05:44:34.2
  - DII SCLK = 1/0173727875.105, from analysis of approach images
  - DIF SCLK = 1/0173727702.218, from analysis of no-flash/flash images

- Convert character TOIs to floating point Ephemeris Times (ET; seconds
  past J2000 epoch)

- Compare those ETs by difference (subtraction)
  N.B. DIF SCLK includes light travel time from comet 9P/Tempel 1, ~30ms

- Convert UTCTOI ET to DII and DIF SCLKs

\begindata
KERNELS_TO_LOAD = (
'kernels/naif0010.tls'
'kernels/dif_sclkscet_00015_science.tsc'
'kernels/dii_sclkscet_00008_science_btc.tsc'
)
ETTOIPSEUDO = @2005-07-04T05:44:34.2
\begintext
========================================================================
"""

import spice
import pprint

spice.furnsh(__file__)

### Get UTC and SCLKs of TOI as strings

utctoi = '2005-07-04T05:44:34.2'
diitoi = '1/0173727875.105'
diftoi = '1/0173727702.218'
### N.B. Old code:  pseudo-ET to non-leapsecond-corrected calendar time
###utctoi = spice.etcal( spice.gdpool( 'ETTOIPSEUDO', 0, 1 )[1] )

### Convert UTC and SCLKs strings to ETs
toiet = spice.utc2et( utctoi )
diiet = spice.scs2e(  -70, diitoi )
difet = spice.scs2e( -140, diftoi )

### Output __doc__ string
print( __doc__.replace('\b','\\b') )

### Output differences and UTC TOI ET converted to SCLKs
pprint.pprint( ( 'ET differences:'
               , ( ('%s(DII)-%s'%(diitoi,utctoi,)) ,diiet-toiet,)
               , ( ('%s(DIF)-%s'%(diftoi,utctoi,)) ,difet-toiet,)
               , ( ('%s(DIF)-%s(DII)'%(diftoi,diitoi,)),difet-diiet,)
               , ''
               , 'UTC TOI converted to DII and DIF SCLK:'
               , (utctoi+'=>DII', spice.sce2s(-70,toiet),)
               , (utctoi+'=>DIF', spice.sce2s(-140,toiet),)
               , ''
               ,)
             )

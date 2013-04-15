
"""
\begindata
KERNELS_TO_LOAD = (
'../kernels/naif0010.tls'
'../kernels/dif_sclkscet_00015_science.tsc'
'../kernels/dii_sclkscet_00008_science.tsc'
)
ETTOIPSEUDO = @2005-07-04T05:44:34.2
\begintext
"""

import spice
import pprint

print( __file__)
spice.furnsh(__file__)

utctoi = spice.etcal( spice.gdpool( 'ETTOIPSEUDO', 0, 1 )[1] )
diitoi = '1/0173727875.105'
diftoi = '1/0173727702.218'

toiet = spice.utc2et( utctoi )
diiet = spice.scs2e(  -70, diitoi )
difet = spice.scs2e( -140, diftoi )

pprint.pprint( ( ( ('%s(DII)-%s'%(diitoi,utctoi,)) ,diiet-toiet,)
               , ( ('%s(DIF)-%s'%(diftoi,utctoi,)) ,difet-toiet,)
               , ( ('%s(DII)-%s(DIF)'%(diitoi,diftoi,)),difet-toiet,)
               , ('dii-dif',diiet-difet,)
               , (utctoi+'=>DII', spice.sce2s(-70,toiet),)
               , (utctoi+'=>DIF', spice.sce2s(-140,toiet),)
               ,)
             )
print( __doc__ )

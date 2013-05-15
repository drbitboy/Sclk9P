"""
readtemps.py

Read DII and DIF SCU temperatures from whitespace-separated, 3-column file:

EarthReceivedTime   Temperature   SpaceCraft_spice_ID

E.g.

EarthReceivedTime       T,degC  -70
05-170//01:42:13.721	32.1  -70
05-170//01:43:02.688	31.9  -70
05-170//01:44:53.486	32.1  -70
...

Usage:

  Shell:

    python readtemps.py dii_scutemp.py
    python readtemps.py dif_scutemp.py
    cat dif_scutemp.py dii_scutemp.py | python readtemps.py


  Python:

    import readtemps
    import spice
    spice.furnsh( readtemps.__file__ )   ### metakernel
    tts = readtemps.readtemps('dii_scutemp.py')
    dii = DiScuTemps( tts, which=-70 )
    dif = DiScuTemps( tts, which=-140 )

SPICE meta-kernel:
- Need LSK, and DII+DIF SCLK and SPK
- SPKs are only for light-time correction, preencounter versions
  are good enough

\begindata
KERNELS_TO_LOAD = (
'../kernels/naif0010.tls'
'../kernels/dif_sclkscet_00015_science.tsc'
'../kernels/dii_sclkscet_00008_science_btc.tsc'
'../kernels/dii_preenc174_nav_v1.bsp'
'../kernels/dif_preenc174_nav_v1.bsp'
)
\begintext

"""

import sys
import spice
import numpy

### parse one line of SCU Temperature file

def readone( lin ):

  ### Exception for lines that do not match
  try:

    ### Parse (split on whitespace) three items from line

    tims,tems,scids = lin.split()[:3]

    ### Parse strings:  Temp, degC; S/C SPICE ID; ERT UTC to ET(s past J2k)
    tem = float(tems)
    scid = int(scids)
    ert = spice.utc2et(tims)
    if spice.failed():
      spice.reset()
      assert False

    ### Discard invalid data
    ### - temperature < 10degC; typically -61.0 = null return
    ### - SCID neither DII nor DIF

    if tem<10: assert False
    if scid!=-140 and scid!=-70: assert False

    ### Calculate light time to Earth from S/C to get time at S/C
    stateVector,lighttime = spice.spkez(scid,ert,"j2000","LT",399)
    
    return ert-lighttime,tem,scid   ### success

  except:
    return [0.0,0.0,0]    ### failure (SCID==0)

  
### Parse all lines in a file
def readtemps( fArg ):

  if type(fArg) is str:    ### Assume fArg is filepath
    f = open(fArg,'rb')
  else:                    ### Assume fArg is open file
    f = fArg

  tts = [ [tim,tem,scid] for tim,tem,scid in [readone(lin) for lin in f.readlines()] if scid<0 ]

  if type(fArg) is str: f.close( )

  tts = numpy.array(tts)

  ### Filter data on changes in 1) temperature and 2) time

  ### 1) Exclude each point that is more than 1.2degC greater than either of the two previous points

  ids = list(tts[:,2])     ### SCID[i]

  temps = tts[:,1]         ### Temperature[i]

  dt1 = [0] + list(temps[1:-1] - temps[:-2]) + [0]   ### prev delta = temp[i] - temp[i-1]
  dt2 = [0,0] + list(temps[2:] - temps[:-2])         ### 2nd prev delta = temp[i] - temp[i-2]
  id1 = ids[:1] + ids[:-1]                           ### prev SCID
  id2 = ids[:2] + ids[:-2]                           ### 2nd prev SCID

  iw = [ i for i in range(len(ids)) if dt1[i]<1.2 and dt2[i]<1.2 and id1[i]==ids[i] and id2[i]==ids[i] ]

  tts = tts[iw,:]

  ### 2) Exclude each point that is more than 1000s away from previous and next points

  ids = list(tts[:,2])     ### SCID[i]

  times = tts[:,0]         ### Times[i]

  dts = list(times[1:] - times[:-1])
  dt1 = [0] + dts            ### prev delta = time[i]-time[i-1]
  dt2 = dts + [0]            ### next delta = time[i]-time[i+1]
  id1 = ids[:1] + ids[:-1]   ### prev scid
  id2 = ids[1:] + ids[-1:]   ### next scid

  iw = [ i for i in range(len(dt1)) if dt1[i]<1000 or dt2[i]<1000 or ids[i]!=id1[i] or ids[i]!=id2[i] ]

  return tts[iw,:]


class DiScuTemps:
  def __init__(self,tts,which=False):
    if which:
      self.tts = tts[ numpy.where(tts[:,2]==which)[0], : ]
    else:
      self.tts = tts

    self.bintemps()

  def empty(self):
    return self.tts.shape[0]==0
  ######################################################################
  ### group data into bins of size 64-128 elements
  def bintemps(self):
    self.breaks = numpy.where( (self.tts[1:,0] - self.tts[:-1,0])>1000 )[0] + 1
    self.ttsBinned = None
    pass

########################################################################
if __name__=='__main__':

  spice.furnsh( __file__ )
  tts = readtemps( sys.stdin if len(sys.argv)<2 else sys.argv[1] )
  dii = DiScuTemps( tts, which=-70 )
  dif = DiScuTemps( tts, which=-140 )

  print( tts )          ### numpy default print will limit to less than a dozen lines

  print( ( tts.shape, dii.tts.shape, dif.tts.shape, )  )    ### Should be (N,3)

  if not dii.empty():
    print( (dii.tts[:,1].min(),dii.tts[:,1].max(),) )
    print( (dii.breaks[1:]-dii.breaks[:-1],) )
  if not dif.empty():
    print( (dif.tts[:,1].min(),dif.tts[:,1].max(),) )
    print( (dif.breaks[1:]-dif.breaks[:-1],) )

  import matplotlib.pyplot as plt
  if not dii.empty(): plt.plot( dii.tts[:,0],dii.tts[:,1], '.', label='DII' )
  if not dif.empty(): plt.plot( dif.tts[:,0],dif.tts[:,1], '.', label='DIF' )
  plt.xlabel( 'Time, VTC' )
  plt.ylabel( 'Temperature, degC' )
  if not ( dii.empty() or dif.empty() ):
    plt.legend(loc='center left')
  else:
    plt.legend(loc='lower left')
  plt.show()


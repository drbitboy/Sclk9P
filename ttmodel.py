"""
Usage:

  python smoothtemps.py all_scutemp.txt [--sf=#samples/smoothingFactor, default=150]

"""
import os
import sys
import numpy
import matplotlib.pyplot as plt
import smoothtemps
import timediffs
import spice


########################################################################
def setupTemperatures():

  ### Use smoothtmeps.SmoothDiTemps class to get temperature data
  smoothditemps = smoothtemps.SmoothDiTemps()

  ### Get DII and DIF smoothed temperatures at 60s intervals
  smoothTimes, diiSmooth, difSmooth = smoothditemps.smoothedTTs(60.)

  ### Return those, plus DII-DIF differences between smoothed data

  return smoothTimes, diiSmooth, difSmooth, diiSmooth - difSmooth, smoothditemps


########################################################################
def setupTimeDiffs():

  ### Get DII & DIF time correlation data for approach, suspect point,
  ### and TOI times
  diDiffs,diBadDiffs, diTOIDiff = timediffs.parsedoclines()

  ### Build good and supect arrays of DII-DIF time differences
  ### - append1.0 to prep goods for least-squares fit to remove slope
  goods = numpy.array( [ [i.imFbDiff,i.imFracSec,1.0] for i in diDiffs ] )
  bads = numpy.array( [ [i.imFbDiff,i.imFracSec] for i in diBadDiffs ] )

  ### Do least squares fit to good data
  A = goods[:,1:3].copy()             ### A i.e. [[t0,1],[t1,1],...]
  y = goods[:,0].copy()               ### y
  nll = numpy.linalg.lstsq( A, y )    ### ... do fit ...
  m,c = nll[0]                        ### x  i.e. y =  Ax

  ### Subtract fit from data, so mX+b becomes y=0; enhances deviations visually
  goods[:,0] = goods[:,0] - (m * goods[:,1] + c)
  bads[:,0] = bads[:,0] - (m * bads[:,1] + c)
  diTOIDiff.imFbDiff -= m * diTOIDiff.imFracSec + c

  ### Flatten data
  diffsAbstimes, diffsNets = goods[:,1].flatten(), goods[:,0].flatten()

  ### Select first data group i.e. within ~1h of first point
  iw = numpy.where( (diffsAbstimes-diffsAbstimes[0]) < 3610 )

  diffsGroup0 = numpy.mean( diffsAbstimes[iw] ), numpy.mean( diffsNets[iw] )
  
  return diffsAbstimes, diffsNets, diffsGroup0, m, bads, diTOIDiff


########################################################################
if __name__=="__main__":

  diffsAbstimes, diffsNets, diffsGroup0, m, bads, diTOIDiff = setupTimeDiffs()
  smoothTimes, diiSmooth, difSmooth, diffSmooth, smoothditemps = setupTemperatures()

  f,(timePlt,tempPlt) = plt.subplots( 2, 1, sharex=True)

  timePlt.plot( diffsGroup0[0], diffsGroup0[1], 'o', label='GoodAvg' )
  timePlt.plot( diffsAbstimes, diffsNets, '.', label='Good' )
  timePlt.plot( bads[:,1],bads[:,0], 'o', label='Suspect' )
  timePlt.plot( diTOIDiff.imFracSec, diTOIDiff.imFbDiff, 'o', label='TOI' )

  timePlt.legend( loc='lower left' )


  ### Plot DII and DIF raw data as points
  tempPlt.plot( smoothditemps.diitimes(),smoothditemps.diitemps(), '.', label='DII' )
  tempPlt.plot( smoothditemps.diftimes(), smoothditemps.diftemps(), '.', label='DIF' )

  ### Plot smoothed DII and DIF data as lines
  tempPlt.plot( smoothTimes,diiSmooth,label='DII smooth')
  tempPlt.plot( smoothTimes,difSmooth,label='DIF smooth')

  ### Plot DII-DIF differences, offset +10C
  tempPlt.plot(smoothTimes,10+diffSmooth,label='Smooth diff + 10')

  tempPlt.legend(loc='center left')

  plt.show()


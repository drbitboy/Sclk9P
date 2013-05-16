#!/usr/bin/env python
"""

"""
rawdata = """
170	0a46dff3	ca97c	0a46e0a3	9d5	172417011.8298	2005-06-19T01:36:52	172417187.6444	175.8145
170	0a46e24b	cc5fe	0a46e2fb	9ec	172417611.8371	2005-06-19T01:46:52	172417787.6502	175.8131
170	0a46e4a3	c640c	0a46e553	984	172418211.8120	2005-06-19T01:56:52	172418387.6236	175.8116
170	0a46e6fb	c8094	0a46e7ab	99b	172418811.8193	2005-06-19T02:06:52	172418987.6295	175.8102
170	0a46ebab	cb9ab	0a46ec5b	9c9	172420011.8340	2005-06-19T02:26:52	172420187.6413	175.8073
170	0a46ee03	cd638	0a46eeb3	9e0	172420611.8413	2005-06-19T02:36:52	172420787.6472	175.8059
171	0a4840ab	a3b6a	0a48415b	415	172507307.6706	2005-06-20T02:41:48	172507483.2675	175.5970
171	0a484303	9d996	0a4843b3	3ae	172507907.6455	2005-06-20T02:51:48	172508083.2412	175.5956
171	0a48455b	9f63a	0a48460b	3c5	172508507.6529	2005-06-20T03:01:48	172508683.2470	175.5942
171	0a4847b3	a12de	0a484863	3db	172509107.6602	2005-06-20T03:11:48	172509283.2527	175.5925
171	0a484a0b	9b10b	0a484abb	374	172509707.6351	2005-06-20T03:21:48	172509883.2263	175.5912
171	0a484c63	9cdb0	0a484d13	38b	172510307.6425	2005-06-20T03:31:48	172510483.2322	175.5897
171	0a484ebb	9ea54	0a484f6b	3a2	172510907.6498	2005-06-20T03:41:48	172511083.2381	175.5883
172	0a49c65d	d9987	0a49c70d	3b8	172607069.8913	2005-06-21T06:24:30	172607245.2437	175.3524
172	0a49c8b5	db643	0a49c965	3cf	172607669.8986	2005-06-21T06:34:30	172607845.2496	175.3510
172	0a49cb0d	d5485	0a49cbbd	367	172608269.8736	2005-06-21T06:44:30	172608445.2230	175.3494
172	0a49cd65	d7140	0a49ce15	37e	172608869.8810	2005-06-21T06:54:30	172609045.2289	175.3479
172	0a49cfbd	d8dfa	0a49d06d	395	172609469.8883	2005-06-21T07:04:30	172609645.2348	175.3464
172	0a49d215	daab5	0a49d2c5	3ac	172610069.8957	2005-06-21T07:14:30	172610245.2406	175.3450
172	0a49d46d	dc76f	0a49d51d	3c3	172610669.9030	2005-06-21T07:24:30	172610845.2465	175.3435
176	0a4f38b4	1549a	0a4f3962	84b	172964020.0872	2005-06-25T09:33:40	172964194.5435	174.4563
176	0a4f3b0c	1718e	0a4f3bba	862	172964620.0946	2005-06-25T09:43:40	172964794.5494	174.4548
176	0a4f3d64	1100e	0a4f3e12	7fb	172965220.0696	2005-06-25T09:53:40	172965394.5230	174.4534
176	0a4f3fbc	12d0a	0a4f406a	812	172965820.0771	2005-06-25T10:03:40	172965994.5289	174.4518
176	0a4f4214	14a0a	0a4f42c2	829	172966420.0845	2005-06-25T10:13:40	172966594.5348	174.4503
176	0a4f446c	1670c	0a4f451a	83f	172967020.0919	2005-06-25T10:23:40	172967194.5404	174.4485
176	0a4f46c4	1840f	0a4f4772	856	172967620.0993	2005-06-25T10:33:40	172967794.5463	174.4470
177	0a506998	1bd94	0a506a46	589	173042072.1141	2005-06-26T07:14:32	173042246.3628	174.2487
177	0a506bf0	15c70	0a506c9e	521	173042672.0892	2005-06-26T07:24:32	173042846.3361	174.2469
177	0a506e48	179c1	0a506ef6	538	173043272.0967	2005-06-26T07:34:32	173043446.3420	174.2453
177	0a5070a0	19712	0a50714e	54f	173043872.1042	2005-06-26T07:44:32	173044046.3479	174.2437
177	0a5072f8	1b462	0a5073a6	566	173044472.1117	2005-06-26T07:54:32	173044646.3538	174.2421
177	0a507550	15338	0a5075fe	4fe	173045072.0868	2005-06-26T08:04:32	173045246.3272	174.2403
177	0a5077a8	17083	0a507856	515	173045672.0943	2005-06-26T08:14:32	173045846.3331	174.2387
BAD:181	0a561dd6	61ffa	0a561e83	53d	173415894.4014	2005-06-30T15:04:54	173416067.3433	172.9419
TOI:185	0A5ADFD6	DA000	0A5AE083	690	173727702.8929	2005-07-04T05:41:43	173727875.4301	172.5372
#DOY	FbSecHex	FbSubHx	ImSecHex	ImSubHx	FbFracSec	FbPseudoDateAndTime	ImFracSec	ImFbDiff
#
#BAD:181 => Possible bad point?
#T0i:185 => TOI
"""
from collections import OrderedDict as OD

tab = '\t'
nl = '\n'

class didiff:
  def __init__(self,oneline):
    self.oneline = oneline.strip()
    doy,FbSecHex,FbSubHx,ImSecHex,ImSubHx,FbFracSec,FbPseudoDT,ImFracSec,ImFbDiff = self.oneline.split(tab)

    self.bad = doy[:4]=='BAD:'
    self.toi = doy[:4]=='TOI:'
    if self.bad or self.toi: doy = doy[4:]
    self.doy = int(doy)

    self.fbSec,self.fbSubsec,self.imSec,self.imSubsec = [ int(i,16) for i in [FbSecHex,FbSubHx,ImSecHex,ImSubHx]]

    self.fbPseudoDT = FbPseudoDT

    self.fbFracSec = self.fbSec + ( (self.fbSubsec << 0) / 1e6 )
    self.imFracSec = self.imSec + ( (self.imSubsec << 8) / 1e6 )

    self.imFbDiff = self.imFracSec - self.fbFracSec

    self.maxError = max( [abs(i-eval(j)) for i,j in [ (self.fbFracSec,FbFracSec,), (self.imFracSec,ImFracSec,), (self.imFbDiff,ImFbDiff,) ] ] )

  def __repr__(self):
    od = OD()
    od["Fb"] = self.fbFracSec
    od["Im"] = self.imFracSec
    od["ImFbDiff"] = self.imFbDiff
    od["MaxError"] = self.maxError
    od["BAD"] = self.bad
    od["TOI"] = self.toi
    return str(od)

def parselines(lines):
  diDiffs = []
  diBadDiffs = []
  diTOIDiff = None
  for oneline in [i.strip() for i in lines.strip().split(nl)]:
    if oneline[:0] == '#': continue
    try:
      newDiDiff = didiff(oneline)
      if newDiDiff.toi: diTOIDiff = newDiDiff
      elif newDiDiff.bad: diBadDiffs.append( newDiDiff )
      else: diDiffs.append( newDiDiff )
    except:
      #import traceback as tb
      #tb.print_exc()
      continue
  return diDiffs,diBadDiffs,diTOIDiff

def parsedoclines():
  return parselines( rawdata )

if __name__=="__main__":
  import sys
  if ( not sys.argv[1:] ) or ( sys.argv[1][:4]!='plot' ):
    import pprint
    pprint.pprint( parsedoclines() )
  else:
    import matplotlib.pyplot as plt
    import numpy
    diDiffs,diBadDiffs, diTOIDiff = parsedoclines()
    goods = numpy.array( [ [i.imFbDiff,i.imFracSec,1.0] for i in diDiffs ] )
    bads = numpy.array( [ [i.imFbDiff,i.imFracSec] for i in diBadDiffs ] )


    A = goods[:,1:3].copy()
    y = goods[:,0].copy()
    nll = numpy.linalg.lstsq( A, y )
    m,c = nll[0]

    goods[:,0] = goods[:,0] - (m * goods[:,1] + c)
    bads[:,0] = bads[:,0] - (m * bads[:,1] + c)

    toiDiff = diTOIDiff.imFbDiff - (m * diTOIDiff.imFracSec + c)

    plt.plot( goods[:,1],goods[:,0], '.', label='Good' )
    plt.plot( bads[:,1],bads[:,0], 'o', label='Suspect' )
    plt.plot( diTOIDiff.imFracSec, toiDiff, 'o', label='TOI' )
    plt.legend( loc='lower left' )
    plt.show()

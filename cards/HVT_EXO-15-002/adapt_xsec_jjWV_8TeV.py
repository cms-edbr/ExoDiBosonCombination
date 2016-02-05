from ROOT import *
import ROOT
import array, math
import os
import sys
from array import array

def get_theo_map():

   V_mass = array('d',[])

   brs = {}
   index = {}

   mapping = ["M0","M+","BRWW","BRhZ","BRZW","BRWh","CX+(pb)","CX0(pb)","CX-(pb)"]

   for m in xrange(0,len(mapping)):
      if mapping[m] != "M0" and mapping[m] != "M+":
   	 brs[mapping[m]] = array('d',[])
   	 #print mapping[m]

   f = open('xsect_HVT_8TeV.txt','r')
   for line in f:
      brDict = line.split(",")
      for d in xrange(0,len(brDict)):
   	 if brDict[d].find('\n') != -1:
   	    brDict[d] = brDict[d].split('\n')[0]
   	 for m in xrange(0,len(mapping)):
   	    if brDict[d] == mapping[m]:
   	       index[mapping[m]] = d
   	       #print "%s %i" %(mapping[m],d)
	    
   f.close()

   f = open('xsect_HVT_8TeV.txt','r')
   for line in f:
      if line.find('M0') != -1: continue
      brDict = line.split(",")  	    
      V_mass.append(float(brDict[index['M0']]))
      for m in xrange(0,len(mapping)):
   	 if mapping[m] != "M0" and mapping[m] != "M+":
   	    brs[mapping[m]].append(float(brDict[index[mapping[m]]]))

   f.close()

   return [brs,V_mass]
# This script changes multiplies the rate in the data cards
# from Bulk graviton cross section to W'/Z' cross sections
# and also account for the efficiency difference for Bulk and W'/Z' selection

gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.03)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(1.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

masses =[m*100 for m in range(10,29+1)]

if len(sys.argv)>1:
  masses=[int(sys.argv[1])]

thMap = get_theo_map()
xsecMap = thMap[0]
#massMap = thMap[1]

for mass in masses:

 #print "mass = ",mass
 m = int((mass-745)/5) #for jen's 8 TeV theo map 
 #m = int((mass-800)/100) #for jen'2 13 TeV theo map or 8 TeV alternative model B
 
 fWW=open("JJ_cards_8TeV/datacards/CMS_jj_WZ_"+str(mass)+"_8TeV_CMS_jj_VV.txt").readlines()
 outfile="JJ_cards_8TeV/datacards/CMS_jj_WVfix_"+str(mass)+"_8TeV_CMS_jj_VV.txt"
 print outfile
 f=open(outfile,"w")

 HVTVW={}
 HVTVW[mass]=(xsecMap['CX-(pb)'][m]+xsecMap['CX+(pb)'][m])*xsecMap['BRZW'][m]+xsecMap['CX0(pb)'][m]*xsecMap['BRWW'][m]

 for l in range(len(fWW)):
   if "rate" in fWW[l]:
     line="rate 				    "
     fWWsplit=fWW[l].replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
     for s in range(len(fWWsplit)):
       try:
 	 float(fWWsplit[s])
       except: continue
       signal=(s in [2,6]) # only change signal
       numberWW=float(fWWsplit[s])
       if signal:
 	 numberWW=numberWW*100.*HVTVW[mass]
       line+="%.5e  " % numberWW
     line+="\n"
     f.write(line)
   else:
     f.write(fWW[l])

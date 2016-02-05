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

masses =[m*100 for m in range(8,25+1)]

if len(sys.argv)>1:
  masses=[int(sys.argv[1])]

thMap = get_theo_map()
xsecMap = thMap[0]
massMap = thMap[1]

for mass in masses:
 #print "mass = ",mass
 m = int((mass-745)/5) #for jen's 8 TeV theo map 
 #m = int((mass-800)/100) #for jen'2 13 TeV theo map or 8 TeV alternative model B

 fZZ=open("LLJ_cards_8TeV/"+str(mass)+"/comb_xzz."+str(mass)+".txt").readlines()
 outfile="LLJ_cards_8TeV/"+str(mass)+"/comb_lljwz8."+str(mass)+".txt"
 print outfile
 f=open(outfile,"w")

 bulkZZ={}
 for line in open("xsect_BulkG_ZZ_c0p5_xsect_in_pb_factor4wrong.txt").readlines():
    split=line.replace(" ","").replace(" ","").replace(" ","").replace("\n","").split("\t")
    bulkZZ[int(split[0])]=float(split[1])

 HVTWZ={}
 HVTWZ[mass]=(xsecMap['CX-(pb)'][m]+xsecMap['CX+(pb)'][m])*xsecMap['BRZW'][m]

 for l in range(len(fZZ)):
   if "rate" in fZZ[l]:
     line="rate 				    "
     fZZsplit=fZZ[l].replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
     for s in range(len(fZZsplit)):
       try:
 	 float(fZZsplit[s])
       except: continue
       signal=(s in [1,3,5,7]) # only change signal
       numberZZ=float(fZZsplit[s])
       if signal:
 	 #print numberZZ/19700./bulkZZ[mass]/0.0941
 	 #numberZZ=numberZZ/bulkZZ[mass]*0.8*(HVTWZ[mass]*67.60/69.91/2.+0.27*HVTZH[mass]*57.7/67.60/2.) #factor /2 from combinatorics of llqq into ZZ or WZ
 	 numberZZ=numberZZ/bulkZZ[mass]*0.8*(HVTWZ[mass]*67.60/69.91/2.) #factor /2 from combinatorics of llqq into ZZ or WZ
       line+="%.5e  " % numberZZ
     line+="\n"
     f.write(line)
   else:
     f.write(fZZ[l])

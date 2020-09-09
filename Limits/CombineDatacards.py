from ROOT import *
import ROOT
import array, math
import os
from optparse import OptionParser
import sys

argv = sys.argv
parser = OptionParser()   
parser.add_option("-b", "--batch", dest="batch", default=False,action="store_true",
                              help="set batch mode")
parser.add_option("-s", "--signal", dest="signal", default="BulkWW",action="store",
                              help="set signal. only in batch mode")
parser.add_option("-m", "--mass", dest="mass", default=1200,action="store",
                              help="set mass. only in batch mode")
parser.add_option("-p", "--path", dest="path",action="store", default="/usr/users/dschaefer/CMSSW_7_4_7/src/DijetCombineLimitCode/",
                              help="set input path")
(opts, args) = parser.parse_args(argv) 

postfix = ""
#channels=["WZ","BulkWW","BulkZZ","ZprimeWW","qW","qZ"]
#channels=["altqW"]#,"ZprimeWW","WZ","qW","qZ"]
#channels=["WZ","ZprimeWW"]
channels=["WZ"]
outdir = opts.path+"datacards/"
if opts.batch:
    channels =[opts.signal]


for chan in channels:

    if "q" in chan:
       #masses =[m*100/2 for m in range(2*10,2*40+1)]
       masses =[m*100 for m in range(12,62+1)]
    else:
       masses =[m*50 for m in range(20,80+1)]
       masses =[m*100 for m in range(11,45+1)]
    if opts.batch:
        masses=[int(opts.mass)]
    for mass in masses:
        print "mass = ",mass

        # bin0="CMS_jj_VVHP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_VVHP.txt "
        # bin1="CMS_jj_VVLP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_VVLP.txt "
        # bin3="CMS_jj_qVHP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qVHP.txt "
        # bin4="CMS_jj_qVLP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qVLP.txt "
        
        bin5="CMS_jj_WWHP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_WWHP.txt "
        bin6="CMS_jj_WZHP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_WZHP.txt "
        bin7="CMS_jj_ZZHP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_ZZHP.txt "
    
        bin8="CMS_jj_WWLP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_WWLP.txt "
        bin9="CMS_jj_WZLP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_WZLP.txt "
        bin10="CMS_jj_ZZLP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_ZZLP.txt "
        
        bin11="CMS_jj_qWHP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qWHP.txt "
        bin12="CMS_jj_qZHP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qZHP.txt "
        
        bin13="CMS_jj_qWLP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qWLP.txt "
        bin14="CMS_jj_qZLP="+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qZLP.txt "
        
        
        # bin01="/mnt/t3nfs01/data01/shome/dschafer/DijetCombineLimitCode/datacards/"+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_VV.txt "
        # bin34="/mnt/t3nfs01/data01/shome/dschafer/DijetCombineLimitCode/datacards/"+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qV.txt "
        
        bin567=""+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_VVHPnew.txt "
        bin8910=""+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_VVLPnew.txt "
        bin5678910=""+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_VVnew.txt "
        
        bin1112=""+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qVHPnew.txt "
        bin1314=""+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qVLPnew.txt "
        bin11121314=""+outdir+postfix+"CMS_jj_"+chan+"_"+str(mass)+"_13TeV_CMS_jj_qVnew.txt "

        # comb01 = "combineCards.py " + bin0 + bin1 + " >" + bin01
        # comb34 = "combineCards.py " + bin3 + bin4 + " >" + bin34
        
        comb567 = "combineCards.py " + bin5 + bin6 + bin7 + " >" + bin567
        comb8910 = "combineCards.py " + bin8 + bin9 + bin10 + " >" + bin8910
        comb5678910 = "combineCards.py " + bin5 + bin6 + bin7+ bin8 + bin9 + bin10 +  " >" + bin5678910
        
        comb1112 = "combineCards.py " + bin11 + bin12 + " >" + bin1112
        comb1314 = "combineCards.py " + bin13 + bin14 + " >" + bin1314
        comb11121314 = "combineCards.py " + bin11 + bin12 + bin13 + bin14 + " >" + bin11121314
        

        if "q" in chan:
            # print comb34
            # os.system( comb34  )
            print comb1112
            os.system( comb1112  )
            print comb1314
            os.system( comb1314  )
            print comb11121314
            os.system( comb11121314  )
            
        else:
          # print comb01
          # os.system( comb01  )
          print comb567
          os.system( comb567  )
          print comb8910
          os.system( comb8910  )
          print comb5678910
          os.system( comb5678910  )

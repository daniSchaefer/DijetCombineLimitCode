import numpy
import tempfile
import platform
from copy import deepcopy
import subprocess
import ROOT 
from ROOT import *



def getXSweight(mass):
    xsWfile = TFile.Open("/usr/users/dschaefer/CMSSW_7_4_7/src/DijetCombineLimitCode/Limits/WZ_xSecUnc.root","READ")
    xsWgraph = xsWfile.Get("gtheory")
    upW = xsWfile.Get("gtheoryUP")
    downW = xsWfile.Get("gtheoryDOWN")
    xsW = xsWgraph.Eval(mass,0,"S")
    xsZfile = TFile.Open("/usr/users/dschaefer/CMSSW_7_4_7/src/DijetCombineLimitCode/Limits/ZprimeWW_xSecUnc.root","READ")
    xsZgraph = xsZfile.Get("gtheory")
    xsZ = xsZgraph.Eval(mass,0,"S")
    upZ = xsZfile.Get("gtheoryUP")
    downZ = xsZfile.Get("gtheoryDOWN")
    xsZup = xsZ/upZ.Eval(mass,0,"S")
    xsZdown = xsZ/downZ.Eval(mass,0,"S")
    xsWup = xsW/upW.Eval(mass,0,"S")
    xsWdown = xsW/downW.Eval(mass,0,"S")
    #xsWeight = xsZ/xsW
    #print xsZ
    #print xsW
    xsWeight=[xsW,xsZ,xsWup,xsWdown,xsZup,xsZdown]
    return xsWeight


def getUncertainties(i,result,unc):
    if unc in i:
            a,b = i.split("lnN")
            r = b.split("   ")
            #print r
            for x in r:
                if x == "":continue
                result[unc] = x
                break


def readDatacard(filename):
    result ={}
    config = open(filename,'r')
    for i in config.readlines():
        #if '#' in i: continue
        if 'rate' in i:
            a,b = i.split("rate")
            r = b.split("   ")
            #print r
            for x in r:
                if x == "": continue
                #print float(x)
                if float(x) > 0 and float(x)!=1.0:
                    result['rate'] = float(x)
        getUncertainties(i,result,"CMS_mass_scale_j_13TeV")
        getUncertainties(i,result,"CMS_mass_res_j_13TeV")
        getUncertainties(i,result,"CMS_scale_j_13TeV")
        getUncertainties(i,result,"CMS_res_j_13TeV")
    #print result
    return result
            
            
            
            
 

          
          
if __name__=="__main__":
    channels = ["WWHP","WZHP","ZZHP","WWLP","WZLP","ZZLP"]
    for channel in channels:
        for m in range(41,46):
            mass = float(m)/10.
        
            xsweight= getXSweight(mass)
            print "for mass "+str(mass*1000)
            print "cross section " 
            print xsweight
            print "calculated rate:"
        
            wprime = readDatacard("datacards/CMS_jj_WZ_"+str(int(mass*1000))+"_13TeV_CMS_jj_"+channel+".txt")
            zprime = readDatacard("datacards/CMS_jj_ZprimeWW_"+str(int(mass*1000))+"_13TeV_CMS_jj_"+channel+".txt")
            HVTdatacard = open("datacards/CMS_jj_HVTtriplett_"+str(int(mass*1000))+"_13TeV_CMS_jj_"+channel+".txt",'w')
        
            config = open("datacards/CMS_jj_WZ_"+str(int(mass*1000))+"_13TeV_CMS_jj_"+channel+".txt",'r')
            for line in config.readlines():
                if "CMS_xs_unc_13TeV" in line:
                    continue
                if 'rate' in line:
                    #HVTdatacard.write( "rate                      " + str(wprime['rate']*(0.6991*0.6760))+"          "+str(xsweight[1]/xsweight[0]*zprime['rate'])+"         "+str(1)+"\n")
                    HVTdatacard.write( "rate                      " + str(wprime['rate']*(0.6991*0.6760)*xsweight[0]/0.01)+"          "+str(xsweight[1]*zprime['rate']/0.01)+"         "+str(1)+"\n")
                    print "rate                      " + str(wprime['rate']*(0.6991*0.6760)*xsweight[0]/0.01)+"          "+str(xsweight[1]*zprime['rate']/0.01)+"         "+str(1)+"\n"
                    HVTdatacard.write( "CMS_xs_unc_13TeV  lnN "+str(round(max(xsweight[2],xsweight[3]),1))+" "+str(round(max(xsweight[4],xsweight[5]),1))+" -\n")
                    #HVTdatacard.write( "CMS_xs_unc_13TeV  lnN "+str(round(xsweight[2],1))+"/"+str(round(xsweight[3],1))+" "+str(round(xsweight[4],1))+"/"+str(round(xsweight[5],1))+" -\n")
                    continue
                if 'CMS_mass_scale_j_13TeV' in line:
                    HVTdatacard.write( "CMS_mass_scale_j_13TeV       lnN      " + str(wprime['CMS_mass_scale_j_13TeV'])+"          "+str(zprime['CMS_mass_scale_j_13TeV'])+"         -\n")
                    continue
                if 'CMS_mass_res_j_13TeV' in line:
                    HVTdatacard.write( "CMS_mass_res_j_13TeV         lnN      " + str(wprime['CMS_mass_res_j_13TeV'])+"          "+str(zprime['CMS_mass_res_j_13TeV'])+"         -\n")
                    continue
                if 'CMS_scale_j_13TeV' in line:
                    HVTdatacard.write( "CMS_scale_j_13TeV            lnN      " + str(wprime['CMS_scale_j_13TeV'])+"          "+str(zprime['CMS_scale_j_13TeV'])+"         -\n")
                    continue
                if 'CMS_res_j_13TeV' in line:
                    HVTdatacard.write( "CMS_res_j_13TeV              lnN      " + str(wprime['CMS_res_j_13TeV'])+"          "+str(zprime['CMS_res_j_13TeV'])+"         -\n")
                    continue
                HVTdatacard.write(line)
        
    

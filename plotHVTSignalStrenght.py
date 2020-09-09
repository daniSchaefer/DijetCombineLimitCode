import ROOT as rt
import time
import CMS_lumi, tdrstyle
from ROOT import *
import os
import glob
import math
import array
import sys
import time
import random
import numpy as np
from optparse import OptionParser

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = ""
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4



def plotGraph(modelname,channel,radmasses,color,obs=False):
    
    efficiencies={}
    rad = []
    limits = []
    filenames =[]
    for m in radmasses:
        filename = "Limits/CMS_jj_"+str(int(m))+"_"+modelname+"_13TeV_CMS_jj_"+channel+"_asymptoticCLs_new.root"
        #filename = "withoutPDFandScale/CMS_jj_"+str(int(m*1000))+"_"+modelname+"_13TeV_CMS_jj_"+channel+"_asymptoticCLs_new.root"
        filenames.append(filename)
        efficiencies[m]=1

    for onefile in filenames:
        print "using file " + onefile
        file = rt.TFile(onefile)
        tree = file.Get("limit")
        print tree
        limits = []
        for quantile in tree:
            limits.append(tree.limit)
            print ">>>   %.2f" % limits[-1]
            print limits

        rad.append(limits[:6])
    

    print limits
    print rad
    x = []
    yobs = []
    y2up = []
    y1up = []
    y1down = []
    y2down = []
    ymean = []

    for i in range(0,len(efficiencies)):
        y2up.append(rad[i][0]*efficiencies[radmasses[i]])
        y1up.append(rad[i][1]*efficiencies[radmasses[i]])
        ymean.append(rad[i][2]*efficiencies[radmasses[i]])
        y1down.append(rad[i][3]*efficiencies[radmasses[i]])
        y2down.append(rad[i][4]*efficiencies[radmasses[i]])
        yobs.append(rad[i][5]*efficiencies[radmasses[i]])
     
    grobs = rt.TGraphErrors(1)
    grobs.SetMarkerStyle(8)
    grobs.SetMarkerSize(0.8)
    grobs.SetLineColor(kBlack)
    grobs.SetLineWidth(2)


    grmean = rt.TGraphErrors(1)
    grmean.SetLineColor(1)
    grmean.SetLineWidth(4)
    grmean.SetLineStyle(3)
   
    print len(rad)
    print len(radmasses)
    print len(y2up)
    n = len(radmasses)
    grgreen = rt.TGraph(2*n)
    for r in range(0,len(radmasses)):
        radmasses[r] = radmasses[r]*0.001
    for i in range(0,n):
        grgreen.SetPoint(i,radmasses[i],y2up[i])
        grgreen.SetPoint(n+i,radmasses[n-i-1],y2down[n-i-1])

    grgreen.SetFillColor(rt.kOrange)
    grgreen.SetLineColor(rt.kOrange)
    grgreen.SetFillStyle(1001)


    gryellow = rt.TGraph(2*n)
    for i in range(0,n):
        gryellow.SetPoint(i,radmasses[i],y1up[i])
        gryellow.SetPoint(n+i,radmasses[n-i-1],y1down[n-i-1])

    gryellow.SetFillColor(rt.kGreen+1)
    gryellow.SetLineColor(rt.kGreen+1)
    gryellow.SetFillStyle(1001)
    
    for j in range(0,len(radmasses)):
        grobs.SetPoint(j, radmasses[j], yobs[j])
        print str(radmasses[j])+ " "+str( yobs[j])
        grmean.SetPoint(j, radmasses[j], ymean[j])
       
    print grobs.Eval(3.750)
    return [grobs,grmean,gryellow,grgreen]
   
def Plot(modelname,channel,radmasses,obs):
    #mg = rt.TMultiGraph()
    #mg.SetTitle("X -> ZZ")
    #mg.Add(gr2up)#.Draw("same")
    #mg.Add(gr1up)#.Draw("same")
    #mg.Add(grmean,"L")#.Draw("same,AC*")
    #mg.Add(gr1down)#.Draw("same,AC*")
    #mg.Add(gr2down)#.Draw("same,AC*")
    #if obs: mg.Add(grobs,"L")#.Draw("AC*")
    
    
    H_ref = 600; 
    W_ref = 800; 
    W = W_ref
    H  = H_ref
  
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.15*W_ref
    R = 0.04*W_ref

    c1 = rt.TCanvas("c1","c1",50,50,W,H)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.GetWindowHeight()
    c1.GetWindowWidth()
    #c1.SetGrid()
    c1.SetLogy()
    c1.cd()
    
    leg = rt.TLegend(0.3,0.7002591,0.606734,0.9011917)
    leg2 = rt.TLegend(0.3,0.7002591,0.606734,0.9011917)
    leg.SetTextSize(0.038)
    leg.SetLineColor(0)
    leg.SetShadowColor(0)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(kWhite)
    # leg.SetFillStyle(0)
    leg.SetMargin(0.35)
    leg2.SetTextSize(0.038)
    leg2.SetLineColor(0)
    leg2.SetShadowColor(0)
    leg2.SetLineStyle(1)
    leg2.SetLineWidth(1)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(0)
    leg2.SetMargin(0.35)
    
    
    graphs = plotGraph(modelname,channel,radmasses,2)
    graphs[3].GetXaxis().SetLimits(1.2,4.1)
    graphs[3].GetYaxis().SetLimits(0.001,100)
    graphs[3].GetYaxis().SetTitleOffset(1.15)
    graphs[3].GetXaxis().SetTitleOffset(1.05)
    
    
    leg.AddEntry(graphs[0], "Observed", "Lp")
    leg.AddEntry(graphs[2], "Expected #pm 1 std. deviation", "f")
    leg.AddEntry(graphs[3] , "Expected #pm 2 std. deviation", "f")
    leg2.AddEntry(graphs[0], " ", "")
    leg2.AddEntry(graphs[1], " ", "L")
    leg2.AddEntry(graphs[1], " ", "L")
    
    
    graphs[3].GetYaxis().SetTitleSize(0.05)
    graphs[3].GetXaxis().SetTitleSize(0.05)
    graphs[3].GetXaxis().SetTitle("M_{W'/Z'} (TeV)")
    graphs[3].GetYaxis().SetTitle("#frac{#sigma #times #bf{#it{#Beta}}(W'/Z' #rightarrow WW/WZ)}{#sigma_{HVT model B}}")
    graphs[3].SetMaximum(30)
    graphs[3].Draw("FA")
    graphs[2].Draw("Fsame")
    graphs[1].Draw("Lsame")
    graphs[0].Draw("LPsame")
    print graphs[0].Eval(1.3)
    
    line = TLine(1.2,1,4.1,1)
    line.SetLineWidth(2)
    line.SetLineColor(kRed)
    line.Draw("same")
    #c1.Update() 
    #frame = c1.GetFrame()
    #frame.Draw()
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
    c1.cd()
    c1.Update()
    #c1.RedrawAxis()
    c1.RedrawAxis("g")
    leg.Draw("same")
    leg2.Draw("same")
    #c1.cd()
    #c1.Update()
    
    #c1.cd()
    #c1.Update()
    c1.SaveAs("testHVT.pdf")
    c1.SaveAs("testHVT.png")
    c1.SaveAs("testHVT.jpg")
    
    
    
    
    
    
   
if __name__=="__main__":
    radmasses=[]
    for i in range(12,42):
        radmasses.append(i*100)
    Plot("HVTtriplett","VVnew",radmasses,True)
   

import time,sys
from ROOT import *
from ROOT import gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooArgusBG,RooDataSet, RooExponential,RooBreitWigner, RooVoigtian, RooNovosibirsk, RooRealVar,RooFormulaVar, RooDataHist, RooHist,RooCategory, RooChebychev, RooSimultaneous, RooGenericPdf,RooConstVar, RooKeysPdf, RooHistPdf, RooEffProd, RooProdPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan, kMagenta, kWhite
import CMS_lumi, tdrstyle

#ROOT.gSystem.Load("./PDFs/PdfDiagonalizer_cc.so")
#ROOT.gSystem.Load("./PDFs/Util_cxx.so")
#ROOT.gSystem.Load("./PDFs/HWWLVJRooPdfs_cxx.so")

#from ROOT import draw_error_band, draw_error_band_extendPdf, draw_error_band_Decor, draw_error_band_shape_Decor, Calc_error_extendPdf, Calc_error, RooErfExpPdf, RooAlpha, RooAlpha4ErfPowPdf, RooAlpha4ErfPow2Pdf, RooAlpha4ErfPowExpPdf, PdfDiagonalizer, RooPowPdf, RooPow2Pdf, RooErfPowExpPdf, RooErfPowPdf, RooErfPow2Pdf, RooQCDPdf, RooUser1Pdf, RooBWRunPdf, RooAnaExpNPdf, RooExpNPdf, RooAlpha4ExpNPdf, RooExpTailPdf, RooAlpha4ExpTailPdf, Roo2ExpPdf, RooAlpha42ExpPdf

def get_canvas(cname):

   #tdrstyle.setTDRStyle()
   CMS_lumi.lumi_13TeV = ""
   CMS_lumi.lumi_sqrtS = ""
   CMS_lumi.writeExtraText = 1
   CMS_lumi.extraText = "Simulation"

   iPos = 11
   if( iPos==0 ): CMS_lumi.relPosX = 0.15

   H_ref = 630#600; 
   W_ref = 600#800; 
   W = W_ref
   H  = H_ref

   T = 0.08*H_ref
   B = 0.12*H_ref 
   L = 0.12*W_ref
   R = 0.06*W_ref

   canvas = TCanvas(cname,cname,W,H)
   canvas.SetFillColor(0)
   canvas.SetBorderMode(0)
   canvas.SetFrameFillStyle(0)
   canvas.SetFrameBorderMode(0)
   canvas.SetLeftMargin( L/W )
   canvas.SetRightMargin( R/W )
   canvas.SetTopMargin( T/H )
   canvas.SetBottomMargin( B/H+0.03 )
   canvas.SetTickx()
   canvas.SetTicky()
   
   return canvas

tdrstyle.setTDRStyle()
       

fin = TFile.Open('workspaces/B2G17001/CMS_jj_qW_1200_13TeV.root')

fin.ls()
workspace = fin.Get("w_all")
workspace.Print()

print "----------- Parameter Workspace -------------";
parameters_workspace = workspace.allVars();
par = parameters_workspace.createIterator();
par.Reset();
param = par.Next()
while (param):
    param.Print();
    param=par.Next()
print "---------------------------------------------";

#workspace.data("data_obs_CMS_jj_WWHP").Print()

print "----------- Pdf in the Workspace -------------";
pdfs_workspace = workspace.allPdfs();
par = pdfs_workspace.createIterator();
par.Reset();
param=par.Next()
while (param):
    param.Print();
    param = par.Next()
print "----------------------------------------------";


#sys.exit()

indir = 'workspaces/B2G17001/'

##### bulkg ####
files_g = []
files_g.append(TFile(indir+"CMS_jj_qW_1200_13TeV.root","READ"))
masses = [1200,2000,3000,4000,5000]
for m in masses:
 files_g.append(TFile(indir+"CMS_jj_qW_%s_13TeV.root"%(m),"READ"))

ws_g = []
for f in files_g:
 ws_g.append(f.Get("w_all"))
 pdfs_workspace = ws_g[-1].allPdfs();
 par = pdfs_workspace.createIterator();
 par.Reset();
 param=par.Next()
 while (param):
    param.Print();
    param = par.Next()
 
models_g = []
signalMC =[]
for w in range(len(ws_g)):
 models_g.append(ws_g[w].pdf("qW_jj_CMS_jj_qZHP"))
 
 #else: models_g.append(ws_g[w].pdf("BulkWW_xww_mu_HPW"))

################

###### wprime ####
#files_wp = []
#masses = [800,1000,2000,3000,4000]
#for m in masses:
 #files_wp.append(TFile(indir+"Wprime_EXO-15-002-paper/comb_%i/wwlvj_Wprime_WZ_lvjj_M%i_mu_HPZ_workspace.root"%(m,m),"READ"))

#ws_wp = []
#for f in files_wp:
 #ws_wp.append(f.Get("workspace4limit_"))

#models_wp = []
#for w in ws_wp:
 #models_wp.append(w.pdf("WprimeWZ_xww_mu_HPZ"))
 
#################

###### zprime ####
#files_zp = []
#files_zp.append(TFile(indir+"Zprime_EXO-15-002-paper/comb_800/wwlvj_Zprime800_mu_HP_workspace.root","READ"))
#masses = [1000,2000,3000,4000]
#for m in masses:
 #files_zp.append(TFile(indir+"Zprime_EXO-15-002-paper/comb_%i/wwlvj_Zprime_WW_lvjj_M%i_mu_HPW_workspace.root"%(m,m),"READ"))

#ws_zp = []
#for f in files_zp:
 #ws_zp.append(f.Get("workspace4limit_"))

#models_zp = []
#for w in range(len(ws_zp)):
 #if w==0: models_zp.append(ws_zp[w].pdf("Zprime800_xww_mu_HP"))
 #else: models_zp.append(ws_zp[w].pdf("ZprimeWW_xww_mu_HPW"))
 
#################

l = TLegend(0.3607383,0.6063123,0.5704698,0.8089701);
l.SetLineWidth(2)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetTextFont(42)
l.SetTextSize(0.03)
l.SetTextAlign(12)

x = ws_g[1].var("mgg13TeV")
plot = x.frame(RooFit.Title("")) ;
plot.SetXTitle("m_{lvj} (GeV)")
plot.SetYTitle("Arbitrary scale")

for m in models_g:
 m.plotOn(plot,RooFit.LineColor(kAzure+1),RooFit.LineWidth(2),RooFit.Range(1000,6500))
#for m in models_wp:
 #m.plotOn(plot,RooFit.LineColor(kAzure+5),RooFit.LineWidth(2))
#for m in models_zp:
 #m.plotOn(plot,RooFit.LineColor(kAzure+3),RooFit.LineWidth(2))

h_g = TH1F("h_g","h_g",1,0,1) 
h_g.SetLineColor(kAzure+1)
h_g.SetLineWidth(2)
h_wp = TH1F("h_wp","h_wp",1,0,1) 
h_wp.SetLineColor(kAzure+5)
h_wp.SetLineWidth(2)
h_zp = TH1F("h_zp","h_zp",1,0,1) 
h_zp.SetLineColor(kAzure+3)
h_zp.SetLineWidth(2)

#l.AddEntry(h_g,'G_{bulk} #rightarrow WW (MADGRAPH)','L')
#l.AddEntry(h_wp,"W' #rightarrow WZ (MADGRAPH)",'L')
#l.AddEntry(h_zp,"Z' #rightarrow WW (MADGRAPH)",'L')

canv = get_canvas("c")
canv.cd()

plot.Draw()
l.Draw()

canv.Update()
canv.cd()
CMS_lumi.CMS_lumi(canv, 4, 11)	
canv.cd()
canv.Update()
canv.RedrawAxis()
frame = canv.GetFrame()
frame.Draw()   
canv.cd()
canv.Update()

time.sleep(10000)

#'''
#workspace = files[0].Get("workspace4limit_")
#workspace.Print()

#print "----------- Pdf in the Workspace -------------"
#pdfs_workspace = workspace.allPdfs()
#par = pdfs_workspace.createIterator()
#par.Reset()
#param=par.Next()
#while (param):
    #param.Print()
    #param = par.Next()
#print "----------------------------------------------"
#'''

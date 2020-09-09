import ROOT as rt
from array import *
import time
import CMS_lumi, tdrstyle
from heapq import nsmallest


tdrstyle.setTDRStyle()
rt.gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = ""
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4



rt.gStyle.SetOptFit(1)

massBins =[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 990, 1058,
             1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 
             4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808] 

xbins = array('d',massBins)


fileIN = rt.TFile.Open("/usr/users/dschaefer/SFrame_setup/ExoDiBosonAnalysis/results/ReRecoData_qVdijet_test.root")

scalesigmas= [4.35053e+00,3.33072e+00, 3.22366e+00,4.49552e+00] #qWHP,qWLP,qZHP,qZLP @ 4 TeV
alphas     = [1.07854e+00,7.94829e-01, 9.29944e-01,9.75533e-01]
sigfracs   = [1.56120e-01,1.95228e-01, 2.13429e-01,1.93622e-01]
means      = [4.00728e+03,4.01984e+03, 4.01382e+03,4.02231e+03]
signs      = [1.29946e+02,1.15277e+02, 1.24129e+02,1.21744e+02]
sigmas     = [1.71478e+02,1.50507e+02, 1.54579e+02,1.77653e+02]    

signalrate      = [11.9712,8.56735,13.0257,6.47405]
scaleToExcluded = [1. ,1. ,1. ,1.] #xsec*100, to account for assuming signal cross section of 0.01pb in workspace!

parameters=[3,3,3,3] 
xsec=[0.01] #pb
categories = ["qW, high-purity","qW, low-purity","qZ, high-purity","qZ, low-purity"]
legends=["q*(4 TeV)#rightarrowqW","q*(4 TeV)#rightarrowqW","q*(4 TeV)#rightarrowqZ","q*(4 TeV)#rightarrowqZ"]         
histos = ["DijetMassHighPuriqW","DijetMassLowPuriqW","DijetMassHighPuriqZ", "DijetMassLowPuriqZ"]
#histos = ["DijetMassLowPuriqW"]
lumi = 35867.
outdir = "/usr/users/dschaefer/SFrame_setup/ExoDiBosonAnalysis/results/"
# parameters=[4]
# categories = ["qZ, high-purity"]
# legends=["q^{*}(2 TeV)#rightarrowqZ"]
# histos = ["DijetMassHighPuriqZ"]

#
ii = -1        
for h in histos:
    ii += 1
    # if ii !=4: continue
    title = h.replace("DijetMass","")
    print fileIN.GetName()
    print h
    htmp = fileIN.Get(h)
  
    
    firstbin = 1058 # htmp.GetBinCenter(htmp.FindFirstBinAbove(0.99999))
    lastbin = htmp.GetBinCenter(htmp.FindLastBinAbove(0.99999))
    lower = (nsmallest(2, massBins, key=lambda x: abs(x-lastbin)))[0]
    higher  = (nsmallest(2, massBins, key=lambda x: abs(x-lastbin)))[1]
    if lower > higher:
      fFitXmax = lower
    if higher > lower:
      fFitXmax = higher
    maxbintest =0
    for i in range(0,htmp.GetNbinsX()):
        ctmp = htmp.GetBinContent(i)
        if ctmp >0.99999:
            maxbintest = htmp.GetBinCenter(i) 
    print maxbintest
    print lastbin
    print "Last non-zero bin is at x=%f. Closest dijet mass bins are L = %i  H = %i" %(lastbin,lower,higher)
    print "Using x max = %i" %fFitXmax
    


    dataDistOLD = htmp.Rebin(len(xbins)-1,"hMass_rebinned",xbins)
    minVal = 1058
    maxVal = fFitXmax
    print "Using x min = %i  x max = %i" %(minVal,maxVal)


    bins = []
    for i in range(0, dataDistOLD.GetXaxis().GetNbins()):
        thisVal = dataDistOLD.GetXaxis().GetBinLowEdge(i+1)
        if thisVal >= minVal and thisVal <= maxVal:
          bins.append(dataDistOLD.GetXaxis().GetBinLowEdge(i+1))

    dataDist = htmp #rt.TH1F("dataDist", "dataDist", len(xbins)-1, array('d',xbins))
    # for i in range(0, dataDistOLD.GetXaxis().GetNbins()):
#         binCenter = dataDistOLD.GetXaxis().GetBinCenter(i+1)
#         binContent = dataDistOLD.GetBinContent(i+1)
#         binWidth = dataDistOLD.GetBinWidth(i+1)
#         if binCenter >= minVal:
#             iBin =  dataDist.GetXaxis().FindBin(binCenter)
#             dataDist.SetBinContent(iBin, binContent)
#
    
                      
    p1 = rt.RooRealVar("p1", "p1",9.28433e+00, -100. , 100.)
    p2 = rt.RooRealVar("p2", "p2",1.03641e+01, -200, 200)
    p3 = rt.RooRealVar("p3", "p3",2.35256e+00, -100., 100.)
    p4 = rt.RooRealVar("p4", "p4",4.17695e-01, -100., 100.)

    mjj = rt.RooRealVar("mjjCMS","Dijet invariant mass (GeV)",len(bins)-1, bins[0], bins[-1])

    # bkg_fit = rt.RooGenericPdf("bkg_fitCMS", "pow(1-@0/13000., @1)/pow(@0/13000., @2+@3*log(@0)+@4*pow(log(@0),2))", rt.RooArgList(mjj, p1, p2, p3, p4))
    # bkg_fit = rt.RooGenericPdf("bkg_fitCMS", "pow(1-@0/13000., @1)/pow(@0/13000., @2+@3*log(@0/13000.))", rt.RooArgList(mjj, p1, p2,p3))
    bkg_fit = rt.RooGenericPdf("bkg_fitCMS", "pow(1-@0/13000., @1)/pow(@0/13000., @2)", rt.RooArgList(mjj, p1, p2))
    #if ii == 0:  
      #bkg_fit = rt.RooGenericPdf("bkg_fitCMS", "pow(1-@0/13000., @1)/ ( pow(@0/13000., @2+@3*log(@0/13000.)+@4*pow(log(@0/13000.),2)) )", rt.RooArgList(mjj, p1, p2, p3, p4))


    alpha       = rt.RooRealVar("alpha","alpha",alphas[ii])
    sigfrac     = rt.RooRealVar("sigfrac","sigfrac",sigfracs[ii])
    scalesigma  = rt.RooRealVar("scalesigma","scalesigma",scalesigmas[ii])
    mean        = rt.RooRealVar("mean","mean",means[ii])
    # gmean       = rt.RooRealVar("gmean","gmean",gmeans[ii])
    sign        = rt.RooRealVar("sign","sign",signs[ii])
    sigma       = rt.RooRealVar("sigma","sigma",sigmas[ii])
    gsigma      = rt.RooFormulaVar("gsigma","@0*@1", rt.RooArgList(sigma,scalesigma))
    
    gauss = rt.RooGaussian("gauss", "gauss", mjj, mean, gsigma)
    cb    = rt.RooCBShape("cb", "cb",mjj, mean, sigma, alpha, sign)
    sig_fit = rt.RooAddPdf("sigP", "sigP",gauss, cb, sigfrac)
    
    scalesigma.setConstant(rt.kTRUE)
    sigfrac.setConstant(rt.kTRUE)
    alpha.setConstant(rt.kTRUE)
    sign.setConstant(rt.kTRUE)
    mean.setConstant(rt.kTRUE)
    # gmean.setConstant(rt.kTRUE)
    sigma.setConstant(rt.kTRUE)

    syield = signalrate[ii]*scaleToExcluded[ii]
    nsig = rt.RooRealVar("NsExp", "Expected signal yield",syield, 0, 10)
    signalPDF = rt.RooExtendPdf("mysig","mysig",sig_fit,nsig)
    nsig.setConstant(rt.kTRUE)

    s = rt.RooRealVar("Ns", "signal yield",0.)
    b = rt.RooRealVar("Nb", "background yield", dataDist.Integral(), 0, dataDist.Integral()*2.)

    sumPDF = rt.RooAddPdf("sum", "gaussian plus exponential PDF", rt.RooArgList(sig_fit, bkg_fit), rt.RooArgList(s, b))

    s.setConstant(rt.kTRUE)

    mjjbins = rt.RooBinning(len(bins)-1, array('d',bins), "mjjbins")
    mjj.setBinning(mjjbins)

    ws = rt.RooWorkspace("ws","ws")
    getattr(ws,'import')(p1)
    getattr(ws,'import')(p2)
    getattr(ws,'import')(p3)
    getattr(ws,'import')(p4)
    getattr(ws,'import')(mjj)
    getattr(ws,'import')(mean)
    # getattr(ws,'import')(gmean)
    getattr(ws,'import')(sigma)
    getattr(ws,'import')(scalesigma)
    getattr(ws,'import')(s)
    getattr(ws,'import')(b)
    getattr(ws,'import')(sign)
    getattr(ws,'import')(alpha)
    getattr(ws,'import')(sigfrac)
    getattr(ws,'import')(sumPDF)
    getattr(ws,'import')(signalPDF)
    getattr(ws,'import')(bkg_fit)

    dataset = rt.RooDataHist("dataCMS", "dataCMS", rt.RooArgList(mjj), rt.RooFit.Import(dataDist))
    getattr(ws,'import')(dataset)
    
    
    currentlist = rt.RooLinkedList()
    cmd=rt.RooFit.Save()
    currentlist.Add(cmd)
    
    
      # for r in range(0,10):
    fr = sumPDF.fitTo(dataset,rt.RooFit.Save())
      # fr = sumPDF.chi2FitTo(dataset,currentlist)
 


    frame = mjj.frame()
    dataset.plotOn(frame,rt.RooFit.DataError(rt.RooAbsData.Poisson), rt.RooFit.Binning(mjjbins),rt.RooFit.Name("data"),rt.RooFit.Invisible())
    sumPDF.plotOn(frame, rt.RooFit.VisualizeError(fr,1),rt.RooFit.FillColor(rt.kRed-7),rt.RooFit.LineColor(rt.kRed-7),rt.RooFit.Name("fiterr"), rt.RooFit.Binning(mjjbins))
    sumPDF.plotOn(frame,rt.RooFit.LineColor(rt.kRed+1),rt.RooFit.Name("sumPDF"))
    
    frame3 = mjj.frame()
    hpull = frame.pullHist("data","sumPDF",True)
    frame3.addPlotable(hpull,"X0 P E1")
   
    
    dataset.plotOn(frame,rt.RooFit.DataError(rt.RooAbsData.Poisson), rt.RooFit.Binning(mjjbins),rt.RooFit.Name("data"))#,rt.RooFit.XErrorSize(0))
    mjj.setRange("sigRegion",4000*0.8,4000*1.2) ;
    signalPDF.plotOn(frame,rt.RooFit.LineColor(rt.kBlack),rt.RooFit.LineStyle(rt.kDashed),rt.RooFit.Binning(mjjbins),rt.RooFit.Name("sig"),rt.RooFit.Normalization(1, rt.RooAbsReal.RelativeExpected),rt.RooFit.Range("sigRegion"))

    
    

    c1 =rt.TCanvas("c1","",800,800)
    c1.SetLogy()
    c1.Divide(1,2,0,0,0)
    c1.SetLogy()
    c1.cd(1)
    p11_1 = c1.GetPad(1)
    p11_1.SetPad(0.01,0.26,0.99,0.98)
    p11_1.SetLogy()
    p11_1.SetRightMargin(0.05)
    
    p11_1.SetTopMargin(0.1)
    p11_1.SetBottomMargin(0.02)
    p11_1.SetFillColor(0)
    p11_1.SetBorderMode(0)
    p11_1.SetFrameFillStyle(0)
    p11_1.SetFrameBorderMode(0)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetTitleOffset(0.98)
    # frame.GetYaxis().SetLabelSize(0.09)
    frame.SetMinimum(0.2)
    frame.SetMaximum(1E7)
    frame.SetName("mjjFit")
    frame.GetYaxis().SetTitle("Events / 100 GeV")
    frame.SetTitle("")
    frame.Draw()

    legend = rt.TLegend(0.45097293,0.64183362,0.6681766,0.879833)
    legend2 = rt.TLegend(0.45097293,0.64183362,0.6681766,0.879833)
    legend.SetTextSize(0.046)
    legend.SetTextFont(42)
    legend.SetLineColor(0)
    legend.SetShadowColor(0)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetMargin(0.35)
    #legend2.SetTextSize(0.038)
    legend2.SetLineColor(0)
    legend2.SetShadowColor(0)
    legend2.SetLineStyle(1)
    legend2.SetLineWidth(1)
    legend2.SetFillColor(0)
    legend2.SetFillStyle(0)
    legend2.SetMargin(0.35)
    legend.AddEntry(frame.findObject("data"),"CMS data","lpe")
    legend.AddEntry(frame.findObject("sumPDF"),"%i par. background fit"%parameters[ii],"l")
    xsec= scaleToExcluded[ii]*0.01
    legend.AddEntry(frame.findObject("sig"),"%s (#sigma = %.2f pb)"%(legends[ii],xsec),"l")
    legend2.AddEntry("","","")
    legend2.AddEntry(frame.findObject("fiterr"),"","f")
    legend2.AddEntry("","","")

    legend2.Draw("same")
    legend.Draw("same")


    addInfo2 = rt.TPaveText(0.43010112,0.6166292,0.8502143,0.6023546,"NDC")
    addInfo2.SetTextFont(62)
    addInfo2.AddText(categories[ii])
    addInfo2.SetFillColor(0)
    addInfo2.SetLineColor(0)
    addInfo2.SetFillStyle(0)
    addInfo2.SetBorderSize(0)
    #addInfo.SetTextFont(42)
    addInfo2.SetTextSize(0.050)
    
    
    addInfo = rt.TPaveText(0.5010112,0.4166292,0.8502143,0.5723546,"NDC")
    addInfo.SetTextFont(42)
    #addInfo.AddText(categories[ii])
    #addInfo.SetTextFont(42)
    addInfo.AddText("|#eta| #leq 2.5, p_{T} > 200 GeV")
    addInfo.AddText("m_{jj} > 1050 GeV, |#Delta#eta_{jj}| #leq 1.3")
    addInfo.SetFillColor(0)
    addInfo.SetLineColor(0)
    addInfo.SetFillStyle(0)
    addInfo.SetBorderSize(0)
    #addInfo.SetTextFont(42)
    addInfo.SetTextSize(0.050)
    addInfo.SetTextAlign(12)
    addInfo2.Draw()
    addInfo.Draw()
    CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
    c1.Update()



    c1.cd(2)
    p11_2 = c1.GetPad(2)
    p11_2.SetPad(0.01,0.02,0.99,0.27)
    p11_2.SetBottomMargin(0.35)
    p11_2.SetRightMargin(0.05)
    p11_2.SetGridx(0)
    p11_2.SetGridy(0)
    frame3.SetMinimum(-2.9)
    frame3.SetMaximum(2.9)
    frame3.SetTitle("")
    frame3.SetXTitle("Dijet invariant mass (GeV)")
    frame3.GetXaxis().SetTitleSize(0.06)
    frame3.SetYTitle("#frac{Data-Fit}{s.d._{data}}")
    frame3.GetYaxis().SetTitleSize(0.17)
    frame3.GetYaxis().CenterTitle()
    frame3.GetYaxis().SetTitleOffset(0.30)
    frame3.GetYaxis().SetLabelSize(0.15)
    frame3.GetXaxis().SetTitleSize(0.17)
    frame3.GetXaxis().SetTitleOffset(0.91)
    frame3.GetXaxis().SetLabelSize(0.12)
    frame3.GetXaxis().SetNdivisions(906)
    frame3.GetYaxis().SetNdivisions(305)
    frame3.Draw("same")
    line = rt.TLine(minVal,0,frame3.GetXaxis().GetXmax(),0)
    line1  = rt.TLine(minVal,1,frame3.GetXaxis().GetXmax(),1)
    line2  = rt.TLine(minVal,-1,frame3.GetXaxis().GetXmax(),-1)
    line1.SetLineStyle(2)
    line1.SetLineWidth(2)
    line2.SetLineStyle(2)
    line2.SetLineWidth(2)
    line.Draw("same")
    line1.Draw("same")
    line2.Draw("same")
    c1.Update()

    print title
    canvname = "MLBkgFit_%s.pdf"%histos[ii]
    c1.SaveAs(outdir+canvname)
    c1.SaveAs(outdir+canvname.replace("pdf","C"),"C")

    time.sleep(5)

import ROOT  # ROOT binding for python.
import glob
import pandas as pd
import numpy as np
from PIL import Image
import pdf_parametrizations as pp # the pdf functions

pdf_directory_url = "/opt/qcdnum-17-01-14/output/"
imgs_url = "/home/angelica/Downloads/thesis/imgs/root/"
names = []


# PDFs
def x_uv(x):
  A, B, C, D, E, F, G = pp.A_uv, pp.B_uv, pp.C_uv , 0, pp.E_uv, pp.F_uv, pp.G_uv
  return A*x**B * (1-x)**C * (1 + D*x + E*x**2 + F*np.log(x) + G*np.log(x)**2) 
def x_dv(x):
  A, B, C, D, E, F, G = 0, pp.B_dv, pp.C_dv, 0, 0 , 0, 0
  return A*x**B * (1-x)**C * (1 + D*x + E*x**2 + F*np.log(x) + G*np.log(x)**2) 


# for quarks:
c1 = ROOT.TCanvas('c1', 'quarks PDFs', 200, 10, 700, 500)
c1.SetGrid()

# for the gluon:
#c2 = ROOT.TCanvas('c2', 'gluon PDF', 200, 10, 700, 500)
#c2.SetGrid()


# for each pdf file
for csv in glob.glob(pdf_directory_url + "*.csv"):
  dataset = pd.read_csv(csv, delimiter=" ")
  number_lines = max(dataset.index)   # number of lines of current pdf file = number of points

  # to get the q energy scale
  array = csv.split("_")
  q = float(array[2][:-4])
  names.append(int(q*100))
  
  # the pdfs
  x = np.asarray(dataset.iloc[:,0])
  pdfs = []     # uv, dv, ubar, dbar

  for i in range(1, len(dataset.columns)-1):   # from uv to dbar column
    pdfs.append(np.asarray(dataset.iloc[:,i]))

  xuv, xdv, xubar, xdbar = pdfs[0], pdfs[1], pdfs[2], pdfs[3]


  # TGraphs for quarks
  xuv_graph = ROOT.TGraph(number_lines, x, xuv)
  xdv_graph = ROOT.TGraph(number_lines, x, xdv)
  xubar_graph = ROOT.TGraph(number_lines, x, xubar)
  xdbar_graph = ROOT.TGraph(number_lines, x, xdbar)
  
  xuv_fitting = ROOT.TGraph(number_lines, x, xuv)

  # line color
  xuv_graph.SetLineColor(3)             # TAttLine Class attributes: https://root.cern.ch/doc/master/classTAttLine.html
  xdv_graph.SetLineColor(4) 
  xdbar_graph.SetLineColor(2)

  # least square fit
  xuv_fitting.LeastSquareFit(1, x_uv(x))  #6, [pp.A_uv, pp.B_uv, pp.C_uv, pp.E_uv, pp.F_uv, pp.G_uv]

  # converting from python functions to TF1 ROOT classes
  TF1_xuv = ROOT.TF1("TF1_xuv", "[0]*TMath::Power(x, [1]) * TMath::Power(1-x, [2]) * (1 + [3]*x + [4]*TMath::Power(x, 2) + [5]*TMath::Log(x) + [6]* TMath::Power(TMath::Log(x), 2) )", 0, 1)   # 0, 1: x range
  #pp.x, pp.A_uv, pp.B_uv, pp.C_uv , 0, pp.E_uv, pp.F_uv, pp.G_uv
  #TF1_xuv.SetParameter(0, *pp.x)
  TF1_xuv.SetParameter(0, pp.A_uv)
  TF1_xuv.SetParameter(1, pp.B_uv)
  TF1_xuv.SetParameter(2, pp.C_uv)
  TF1_xuv.SetParameter(3, 0)
  TF1_xuv.SetParameter(4, pp.E_uv)
  TF1_xuv.SetParameter(5, pp.F_uv)
  TF1_xuv.SetParameter(6, pp.G_uv)

  # chi square
  xuv_chisquare = xuv_graph.Chisquare(TF1_xuv)
  print("xuv_chisquare = ", xuv_chisquare)

  # Some attributes
  xuv_graph.SetTitle("Quarks PDFs at Q^{2} = " + str(q) + " GeV^{2}")
  xuv_graph.GetXaxis().SetTitle("x")
  xuv_graph.GetYaxis().SetTitle("x quarks")
  xuv_graph.GetYaxis().SetRangeUser(-0.3,0.8)

  # Draw these graphs with their current attributes
  xuv_graph.Draw("ACP")      # in parenthesis are the options (see: https://root.cern.ch/doc/master/classTGraphPainter.html)
  xdv_graph.Draw("pl same")
  xubar_graph.Draw("pl same")
  xdbar_graph.Draw("pl same")
  xuv_fitting.Draw("pl same")

  # legend class
  legend = ROOT.TLegend(0.88, 0.7, 0.7, 0.88)    # x_derecha, y_abajo, x_izquierda, y_arriba --> como plano cartesiano
  #legend.SetHeader("The Legend Title","C")
  legend.AddEntry(xuv_graph,"xu_{v}")
  legend.AddEntry(xdv_graph,"xd_{v}")
  legend.AddEntry(xubar_graph,"x#bar{u}")
  legend.AddEntry(xdbar_graph,"x#bar{d}")
  legend.Draw()

  # updating the canvas
  c1.Update()
  c1.SaveAs(imgs_url + str(int(q*100)) + ".png")

  # for the gluon:


# Creates the gifs with the output imgs
names.sort()

# Create the frames
frames = []
imgs = [imgs_url + str(x) + ".png" for x in names]
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save(imgs_url+'pdfs_evolution_gif.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=100, loop=0)
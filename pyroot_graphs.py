import ROOT  # ROOT binding for python.
import glob
import pandas as pd
import numpy as np
from PIL import Image

pdf_directory_url = "/opt/qcdnum-17-01-14/output/"
imgs_url = "/home/angelica/Downloads/thesis/imgs/root/"
names = []

c1 = ROOT.TCanvas('c1', 'quarks PDFs', 200, 10, 700, 500)
c1.cd()
c1.SetGrid()

# for each pdf file
for csv in glob.glob(pdf_directory_url + "*.csv"):
  dataset = pd.read_csv(csv, delimiter=" ")
  number_lines = max(dataset.index)   # number of lines of current pdf file = number of points

  # to get the q energy scale
  array = csv.split("_")
  q = float(array[2][:-4])
  names.append(int(q*10))
  
  # the pdfs
  x = np.asarray(dataset.iloc[:,0])
  pdfs = []     # uv, dv, ubar, dbar

  for i in range(1, len(dataset.columns)-1):   # from uv to dbar column
    pdfs.append(np.asarray(dataset.iloc[:,i]))

  xuv, xdv, xubar, xdbar = pdfs[0], pdfs[1], pdfs[2], pdfs[3]

  # Graphs
  xuv_graph = ROOT.TGraph(number_lines, x, xuv)
  xuv_graph.SetLineColor(3)             # TAttLine Class attributes: https://root.cern.ch/doc/master/classTAttLine.html
  xuv_graph.SetTitle(" ")
  xuv_graph.GetXaxis().SetTitle("x")
  xuv_graph.GetYaxis().SetTitle(r"xq")
  xuv_graph.GetYaxis().SetRangeUser(-0.3,0.8)
  #xuv_graph.GetXaxis().SetRangeUser(0,1)

  xdv_graph = ROOT.TGraph(number_lines, x, xdv)
  xdv_graph.SetLineColor(4) 
  xubar_graph = ROOT.TGraph(number_lines, x, xubar)
  xubar_graph.SetLineColor(5) 
  xdbar_graph = ROOT.TGraph(number_lines, x, xdbar)
  xdbar_graph.SetLineColor(2)

  # Draw this graph with its current attributes
  xuv_graph.Draw("ACP")   # in parenthesis are the options (see: https://root.cern.ch/doc/master/classTGraphPainter.html)
  xdv_graph.Draw("pl same")
  xubar_graph.Draw("pl same")
  xdbar_graph.Draw("pl same")

  # updating the canvas
  c1.Update()
  c1.SaveAs(imgs_url + str(int(q*10)) + ".png")


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
"""
Script for the evolution gif of the pdfs obtained with qcdnum.

The pdfs obtained by the DGLAP evolution equations, using qcdnum, are stored in files, containing each one a fixed q energy scale.
The output files with the pdfs and x values are stored in the directory named output (that I have created), inside qcdnum.
Those output files follows the following convention: nameCxxFile_q_energyscale.csv
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import glob
from PIL import Image
import os

from sympy import DiagMatrix

# to delete the old images
os.system("rm imgs/python/*.png imgs/python/*.gif")

output_directory_url = "/opt/qcdnum-17-01-14/output/"   # url of the directory where the output files of qcdnum script are stored.
save_imgs_url = "/home/angelica/Documents/thesis/imgs/python/"

names = []

plt.rcParams.update({"font.size":13})
sns.set_style("darkgrid")

# for each .csv output file cotained in output_directory_url.
for csv in glob.glob(output_directory_url + "*.csv"):
  print(csv)
  array = csv.split("_")
  q = float(array[2][:-4])

  dataset = pd.read_csv(csv, delimiter=" ")
  dataset = dataset.set_index("x")

  names.append(int(q*100))

  plt.figure()
  lp = sns.scatterplot(data=dataset.iloc[:,:])   #, palette=['orange']
  lp.set(xscale="log")
  #lp.text(10, 10, "I am Adding Text To The Plot", fontdict=dict(color='black', fontsize=10))
  plt.ylabel("$x$pdf")
  plt.xlabel("$x$")
  plt.title(f"$Q^2$ = {q:.2e} $GeV^2$")
  plt.ylim((0.0, 1.0))
  plt.xlim((10e-3, 1))
  plt.savefig(save_imgs_url + str(int(q*100)) + ".png", dpi=300)

names.sort()

# Create the frames
frames = []
imgs = [save_imgs_url + str(x) + ".png" for x in names]
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save(save_imgs_url+'pdfs_evolution_gif.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=100, loop=0)
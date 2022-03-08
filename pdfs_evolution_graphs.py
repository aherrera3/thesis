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

sns.set_style("darkgrid")

output_directory_url = "/opt/qcdnum-17-01-14/output/"   # url of the directory where the output files of qcdnum script are stored.
save_imgs_url = "/home/angelica/Documents/thesis/imgs/python/"

names = []

# for each .csv output file cotained in output_directory_url.
for csv in glob.glob(output_directory_url + "*.csv"):
  print(csv)
  array = csv.split("_")
  q = float(array[2][:-4])

  dataset = pd.read_csv(csv, delimiter=" ")
  dataset = dataset.set_index("x")

  names.append(int(q*10))

  plt.figure()
  sns.lineplot(data=dataset.iloc[:,:])   # without gluons graph
  plt.ylim((-0.4, 1))
  plt.savefig(save_imgs_url + str(int(q*10)) + ".png")

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
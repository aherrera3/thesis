"""
Script for the calculation of A_uv, A_dv & A_g, and the python graph for the xPDFs.
The PDF parametrizations are stored as variables (x_uv, x_g, ...).

Parametrizations taken from: Bonvini, M., & Giuli, F. (2019). A new simple PDF parametrization: improved description
																										 of the HERA data. The European Physical Journal Plus, 134(10), 531.
"""

#import sympy 			# for the harmonic numbers
import math 			# for the gamma function
import scipy.special as ss
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# constants
f_s = 0.4       		   
gamma_s = f_s/(1-f_s)

# fitted parameters of the paper (NNLO + NLLx Hell 3.0)
B_uv, C_uv, E_uv, F_uv, G_uv = 0.76, 4.6, 2.6, 0.35, 0.049
B_g, C_g, F_g, G_g = -0.52, 4.5, 0.217, 0.0112
B_dv, C_dv = 0.99, 4.7
A_dbar, B_dbar, C_dbar, D_dbar, F_dbar = 0.14, -0.33, 24, 38, 0.071 
A_ubar, B_ubar, C_ubar, D_ubar, F_ubar = A_dbar, B_dbar, 11, 18, F_dbar

"""
#  NNLO global minimun parameters
B_uv, C_uv, E_uv, F_uv, G_uv = 0.83, 4.6, 1.9, 0.37, 0.058
B_g, C_g, F_g, G_g = -0.55, 4.5, 0.230, 0.0131
B_dv, C_dv = 0.98, 4.7
A_dbar, B_dbar, C_dbar, D_dbar, F_dbar = 0.13, -0.34, 24, 40, 0.072 
A_ubar, B_ubar, C_ubar, D_ubar, F_ubar = A_dbar, B_dbar, 11, 20, F_dbar
"""


# integral equivalents
# for uv and dv
def I1 (B_i, C_i):
	return math.gamma(B_i) * math.gamma(C_i+1) / math.gamma(B_i+C_i+1)

def I2 (B_i, C_i):
	return I1 (B_i+2, C_i)

def I3 (B_i, C_i):
	return I1 (B_i, C_i) * (ss.polygamma(0, B_i) - ss.polygamma(0, B_i+C_i+1))

def I4 (B_i, C_i):
	return I1 (B_i, C_i) * ( (ss.polygamma(0, B_i) - ss.polygamma(0, B_i+C_i+1))**2 + (ss.polygamma(1, B_i) - ss.polygamma(1, B_i+C_i+1)) )

# for gluon:
def I1_i (B_i, C_i):
	return I1(B_i+1, C_i)

def I2_i (B_i, C_i):  
	return I3 (B_i+1, C_i)     #(sympy.harmonic(B_i)-sympy.harmonic(B_i+C_i+1)) , domde ss.polygamma(0, B_i+1) = sympy.harmonic(B_i) cuando B_i > 0.
														# Había un problema cuando B_i <0 (entonces wolfram esta mal?), por ende decido cambiar a polygamma function.
def I3_i (B_i, C_i):
	return I4(B_i+1, C_i)

def I4_i (B_i, C_i):
	return I2 (B_i, C_i)

def I5_i (B_i, C_i):
	return I1(B_i+3, C_i)


# A_uv calculation
A_uv = 2 / (I1 (B_uv, C_uv) + E_uv*I2 (B_uv, C_uv) + F_uv*I3 (B_uv, C_uv) + G_uv*I4 (B_uv, C_uv))
print("A_uv: ", A_uv)


# A_dv calculation
A_dv = 1 / (I1(B_dv, C_dv))
print("A_dv: ", A_dv)


# Ag calculation
I1_uv, I1_dv, I1_g, I1_ubar, I1_dbar  =  I1_i (B_uv, C_uv), I1_i (B_dv, C_dv), I1_i (B_g, C_g), I1_i (B_ubar, C_ubar), I1_i (B_dbar, C_dbar)
I2_uv, I2_ubar, I2_dbar, I2_g = I2_i (B_uv, C_uv), I2_i (B_ubar, C_ubar), I2_i (B_dbar, C_dbar), I2_i (B_g, C_g)
I3_uv, I3_g = I3_i (B_uv, C_uv), I3_i (B_g, C_g)
I4_ubar, I4_dbar = I4_i (B_ubar, C_ubar), I4_i (B_dbar, C_dbar)
I5_uv = I5_i (B_uv, C_uv)

A_g = (1 - (A_uv*(I1_uv + E_uv*I5_uv + F_uv*I2_uv + G_uv*I3_uv) + A_dv*I1_dv + 2*A_ubar*(I1_ubar + D_ubar*I4_ubar + F_ubar*I2_ubar)
				 + 2*(1+gamma_s)*A_dbar*(I1_dbar + D_dbar*I4_dbar + F_dbar*I2_dbar)) ) / (I1_g + F_g*I2_g + G_g*I3_g)
print("A_g: ", A_g)



# ------------------------------------------------------------------------------------------------------------------------------    
# -----------------------------------------------xPDFS GRAPHS-------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------   
x = np.linspace(5.2427e-4, 1, 1000)

# Parton Distribution Functions (PDFs)
def x_pdf(x, A, B, C , D, E, F, G):
	return A*x**B * (1-x)**C * (1 + D*x + E*x**2 + F*np.log(x) + G*np.log(x)**2) 

x_g = x_pdf(x, A_g, B_g, C_g , 0, 0, F_g, G_g)
x_uv, x_dv = x_pdf(x, A_uv, B_uv, C_uv , 0, E_uv, F_uv, G_uv), x_pdf(x, A_dv, B_dv, C_dv , 0, 0, 0, 0)
x_ubar, x_dbar = x_pdf(x, A_ubar, B_ubar, C_ubar , D_ubar, 0, F_ubar, 0), x_pdf(x, A_dbar, B_dbar, C_dbar , D_dbar, 0, F_dbar, 0)
x_qv = x_uv + x_dv   		# pdf for the sum of valence quarks pdfs
x_qs = x_ubar + x_dbar  # pdf for the sum of sea quarks pdfs
x_Sigma = x_uv + x_dv + 2*x_ubar + 2*(1+gamma_s)*x_dbar   

"""
with open("data.txt", "w") as f:
	f.write("x uv dv \n")
	for i in range(10):
		line = str(x[i]) + " " + str(x_uv[i]) + " " + str(x_dv[i]) +"\n"
		f.write(line)
"""

# converting to pd.DataFrames for graph in seaborn. And for convert easily into .csv
x_q = pd.DataFrame({'x$u_{v}$': x_uv, 'x$d_{v}$': x_dv, 'x$\\bar{u}$': x_ubar, 'x$\\bar{d}$': x_dbar}, index=x)
x_qv = pd.DataFrame({'x$q_{v}$': x_qv, 'x$q_{s}$': x_qs}, index=x)
x_g = pd.DataFrame({'xg': x_g}, index=x)
x_Sigma =  pd.DataFrame({'x$\\Sigma$': x_Sigma}, index=x)    # sum of all quark momentums
#print(x_q)

# Graphics
sns.set_style("darkgrid")

fig, axes = plt.subplots(2, 2, figsize=(30,15))
#fig.suptitle('PDF')
q_graph = sns.lineplot(ax=axes[0,0], data=x_q)
qv_graph = sns.lineplot(ax=axes[0,1], data=x_qv)
sigma_graph = sns.lineplot(ax=axes[1,0], data=x_Sigma)
g_graph = sns.lineplot(ax=axes[1,1], data=x_g)
q_graph.set(xlabel = 'x', title='Quarks xPDFs')
qv_graph.set(xlabel = 'x', title='Valence and Sea Quarks xPDFs')
sigma_graph.set(xlabel = 'x', title='Sum of Quarks xPDFs')
g_graph.set(xlabel = 'x', title='Gluon xPDFs')
#q_graph.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ["$5.24^{-4}$", "$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$"])
#qv_graph.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ["$5.24^{-4}$", "$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$"])
#sigma_graph.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ["$5.24^{-4}$", "$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$"])
#g_graph.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1], ["$5.24^{-4}$", "$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$"])
#plt.show()
plt.savefig("imgs/python/xpdfs_q0.png")

# Plotting speed and attenuation against initial saturation for transverse case
from config import epsilon
from dispersion_relation import transverse_disp
from sympy.solvers import solveset
from sympy import re, im, Symbol
import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)

# Number of data points
N = 150

# Choose non-wetting material
# 0 - Air
# 1 - Oil
# 2 - Gas
material_mode = 2

S0 = np.linspace(epsilon, 1-epsilon, N)
w_array = [10, 100, 500, 1000, 5000]
w_label = [str(i) for i in w_array]
k = Symbol('k')

for i in range(len(w_array)):
    w = w_array[i]
    print('Progress: ' + str(int(100*(i+1)/5)) + '%')
    disp_rel = transverse_disp(S0, w, material_mode)
    k_array = [list(solveset(i,k))[0] for i in disp_rel]
    speed_array = [w/abs(re(e)) for e in k_array]
    attenuation_array = [abs(im(e)) for e in k_array]

    plt.figure(1)
    plt.plot(S0,speed_array,'-',label=w_label[i])

    plt.figure(2)
    plt.semilogy(S0,attenuation_array,'-',label=w_label[i])

plt.figure(1)
plt.legend()
plt.xlabel(r'initial saturation $S_0$')
plt.ylabel(r'velocity / $ms^{-1}$')
plt.savefig('../plots/speed_sat_s.eps')
plt.clf()

plt.figure(2)
plt.legend()
plt.xlabel(r'initial saturation $S_0$')
plt.ylabel(r'attenuation / $m^{-1}$')
plt.savefig('../plots/attenuation_sat_s.eps')
plt.clf()
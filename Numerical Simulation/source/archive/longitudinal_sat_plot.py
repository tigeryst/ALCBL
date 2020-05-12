# Plotting speed and attenuation against initial saturation for longitudinal case
from config import epsilon
from dispersion_relation import longitudinal_disp
from sympy import nroots
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

S0 = np.linspace(epsilon, 0.9, N)
w_array = [10, 100, 500, 1000, 5000]
w_label = [str(i) for i in w_array]
k = Symbol('k')

for i in range(len(w_array)):
    w = w_array[i]
    print('Progress: ' + str(int(100*(i+1)/5)) + '%')
    disp_rel = longitudinal_disp(S0, w, material_mode)
    k_array = [list(nroots(d, maxsteps = 100))[0:3] for d in disp_rel]
    for j in range(3):
        speed_array = [w/abs(re(e[j])) for e in k_array]
        attenuation_array = [abs(im(e[j])) for e in k_array]

        plt.figure(j)
        if j == 2:
            plt.plot(S0,speed_array,label=w_label[i])
        else:
            plt.semilogy(S0,speed_array,label=w_label[i])

        plt.figure(j+3)
        plt.semilogy(S0,attenuation_array,label=w_label[i])

for j in range(3):
    plt.figure(j)
    plt.legend()
    plt.xlabel(r'initial saturation $S_0$')
    plt.ylabel(r'velocity / $ms^{-1}$')
    plt.savefig('../plots/speed_sat_p' + str(3-j) + '.eps')
    plt.clf()

    plt.figure(j+3)
    plt.legend()
    plt.xlabel(r'initial saturation $S_0$')
    plt.ylabel(r'attenuation / $m^{-1}$')
    plt.savefig('../plots/attenuation_sat_p' + str(3-j) + '.eps')
    plt.clf()
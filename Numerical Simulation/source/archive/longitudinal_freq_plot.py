# Plot speed and attenuation against frequency for longitudinal case
from config import epsilon
from plot_config import *
from dispersion_relation import longitudinal_disp
from sympy import nroots
from sympy.solvers import solveset
from sympy import re, im, Symbol
import numpy as np
from math import pi

# Number of data points
N = 150

# Choose non-wetting material
# 0 - Air
# 1 - Oil
# 2 - Gas
material_mode = 2

# w_lin = np.linspace(1, 1E7, N)
# w_log = np.logspace(0, 7, N)
w_lin = np.linspace(20, 20E3*6, N)
w_log = np.logspace(0, 5, N)
w = np.concatenate((w_lin, w_log), axis=0)
f = w/(2*pi)
S0_array = [0.2, 0.4, 0.6, 0.8, 1-epsilon]
S0_label = [str(i) for i in S0_array]
k = Symbol('k')

for i in range(len(S0_array)):
    S0 = S0_array[i]
    print('Progress: ' + str(int(100*(i+1)/5)) + '%')
    disp_rel = longitudinal_disp(S0, w, material_mode)
    k_array = [list(nroots(d, maxsteps = 100))[0:3] for d in disp_rel]
    for j in range(3):
        speed_array = w[N:]/[abs(re(e[j])) for e in k_array][N:]
        attenuation_array = [abs(im(e[j])) for e in k_array][:N]

        plt.figure(j)
        plt.semilogx(f[N:], speed_array, label=S0_label[i])

        plt.figure(j+3)
        if j == 2:
            plt.plot(f[:N], attenuation_array, label=S0_label[i])
        else:
            plt.semilogy(f[:N], attenuation_array, label=S0_label[i])


for j in range(3):
    plt.figure(j)
    plt.legend()
    plt.xlabel('frequency / Hz')
    plt.ylabel(r'velocity / $ms^{-1}$')
    plt.savefig('../plots/speed_freq_p' + str(3-j) + '.eps')
    plt.clf()

    plt.figure(j+3)
    plt.legend()
    plt.xlabel('frequency / Hz')
    plt.ylabel(r'attenuation / $m^{-1}$')
    plt.savefig('../plots/attenuation_freq_p' + str(3-j) + '.eps')
    plt.clf()
# Plot speed and attenuation against frequency for transverse case
from config import epsilon
from dispersion_relation import transverse_disp
from sympy.solvers import solveset
from sympy import re, im, Symbol
import numpy as np
import matplotlib.pyplot as plt
from math import pi

plt.rc('text', usetex=True)

# Number of data points
N = 150

# Choose non-wetting material
# 0 - Air
# 1 - Oil
# 2 - Gas
material_mode = 2

w_lin = np.linspace(1E-2, 1E7, N)
w_log = np.logspace(-2, 7, N)
w = np.concatenate((w_lin, w_log), axis=0)
f = w/(2*pi)
S0_array = [0.2, 0.4, 0.6, 0.8, 1-epsilon]
S0_label = [str(i) for i in S0_array]
k = Symbol('k')

for i in range(len(S0_array)):
    S0 = S0_array[i]
    print('Progress: ' + str(int(100*(i+1)/5)) + '%')
    disp_rel = transverse_disp(S0, w, material_mode)
    k_array = [list(solveset(i,k))[0] for i in disp_rel]
    speed_array = w[N:]/[abs(re(e)) for e in k_array][N:]
    attenuation_array = [abs(im(e)) for e in k_array][:N]

    plt.figure(1)
    plt.semilogx(f[N:],speed_array, label=S0_label[i])

    plt.figure(2)
    plt.plot(f[:N],attenuation_array, label=S0_label[i])

plt.figure(1)
plt.legend()
plt.xlabel('frequency / Hz')
plt.ylabel(r'velocity / $ms^{-1}$')
plt.savefig('../plots/speed_freq_s.eps')
plt.clf()

plt.figure(2)
plt.legend()
plt.xlabel('frequency / Hz')
plt.ylabel(r'attenuation / $m^{-1}$')
plt.savefig('../plots/attenuation_freq_s.eps')
plt.clf()
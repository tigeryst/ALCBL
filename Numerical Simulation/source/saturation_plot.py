# Plot speed and attenuation against saturation
from config import epsilon, print_progress
from plot_config import *
from dispersion_relation import transverse_disp, longitudinal_disp
from sympy.solvers import solveset
from sympy import nroots
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

f = np.array([20, 100, 1000, 5000, 20000])
w_array = 2*pi*f
S0 = np.linspace(epsilon, 1-epsilon, N)
k = Symbol('k')

# Progress bar setup
total = len(w_array)*11
counter = 0

# Set axes
fig1, axs1 = plt.subplots(2, 1, figsize=(3.17, 6.44))
fig2, axs2 = plt.subplots(3, 2, figsize=(6.86, 9.68))

for ax in axs1:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(r'initial saturation $S_0$')
    ax.set_xlim(0, 1)
axs1[0].set_ylabel(r'phase speed $(ms^{-1})$')
axs1[1].set_ylabel(r'attenuation $(m^{-1})$')

for ax in axs2[:,0]:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(r'initial saturation $S_0$')
    ax.set_ylabel(r'phase speed $(ms^{-1})$')
    ax.set_xlim(0, 1)
for ax in axs2[:,1]:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(r'initial saturation $S_0$')
    ax.set_ylabel(r'attenuation $(m^{-1})$')
    ax.set_xlim(0, 1)

for i in range(len(w_array)):
    counter += 1
    print_progress(counter, total)
    w = w_array[i]
    # Transverse case
    disp_rel = transverse_disp(S0, w, material_mode)
    ks_array = [[list(solveset(d, k))[0]] for d in disp_rel]
    counter += 1
    print_progress(counter, total)
    # Longitudinal case
    disp_rel = longitudinal_disp(S0, w, material_mode)
    kp_array = [list(nroots(d, maxsteps = 100))[0:3] for d in disp_rel]
    counter += 1
    print_progress(counter, total)
    # Join arrays
    ks_array = np.array(ks_array)
    kp_array = np.array(kp_array)
    k_array = np.concatenate((ks_array, kp_array), axis = 1)

    for j in range(4):
        # Calculate speed and attenuation
        speed_array = w/[abs(re(e[j])) for e in k_array]
        attenuation_array = [abs(im(e[j])) for e in k_array]
        counter += 1
        print_progress(counter, total)
        # Plot in separate axes
        if j == 0:
            # The S wave case
            speedax = axs1[0]
            attenax = axs1[1]
        else:
            # Note the inversion of indices
            # The solution gave order P3, P2, P1 so must be reversed
            speedax = axs2[3-j,0]
            attenax = axs2[3-j,1]
        # if j == 1:
        #     # P3 wave should be plotted with semilog y since large difference
        #     speedax.plot(S0, speed_array, label=str(S0))
        #     attenax.semilogy(S0, attenuation_array, label=str(S0))
        # else:
        speedax.plot(S0, speed_array, label=str(f[i]))
        attenax.semilogy(S0, attenuation_array, label=str(f[i]))


        counter += 1
        print_progress(counter, total)

# Final plot limit tweaks
for ax in axs2[1:3,0]:
    ax.set_ylim(bottom = 0)

axs2[2,1].set_ylim(top = 1E10)

# Add legend
for ax in axs1:
    ax.legend(loc='lower left', bbox_to_anchor= (-0.1, 1.01), ncol=3,
            borderaxespad=0, frameon=False)
for ax in axs2:
    ax[0].legend(loc='lower left', bbox_to_anchor= (-0.1, 1.01), ncol=3,
            borderaxespad=0, frameon=False)
    ax[1].legend(loc='lower left', bbox_to_anchor= (-0.1, 1.01), ncol=3,
            borderaxespad=0, frameon=False)

fig1.tight_layout(pad=0.3, w_pad=0.7, h_pad=0.7)
fig2.tight_layout(pad=0.3, w_pad=0.7, h_pad=0.7)

fig1.savefig('../plots/saturation_s.eps', bbox_inches = 'tight')
fig2.savefig('../plots/saturation_p.eps', bbox_inches = 'tight')
plt.clf()
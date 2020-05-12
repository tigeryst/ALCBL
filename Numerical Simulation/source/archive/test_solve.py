# import numpy as np
# from sympy import Symbol, Poly, simplify, re, im
# from dispersion_relation import longitudinal_disp, transverse_disp

# # Number of data points
# # N = 10

# k = Symbol('k')
# S0 = Symbol('S0')
# w = Symbol('w')

# S0 = 0.4
# w_array = np.linspace(100,1E7,5)

# for w in w_array:
#     disp_rel = Poly(simplify(longitudinal_disp(S0,w,1)),k)
#     print('w = ' + str(w))
#     coeffs = disp_rel.all_coeffs()
#     j = complex(0,1)
#     real = np.array([float(re(c)) for c in coeffs])
#     imag = np.array([float(im(c)) for c in coeffs])
#     co = real + imag*j
#     print(co)
#     roots = np.roots(co)
#     print(roots)
#     print(np.poly(roots))


# Plotting speed and attenuation against initial saturation for longitudinal case
from config import epsilon
from dispersion_relation import longitudinal_disp
from sympy import nroots
from sympy import re, im, Symbol, simplify, Poly
import numpy as np
import matplotlib.pyplot as plt
from math import pi

plt.rc('text', usetex=True)

# Number of data points
N = 50

# Choose non-wetting material
# 0 - Air
# 1 - Oil
# 2 - Gas
material_mode = 2

w_lin = np.linspace(1, 1E7, N)
w_log = np.logspace(0, 7, N)
w = np.concatenate((w_lin, w_log), axis=0)
f = w/(2*pi)
S0_array = [0.2, 0.4, 0.6, 0.8, 1-epsilon]
S0_label = [str(i) for i in S0_array]
k = Symbol('k')

j = complex(0,1)

for i in range(len(S0_array)):
    S0 = S0_array[i]
    print('Progress: ' + str(int(100*(i+1)/5)) + '%')
    disp_rel = longitudinal_disp(S0, w, material_mode)
    disp_rel = [Poly(simplify(d), k) for d in disp_rel]
    coeff = [d.all_coeffs() for d in disp_rel]
    root_array = np.array([])
    for c in coeff:
        real = np.array([float(re(a)) for a in c])
        imag = np.array([float(im(a)) for a in c])
        co = real + imag*j
        roots = np.roots(co)
        roots = roots[::2]
        root_array = np.append(root_array, roots)
    print('real')
    reals = np.abs(np.real(root_array))
    print(reals)
    print('imag')
    imags = np.abs(np.imag(root_array))
    print(imags)

    for l in range(3):
        # speed_array = w[100:200]/[abs(re(k_array[i][j])) for i in range(len(k_array)) if i > N-1]
        # attenuation_array = [abs(im(k_array[i][j])) for i in range(len(k_array)) if i < N]
        print(l)
        print('real_short')
        realx = reals[l::3]
        print(realx)
        print('imag_short')
        imagx = imags[l::3]
        print(imagx)
        speed_array = w[N:]/realx[N:]
        attenuation_array = imagx[:N]

        plt.figure(l)
        plt.semilogx(f[N:], speed_array, label=S0_label[i])

        plt.figure(l+3)
        if l == 2:
            plt.plot(f[:N], attenuation_array, label=S0_label[i])
        else:
            plt.semilogy(f[:N], attenuation_array, label=S0_label[i])


for j in range(3):
    plt.figure(j)
    plt.legend()
    plt.xlabel('frequency / Hz')
    plt.ylabel(r'velocity / $ms^{-1}$')
    plt.title('P' + str(3-j) + '-wave Velocity Against Frequency')
    plt.savefig('../plots/speed_freq_p' + str(3-j) + '.eps')
    plt.clf()

    plt.figure(j+3)
    plt.legend()
    plt.xlabel('frequency / Hz')
    plt.ylabel(r'attenuation / $m^{-1}$')
    plt.title('P' + str(3-j) + '-wave Attenuation Against Frequency')
    plt.savefig('../plots/attenuation_freq_p' + str(3-j) + '.eps')
    plt.clf()
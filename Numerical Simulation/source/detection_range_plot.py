from contour_atten import *
from plot_config import *
from math import pi
import numpy as np

# Transverse case
rangemesh = np.load("rangemesh_s.npy")
rangemesh = np.log10(np.float64(rangemesh))
# Contour plot
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
cp = ax.contourf(SS, ww/(2*pi), rangemesh, levels=np.arange(-2,8))

# Show colourbar
cbar = fig.colorbar(cp)
cbar.ax.set_ylabel(r'$\textrm{log\,}$(range/$\textrm{m}$)')

# Set axes
#ax.set_xlim((40, 120))
ax.set_xlabel(r'initial saturation $S_0$')
ax.set_ylabel(r'frequency $(\textrm{Hz})$')

# Save contour plot of libration amplitude on phase space
fig.savefig('../plots/detect_range_s.eps', bbox_inches = 'tight')
plt.clf()

# Longitudinal case
rangemesh = np.load("rangemesh_p1.npy")
rangemesh = np.log10(np.float64(rangemesh))
# Contour plot
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
cp = ax.contourf(SS, ww/(2*pi), rangemesh, levels=np.arange(-2,8))

# Show colourbar
cbar = fig.colorbar(cp)
cbar.ax.set_ylabel(r'$\textrm{log\,}$(range/$\textrm{m}$)')

# Set axes
#ax.set_xlim((40, 120))
ax.set_xlabel(r'initial saturation $S_0$')
ax.set_ylabel(r'frequency $(\textrm{Hz})$')

# Save contour plot of libration amplitude on phase space
fig.savefig('../plots/detect_range_p1.eps', bbox_inches = 'tight')
plt.clf()
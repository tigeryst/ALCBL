# Plot the capillary pressure curves for the two models
from config import epsilon
from plot_config import *
from soil_acoustic import capillary
import numpy as np

# Set plot resolution
N = 150

S0 = np.linspace(epsilon, 1-epsilon, N)
p_vG = capillary(S0, 0)[0]
p_santos = capillary(S0, 1)[0]

# van Genuchten capillary pressure
# Set axes
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel('capillary pressure (Pa)')
ax.set_ylabel(r'initial saturation $S_0$')
ax.set_xlim(1E3, 1E9)
ax.set_ylim(0, 1)

# Plot and save
ax.semilogx(p_vG, S0)
fig.tight_layout(pad=0.3)
fig.savefig('../plots/capillary_vG.eps', bbox_inches = 'tight')
plt.clf()

# Santos capillary pressure
# Set axes
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel('capillary pressure (Pa)')
ax.set_ylabel(r'initial saturation $S_0$')
ax.set_xlim(0, 1200)
ax.set_ylim(0, 1)

# Plot and save
ax.plot(-p_santos, S0)
fig.tight_layout(pad=0.3)
fig.savefig('../plots/capillary_santos.eps', bbox_inches = 'tight')
plt.clf()
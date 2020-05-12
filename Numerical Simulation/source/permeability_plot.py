# Plot relative permeability parameters depending on saturation
from config import epsilon
from plot_config import *
from soil_acoustic import permeability
import numpy as np

S0 = np.linspace(epsilon, 1-epsilon, 100)

kf, kg = permeability(S0)

fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.plot(S0, kg, label= 'kg')
ax.plot(S0, kf, label = 'kf')

plt.legend()
ax.set_xlabel(r'initial saturation $S_0$')
ax.set_ylabel('relative permeabilities')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

fig.tight_layout(pad=0.3)
fig.savefig('../plots/permeability.eps', bbox_inches = 'tight')
plt.clf()
# Plot Albers parameters for water-air, water-oil and water-gas case
from config import epsilon
from plot_config import *
from soil_acoustic import capillary, albers_param, material_param
import numpy as np

# Set plot resolution
N = 150

S0 = np.linspace(epsilon, 1-epsilon, N)

materials = ['air', 'oil', 'gas']

# Select capillary relation
pc, dpcdS = capillary(S0, 1)

# Plot labels
labels = [r'$\lambda^S$', r'$\rho^F_0\kappa^F$', \
            r'$\rho^G_0\kappa^G$', r'$Q^F$', r'$Q^G$', r'$Q^FG$']

for i in range(len(materials)):
    # Evaluate Albers' parameters for each material
    params = albers_param(S0, pc, dpcdS, i)

    # Set axes
    fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlabel(r'initial saturation $S_0$')
    ax.set_ylabel('parameter values (Pa)')
    ax.set_xlim(0, 1)
    ax.set_ylim(1E2, 1E10)

    for j in range(len(params)):
        # Plot parameters
        ax.semilogy(S0, params[j], label=labels[j])

    ax.legend(loc='lower left', bbox_to_anchor= (0.2, 0.05), ncol=2,
            borderaxespad=0, frameon=True)
    fig.tight_layout(pad=0.3)

    fig.savefig('../plots/detmann_param_' + materials[i] + '.eps', bbox_inches = 'tight')
    plt.clf()
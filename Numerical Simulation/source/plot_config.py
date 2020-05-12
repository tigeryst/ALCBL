from matplotlib import pyplot as plt
from cycler import cycler
default_cycler = (cycler(color=['k', 'b', 'm', 'c', 'r', 'g']) +
                  cycler(linestyle=['-', '--', (0, (7, 1)), (0, (5, 1, 1, 1)), (0, (5, 1, 1, 1, 1, 1)), (0, (5, 1, 1, 1, 1, 1, 1, 1))]))

plt.rc('lines', linewidth=1.5)
plt.rc('axes', prop_cycle=default_cycler)
plt.rc('text', usetex=True)

def set_size(width, fraction=1):
    """ Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float
            Document textwidth or columnwidth in pts
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (fig_width_in, fig_width_in*0.8)

    return fig_dim
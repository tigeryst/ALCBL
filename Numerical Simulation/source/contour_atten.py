from dispersion_relation import transverse_disp, longitudinal_disp
from dispersion_relation import atten_coeff, detect_range
from config import epsilon
import numpy as np
from math import pi
from multiprocessing import Pool  # multiprocessing module improves performance

N = 50

S0 = np.linspace(epsilon, 1-epsilon, N)
f = np.linspace(20, 20000, N)
w = 2*pi*f

# Define source power and noise power
# Data taken from experiment (Fourier spectrum)
psource = 7.28720
pnoise = 0.00097

# Generate an N by N grid defining points on S0-w space
SS, ww = np.meshgrid(S0, w)

# If the module is run as a standalone program, perform parallel calculation
if __name__ == "__main__":

    # Define function to scan through phase space and calculate wander
    def range_trans_mesh(ww):
        alpha = [atten_coeff(transverse_disp(S[0], ww[0], 2), 0) for S in SS.T]
        return [detect_range(a, psource, pnoise) for a in alpha]

    def range_long_mesh(ww):
        alpha = [atten_coeff(longitudinal_disp(S[0], ww[0], 2), 1) for S in SS.T]
        return [detect_range(a, psource, pnoise) for a in alpha]

    # Use Pool to bypass the Global Interpreter Lock and utilise all 4 cores
    pool = Pool(4) # 4 cores on processor
    rangemesh = pool.map(range_trans_mesh, ww)
    # Save the result in a file that can be retrieved later for plotting
    np.save("rangemesh_s.npy",rangemesh)

    rangemesh = pool.map(range_long_mesh, ww)
    np.save("rangemesh_p1.npy",rangemesh)
# Configuration file for adjusting constants depending on soil and fluid types

# === Define material parameters experimentally/empirically obtained ===
# True compressibility moduli (microscopic)
Ks = 48E9   # solid - sandstone
Kf = 2.25E9 # fluid - water

# True (microscopic) densities
rhoSR0 = 2650      # sandstone
rhoFR0 = 1000      # water

# Shear modulus (second lame constant) for sandstone
muS = 1641041323

# Viscosity dependent parameters
piF = 1E7       # water

# g parameter for empirical expression of drained compressibility modulus Kd
g = 50

# === Define initial conditions ===
# Initial pressure corresponding to microscopic relative volume changes
pSR0 = 0    # solid
pFR0 = 0    # gas

# Initial porosity
# Defined as ratio of volume of void to bulk volume
n0 = 0.25   # depends on compaction of soil

# Small value close to zero
epsilon = 1E-5

# Print iterations progress
def print_progress (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
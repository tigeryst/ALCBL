import csv
from plot_config import *
import numpy as np
from math import pi
from basic_units import radians
from matplotlib.ticker import AutoMinorLocator

plt.rc('text', usetex=True)

w = 1515

with open('../data/vel-on-axis.csv') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    distance = []
    distance_err = []
    phase = []
    phase_err = []
    for row in read_csv:
        dist = row[0]
        disterr = row[1]
        pha = row[2]
        phaerr = row[3]

        distance.append(float(dist))
        distance_err.append(float(disterr))
        phase.append(float(pha))
        phase_err.append(float(phaerr))

distance = np.array(distance)/100
distance_err = np.array(distance_err)/100

phase = np.array(phase)*pi/180
phase_err = np.array(phase_err)*pi/180

# Calculate trendline
fit = np.polyfit(distance, phase, 1)
print(np.polyfit(distance, phase, 1, full=True))
trend = np.poly1d(fit)

phase = phase*radians
phase_err = phase_err*radians

# Set axes
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel(r'relative distance (\textrm{m})')
ax.set_ylabel(r'phase shift / $\textrm{rad}$')
ax.xaxis.set_minor_locator(AutoMinorLocator())
# ax.set_xlim(0,25)
# ax.set_ylim(-80,20)

ax.text(0.05, 6, "y=%.3fx-%.3f"%(trend[1],abs(trend[0])))

# Plot data
ax.errorbar(distance, phase, xerr = distance_err, yerr = phase_err, \
            fmt='none', elinewidth = 0.3, capsize=0.7, capthick=0.3)
ax.plot(distance, trend(distance), 'b-', linewidth=0.7)

fig.tight_layout(pad=0.3)
fig.savefig('../plots/phaseshift.eps')
plt.clf()

print(trend)
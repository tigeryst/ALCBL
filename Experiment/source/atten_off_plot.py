import csv
from plot_config import *
import numpy as np
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, AutoMinorLocator

with open('../data/atten-off-axis.csv') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    distance = []
    distance_err = []
    amplitude = []
    amplitude_err = []
    for row in read_csv:
        dist = row[0]
        disterr = row[1]
        amp = row[2]
        amperr = row[3]

        distance.append(float(dist))
        distance_err.append(float(disterr))
        amplitude.append(float(amp))
        amplitude_err.append(float(amperr))

# Convert distance unit to m
distance = np.array(distance)/100
distance_err = np.array(distance_err)/100
distance_ord = np.linspace(min(distance), max(distance), 100)

# Convert peak-to-peak voltage to V
amplitude = np.array(amplitude)/1000
amplitude_err = np.array(amplitude_err)/1000

# Calculate trendline
fit = np.polyfit(distance, amplitude, 6)
trend = np.poly1d(fit)

print(trend)

# Set axes
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel(r'relative distance $(\textrm{m})$')
ax.set_ylabel(r'$V_{PP}~(\textrm{V})$')
ax.xaxis.set_minor_locator(AutoMinorLocator())

ax.errorbar(distance, amplitude, xerr = distance_err, yerr = amplitude_err, \
            fmt='none', elinewidth = 0.3, capsize=0.7, capthick=0.3)
ax.plot(distance_ord, trend(distance_ord),'b-', linewidth=0.7)

fig.tight_layout(pad=0.3)
fig.savefig('../plots/attenoff.eps', bbox_inches = 'tight')
plt.clf()

# plt.yscale('log', nonposy='clip')
# ax.yaxis.set_minor_formatter(ScalarFormatter())
# ax.yaxis.set_minor_formatter(FormatStrFormatter('%.1f'))
# ax.yaxis.set_major_formatter(ScalarFormatter())
# ax.set_ylabel(r'$\textrm{log\,}(V_{PP}/V)$')
# fig.savefig('../plots/attenoff_log.eps', bbox_inches = 'tight')
# plt.clf()

# # Convert amplitude and error for log plot
# amplitude_err = 0.434*np.divide(amplitude_err,amplitude)
# amplitude = np.log(amplitude)

# # Calculate trendline
# fit = np.polyfit(distance, amplitude, 1)
# trend = np.poly1d(fit)

# print(trend)
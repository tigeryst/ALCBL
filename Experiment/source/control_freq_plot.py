import csv
from plot_config import *
import numpy as np

# Time / s, N, Va / V, Vb / V, Freq A / Hz, Freq B / Hz, Phase A - B / deg, Voltage Input / Voltage
# This data file has the A probe connected to the control voltage and the B probe connected to the microphone

with open('../data/control-voltage-freq.csv') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    time = []
    va = []
    vb = []
    freqa = []
    freqb = []
    phase = []
    vin = []
    for row in read_csv:
        time_temp = row[0]
        va_temp = row[2]
        vb_temp = row[3]
        freqa_temp = row[4]
        freqb_temp = row[5]
        phase_temp = row[6]
        vin_temp = row[7]

        time.append(float(time_temp))
        va.append(float(va_temp))
        vb.append(float(vb_temp))
        freqa.append(float(freqa_temp))
        freqb.append(float(freqb_temp))
        phase.append(float(phase_temp))
        vin.append(float(vin_temp))

vcont_err = np.array(va)*(0.00538)
vin_err = np.array(vin)*(0.001)
freq_err = np.array(freqb)*(1/1515)
# Set axes
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel(r'd.c. control voltage (\textrm{V})')
ax.set_ylabel(r'frequency (\textrm{Hz})')
ax.set_xlim(0,5)

# Calculate trendline
fit = np.polyfit(va, freqb, 1)
trend = np.poly1d(fit)
ax.text(0.5, 12000, "y=%.3fx+%.3f"%(trend[1],trend[0]))

print('Function generator frequency against control voltage:')
print(trend)

ax.errorbar(va, freqb, xerr = vcont_err, yerr = freq_err, \
            fmt='none', elinewidth = 0.3, capsize=0.7, capthick=0.3)
ax.plot(va, trend(va),'b-', linewidth=0.7)

fig.tight_layout(pad=0.3)
fig.savefig('../plots/control_freq.eps')
plt.clf()

# Set axes
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel(r'LabVIEW voltage setting (\textrm{V})')
ax.set_ylabel(r'd.c. control voltage (\textrm{V})')
ax.set_xlim(0,5)
ax.set_ylim(0,5)

# Calculate trendline
fit = np.polyfit(vin, va, 1)
trend = np.poly1d(fit)
ax.text(0.3, 4.7, "y=%.3fx-%.3f"%(trend[1],abs(trend[0])))

print('Control voltage against LabVIEW voltage setting:')
print(trend)

ax.errorbar(vin, va, xerr = vin_err, yerr = vcont_err, \
            fmt='none', elinewidth = 0.3, capsize=0.7, capthick=0.3)
ax.plot(vin, trend(vin),'b-', linewidth=0.7)

fig.tight_layout(pad=0.3)
fig.savefig('../plots/labview_control.eps')
plt.clf()
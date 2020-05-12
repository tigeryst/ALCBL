import csv
from plot_config import *

with open('../data/fourier.csv') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    frequency = []
    channelA = []
    channelB = []
    for row in read_csv:
        freq = row[0]
        chanA = row[1]
        chanB = row[2]

        frequency.append(float(freq))
        channelA.append(float(chanA))
        channelB.append(float(chanB))

# Set axes
fig, ax = plt.subplots(1, 1, figsize=(3.17, 2.37))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xlabel(r'frequency (\textrm{kHz})')
ax.set_ylabel(r'power (\textrm{dB})')
ax.set_xlim(0,25)
ax.set_ylim(-80,20)

ax.plot(frequency,channelA, linewidth = 0.3)

fig.tight_layout(pad=0.3)
fig.savefig('../plots/fourier.eps')
plt.clf()
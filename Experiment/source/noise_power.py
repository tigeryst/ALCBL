import csv
import numpy as np
from math import log

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

db_noisepower = channelA[0:600] + channelA[1200:4500]
db_noisepower = np.array(db_noisepower)
noisepower = np.power(10,db_noisepower/20)
mean_noisepower = sum(noisepower)/len(db_noisepower)

db_signalpower = channelA[600:1200]
db_signalpower = np.array(db_signalpower)
signalpower = np.power(10,db_signalpower/20)
max_signalpower = max(signalpower)

print('Mean noise power = %.5f' % mean_noisepower)
print('Signal power = %.5f' % max_signalpower)
print('ln(power ratio) = %.5f' % log(mean_noisepower/max_signalpower))
import math
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path', metavar='N', type=str, nargs='+',
                   help='an integer for the accumulator')
args = parser.parse_args()
print args.path

'''
import pylab
import matplotlib.pyplot as plt
radius = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
area = [3.14159, 12.56636, 28.27431, 50.26544, 78.53975, 113.09724]

time = []
happy_values = []
concentrated_values = []
bored_values = []
annoyed_values = []
angry_values = []




#plt.plot(radius, area)
#plt.show()

logfiles = args.path

for logfile in logfiles:

    f = open(logfile, 'r')

    second = 0

    for line in f:
        values = line.split(' ')
        values.pop(0)

        second += 1
        happy = 0.0
        concentrated = 0.0
        bored = 0.0
        annoyed = 0.0
        angry = 0.0
        
        for value in values:
            emo = value.split('=')[0]
            strength = value.split('=')[1]
            if emo == 'happy':
                happy = strength
            if emo == 'concentrated':
                concentrated = strength
            if emo == 'bored':
                bored = strength
            if emo == 'annoyed':
                annoyed = strength
            if emo == 'angry':
                angry = strength
        time.append(second)
        happy_values.append(happy)
        concentrated_values.append(concentrated)
        bored_values.append(bored)
        annoyed_values.append(annoyed)
        angry_values.append(angry)


plt.plot(time, happy_values, color='g', label='happy')
plt.plot(time, concentrated_values, color='b', label='concentrated')
plt.plot(time, bored_values, color='y', label='bored')
plt.plot(time, annoyed_values, color='m', label='annoyed')
plt.plot(time, angry_values, color='r', label='angry')

plt.xlabel('Time in seconds since first answer')
plt.ylabel('Intense')
plt.title('VP ' + logfiles[0].split('.')[0])
plt.legend(loc='upper right', bbox_to_anchor=(1.004, 1.12),
          ncol=5, fancybox=True, shadow=True)

#plt.show()

figure = plt.gcf() # get current figure
figure.set_size_inches(22, 5)
figure.set_frameon(False)
figure.set_tight_layout(True)
# when saving, specify the DPI
plt.savefig(logfiles[0].split('.')[0] + ".png", dpi = 100)

print 'done'
'''













stats_file = 'stats.csv'
output = open(stats_file, 'w')
output.write('VP,C1,L1,C2,L2,C3,L3,C4,L4,C5,L5,C6,L6,C7,L7,C8,L8\n')
output.close()

logfiles = args.path

for logfile in logfiles:
    vp_nr = logfile.split('-')[0]

    f = open(logfile, 'r')
    nr_correct = [0.0 for i in range(8)]
    latencies = [0.0 for i in range(8)]

    for line in f:
        values = line.split(',')
        if values[0] != 'run':
            correct = int(values[5])
            nr_correct[int(values[0])] += correct

            latency = values[6].split(':')[2]

            seconds = float(latency.split('.')[0])
            if len(latency.split('.')) < 2:
                mseconds = 0.0
            else:
                mseconds = float(latency.split('.')[1]) / 1000000
            latencies[int(values[0])] += seconds + mseconds

    data = [vp_nr]
    for i in range(8):
        data.append(int(nr_correct[i] / 20 * 100))
        data.append(int(latencies[i] / 20 * 1000))
        #print (i, nr_correct[i]/20, latencies[i]/20)

    output = open(stats_file, 'a')
    for i in range(len(data)):
        output.write(str(data[i]) + ',')
    output.write('\n')
    output.close()


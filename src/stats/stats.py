import math
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path', metavar='N', type=str, nargs='+',
                   help='an integer for the accumulator')
args = parser.parse_args()
print args.path


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
            correct = int(values[4])
            nr_correct[int(values[0])] += correct

            latency = values[5].split(':')[2]

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

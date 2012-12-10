''' The module for all cognitve reactions of the agent
'''

import random
import math
import datetime

import utilities
from emomodule import Hope, Fear, Relief, FearsConfirmed

class CogModule:
    ''' This class handles all cognitive activity of the agent
    '''
    EXPECT_NEG = ('Fear', 'Fears-Confirmed', 'None')
    EXPECT_POS = ('Hope', 'Relief', 'None')

    ACT_POS = 90
    ACT_NEG = 60
    DECAY_RATE = 0.5
    NOISE = 0.5
    LATENCY = 0.4
    THRESHOLD = -2.0    

    FUNCTION = 'baselevel'   # or 'optimized'


    def __init__(self):
        self.expectation = None


    def baselevel_activation(self, times, d, now=None):
        ''' Base level activation.

            Input: Vector of calling times for a chunk.
                   Like [45023, 45046, 45102]

            Formula to compute baselevel activation:

            B_i = ln(sum_from_j=1_to_n(t_j^(-d)))    with

            n:  The number of presentations for chunk i = length of times.
            tj: The time since the jth presentation.
            d:  The decay parameter which is set using the
                :bll (base-level learning) parameter.
                This parameter is almost always set to 0.5.

            Values range around 0
                - activation falls
                + activation rises
        '''
        if not now:
            now = utilities.milliseconds(datetime.datetime.now())

        summed = 0
        for j in range(len(times)):
            diff = (now - times[j]) / 1000
            summed += math.pow(diff, -d)

        return math.log(summed)


    def optimized_learning(self, times, d, now=None):
        ''' Formula for base level learning. Optimizes computation time.

            B_i = ln(n / (1-d)) - d * ln(L)     with

            n = nr of presentations of chunk i
            L = The lifetime of chunk i (the time since its creation)
            d = The decay parameter
        '''
        if not now:
            now = utilities.milliseconds(datetime.datetime.now())

        n = len(times)
        L = now - times[0]

        return math.log(n / (1 - d)) - d * math.log(L)


    def logistic_distribution(self, s):
        ''' Formula for computing activation noise.

            The mean is 0
            The variance = (pi^2 / 3 * s^2)

            F(x) = 1 / (1 + e^(-(x - mean) / variance))
        '''
        mean = 0
        variance = math.pow(math.pi, 2) / 3 * math.pow(s, 2)

        return random.lognormvariate(mean, variance)


    def activation(self, times, now=None):
        ''' Computes the activation for the given chunk.
        '''
        if not times:
            return 0.0
        
        d = CogModule.DECAY_RATE
        s = CogModule.NOISE

        if not now:
            now = utilities.milliseconds(datetime.datetime.now())

        if CogModule.FUNCTION == 'optimized':
            base_activation = self.optimized_learning(times, d)
        else:
            base_activation = self.baselevel_activation(times, d)

        noise = self.logistic_distribution(s)
        return base_activation + noise

    
    def retrieval_probability(self, activation, threshold, noise):
        ''' Computes the recall probability
            = 1 / (1 + e^((threshold - activation) / noise))
        '''
        if activation == 0.0:
            return 0.0
        return 1.0 / (1.0 + math.exp((threshold - activation) / noise)) * 100


    def retrieval_latency(self, latency_factor, activation):
        '''
            time = latency_factor * e^(-activation)
        '''
        if activation == 0.0:
            return 0.0
        return latency_factor * math.exp(-activation)


    def get_expectation_name(self, retrieval_prob):
        expectation = 'none'
        if retrieval_prob > CogModule.ACT_POS:
            expectation = 'positive'
        elif retrieval_prob < CogModule.ACT_NEG:
            expectation = 'negative'
        return expectation


    def formulate_expectation(self, word):

        now = utilities.milliseconds(datetime.datetime.now())

        activation = self.activation(word.times)
        retrieval_prob = self.retrieval_probability(activation, CogModule.THRESHOLD, CogModule.NOISE)
        retrieval_latency = self.retrieval_latency(CogModule.LATENCY, activation)
        
        #retrieval_prob = self.retrieval_prob(word.times)

        self.expectation = self.get_expectation_name(retrieval_prob)

        print ('CogModule: Formulate expectation: {0}. {1:.2f}%. latency {2:.2f}s'.format(self.expectation, retrieval_prob, retrieval_latency))

        status = str(retrieval_prob) + ': '
        emotion = None

        if self.expectation == 'positive':
            status += 'Expecting right answer.'
            emotion = CogModule.EXPECT_POS[0]
        elif self.expectation == 'none':
            status += 'Expecting nothing.'
        elif self.expectation == 'negative':
            status += 'Expecting wrong answer'
            emotion = CogModule.EXPECT_NEG[0]
        else:
            print 'Wrong expectation value', self.expectation

        return (status, utilities.emotion_by_name(emotion))


    def react(self, correct, times):
        ''' Cognitive reaction to correctness and times of a given word.
        '''
        if self.expectation == 'negative':
            if correct:
                return utilities.get_emotion_by_name(CogModule.EXPECT_NEG[2])
            else:
                return utilities.get_emotion_by_name(CogModule.EXPECT_NEG[1])
        elif self.expectation == 'positive':
            if correct:
                return utilities.get_emotion_by_name(CogModule.EXPECT_POS[1])
            else:
                return utilities.get_emotion_by_name(CogModule.EXPECT_POS[2])


    ''' TODO: Remove?
    def get_remaining_task(self, task, current):
        # remove all items which are already done:
        remaining_task = []
        i = 0
        for group in task:
            remaining_group = []
            for item in group:
                if i < current:
                    i += 1
                else:
                    remaining_group.append(item)
            if remaining_group:
                remaining_task.append(remaining_group)

        return remaining_task
    '''


    def paired_associate(self):
        ''' Simulating the paired associate example.
        '''
        from environment import Word, Pair

        pairs = [Pair('bank', '0'), Pair('card', '1'), Pair('dart', '2'),
                 Pair('face', '3'), Pair('game', '4'),
                 Pair('hand', '5'), Pair('jack', '6'), Pair('king', '7'),
                 Pair('lamb', '8'), Pair('mask', '9'),
                 Pair('neck', '0'), Pair('pipe', '1'), Pair('guip', '2'),
                 Pair('rope', '3'), Pair('sock', '4'),
                 Pair('tent', '5'), Pair('vent', '6'), Pair('wall', '7'),
                 Pair('xray', '8'), Pair('zinc', '9')]

        nr_runs = 8
        now = utilities.milliseconds(datetime.datetime.now())

        total_recalled = [0 for i in range(nr_runs)]
        total_probs = [0 for i in range(nr_runs)]
        for k in range(100):

            times = self.get_times(nr_runs, now)
            probs = self.get_probabilities(times, now)
            mean_probs = self.get_mean(probs)
            recalled = self.simulate_run(probs)

            for j in range(len(recalled)):
                total_recalled[j] += recalled[j]
                total_probs[j] += mean_probs[j]

        for i in range(nr_runs):
            print i+1, total_recalled[i] / 100, total_probs[i] / 100


    def get_mean(self, item_run_pairs):
        means = [0 for i in range(len(item_run_pairs[0]))]
        for item_index in range(len(item_run_pairs)):
            for run_index in range(len(item_run_pairs[item_index])):
                means[run_index] += item_run_pairs[item_index][run_index]

        for i in range(len(means)):
            means[i] = means[i] / len(item_run_pairs)
        return means


    def get_times(self, nr_runs, now):
        ''' Returns a vector of times:

            [[5, 20], [10, 30], [15, 25]

            First index: Item
            Second Index: Run
        '''
        times = [[] for i in range(20)]

        for current_run in range(nr_runs):
            for i in range(20):

                offset = (nr_runs - current_run - 1) * 200
                time = now - (i*10+5+offset)
                assert time < now
                times[i].append(time)

        return times


    def get_probabilities(self, times, now):
        ''' Input: Vector of calling times for each item:

            [[5, 20], [10, 30], [15, 25]

            First index: Item
            Second Index: Run

            Returns: Vector of possibilities. Each entry represents the
            possibility of the current item in the selected run.

            [[0.43, 0.67], [33.0, 60.9], [0.50, 0.70]]

            First index: Item
            Second Index: Run nr
        '''
        probs = [[0.0] for i in range(20)]
        nr_runs = len(times[0])

        for current_run in range(1, nr_runs):
            offset = (nr_runs - current_run - 1) * 200
            for i in range(20):
                activation = self.activation(times[i][:current_run], now-offset)
                s = 0.5
                threshold = -2.0
                prob = self.retrieval_probability(activation, threshold, s)
                probs[i].append(prob)

        return probs


    def simulate_run(self, probs):
        recalled = [0 for i in range(len(probs[0]))]

        for item in probs:
            for run_index in range(len(item)):
                randvar = random.randint(0, 100)
                if randvar < item[run_index] * 100:
                    recalled[run_index] += 1

        return recalled


if __name__ == '__main__':
    cog = CogModule()
    cog.paired_associate()

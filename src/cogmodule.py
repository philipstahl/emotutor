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

    ACT_POS = 0.0
    ACT_NEG = -0.5

    FUNCTION = 'baselevel'   # or 'optimized'


    def __init__(self):
        self.last_expectation = None

    def get_emotion_by_name(self, name):
        if name == 'Fear':
            return Fear()
        elif name == 'Fears-Confirmed':
            return FearsConfirmed()
        elif name == 'Hope':
            return Hope()
        elif name == 'Relief':
            return Relief()
        else:
            return None

    def print_random_activation_values(self, runs, max_time):
        ''' Function for visualizing the baseline activation
        '''
        now = utilities.seconds(datetime.datetime.now())
        tmp_now = now
        times = []

        # first one: often with small time diff
        for i in range(runs):
            time = random.randint(0, max_time)
            tmp_now = tmp_now - time
            times.insert(0, tmp_now)

        print 'Times:', times
        print 'Activation values:'

        for i in range(len(times)-1):
            t = times[0:i+1]
            activation = self.activation2(t, 0.5)
            print i, activation

    def baselevel_activation(self, times, d, now=None):
        ''' Base level activation for a chunk i is:

            B_i = ln(sum_from_j=1_to_n(t_j^(-d)))    with

            n:  The number of presentations for chunk i.
            tj: The time since the jth presentation.
            d:  The decay parameter which is set using the
                :bll (base-level learning) parameter.
                This parameter is almost always set to 0.5.

            Values range around 0
                - activation falls
                + activation rises
        '''        
        n = len(times)

        summed = 0
        if not now:
            now = utilities.seconds(datetime.datetime.now())
        for j in range(n):
            diff = now - times[j]
            summed += math.pow(diff, -d)

        B = math.log(summed)
        return B

    def optimized_learning(self, times, d):
        ''' Formula for base level learning. Optimizes computation time.

            B_i = ln(n / (1-d)) - d * ln(L)     with

            n = nr of presentations of chunk i
            L = The lifetime of chunk i (the time since its creation)
            d = The decay parameter
        '''
        n = len(times)

        L = self.utilities(datetime.datetime.now()) - times[0]
        B = math.log(n / (1 - d)) - d * math.log(L)

        return B

    def prob_of_recall(self, threshold, activation, noise):
        '''
            recall probability = 1 / (1 + e^((threshold - activation) / noise))
        '''
        return 1.0 / (1.0 + math.exp((threshold - activation) / noise))

    def retrieval_latency(self, latency_factor, activation):
        '''
            time = latency_factor * e^(-activation)
        '''
        return latency_factor * math.exp(-activation)

    def logistic_distribution(self, x, s):
        '''
            The mean is 0
            The variance = (pi^2 / 3 * s^2)

            F(x) = 1 / (1 + e^(-(x - mean) / variance))
        '''
        mean = 0
        variance = math.pow(math.pi, 2) / 3 * math.pow(s, 2)

        return random.lognormvariate(mean, variance)
        #return 1.0 / 1.0 + math.exp(-(x - mean) / variance)

    def paired_associate(self):
        d = 0.5
        s = 0.5
        threshold = -2.0

        
        # init times:
        from environment import Word, Pair

        pairs = [Pair('bank', '0'), Pair('card', '1'), Pair('dart', '2'), Pair('face', '3'), Pair('game', '4'),
                 Pair('hand', '5'), Pair('jack', '6'), Pair('king', '7'), Pair('lamb', '8'), Pair('mask', '9'),
                 Pair('neck', '0'), Pair('pipe', '1'), Pair('guip', '2'), Pair('rope', '3'), Pair('sock', '4'),
                 Pair('tent', '5'), Pair('vent', '6'), Pair('wall', '7'), Pair('xray', '8'), Pair('zinc', '9')]

        
        nr_runs = 8
        now = utilities.seconds(datetime.datetime.now())

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

            #print 'RUN, RECALLED, PROB' 
            #for i in range(nr_runs):
            #    print i+1, recalled[i], mean_probs[i]

        for i in range(nr_runs):
            print i+1, total_recalled[i] / 100, total_probs[i] / 100

        
    def get_prob(self, times, now):
        d = 0.5
        s = 0.5
        threshold = -2.0
        baselevel = self.baselevel_activation(times, d, now)
        noise = self.logistic_distribution(now, s)
        #noise = 0.0
#
        
        activation = baselevel + noise
        #activation = baselevel + 0.8
        return self.prob_of_recall(threshold, activation, s)


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
                
        # TODO: Shuffle
        #random.shuffle(times)
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
                prob = self.get_prob(times[i][:current_run], now-offset)
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



















    def activation(self, times, d):
        if CogModule.FUNCTION == 'optimized':
            return self.optimized_learning(times, d)
        return self.baselevel_activation(times, d)

    def expectation(self, activation):
        expectation = 'none'
        if activation > CogModule.ACT_POS:
            expectation = 'positive'
        elif activation < CogModule.ACT_NEG:
            expectation = 'negative'
        return expectation

    def get_expectation(self, word):
        activation = self.activation(word.times, 0.5)
        self.last_expectation = self.expectation(activation)

        print '  CogModule: Formulate expectation:', self.last_expectation

        status = str(activation) + ': '
        emotion = None

        if self.last_expectation == 'positive':
            status += 'Expecting right answer.'
            emotion = CogModule.EXPECT_POS[0]
        elif self.last_expectation == 'none':
            status += 'Expecting nothing.'
        elif self.last_expectation == 'negative':
            status += 'Expecting wrong answer'
            emotion = CogModule.EXPECT_NEG[0]
        else:
            print 'Wrong expectation value', self.last_expectation

        return (status, self.get_emotion_by_name(emotion))


    def react(self, correct, times):
        ''' Cognitive reaction to correctness and times of a given word.
        '''
        #activation = self.activation(times, 0.5)
        #return self.last_expectation
        if self.last_expectation == 'negative':
            if correct:
                return self.get_emotion_by_name(CogModule.EXPECT_NEG[2])
            else:
                return self.get_emotion_by_name(CogModule.EXPECT_NEG[1])
        elif self.last_expectation == 'positive':
            if correct:
                return self.get_emotion_by_name(CogModule.EXPECT_POS[1])
            else:
                return self.get_emotion_by_name(CogModule.EXPECT_POS[2])


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

    def focus_activation(self, task, current):
        ''' The activation of a chunk is the sum of its base-level activation
            and the activations it receives from the elements currently in
            the focus of attention. Formally, the equation in ACT-R for the
            actvation, Ai , of chunk i is

            Ai = Bi + sum_{over j} Wj * Sji

            where Bi is the base-level activation of chunk i, Wj is the
            salience or source activation of element j in the focus of
            attention, and Sji is the strength of association from element j
            to chunk i.

            FRAGE: WELCHE EMLEMENTE SIND ALLES IM FOKUS?
        '''


        ''' The typical ACT-R assumption is that, if there are n sources of
            activation the Wj are all set to l/n.
        '''

        ''' The associative strengths, Sji, reflect the competition among
            the associations to the cue j. According to the ACT-R theory,
            Sji = S + ln(P(i | j)), where P(i | j) is the probability that
            chunk i will be needed when j appears in the context.
            S is a constant.

            That is, if there are m elements associated to j their average
            probability will be l/m and Sji = S - ln(m). This is the
            simplification that will be used in all the simulations presented
            in the paper. Thus,

            Sji = S - ln(m).

            m = NR ELEMENTS ASSOCIATED TO j

            S = constant: WELCHER WERT?
                It can be set in the simulation but if not set it will default to the log
                of the total number of chunks.
        '''
        n = 0                                                   # total nr of items
        for group in task:
            n += len(group)

        nr_chunks = len(task)                                   # total nr of chunks

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

        task = remaining_task

        activations = []
        for group in task:
            group_activations = []
            for item in group:
                group_activations.append(0.0)
            activations.append(group_activations)

        nr_elem_associated_to = []
        for group in task:
            #nr_elem_associated_to.append(len(group))
            nr_elem_associated_to.append(len(group) - 1)

        for group_index in range(len(activations)):


            for i in range(len(activations[group_index])):



                m = nr_elem_associated_to[group_index]              # nr elements associated to j
                if m == 0:
                    m = 1

                S = math.log(nr_chunks)

                elements_in_focus = 0
                for group in task:                                  # ALLE ELEMENTE
                    elements_in_focus += len(group)                 # ODER
                #elements_in_focus = len(activations[group_index])    # NUR DIE DER GRUPPE?


                for j in range(elements_in_focus):
                    Wj = 1.0 / n
                    Sji = S - math.log(m)
                    activations[group_index][i] += Wj * Sji

        return activations

    def prob(self, Mi, Mjs):
        ''' 1 / (1 + e_to_the_power(Ai - threshold))
            return 1.0/(1.0 + math.exp((Ai - (-0.35)) / 0.3))
        '''
        s = 0.3
        t = math.sqrt(2*s)

        divisor = 0
        for j in Mjs:
            if j != Mi:
                divisor += math.exp(j/t)

        result = math.exp(Mi/t) #/ divisor
        print Mi, ': ', result
        return result




    def equation8(self, time, length):
        ''' Activation = ln(n) - 0.5 * ln(T) - ln(L)

            n = number of rehearsals
            T = delay / time since presentation
            L = list length
        '''
        activation = math.log(1.0) - 0.5 * math.log(time) - math.log(length)
        # SEE ALSO EQUATION NR 9
        return activation


if __name__ == '__main__':
    cog = CogModule()
    cog.paired_associate()

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

    def baselevel_activation(self, times, d):
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

    task = [[1, 5, 3], [8, 4, 7], [2, 6, 9]]
    #task = [[1, 2, 3]]

    length = len(task)
    current = 0

    focus_activations = cog.focus_activation(task, current)

    now = cog.seconds(datetime.datetime.now())
    diff = 9
    times = []
    for d in range(diff):
        times.insert(0, now - (d+2))

    time_diffs = []
    for time in times:
        time_diffs.append(now - time)

    task = cog.get_remaining_task(task, current)

    num_remaining = 0
    for group in task:
        num_remaining += len(group)
    times = times[(len(times) - num_remaining):]

    baselevel_activations = []
    for group_index in range(len(task)):
        group_activations = []
        for item_index in range(len(task[group_index])):
            index = item_index
            if group_index == 1:
                index += len(task[group_index-1])
            if group_index == 2:
                index += len(task[group_index-1]) + len(task[group_index-2])

            time = [times[index]]

            activation = cog.baselevel_activation(time, 0.5)
            group_activations.append(activation)
        baselevel_activations.append(group_activations)

    eq1_activations = []
    for group_index in range(len(baselevel_activations)):
        group_activations = []
        for item_index in range(len(baselevel_activations[group_index])):
            activation = baselevel_activations[group_index][item_index] + focus_activations[group_index][item_index]
            group_activations.append(activation)
        eq1_activations.append(group_activations)


    '''EQUATION 8:'''
    activations = []
    for group_index in range(len(task)):
        group_activations = []
        for item_index in range(len(task[group_index])):
            index = item_index
            if group_index == 1:
                index += len(task[group_index-1])
            if group_index == 2:
                index += len(task[group_index-1]) + len(task[group_index-2])

            time = time_diffs[index]

            activation = cog.equation8(time, length)
            group_activations.append(activation)
        activations.append(group_activations)

    print 'BASELEVEL'
    for group in baselevel_activations:
        for item in group:
            print item
    '''
    print 'FOCUS'
    for group in focus_activations:
        for item in group:
            print item
    '''
    print 'EQUATION 1:'
    for group in eq1_activations:
        for item in group:
            print item
    '''
    print 'EQUATION 8'
    for group in activations:
        for item in group:
            print item
    '''
    Mis = []
    for group in eq1_activations:
        for item in group:
            Mis.append(item)

    print 'Mis:'
    print Mis
    print 'PROBAILITY:'
    for activation in Mis:
        cog.prob(activation, Mis)

''' The module for all cognitve reactions of the agent
'''

import random
import math
import datetime

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

    def seconds(self, time):
        ''' Returns the given time in seconds
        '''
        return time.second + 60 * time.minute + 60 * 60 * time.hour


    def print_random_activation_values(self, runs, max_time):
        ''' Function for visualizing the baseline activation
        '''
        now = self.seconds(datetime.datetime.now())
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
        now = self.seconds(datetime.datetime.now())
        for j in range(n):
            summed += math.pow(now - times[j], -d)

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

        L = self.seconds(datetime.datetime.now()) - times[0]
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


if __name__ == '__main__':
    cog = CogModule()
    cog.print_random_activation_values(10, 20)

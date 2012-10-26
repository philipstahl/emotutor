''' The module for all cognitve reactions of the agent
'''

import random
import math
import datetime



class CogModule:
    ''' This class handles all cognitive activity of the agent
    '''
    tasks = []
    times = []

    def __init__(self):
        pass

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
            activation = self.baselevel_activation2(t, 0.5)
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

    def check(self, task, times):
        ''' A cognitive analysis of the task.

            The Agent predicts the answer given
            by the human solver and the time needed.
            If the predictions do not match to the facts, the agent will show a
            reaction of surprise.

        '''
        activation = self.baselevel_activation(times, 0.5)
        question = task.question
        return "[not surprised]"


    def react(self, correct, times):
        ''' Cognitive reaction to correctness and times of a given word.
            Returns emotional and surprise intense.
        '''
        activation = self.baselevel_activation(times, 0.5)

        surprise = 0         # surprise intensity: 0.0, 0.5 or 1.0
        emotion = 0          # emotion intensity: 0.3, 0.6, 1.0

        if activation > 0 and correct:
            # expected result happes. no surprise. low intensity
            surprise = 0
            emotion = 30

        elif activation > -0.5 and correct:
            # expected result happens. no surprise. mid intensity
            surprise = 0
            emotion = 60

        elif activation > -1.0 and correct:
            # result was not expected. low surprise. mid intensity
            surprise = 50
            emotion = 60

        elif correct:
            # result was not expected. high surprise. high intensity
            surprise = 100
            emotion = 100

        if activation > 0 and not correct:
            # result was not expected. high surprise. high intensity
            surprise = 100
            emotion = 100

        elif activation > -0.5 and not correct:
            # result was not expected. low surprise. mid intensity
            surprise = 50
            emotion = 60

        elif activation > -1.0 and not correct:
            # result was expected. no surprise. mid intensity
            surprise = 0
            emotion = 60
        else:
            # result was expected. no surprise. low intensity
            surprise = 0
            emotion = 30

        return (surprise, emotion)

    def expectation(self, word):
        activation = self.baselevel_activation(word.times, 0.5)
        expectation = str(activation) + ': '
        if activation > 0:
            expectation += 'Highly expecting'
        elif activation > -0.5:
            expectation += 'Expecting'
        elif activation > -1.0:
            expectation += 'Not expecting'
        else:
            expectation += 'Highly not expecting'

        return expectation + ' ' + word.word


if __name__ == '__main__':
    cog = CogModule()
    cog.print_random_activation_values(10, 20)

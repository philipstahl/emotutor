''' The module for all cognitve reactions of the agent
'''

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

        log = '  ln('
        summed = 0
        now = datetime.datetime.now()
        for j in range(n):
            single = math.pow(self.seconds(now) - self.seconds(times[j]), -d)
            log += str(single)
            if j < n-1:
                log += ' + '
            summed += single

        print 'times', times
        print 'summed', summed
        B = math.log(summed)
        log += ') = ' + str(B)
        print log
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

        if activation > 0.5 and correct:
            # expected result happes. no surprise. low intensity
            surprise = 0
            emotion = 30

        elif activation > 0 and correct:
            # expected result happens. no surprise. mid intensity
            surprise = 0
            emotion = 60

        elif activation > -0.5 and correct:
            # result was not expected. low surprise. mid intensity
            surprise = 50
            emotion = 60

        elif correct:
            # result was not expected. high surprise. high intensity
            surprise = 100
            emotion = 100

        if activation > 0.5 and not correct:
            # result was not expected. high surprise. high intensity
            surprise = 100
            emotion = 100

        elif activation > 0 and not correct:
            # result was not expected. low surprise. mid intensity
            surprise = 50
            emotion = 60

        elif activation > -0.5 and not correct:
            # result was expected. no surprise. mid intensity
            surprise = 0
            emotion = 60
        else:
            # result was expected. no surprise. low intensity
            surprise = 0
            emotion = 30

        return (surprise, emotion)

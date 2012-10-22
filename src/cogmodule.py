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

    def seconds(time):
        return time.second + 60 * time.minute + 60 * 60 * time.hour

    def baselevel_activation(n, d, times):
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
        log = '  ln('
        summed = 0
        now = datetime.datetime.now()
        for j in range(n):
            single = math.pow(seconds(now) - seconds(times[j]), -d)
            log += str(single)
            if j < n-1:
                log += ' + '
            summed += single
        B = math.log(summed)
        log += ') = ' + str(B)
        print log
        return B


    def check(self, task):
        ''' A cognitive analysis of the task.

            The Agent predicts the answer given
            by the human solver and the time needed.
            If the predictions do not match to the facts, the agent will show a
            reaction of surprise.

        '''
        activation = baselevel_activation(len(times[i]), 0.5, times[i])
        question = task.question
        return "[not surprised]"

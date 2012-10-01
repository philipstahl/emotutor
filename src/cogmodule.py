''' The module for all cognitve reactions of the agent
'''

class CogModule:
    ''' This class handles all cognitive activity of the agent
    '''
    def __init__(self):
        pass

    def check(self, task):
        ''' A cognitive analysis of the task.

            The Agent predicts the answer given
            by the human solver and the time needed.
            If the predictions do not match to the facts, the agent will show a
            reaction of surprise.

        '''
        question = task.question
        return "[not surprised]"

class CogModule:

    def __init__(self):
        pass

    ''' A cognitive analysis of the task: The Agent predicts the answer given
        by the human solver and the time needed.
        If the predictions do not match to the facts, the agent will show a
        reaction of surprise.
    '''
    def check(self, task):
        question = task.question
        return "[not surprised]"

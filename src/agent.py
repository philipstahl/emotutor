from cogmodule import CogModule
from emomodule import EmoModule
from speachmodule import SpeachModule

class Agent:

    def __init__(self, tasks):
        self.tasks = tasks
        self.cogModule = CogModule()
        self.emoModule = EmoModule()
        self.speachModule = SpeachModule()
        pass


    ''' The agent introduces the human solver to the experiment, explaining
        the rules of the task.
    '''
    def introduce(self):
        return "Welcome to your vocabulary session.Press 'Enter' to begin:\n"


    ''' The agent presents a single task.
    '''
    def present(self, task):
        return task.question + ": "


    ''' The agent evalutates the solution given by the human solver and shows
        an emotional and verbal reaction.The reaction depends on the feedback
        of the cognitive (= surprise) and emotional (= mood) modules.
    '''
    def evaluate(self, task):
        correct, time = task.last_trial()
        surprise = self.cogModule.check(task)
        mood = self.emoModule.check(task)
        answer = surprise + mood + " "
        answer += self.speachModule.get_verbal_reaction(correct, surprise, mood)
        return answer + "You needed " + str(time) + " sec."


    ''' The Agent gives feedback for the whole test telling how many tasks
        have been done wrong.
    ''' 
    def end(self, tasks):
        total_misses = 0
        for task in tasks:
            total_misses += task.misses()
        return "Test finished. You had " + str(total_misses) + " misses in total."

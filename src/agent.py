from cogmodule import CogModule
from emomodule import EmoModule
from speachmodule import SpeachModule
from marc import Marc
from expression import Anger, Joy, Relax
from speech import Speech

class Agent:

    ''' Constructor
    '''
    def __init__(self, tasks, MARC = True):
        self.tasks = tasks
        self.cogModule = CogModule()
        self.emoModule = EmoModule()
        self.speachModule = SpeachModule()
        if MARC:
            self.marc = Marc()
        else:
            self.marc = None


    ''' The agent introduces the human solver to the experiment, explaining
        the rules of the task.
    '''
    def introduce(self):
        text = "Welcome to your vocabulary session. Press 'Enter' to begin."
        
        if self.marc:
            self.marc.show(Relax())
            self.marc.speak(Speech("introduction", text))
        
        return text + "\n"


    ''' The agent presents a single task.
    '''
    def present(self, task):
        text = "What is the german word for " + task.question
        
        if self.marc:
            self.marc.speak(Speech("task", text))

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
        text= self.speachModule.get_verbal_reaction(correct, surprise, mood)

        if self.marc:
            if mood == "[very happy]" or mood == "[happy]":
                self.marc.show(Joy())
            elif mood == "normal":
                self.marc.show(Relax())
            elif mood == "[very angry]" or mood == "[angry]":
                self.marc.show(Anger())

            self.marc.speak(Speech("evaluation", text))

        return answer + text + "You needed " + str(time) + " sec."


    ''' The Agent gives feedback for the whole test telling how many tasks
        have been done wrong.
    ''' 
    def end(self, tasks):
        total_misses = 0
        for task in tasks:
            total_misses += task.misses()
        return "Test finished. You had " + str(total_misses) + " misses in total."

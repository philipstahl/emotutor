from cogmodule import CogModule
from emomodule import EmoModule
from speechmodule import SpeechModule
from marc import Marc
from expression import Anger, Joy, Relax
from speech import Speech
from globalsettings import *


class Agent:

    ''' Constructor
    '''
    def __init__(self, tasks):
        self.tasks = tasks
        self.marc = None
        if MARC:
            self.marc = Marc()
        self.cogModule = CogModule()
        self.emoModule = EmoModule(self.marc)
        self.speechModule = SpeechModule()

    ''' The agent introduces the human solver to the experiment, explaining
        the rules of the task.
    '''
    def introduce(self):
        emotion = Relax()
        speech = Speech("introduction", "Welcome to your vocabulary session.")

        if self.marc:
            self.marc.show(emotion)
            self.marc.speak(speech)

        return (emotion.name, speech.text)

    ''' The agent presents a single task.
    '''
    def present(self, task):
        speech = Speech("task", "What is the german word for " + task.question
                                + "?")

        if self.marc:
            self.marc.speak(speech)

        return ('None', speech.text)

    ''' The agent evalutates the solution given by the human solver and shows
        an emotional and verbal reaction.The reaction depends on the feedback
        of the cognitive (= surprise) and emotional (= mood) modules.
    '''
    def evaluate(self, task):
        correct, time = task.last_trial()
        surprise = self.cogModule.check(task)
        emotion = self.emoModule.check(task)


        answer = surprise + "[" + emotion.name + ", " \
                          + str(emotion.impulse) + "] "
        speech = Speech("evaluation",
                        self.speechModule.get_verbal_reaction(correct, surprise,
                                                              emotion.name,
                                                              emotion.impulse))

        if self.marc:
            self.marc.speak(speech)

        return (emotion.name + " " + str(emotion.impulse), speech.text)

    ''' The Agent gives feedback for the whole test telling how many tasks
        have been done wrong.
    '''
    def end(self, tasks):
        total_misses = 0
        for task in tasks:
            total_misses += task.misses()
        return ("None", "Test finished. \
                 You had {0} misses in total.".format(str(total_misses)))

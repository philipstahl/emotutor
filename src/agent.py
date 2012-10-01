''' The class for the agent
'''
from cogmodule import CogModule
from emomodule import EmoModule, Relax
from speechmodule import SpeechModule, Speech
from marc import Marc

JOY = "JOY"
ANGER = "ANGER"
RELAX = "RELAX"

class Agent:
    ''' The Agent class contains methods for the agents behaviour.

        All methods return the current emotional and verbal reaction to the event
        that triggered the method.

    '''

    def __init__(self, tasks):
        self.tasks = tasks
        self.marc = None
        self.cog_module = CogModule()
        self.emo_module = EmoModule()
        self.speech_module = SpeechModule()

    def enable_marc(self, ip_addr, port_in, port_out, emotions):
        ''' Enables marc module.

            The agent show emotional and verbal output via marc.
            @emotions: dictionary specifying which emotions marc shall use

        '''
        self.marc = Marc(ip_addr, port_in, port_out, emotions)

    def enable_open_mary(self, ip_addr, voice, path):
        ''' Enables Open Mary.

            The agents speech module uses open mary to produce text to speech
            output
         '''
        self.speech_module.enable_open_mary(self, ip_addr, voice, path)

    def enable_wasabi(self, ip_addr, port_in, port_out, emotions):
        ''' Enables the wasabi module.

            The agent uses wasabi to simulate its emotion status
            @emotions: dictionary specifying the use of emotions in wasabi
        '''
        self.emo_module.enable_wasabi(ip_addr, port_in, port_out, emotions,
                                      self.marc)


    def introduce(self):
        ''' The agents reaction at the beginning of the training

            The agent introduces the human solver to the experiment, explaining
            the rules of the task.

        '''

        emotion = Relax()
        speech = Speech("introduction", "Welcome to your vocabulary session.")

        if self.marc:
            self.marc.show(emotion)
            self.marc.speak(speech)

        return (emotion.name, speech.text)

    def present(self, task):
        ''' The agent presents a single task.

        '''
        speech = Speech("task", "What is the german word for " + task.question
                                + "?")

        if self.marc:
            self.marc.speak(speech)

        return ('None', speech.text)

    def evaluate(self, task):
        ''' The agents reaction to an answer by the user.

            The agent evalutates the solution given by the human solver and shows
            an emotional and verbal reaction.The reaction depends on the feedback
            of the cognitive (= surprise) and emotional (= mood) modules.

        '''
        correct = task.last_trial()[0]
        surprise = self.cog_module.check(task)
        emotion = self.emo_module.check(task)
        speech = Speech("evaluation",
                        self.speech_module.get_verbal_reaction(correct,
                                                               surprise,
                                                               emotion.name,
                                                               emotion.impulse))

        if self.marc:
            self.marc.speak(speech)

        return (emotion.name + " " + str(emotion.impulse), speech.text)

    def end(self, tasks):
        ''' The Agents output at the end of the training.

            The Agent gives feedback for the whole test telling how many tasks
            have been done wrong.

        '''
        total_misses = 0
        for task in tasks:
            total_misses += task.misses()

        speech = Speech("end", "Test finished. \
                        You had {0} misses in total.".format(str(total_misses)))
        if self.marc:
            self.marc.speak(speech)
        return ("None", speech.text)

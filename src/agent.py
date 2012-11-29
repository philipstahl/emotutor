''' The class for the agent
'''

from threading import Thread

from cogmodule import CogModule
from emomodule import EmoModule, Happy, Angry
from speechmodule import SpeechModule
from marc import Marc


class Agent:

    INIT_EMOTION = 'None'

    def __init__(self, use_marc, use_wasabi, use_mary):
        self.marc = None
        if use_marc:
            self.marc = Marc()

        self.emo_module = EmoModule(self.marc, function='wasabi')
   
        self.speech_module = SpeechModule(use_mary)
        self.cog_module = CogModule()

    def start(self):
        ''' The agents reaction at the beginning of the training

            The agent introduces the human solver to the experiment, explaining
            the rules of the task.

        '''
        self.emo_module.start_hearing()
        if Agent.INIT_EMOTION == 'Wasabi':
            self.emo_module.start_expressing()
        else:
            inits = {'Happy': Happy(), 'Neutral': None, 'Angry': Angry()}
            self.emo_module.show_static_emotion(inits[Agent.INIT_EMOTION])

        emotion = self.emo_module.get_primary_emotion()

        speech = self.speech_module.start_list(emotion)
        self.speak(speech)
        return (str(emotion), '...', speech.text)

    def introduce(self):
        ''' The agent speaks the introduction text to present the list of words.
        '''
        emotion = self.emo_module.get_primary_emotion()
        speech = self.speech_module.present_list(emotion)
        self.speak(speech)
        return (str(emotion), '...', speech.text)

    def present(self, word):
        ''' The Agent present the given word
        '''

        emotion = self.emo_module.get_primary_emotion()
        speech = self.speech_module.present_word(word, emotion)
        self.speak(speech)
        return (str(emotion), '...', speech.text)

    def wait(self, word):
        ''' Wait for user input and return the current emotion
        '''
        print 'Agent: Waiting ...'
        if not self.emo_module.is_dynamic() and self.emo_module.use_wasabi:

            self.emo_module.start_expressing()

        emotion = self.emo_module.get_primary_emotion()
        expectation, emo = self.cog_module.get_expectation(word)
        if emo:
            self.emo_module.trigger(emo)

        return (str(emotion), expectation, '...')


    def speak(self, speech):
        ''' Speaks the given speech via marc or wave file
        '''
        if self.marc:
            self.marc.speak(speech)
        elif self.speech_module.tts:
            self.play_wave(speech.name)

    def evaluate(self, word, correct):
        ''' Evalutes the given words regarding to its correctness and time.
            Return emotional and verbal output, based on the cognitve,
            emotional and verbal evaluation
        '''
        print 'Agent: Evaluating answer ...'
        # cognitive evaluation: Determines surprise and intensity of emotion
        #expectation = self.cog_module.last_expectation
        expectation = 'none'

        # emotional evaluation:
        emotion = self.emo_module.check(correct, expectation)

        #cog_react = self.cog_module.react(correct, word.times)

        #if cog_react:
        #    self.emo_module.trigger(cog_react)

        verbal_output = '...'
        #if not correct:
        #    speech = self.speech_module.react(emotion, word.word)
        #    self.speak(speech)
        #    verbal_output = speech.text

        return (str(emotion), '...', verbal_output)

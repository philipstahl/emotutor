''' The class for the agent
'''

from threading import Thread

from cogmodule import CogModule
from emomodule import EmoModule, Happy, Angry
from speechmodule import SpeechModule
from marc import Marc


class Agent:

    INIT_EMOTION = 'None'

    def __init__(self, use_wasabi, logger):
        self.marc = Marc(logger)
        self.emo_module = EmoModule(self.marc, use_wasabi, logger)
        self.speech_module = SpeechModule(logger)
        self.cog_module = CogModule(logger)
        self.logger = logger

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
        emotion=None

        speech = self.speech_module.start_list(emotion)
        self.speak(speech)
        return (str(emotion), '...', speech.text)

    def introduce(self):
        ''' The agent speaks the introduction text to present the list of words.
        '''
        emotion = self.emo_module.get_primary_emotion()
        emotion=None
        speech = self.speech_module.present_list(emotion)
        self.speak(speech)
        return (str(emotion), '...', speech.text)

    def say(self, text):
        speech = self.speech_module.get_text(text)
        self.speak(speech)



    def present_word(self, word, number):
        emotion = self.emo_module.get_primary_emotion()
        emotion=None

        # formulate expection for number
        expectation, emo = self.cog_module.formulate_expectation(number)
        if emo:
            self.emo_module.trigger(emo)

        speech = self.speech_module.present_word(word, emotion)
        self.speak(speech)

        return (str(emotion), expectation, speech.text)


    def present_number(self, number):       
        emotion = self.emo_module.get_primary_emotion()
        emotion=None
        speech = self.speech_module.present_word(number, emotion)
        self.speak(speech)
        return (str(emotion), '...', speech.text)
    
    '''
    def wait(self, word):
        print 'Agent: Waiting ...'
        if not self.emo_module.is_dynamic() and self.emo_module.use_wasabi:

            self.emo_module.start_expressing()

        emotion = self.emo_module.get_primary_emotion()
        expectation, emo = self.cog_module.get_expectation(word)
        if emo:
            self.emo_module.trigger(emo)

        return (str(emotion), expectation, '...')
    '''

    def speak(self, speech):
        ''' Speaks the given speech via marc or wave file
        '''
        self.marc.speak(speech)
        
    def evaluate(self, correct):
        ''' Evalutes the given words regarding to its correctness and time.
            Return emotional and verbal output, based on the cognitve,
            emotional and verbal evaluation
        '''
        
        # cognitive evaluation: Determines surprise and intensity of emotion
        expectation = self.cog_module.expectation
        cog_react = self.cog_module.resolve_expectation(correct)
            
        # emotional evaluation:
        emotion = self.emo_module.check(correct, expectation)
        emotion=None

        if cog_react:
            self.emo_module.trigger(cog_react)

        verbal_output = '...'
        
        if correct == 1:
            self.marc.headYes()
        elif correct == 0:
            self.marc.headNo()

        return (str(emotion), '...', verbal_output)

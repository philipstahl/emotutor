''' The class for the agent
'''

from threading import Thread
#import winsound                         # sound for windows
#import pygame
from PyQt4.QtGui import QSound

from cogmodule import CogModule
from emomodule import EmoModule
from speechmodule import SpeechModule
from marc import Marc


class Agent:
    ''' The Agent class contains methods for the agents behaviour.

        All methods return the current emotional and verbal reaction to the event
        that triggered the method.
    '''

    def __init__(self, use_marc, use_wasabi, use_mary):
        self.marc = None
        if use_marc:
            self.marc = Marc()
        self.emo_module = EmoModule(self.marc, use_wasabi)
        self.speech_module = SpeechModule(use_mary)
        self.cog_module = CogModule()

    def play_wave(self, soundfile):
        ''' Plays a wave sound
        '''
        print 'play sound', soundfile
        def play():
            ''' Plays a sound as an extra thread
            '''
            # Windows:
            # path = 'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\'
            # winsound.PlaySound(path + '%s.wav' % soundfile,
            #                    winsound.SND_FILENAME)
            pygame.init()
            pygame.mixer.set_num_channels(1)
            pygame.mixer.music.load('sounds/' + soundfile + '.wav')
            pygame.mixer.music.play()

        #thread = Thread(target=play, args=())
        #thread.start()

    def introduce(self):
        ''' The agents reaction at the beginning of the training

            The agent introduces the human solver to the experiment, explaining
            the rules of the task.

        '''
        self.emo_module.start_hearing()
        emotion = self.emo_module.get_primary_emotion()
        speech = self.speech_module.introduce(emotion)

        if self.marc:
            self.marc.speak(speech)
        else:
            self.play_wave(speech.name)

        return (emotion.name, speech.text)

    def present(self, task):
        ''' The agent presents a single task.

        '''
        emotion = self.emo_module.get_primary_emotion()
        speech = self.speech_module.present(task, emotion)

        if self.marc:
            self.marc.speak(speech)
        else:
            self.play_wave(speech.name)

        return ('None', speech.text)

    def evaluate(self, task):
        ''' The agents reaction to an answer by the user.

            The agent evalutates the solution given by the human solver and
            shows an emotional and verbal reaction.The reaction depends on the
            feedback of the cognitive (= surprise) and emotional (= mood)
            modules.

        '''
        correct = task.last_trial()[0]
        surprise = self.cog_module.check(task)
        # TODO: Remove old check method
        self.emo_module.check2(task)
        emotion = self.emo_module.get_primary_emotion()
        speech = self.speech_module.evaluate(correct, surprise, emotion)

        if self.marc:
            self.marc.speak(speech)
        else:
            self.play_wave(speech.name)

        return (emotion.name + " " + str(emotion.impulse), speech.text)

    def end(self, tasks):
        ''' The Agents output at the end of the training.

            The Agent gives feedback for the whole test telling how many tasks
            have been done wrong.

        '''
        total_misses = 0
        for task in tasks:
            total_misses += task.misses()

        emotion = self.emo_module.get_primary_emotion()
        speech = self.speech_module.end(total_misses, emotion)

        if self.marc:
            self.marc.speak(speech)
        else:
            self.play_wave(speech.name)
        return ("None", speech.text)



class ListAgent:

    def __init__(self, use_marc, use_wasabi, use_mary):
        self.marc = None
        if use_marc:
            self.marc = Marc()
        self.emo_module = EmoModule(self.marc, use_wasabi)
        self.speech_module = SpeechModule(use_mary)
        self.cog_module = CogModule()

    def play_wave(self, soundfile):
        ''' Plays a wave sound
        '''
        def play():
             #Windows:
             path = 'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\'
             winsound.PlaySound(path + '%s.wav' % soundfile,
                                 winsound.SND_FILENAME)

        self.thread = Thread(target=play, args=())
        self.thread.start()
#        QSound.play('sounds/' + soundfile + '.wav')
#        pygame.init()
#        pygame.mixer.set_num_channels(1)
#        pygame.mixer.music.load('sounds/' + soundfile + '.wav')
#        pygame.mixer.music.play()


    def start(self):
        ''' The agents reaction at the beginning of the training

            The agent introduces the human solver to the experiment, explaining
            the rules of the task.

        '''
        self.emo_module.start_hearing()
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
        # cognitive evaluation: Determines surprise and intensity of emotion
        surprise = self.cog_module.react(correct, word.times)

        # emotional evaluation:
        emotion = self.emo_module.check(correct, surprise)

        verbal_output = '...'
        if not correct:
            speech = self.speech_module.react(surprise, emotion, word.word)
            self.speak(speech)
            verbal_output = speech.text

        return (str(emotion), '...', verbal_output)

    def wait(self, word):
        ''' Wait for user input and return the current emotion
        '''
        emotion = self.emo_module.get_primary_emotion()
        expectation = self.cog_module.expectation(word)
        return (str(emotion.name), expectation, '...')

''' The module to manage the verbal action of the agent.
'''
import urllib2
import wave
from emomodule import Emotion

class Speech:
    ''' A class for some spoken text. Generates the spoken text via Open Mary
    '''
    def __init__(self, name, text):
        self.name = name
        self.text = text
        #if MARY:
        #    tts = TextToSpeech()
        #    tts.save(name, text)

    def get_bml_code(self):
        ''' Return the bml code of the text
        '''
        return "<bml id=\"Perform{0}\"> \
               <marc:fork id=\"Track_0_fork_2\"> \
               <wait duration=\"0.00\" /> \
               <speech id=\"bml_item_2\" \
                marc:file=\"" + PATH + "{1}.wav\" marc:articulate=\"0.4\" /> \
               </marc:fork></bml>".format(self.name, self.name)

class TextToSpeech:
    ''' Class for text to speech support via Open Mary
    '''
    def __init__(self, ip_addr, voice, path):
        self.ip_addr = ip_addr
        self.voice = voice
        self.path = path

    def voices(self):
        ''' Sends a request for available voices
        '''
        received = urllib2.urlopen(self.ip_addr + 'voices')
        data = received.read()
        print 'voices:'
        print data

    def save(self, name, text):
        ''' text must have the form of single words connected via '+'
            Example: Hello+world

            dfki-obadiah\%20en_GB male\%20unitselection\%20general
        '''
        text = text.replace(' ', '+')
        query = self.ip_addr + 'process?INPUT_TEXT=' \
                + text \
                + '&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO\
                   &AUDIO=WAVE_FILE&LOCALE=en_US&VOICE=' + self.voice

        received = urllib2.urlopen(query)
        data = received.read()
        wav = wave.open("sounds\\" + name + ".wav", 'w')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        #wav.setframerate(48000)
        wav.writeframes(data)
        wav.close()


class SpeechModule:
    ''' The class to manage the verbal activity of the agent.

        This is the only class / section in code where the verbal output of the
        agent is defined.
    '''
    def __init__(self):
        self.tts = None

    def enable_open_mary(self, ip_addr, voice, path):
        ''' Enables open mary
        '''
        self.tts = TextToSpech(ip_addr, voice, path)


    def get_verbal_reaction(self, correct, surprise, emotion, intense):
        ''' Returns the verbal reaction of the answer given by the user
        '''
        reaction = ""
        if surprise == "[very surprised]":
            reaction += "Unbelievable! "
        elif surprise == "[surprised]":
            reaction += "Oh! "
        if correct and emotion == Emotion.JOY and intense > 50:
            reaction += "Absolutely correct! You are doing a fantastic job!"
        elif correct and emotion == Emotion.JOY and intense > 10:
            reaction += "Well done my friend, your answer is correct."
        elif correct and emotion == Emotion.JOY:
            reaction += "Allright, your answer is correct."
        elif not correct and emotion == Emotion.JOY:
            reaction += "Your answer is wrong."
        elif not correct and emotion == Emotion.ANGER and intense > -50:
            reaction += "No, that's definitely not the right answer."
        elif not correct and emotion == Emotion.ANGER:
            reaction += "What are you doing? Your answer is really annoying!"
        else:
            reaction += "Wrong emotion or surprise" + emotion + " " + Emotion.JOY
        return reaction

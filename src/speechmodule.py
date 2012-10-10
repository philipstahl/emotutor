''' The module to manage the verbal action of the agent.
'''
import urllib2
import wave
from emomodule import Happy, Angry

class Speech:
    ''' A class for some spoken text. Generates the spoken text via Open Mary
    '''
    def __init__(self, name, text, tts=None):
        self.name = name
        self.text = text
        self.tts = tts
        if tts:
            tts.save(name, text)

    def get_bml_code(self):
        ''' Return the bml code of the text
        '''
        return "<bml id=\"Perform{0}\"> \
               <marc:fork id=\"Track_0_fork_2\"> \
               <wait duration=\"0.00\" /> \
               <speech id=\"bml_item_2\" \
                marc:file=\"" + self.tts.path \
                + "{1}.wav\" marc:articulate=\"0.4\" /> \
               </marc:fork></bml>".format(self.name, self.name)

class OpenMary:
    ''' Class for text to speech support via Open Mary
    '''

    IP = 'http://localhost:59125/'
    VOICE = 'dfki-obadiah'
    PATH = 'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\'

    def __init__(self):
        pass

    def voices(self):
        ''' Sends a request for available voices
        '''
        received = urllib2.urlopen(OpenMary.IP + 'voices')
        print 'voices:', received.read()

    def save_from_text(self, name, text):
        ''' text must have the form of single words connected via '+'
            Example: Hello+world

        '''
        text = text.replace(' ', '+')
        query = OpenMary.IP + 'process?INPUT_TEXT=' \
                + text \
                + '&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO' \
                + '&AUDIO=WAVE_FILE&LOCALE=en_US&VOICE=' + OpenMary.VOICE
        print "REQUEST OPEN MARY: ", query
        received = urllib2.urlopen(query)
        data = received.read()
        wav = wave.open("sounds\\" + name + ".wav", 'w')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        #wav.setframerate(48000)
        wav.writeframes(data)
        wav.close()

    def save_from_xml(self, name, text, emotion):
        ''' Sends a request in RAWMARYXML.

            emotions can be:
            neutral, poker, happy, angry, sad

        '''
        name = "emo_text"
        text = "<maryxml%20version=\"0.5\"%20xmlns=\"http:" \
             + "//mary.dfki.de/2002/MaryXML\"%20xml:lang=\"de\">" \
             + "<voice%20name=\"dfki-pavoque-styles\">" \
             + "<prosody%20style=\"" + emotion + "\">" + text \
             + "</prosody></voice></maryxml>"

        query = OpenMary.IP + 'process?INPUT_TEXT=' \
                + text \
                + '&INPUT_TYPE=RAWMARYXML&OUTPUT_TYPE=AUDIO' \
                + '&AUDIO=WAVE_FILE&LOCALE=en_US&VOICE=' + OpenMary.VOICE

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
    def __init__(self, use_mary=False):
        self.tts = None
        if use_mary:
            self.tts = OpenMary()

    def introduce(self):
        ''' The agents reaction at the beginning of the training

            The agent introduces the human solver to the experiment, explaining
            the rules of the task.

        '''
        return Speech("introduction", "Welcome to your vocabulary session.",
                      self.tts)

    def present(self, task):
        ''' The agent present a task
        '''
        speech = Speech("task", "What is the german word for " + task.question
                                + "?", self.tts)
        return speech

    def evaluate(self, correct, surprise, emotion):
        ''' Returns the verbal reaction of the answer given by the user
        '''
        reaction = ""
        if surprise == "[very surprised]":
            reaction += "Unbelievable! "
        elif surprise == "[surprised]":
            reaction += "Oh! "
        if correct and type(emotion) == Happy and emotion.impulse > 50:
            reaction += "Absolutely correct! You are doing a fantastic job!"
        elif correct and type(emotion) == Happy and emotion.impulse > 10:
            reaction += "Well done my friend, your answer is correct."
        elif correct and type(emotion) == Happy:
            reaction += "Allright, your answer is correct."
        elif not correct and type(emotion) == Happy:
            reaction += "Your answer is wrong."
        elif not correct and type(emotion) == Angry \
                 and emotion.impulse > -50:
            reaction += "No, that's definitely not the right answer."
        elif not correct and type(emotion) == Angry:
            reaction += "What are you doing? Your answer is really annoying!"
        else:
            reaction += "Wrong emotion or surprise" + emotion.name
        return Speech('reaction', reaction, self.tts)

    def end(self, misses):
        ''' Returns the agents verbalk output at the end of the training
        '''
        return Speech("end", "Test finished. \
                        You had {0} misses in total.".format(str(misses)),
                        self.tts)

if __name__ == '__main__':
    import sys
    voice = 'dfki-pavoque-styles'
    #voice = 'dfki-obadiah'
    ip_addr = 'http://localhost:59125/'
    path = 'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\'

    #if len(sys.argv) > 1:
    mary = OpenMary()
    mary.save_from_xml('emo_test', 'Das ist eine schoene Blume', 'happy')
    print 'saved'

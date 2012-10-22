''' The module to manage the verbal action of the agent.
'''
import urllib2
import wave
from emomodule import Happy, Angry, Annoyed, Concentrated, Bored


class Speech:
    ''' A class for some spoken text. Generates the spoken text via Open Mary
    '''
    def __init__(self, name, text, emotion):
        self.text = text
        self.emotion = 'neutral'
        if emotion.NAME == Happy.NAME:
            self.emotion = 'happy'
        if emotion.NAME == Annoyed.NAME:
            self.emotion = 'sad'
        if emotion.NAME == Angry.NAME:
            self.emotion = 'angry'
        self.name = name + '_' + self.emotion


    def get_bml_code(self):
        ''' Return the bml code of the text
        '''
        return "<bml id=\"Perform{0}\"> \
               <marc:fork id=\"Track_0_fork_2\"> \
               <wait duration=\"0.00\" /> \
               <speech id=\"bml_item_2\" \
                marc:file=\"" + OpenMary.PATH \
                + "{1}.wav\" marc:articulate=\"0.4\" /> \
               </marc:fork></bml>".format(self.name, self.name)


class OpenMary:
    ''' Class for text to speech support via Open Mary
    '''

    IP = 'http://localhost:59125/'
    VOICE = 'dfki-pavoque-styles'
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
        query = OpenMary.IP + 'process?INPUT_TEXT=' \
                + text \
                + '&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO' \
                + '&AUDIO=WAVE_FILE&LOCALE=en_US&VOICE=' + OpenMary.VOICE
        received = urllib2.urlopen(query)
        data = received.read()
        wav = wave.open("sounds\\" + name + ".wav", 'w')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(data)
        wav.close()

    def save_from_xml(self, speech):
        ''' Sends a request in RAWMARYXML.

            emotions can be:
            neutral, poker, happy, angry, sad

        '''
        print 'save', speech.name, speech.emotion
        text = speech.text.replace(' ', '+')
        request = "<maryxml%20version=\"0.5\"%20xmlns=\"http:" \
                + "//mary.dfki.de/2002/MaryXML\"%20xml:lang=\"de\">" \
                + "<voice%20name=\"dfki-pavoque-styles\">" \
                + "<prosody%20style=\"" + speech.emotion + "\">" + text \
                + "</prosody></voice></maryxml>"

        query = OpenMary.IP + 'process?INPUT_TEXT=' \
                + request \
                + '&INPUT_TYPE=RAWMARYXML&OUTPUT_TYPE=AUDIO' \
                + '&AUDIO=WAVE_FILE&LOCALE=en_US&VOICE=' + OpenMary.VOICE
        received = urllib2.urlopen(query)
        data = received.read()
        #wav = wave.open("sounds\\" + speech.name + ".wav", 'w')  # Windows
        wav = wave.open("sounds/" + speech.name + ".wav", 'w')  # Linux
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.setnframes(40000)
        wav.writeframesraw(data)
        wav.close()
        print 'wav file written'


class SpeechModule:
    ''' The class to manage the verbal activity of the agent.

        This is the only class / section in code where the verbal output of the
        agent is defined.
    '''

    def __init__(self, use_mary=False):
        self.tts = None
        if use_mary:
            self.tts = OpenMary()

    def introduce(self, emotion):
        ''' The agents reaction at the beginning of the training

            The agent introduces the human solver to the experiment, explaining
            the rules of the task.

        '''

        speech = Speech("introduction", "Willkommen+zum+Vokabel+Test", emotion)
        if self.tts:
            self.tts.save_from_xml(speech)
        return speech

    def present(self, task, emotion):
        ''' The agent present a task
        '''
        speech = Speech("task", "Was ist das englische Wort fuer " + task.question
                                + "?", emotion)
        if self.tts:
            self.tts.save_from_xml(speech)

        return speech

    def evaluate(self, correct, surprise, emotion):
        ''' Returns the verbal reaction of the answer given by the user
        '''
        reaction = ""
        print 'SPEECHMODULE: EVALUATE:', correct, surprise, emotion.NAME

        if correct and emotion.NAME == Happy.NAME:
            reaction += "Super gemacht! Deine Antwort ist richtig."
        elif correct and emotion.NAME == Concentrated.NAME:
            reaction += "Genau. Deine Antwort ist richtig."
        elif correct and emotion.NAME == Bored.NAME:
            reaction += "Deine Antwork ist richtig."
        elif correct and emotion.NAME == Annoyed.NAME:
            reaction += "Deine Antwork ist richtig."
        elif correct and emotion.NAME == Angry.NAME:
            reaction += "Ja deine Antwort ist richtig."
        elif not correct and emotion.NAME == Happy.NAME:
            reaction += "Halb so schlimm. Kann ja mal passieren."
        elif not correct and emotion.NAME == Concentrated.NAME:
            reaction += "Deine Antwort ist leider falsch."
        elif not correct and emotion.NAME == Bored.NAME:
            reaction += "Deine Antwork ist falsch"
        elif not correct and emotion.NAME == Annoyed.NAME:
            reaction += "Schade. Deine Antwort ist falsch."
        elif not correct and emotion.NAME == Angry.NAME:
            reaction += "Unfassbar. Wie kannst Du das nicht wissen?"
        else:
            reaction += "Wrong emotion or surprise" + emotion.name

        speech = Speech('reaction', reaction, emotion)
        if self.tts:
            self.tts.save_from_xml(speech)

        return speech

    def end(self, misses, emotion):
        ''' Returns the agents verbalk output at the end of the training
        '''
        return Speech("end", "Test finished. \
                        You had {0} misses in total.".format(str(misses)),
                        emotion)

if __name__ == '__main__':
    import sys
    voice = 'dfki-pavoque-styles'
    #voice = 'dfki-obadiah'
    ip_addr = 'http://localhost:59125/'
    path = 'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\'


    OpenMary.VOICE = voice
    OpenMary.PATH = path
    #if len(sys.argv) > 1:
    mary = OpenMary()
    speech = Speech('emo_happy', 'Willkommen zum Vokabel Test', Concentrated())
    #mary.save_from_xml('emo_neutral', 'Willkommen+zum+Vokabel+Test', 'neutral')
    mary.save_from_xml(speech)
    #mary.save_from_xml('emo_angry', 'Willkommen+zum+Vokabel+Test', 'angry')
    #mary.save_from_xml('emo_sad', 'Willkommen+zum+Vokabel+Test', 'sad')
    #mary.save_from_xml('emo_poker', 'Willkommen+zum+Vokabel+Test', 'poker')
    print 'saved'

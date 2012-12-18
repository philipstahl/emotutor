# -*- coding: iso-8859-1 -*-

''' The module to manage the verbal action of the agent.
'''
import urllib2
import wave
#from emomodule import Happy, Angry, Annoyed, Concentrated, Bored

''' BML CODE:

<bml id="Track_0">
      <marc:fork id="Track_0_fork_1">
            <wait duration="0.6" />
            <speech  id="bml_item_2"  marc:synthesizer="OpenMary"  marc:voice="dfki-pavoque-styles"  marc:options=""  marc:f0_shift="0.0"  marc:locale="de"  text="Hallo und herzlich Willkommen." />
      </marc:fork>
</bml>

'''


class Speech:
    ''' A class for some spoken text. Generates the spoken text via Open Mary
    '''
    def __init__(self, name, text, emotion):
        self.text = text
        self.emotion = 'neutral'
        if emotion:
            if emotion.name == 'happy':
                self.emotion = 'happy'
            if emotion.name == 'annoyed':
                #self.emotion = 'sad'
                self.emotion = 'angry'
            if emotion.name == 'angry':
                self.emotion = 'angry'
        self.name = name + '_' + self.emotion

    def get_bml_code(self):
        ''' Return the bml code of the text
        '''
        return '<bml id="Track_0"> \
                <marc:fork id="Track_0_fork_1"> \
                <speech  id="bml_item_2"  marc:synthesizer="OpenMary"\
                 marc:voice="dfki-pavoque-styles"  marc:options=""  \
                 marc:f0_shift="0.0"  marc:locale="de"  \
                 marc:style="' + self.emotion + '"\
                 text="' + self.text + '" />\
                <marc:subtitles id="bml_item_3" align="DOWN" duration="5.0">' \
                  + self.text + '</marc:subtitles> \
                </marc:fork></bml>'


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
        text = speech.text.replace(' ', '+')
        text = text.replace('ä', '%C3%A4')
        text = text.replace('ö', '%C3%B6')
        text = text.replace('ü', '%C3%BC')

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
        wav = wave.open("sounds\\" + speech.name + ".wav", 'w')  # Windows
        #wav = wave.open("sounds/" + speech.name + ".wav", 'w')  # Linux
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.setnframes(40000)
        wav.writeframesraw(data)
        wav.close()


class SpeechModule:
    ''' The class to manage the verbal activity of the agent.

        This is the only class / section in code where the verbal output of the
        agent is defined.
    '''

    def __init__(self, logger):
        self.logger = logger
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
        speech = Speech("task", "Was ist das englische Wort fuer "
                                + task.question + "?", emotion)
        if self.tts:
            self.tts.save_from_xml(speech)

        return speech

    def evaluate(self, correct, surprise, emotion):
        ''' Returns the verbal reaction of the answer given by the user
        '''
        reaction = ""

        if correct and emotion.name == 'happy':
            reaction += "Super gemacht! Deine Antwort ist richtig."
        elif correct and emotion.name == 'concentrated':
            reaction += "Genau. Deine Antwort ist richtig."
        elif correct and emotion.name == 'bored':
            reaction += "Deine Antwork ist richtig."
        elif correct and emotion.name == 'annoyed':
            reaction += "Deine Antwork ist richtig."
        elif correct and emotion.name == 'angry':
            reaction += "Ja deine Antwort ist richtig."
        elif not correct and emotion.name == 'happy':
            reaction += "Halb so schlimm. Kann ja mal passieren."
        elif not correct and emotion.name == 'concentrated':
            reaction += "Deine Antwort ist leider falsch."
        elif not correct and emotion.name == 'bored':
            reaction += "Deine Antwork ist falsch"
        elif not correct and emotion.name == 'annoyed':
            reaction += "Schade. Deine Antwort ist falsch."
        elif not correct and emotion.name == 'angry':
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

    def start_list(self, emotion):
        ''' The agents reaction at the beginning of the training
        '''

        speech = Speech("introduction", "Willkommen zum Lernen von Wortpaaren.",
                        emotion)
        #if self.tts:
        #    self.tts.save_from_xml(speech)
        return speech

    def get_text(self, text):
        return Speech("text", text, None)


    def present_list(self, emotion):
        ''' Formulates the task of memorizing a list of words.
        '''
        speech = Speech('present_list', 'Bitte merken Sie sich die folgenden '
                                    + 'Wörter, in der Reihenfolge in der ich '
                                    + 'sie vorlese.', emotion)
        #if self.tts:
        #    self.tts.save_from_xml(speech)

        return speech

    def present_word(self, word, emotion):
        speech = Speech('word', word.word, emotion)
        #if self.tts:
        #    self.tts.save_from_xml(speech)
        return speech

    def react(self, emotion, word):

        reaction = ''
        if not emotion or emotion.name == 'concentrated' or emotion.name == 'bored' \
             or emotion.name == 'annoyed':
            reaction += 'Nein. Richtig wäre ' + word
        elif emotion.name == 'happy':
            reaction += ('Leider nein. Kann jedem passieren. Richtig wäre '
                        + word)
        elif emotion.name == 'angry':
            reaction += 'Nein natürlich nicht! An die Stelle kommt ' + word

        speech = Speech('reaction', reaction, emotion)
        #if self.tts:
        #    self.tts.save_from_xml(speech)

        return speech




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

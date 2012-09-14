import urllib2
import wave


class TextToSpeach:
    def __init__(self):
        pass

    def voices(self):
        f = urllib2.urlopen('http://localhost:59125/voices')
        data = f.read()
        print 'voices:'
        print data

        
    ''' text must have the form of single words connected via '+'
        Example: Hello+world

        dfki-obadiah\%20en_GB male\%20unitselection\%20general
    '''
    def save(self, name, text):
        text = text.replace(' ', '+')
        query = 'http://localhost:59125/process?INPUT_TEXT=' \
                + text \
                + '&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&AUDIO=WAVE_FILE&LOCALE=en_US&VOICE=dfki-obadiah'
                
        print query
        f = urllib2.urlopen(query)
        data = f.read()
        wav = wave.open("sounds\\" + name + ".wav", 'w')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        #wav.setframerate(48000)
        wav.writeframes(data)
        wav.close()

tts = TextToSpeach()
tts.save("positive_right", "Well done!")
tts.save("neutral_right", "You have choosen the right answer.")
tts.save("neutral_wrong", "Your answer is wrong")
tts.save("negative_wrong", "Annoying. That is not the correct answer!")
print "done"

tts.voices()

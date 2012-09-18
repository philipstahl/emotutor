from tts import TextToSpeech
from globalsettings import *

class Speech:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        if MARY:
            tts = TextToSpeech()
            tts.save(name, text)

    def getBMLCode(self):
        return "<bml id=\"Perform{0}\"> \
               <marc:fork id=\"Track_0_fork_2\"> \
               <wait duration=\"0.00\" /> \
               <speech id=\"bml_item_2\"  marc:file=\"C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\{1}.wav\" marc:articulate=\"0.4\" /> \
               </marc:fork></bml>".format(self.name, self.name)


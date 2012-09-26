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
               <speech id=\"bml_item_2\" \
                marc:file=\"" + PATH + "{1}.wav\" marc:articulate=\"0.4\" /> \
               </marc:fork></bml>".format(self.name, self.name)

class SpeechModule:
    def __init__(self):
        pass

    def get_verbal_reaction(self, correct, surprise, emotion, intense):
        reaction = ""
        if surprise == "[very surprised]":
            reaction += "Unbelievable! "
        elif surprise == "[surprised]":
            reaction += "Oh! "
        if correct and emotion == "happy" and intense > 50:
            reaction += "Absolutely correct! You are doing a fantastic job!"
        elif correct and emotion == "happy" and intense > 10:
            reaction += "Well done my friend, your answer is correct."
        elif correct and emotion == "happy":
            reaction += "Allright, your answer is correct."
        elif not correct and emotion == "happy":
            reaction += "Your answer is wrong."
        elif not correct and emotion == "angry" and intense > -50:
            reaction += "No, that's definitely not the right answer."
        elif not correct and emotion == "angry":
            reaction += "What are you doing? Your answer is really annoying!"
        else:
            reaction += "Wrong mood or surprise"
        return reaction

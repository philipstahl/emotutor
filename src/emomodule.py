from wasabi import *

class Emotion:
    def __init__(self, name, impulse):
        self.name = name
        self.impulse = impulse


class EmoModule:

    ''' If WASABI is used, the emotional status of the agent is represented by
        the WASABI model.
        Otherwise the agent shows only direct emotional reactions and does not
        have an overduring emotional model.
    '''
    def __init__(self, marc = None):
        self.marc = marc
        if WASABI:
            self.wasabi = Wasabi(self.marc)
            self.wasabi.start_hearing()

    ''' task evaluation according to the emotional reaction
    '''
    def check(self, task):
        correct, time = task.last_trial()
        emotion = None
        if correct and time < 5 and task.misses() == 0:
            emotion = Emotion('happy', 100)
        elif correct and time < 5:
            emotion = Emotion('happy', 50)
        elif correct:
            emotion = Emotion('happy', 10)
        elif not correct and task.misses() < 2:
            emotion = Emotion('angry', -50)
        else:
            emotion = Emotion('angry', -100)

        if WASABI:
            self.wasabi.send(emotion.name, emotion.impulse)
            current_emo, current_imp = wasabi.get_primary_emotion()
            return Emotion(current_emo, current_imp)
        else:
            return emotion

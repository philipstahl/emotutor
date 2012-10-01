''' The emotion module

    Contains class definitions for all available emotions and the emotional
    module which manages all emotional reactions.
'''

from wasabi import Wasabi

class Emotion:

    JOY = 'JOY'
    ANGER = 'ANGER'
    RELAX = 'RELAX'

    WASABI_JOY = 'happy'
    WASABI_ANGER = 'angry'
    WASABI_RELAX = 'happy'

    MARC_JOY = "CASA_Joy_01"
    MARC_RELAX = "CASA_Relax_01"
    MARC_ANGER = "CASA_Anger_01"

    ''' Class for representing a single Emotion

        Emotion matching: Every emotion has a
        - intern name
        - a name in MARC
        - a name in WASABI
        The intern name is used in the source code.

    '''
    def __init__(self, name, wait=0.0, impulse=100,
                 interpolate=1.0):
        self.name = name
        self.wait = wait
        self.impulse = impulse
        self.intensity = float(impulse) / 100
        if self.intensity < 0:
            self.intensity = self.intensity * -1
        self.interpolate = interpolate
        print 'joy:', Emotion.MARC_JOY

    def get_bml_code(self):
        #TODO use marc names here
        ''' Returns the BML Code of the emotion, for showing in MARC
        '''
        return "<bml id=\"Perform{0}\"> \
                <marc:fork id=\"Show_{1}_fork_1\"> \
                <wait duration=\"{2}\" /> \
                <face id=\"bml_item_2\" > \
                <description level=\"1\" type=\"marcbml\"> \
                <facial_animation name=\"{3}\" \
                    interpolate=\"{4}\" \
                    loop=\"false\"  \
                    intensity=\"{5}\" /> \
                </description> </face> </marc:fork> \
                </bml>".format(self.name, self.name, self.wait, self.name,
                               self.interpolate, self.intensity)

    def __repr__(self):
        return self.name + ": " + str(self.impulse)


class Anger(Emotion):
    ''' Class for an anger emotion
    '''
    def __init__(self, impulse = 100):
        Emotion.__init__(self, Emotion.ANGER, impulse = impulse)

class Joy(Emotion):
    ''' Class for an joy emotion
    '''
    def __init__(self, impulse = 100):
        Emotion.__init__(self, Emotion.JOY, impulse = impulse)

class Relax(Emotion):
    ''' Class for an relax emotion
    '''
    def __init__(self, impulse = 100):
        Emotion.__init__(self, Emotion.RELAX, impulse = impulse)


class EmoModule:
    ''' If WASABI is used, the emotional status of the agent is represented by
        the WASABI model.
        Otherwise the agent shows only direct emotional reactions and does not
        have an overduring emotional model.
    '''
    def __init__(self):
        self.wasabi = None
        pass

    def enable_wasabi(self, ip, port_in, port_out, marc = None):
        ''' The emotion module uses wasabi to simulate the emotion status
        '''
        self.wasabi = Wasabi(ip, port_in, port_out, marc)
        self.wasabi.start_hearing()

    def check(self, task):
        ''' Task evaluation according to the emotional reaction
        '''
        correct, time = task.last_trial()
        emotion = None
        if correct and time < 5 and task.misses() == 0:
            emotion = Joy(100)
        elif correct and time < 5:
            emotion = Joy(50)
        elif correct:
            emotion = Joy(10)
        elif not correct and task.misses() < 2:
            emotion = Anger(-50)
        else:
            emotion = Anger(-100)

        if self.wasabi:
            self.wasabi.send(emotion.name, emotion.impulse)
            current_emo, current_imp = self.wasabi.get_primary_emotion()
            if current_emo == Wasabi.JOY:
                return Joy(current_imp)
            if current_emo == WASABI.Anger:
                return Anger(current_imp)
        else:
            return emotion

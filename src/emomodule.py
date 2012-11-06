''' The emotion module

    Contains class definitions for all available emotions and the emotional
    module which manages all emotional reactions.
'''

import socket
from threading import Thread
import math

class Emotion:
    ''' Class for representing a single Emotion

    '''
    def __init__(self, name, marc, impulse=100, adjust=1, interpolate=1.0,
                 frequence=2):
        self.name = name
        self.marc = str(marc)
        self.impulse = int(impulse)
        self.frequence = int(frequence)
        self.intensity = float(impulse) / 100 * adjust
        self.interpolate = float(interpolate)

    def get_bml_code(self):
        ''' Returns the BML Code of the emotion, for showing in MARC
        '''
        #print 'send', self.__repr__()
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
                </bml>".format(self.marc, self.marc, 0, self.marc,
                               self.interpolate, float(self.impulse) / 100)

    def __repr__(self):
        return self.name + ' ' + str(self.impulse) + ' ' + str(self.intensity)

class Happy(Emotion):
    ''' Class for an happy emotion
    '''
    NAME = 'happy'
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, Happy.NAME, Happy.MARC,

                         impulse = impulse, adjust = Happy.INTENSE,
                         interpolate = Happy.INTERPOLATE,
                         frequence = Happy.FREQUENCE)


class Concentrated(Emotion):
    ''' Class for a concentrated emotion
    '''
    NAME = 'concentrated'
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, Concentrated.NAME, Concentrated.MARC,
                         impulse = impulse, adjust = Concentrated.INTENSE,
                         interpolate = Concentrated.INTERPOLATE,
                         frequence = Concentrated.FREQUENCE)


class Bored(Emotion):
    ''' Class for a bored emotion
    '''
    NAME = 'bored'
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, Bored.NAME, Bored.MARC, impulse = impulse, adjust = Bored.INTENSE,
                         interpolate = Bored.INTERPOLATE,
                         frequence = Bored.FREQUENCE)


class Annoyed(Emotion):
    ''' Class for an annoyed emotion
    '''
    NAME = 'annoyed'
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, Annoyed.NAME, Annoyed.MARC, impulse = -impulse, adjust = -Annoyed.INTENSE,
                         interpolate = Annoyed.INTERPOLATE,
                         frequence = Annoyed.FREQUENCE)


class Angry(Emotion):
    ''' Class for an angry emotion
    '''
    NAME = 'angry'
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, Angry.NAME, Angry.MARC, impulse = -impulse, adjust = -Angry.INTENSE,
                         interpolate = Angry.INTERPOLATE,
                         frequence = Angry.FREQUENCE)

class Surprise(Emotion):
    ''' Class for an angry emotion
    '''
    NAME = 'surprised'
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, string='high'):
        Emotion.__init__(self, Surprise.NAME, Surprise.MARC,
                         impulse = impulse, adjust = Surprise.INTENSE,
                         interpolate = Surprise.INTERPOLATE,
                         frequence = Surprise.FREQUENCE)
        self.string = string

    def string(self):
        return self.string


class EmoModule:
    ''' If WASABI is used, the emotional status of the agent is represented by
        the WASABI model.
        Otherwise the agent shows only direct emotional reactions and does not
        have an overduring emotional model.
    '''

    WASABI_IP = 'localhost'
    WASABI_PORT_IN = 0
    WASABI_PORT_OUT = 0


    SURPRISE_NEG_HIGH = 100             # Higly expected correct, got false
    SURPRISE_NEG_LOW = 50               # Expected correct, got false
    SURPRISE_NEG_NONE = 0               # Expected nothing, got false

    SURPRISE_POS_HIGH = 0              # Higly expected correct, got correct
    SURPRISE_POS_LOW = 50               # Expected correct, got correct
    SURPRISE_POS_NONE = 100             # Expected nothing, got correct


    REACT_NEG_HAPPY = ('Angry', 30, 60, 100)
    REACT_NEG_CONCENTRATED = ('Angry', 30, 60, 100)
    REACT_NEG_BORED = ('Angry', 30, 60, 100)
    REACT_NEG_ANNOYED = ('Angry', 30, 60, 100)
    REACT_NEG_ANGRY = ('Angry', 30, 60, 100)

    REACT_POS_HAPPY = ('Happy', 30, 60, 100)
    REACT_POS_CONCENTRATED = ('Happy', 30, 60, 100)
    REACT_POS_BORED = ('Happy', 30, 60, 100)
    REACT_POS_ANNOYED = ('Happy', 30, 60, 100)
    REACT_POS_ANGRY = ('Happy', 30, 60, 100)


    def __init__(self, marc=None, use_wasabi=False):
        self.marc = marc
        self.wasabi = None
        if use_wasabi:
            self.wasabi = WasabiListener(self.marc)
        self.last_emotion = Concentrated()

    def get_primary_emotion(self):
        ''' Returns the currently dominating emotion
        '''
        if self.wasabi:
            return self.wasabi.get_primary_emotion()
        return self.last_emotion


    def emotion_by_name(self, name, impulse=100):
        ''' Returns an emotion object with the given impulse.
        '''
        name = name.lower()
        name_to_emotion = {'happy': Happy, 'concentrated': Concentrated,
                           'bored': Bored, 'annoyed': Annoyed, 'angry': Angry}
        if name in name_to_emotion.keys():
            return name_to_emotion[name](impulse=impulse)
        else:
            print 'Wrong emotion name given'


    def check(self, correct, surprise):
        ''' Task evaluation according to the emotional reaction.

            Sends an emotional input to wasabi and text back to the agent
        '''
        #if surprise.impulse > 0:
            #if self.marc:
            #    self.marc.show(surprise)
            # TODO(How to send surprise to wasabi correct?)
            #if self.wasabi:
            #    self.send(surprise.NAME, int(surprise.impulse))

        pos_emotions = {'happy': EmoModule.REACT_POS_HAPPY,
                        'concentrated': EmoModule.REACT_POS_CONCENTRATED,
                        'bored': EmoModule.REACT_POS_BORED,
                        'annoyed': EmoModule.REACT_POS_ANNOYED,
                        'angry': EmoModule.REACT_POS_ANGRY}

        neg_emotions = {'happy': EmoModule.REACT_NEG_HAPPY,
                        'concentrated': EmoModule.REACT_NEG_CONCENTRATED,
                        'bored': EmoModule.REACT_NEG_BORED,
                        'annoyed': EmoModule.REACT_NEG_ANNOYED,
                        'angry': EmoModule.REACT_NEG_ANGRY}

        # get emotion:
        current = self.get_primary_emotion()
        reaction = None

        if correct:
            reaction = pos_emotions[current.NAME]
        else:
            reaction = neg_emotions[current.NAME]

        pos_impulses = [EmoModule.SURPRISE_POS_NONE, EmoModule.SURPRISE_POS_LOW, EmoModule.SURPRISE_POS_HIGH]
        neg_impulses = [EmoModule.SURPRISE_NEG_NONE, EmoModule.SURPRISE_NEG_LOW, EmoModule.SURPRISE_NEG_HIGH]
        # get intense:
        if correct:
            impulse = reaction[pos_impulses.index(surprise.impulse) + 1]
        else:
            impulse = reaction[neg_impulses.index(surprise.impulse) + 1]

        # create emotion here:
        emotion = self.emotion_by_name(reaction[0], impulse)

        self.last_emotion = emotion
        if self.wasabi:
            self.send(emotion.NAME, int(emotion.impulse))

        # TODO(How to wait here until first wasabi message is received?)
        return self.get_primary_emotion()


    def send(self, emotion, impulse):
        ''' Possible emotions are:
            happy, angry, annoyed, surprised, bored, sad, depressed, fearful
        '''
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print 'Send to wasabi', emotion, impulse

        message = "JohnDoe&TRIGGER&1&" + emotion
        sock_out.sendto(message, (EmoModule.WASABI_IP,
                                  EmoModule.WASABI_PORT_IN))

        message = "JohnDoe&IMPULSE&1&" + str(impulse)
        sock_out.sendto(message, (EmoModule.WASABI_IP,
                                  EmoModule.WASABI_PORT_IN))

    def start_hearing(self):
        ''' Starts the connectivity to WASABI.
        '''
        if self.wasabi:
            self.wasabi.start()

    def end_hearing(self):
        ''' Ends the connectivity to WASABI
        '''
        if self.wasabi:
            self.wasabi.end()


class WasabiListener():
    ''' Class for recieving input by WASABI

    '''

    def __init__(self, marc):
        self.marc = marc
        self.count = 0
        self.emo_status = {'happy': 0, 'concentrated': 0, 'depressed': 0,
                           'sad': 0, 'angry': 0, 'annoyed': 0, 'bored': 0}
        self.name_to_emo = {'angry': Angry, 'annoyed': Annoyed,
                              'bored': Bored,
                              'concentrated': Concentrated, 'happy': Happy,
                              'surprise': Surprise}
        self.hearing = False
        self.wait_for_message = False
        self.thread = None

    def start(self):
        ''' Starts the thread and waits for WASABI messages
        '''
        self.hearing = True
        def run():
            ''' Wait for wasabi messages. Everytime one is received, update
                current emotional status.
            '''
            sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock_in.bind((EmoModule.WASABI_IP, EmoModule.WASABI_PORT_OUT))

            while self.hearing:
                data = sock_in.recvfrom(1024)[0]
                self.update_emo_status(data)

        self.thread = Thread(target=run, args=())
        self.thread.start()

    def end(self):
        ''' Ends hearing for wasabi messages
        '''
        self.hearing = False

    def extract(self, data):
        ''' Extract data received from wasabi and returns a dict containing
            the emotion status for every current emotion
        '''
        # get the single emotion assignments
        values = data.split(" ")
        # remove eventually empty entries
        values = [val for val in values if val != ""]

        emotions = dict()
        for value in values:
            value = value.replace(' ', '')
            if len(value.split('=')) == 2:
                emotion = value.split('=')[0]
                # match float value to int value
                intensity = int(float(value.split('=')[1]) * 100)
                emotions[emotion] = intensity
            else:
                print 'strange', data, '-', value

        return emotions

    def get_primary_emotion(self):
        ''' Get dominating emotion:

        '''
        # TODO(wait here for next received message)
        #self.wait_for_message = True
        #while wait_for_message:
        #    pass

        primary_emo = ''
        highest_imp = 0
        for emotion in self.emo_status.keys():
            if math.fabs(self.emo_status[emotion]) >= math.fabs(highest_imp):
                primary_emo = emotion
                highest_imp = self.emo_status[emotion]
        if highest_imp == 0:
            primary_emotion = 'concentrated'
        return self.name_to_emo[primary_emo](impulse = highest_imp)

    def update_emo_status(self, data):
        ''' Gets a string of emotion values received from wasabi
            and updates the internal emotion dictionary

            1. Try: Always show dominating emotion
        '''
        # Update emotion status:
        current = self.extract(data)
        for emo in self.emo_status.keys():
            if emo in current.keys():
                self.emo_status[emo] = current[emo]
            else:
                self.emo_status[emo] = 0

        # Get dominating emotion:
        primary_emo = self.get_primary_emotion()
        emotion = self.name_to_emo[primary_emo.NAME]()

        # Send to MARC:
        if self.marc:
            if emotion.FREQUENCE <= self.count:
                self.count = 0
                self.marc.perform(emotion.name, emotion.get_bml_code())
            else:
                self.count += 1

    def print_emotions(self):
        ''' Prints the current emotion status
        '''
        output = ''
        for emotion in self.emo_status.keys():
            intensity = self.emo_status[emotion]
            if intensity != 0:
                output += emotion + '=' + str(intensity) + " "
        print output

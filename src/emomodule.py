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
    def __init__(self, name, impulse=100, interpolate=1.0, frequence=2):
        self.name = name
        self.wait = wait
        self.impulse = impulse
        self.intensity = float(impulse) / 100
        self.frequence = frequence
        if self.intensity < 0:
            self.intensity = self.intensity * -1
        self.interpolate = interpolate

    def get_bml_code(self):
        ''' Returns the BML Code of the emotion, for showing in MARC
        '''
        print 'send', str(self)
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
        return self.name + ": " + self.name + ' (' + str(self.impulse) + ',' \
                         + str(self.intensity) + ') ' + str(self.interpolate) \
                         + ' ' + str(self.frequence)


class Happy(Emotion):
    ''' Class for an happy emotion
    '''
    MARC = ''
    IMPULSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, interpolate = 1.0):
        Emotion.__init__(self, Happy.MARC, impulse = Happy.IMPULSE*impulse,
                         interpolate = Happy.INTERPOLATE*interpolate,
                         frequence = Happy.FREQUENCE)


class Concentrated(Emotion):
    ''' Class for a concentrated emotion
    '''
    MARC = ''
    IMPULSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, interpolate = 1.0):
        Emotion.__init__(self, Concentrated.MARC,
                         impulse = Concentrated.IMPULSE*impulse,
                         interpolate = Concentrated.INTERPOLATE*interpolate,
                         frequence = Concentrated.FREQUENCE)


class Bored(Emotion):
    ''' Class for a bored emotion
    '''
    MARC = ''
    IMPULSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, interpolate = 1.0):
        Emotion.__init__(self, Bored.MARC, impulse = Bored.IMPULSE*impulse,
                         interpolate = Bored.INTERPOLATE*interpolate,
                         frequence = Bored.FREQUENCE)


class Annoyed(Emotion):
    ''' Class for an annoyed emotion
    '''
    MARC = ''
    IMPULSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, interpolate = 1.0):
        Emotion.__init__(self, Annoyed.MARC, impulse = Annoyed.IMPULSE*impulse,
                         interpolate = Annoyed.INTERPOLATE*interpolate,
                         frequence = Annoyed.FREQUENCE)


class Angry(Emotion):
    ''' Class for an angry emotion
    '''
    MARC = ''
    IMPULSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, interpolate = 1.0):
        Emotion.__init__(self, Angry.MARC, impulse = Angry.IMPULSE*impulse,
                         interpolate = Angry.INTERPOLATE*interpolate,
                         frequence = Angry.FREQUENCE)

class Surprise(Emotion):
    ''' Class for an angry emotion
    '''
    MARC = ''
    IMPULSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, interpolate = 1.0):
        Emotion.__init__(self, Surprise.MARC, impulse = Surprise.IMPULSE*impulse,
                         interpolate = Surprise.INTERPOLATE*interpolate,
                         frequence = Surprise.FREQUENCE)


class EmoModule:
    ''' If WASABI is used, the emotional status of the agent is represented by
        the WASABI model.
        Otherwise the agent shows only direct emotional reactions and does not
        have an overduring emotional model.
    '''

    WASABI_IP = 'localhost'
    WASABI_PORT_IN = 0
    WASABI_PORT_OUT = 0

    def __init__(self, marc=None, use_wasabi=False):
        self.marc = marc
        self.wasabi = None
        if use_wasabi:
            self.wasabi = WasabiListener(EmoModule.WASABI_IP,
                                         EmoModule.WASABI_PORT_OUT, self.marc)

    def check(self, task):
        ''' Task evaluation according to the emotional reaction.

            Sends an emotional input to wasabi and text back to the agent
        '''
        correct, time = task.last_trial()
        emotion = None
        if correct and time < 5 and task.misses() == 0:
            emotion = Happy()
        elif correct and time < 5:
            emotion = Happy()
        elif correct:
            emotion = Happy()
        elif not correct and task.misses() < 2:
            emotion = Annoyed()
        else:
            emotion = Angry()

        if self.wasabi:
            self.send(emotion.name, emotion.impulse)

        return emotion

    def send(self, emotion, impulse):
        ''' Possible emotions are:
            happy, angry, annoyed, surprised, bored, sad, depressed, fearful
        '''
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        message = "JohnDoe&TRIGGER&1&" + emotion
        sock_out.sendto(message, (EmoModule.WASABI_IP,
                                  EmoModule.WASABI_PORT_OUT))

        message = "JohnDoe&IMPULSE&1&" + str(impulse)
        sock_out.sendto(message, (EmoModule.WASABI_IP,
                                  EmoModule.WASABI_PORT_OUT))

    def start_hearing(self):
        ''' Starts the connectivity to WASABI.
        '''
        self.wasabi.start()

    def end_hearing(self):
        ''' Ends the connectivity to WASABI
        '''
        self.wasabi.end()


class WasabiListener():
    ''' Class for recieving input by WASABI

    '''

    def __init__(self, marc):
        self.marc = marc
        self.count = 0
        self.emo_status = {'happy': 0, 'concentrated': 0, 'depressed': 0,
                           'sad': 0, 'angry': 0, 'annoyed': 0, 'bored': 0}
        self.hearing = False
        self.thread = None

    def start(self):
        ''' Starts the thread and waits for WASABI messages
        '''
        self.hearing = True
        def run(self):
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
        primary_emo = ''
        highest_imp = 0
        for emotion in self.emo_status.keys():
            if math.fabs(self.emo_status[emotion]) > math.fabs(highest_imp):
                primary_emo = emotion
                highest_imp = self.emo_status[emotion]
        print 'domoinating is ', primary_emo, ' with ', highest_imp

        emotion_names = {'angry': Angry, 'annoyed': Annoyed, 'bored': Bored,
                         'concentrated': Concentrated, 'happy': Happy,
                         'surprise': Surprise}
        emotion = emotion_names[primary_emo]()

        # Send to MARC:
        if self.marc:
            if emotion.FREQUENCE <= self.count:
                self.count = 0
                self.marc.preform(emotion.name, emotion.get_bml_code())
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

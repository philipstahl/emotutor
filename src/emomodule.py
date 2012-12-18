''' The emotion module

    Contains class definitions for all available emotions and the emotional
    module which manages all emotional reactions.
'''

import socket
from threading import Thread
import math
import utilities

class Emotion:
    ''' Class for representing a single Emotion

    '''
    def __init__(self, name, marc, impulse=100, adjust=1, interpolate=1.0,
                 frequence=2):
        self.name = name
        self.marc = str(marc)
        self.impulse = int(impulse)
        self.frequence = int(frequence)
        self.intensity = math.fabs(float(impulse) / 100 * adjust)
        self.interpolate = float(interpolate)

    def get_bml_code(self):
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
                </bml>".format(self.marc, self.marc, 0, self.marc,
                               self.interpolate, self.intensity)

    def __repr__(self):
        return self.name + ' ' + str(self.impulse) + ' ' + str(self.intensity)

class Happy(Emotion):
    ''' Class for an happy emotion
    '''
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, 'happy', Happy.MARC,
                         impulse = impulse, adjust = Happy.INTENSE,
                         interpolate = Happy.INTERPOLATE,
                         frequence = Happy.FREQUENCE)


class Concentrated(Emotion):
    ''' Class for a concentrated emotion
    '''
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, 'concentrated', Concentrated.MARC,
                         impulse = impulse, adjust = Concentrated.INTENSE,
                         interpolate = Concentrated.INTERPOLATE,
                         frequence = Concentrated.FREQUENCE)


class Bored(Emotion):
    ''' Class for a bored emotion
    '''
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, 'bored', Bored.MARC, impulse = impulse, adjust = Bored.INTENSE,
                         interpolate = Bored.INTERPOLATE,
                         frequence = Bored.FREQUENCE)


class Annoyed(Emotion):
    ''' Class for an annoyed emotion
    '''
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, 'annoyed', Annoyed.MARC, impulse = -impulse, adjust = -Annoyed.INTENSE,
                         interpolate = Annoyed.INTERPOLATE,
                         frequence = Annoyed.FREQUENCE)


class Angry(Emotion):
    ''' Class for an angry emotion
    '''
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, 'angry', Angry.MARC, impulse = -impulse, adjust = -Angry.INTENSE,
                         interpolate = Angry.INTERPOLATE,
                         frequence = Angry.FREQUENCE)

class Surprise(Emotion):
    ''' Class for an angry emotion
    '''
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100, string='high'):
        Emotion.__init__(self, 'surprised', Surprise.MARC,
                         impulse = impulse, adjust = Surprise.INTENSE,
                         interpolate = Surprise.INTERPOLATE,
                         frequence = Surprise.FREQUENCE)
        self.string = string

    def string(self):
        return self.string


class Hope(Emotion):
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, 'HOPE', Hope.MARC,
                         impulse = impulse, adjust = Hope.INTENSE,
                         interpolate = Hope.INTERPOLATE,
                         frequence = Hope.FREQUENCE)


class Fear(Emotion):
    MARC = ''
    INTENSE = 1.0
    INTERPOLATE = 1.0
    FREQUENCE = 2

    def __init__(self, impulse = 100):
        Emotion.__init__(self, 'fearful', Fear.MARC,
                         impulse = impulse, adjust = Fear.INTENSE,
                         interpolate = Fear.INTERPOLATE,
                         frequence = Fear.FREQUENCE)


class Relief(Emotion):
    def __init__(self):
        Emotion.__init__(self, name='RELIEF', marc='')


class FearsConfirmed(Emotion):
    def __init__(self):
        Emotion.__init__(self, name='FEARS-CONFIRMED', marc='')



class EmoModule:
    ''' If WASABI is used, the emotional status of the agent is represented by
        the WASABI model.
        Otherwise the agent shows only direct emotional reactions and does not
        have an overduring emotional model.
    '''

    WASABI_IP = 'localhost'
    WASABI_PORT_IN = 0
    WASABI_PORT_OUT = 0

    REACT_NEG_NONE = (False, 'None', 0)
    REACT_NEG_WRONG = (False, 'None', 0)
    REACT_NEG_RIGHT = (True, 'Happy', 80)
    REACT_NONE_NONE = (False, 'None', 0)
    REACT_NONE_WRONG = (False, 'None', -50)
    REACT_NONE_RIGHT = (False, 'None', 50)
    REACT_POS_NONE = (False, 'None', 0)
    REACT_POS_WRONG = (True, 'Angry', -80)
    REACT_POS_RIGHT = (False, 'None', 30)


    def __init__(self, marc=None, use_wasabi=False, logger=None):
        self.marc = marc
        self.logger = logger
        
        self.use_wasabi = use_wasabi
        self.wasabi = WasabiListener(self.marc, self.logger)

    def get_primary_emotion(self):
        ''' Returns the currently dominating emotion
        '''
        return self.wasabi.get_primary_emotion()

    def check(self, correct, expectation):
        ''' Task evaluation according to the emotional reaction.
            Sends an emotional input to wasabi and text back to the agent

            correct: correctness of the given answer: true / false
            expecation: of the answer before answer was given:
                        negative / none / positive
        '''
        emotion = 'None'
        impulse = 0

        reactions = {'negative': {1: EmoModule.REACT_NEG_RIGHT,
                                  0: EmoModule.REACT_NEG_WRONG,
                                  2: EmoModule.REACT_NEG_NONE},
                     'none': {1: EmoModule.REACT_NONE_RIGHT,
                              0: EmoModule.REACT_NONE_WRONG,
                              2: EmoModule.REACT_NONE_NONE},
                     'positive': {1:EmoModule.REACT_POS_RIGHT,
                                  0:EmoModule.REACT_POS_WRONG,
                                  2:EmoModule.REACT_POS_NONE}}
        surprise, emotion, impulse = reactions[expectation][correct]
        self.logger.log('  Reaction: surprise:{}, emotion={}, impulse={}'.format(surprise, emotion, impulse))
        
        if surprise:
            self.trigger(Surprise())

        if self.use_wasabi:
            if emotion != 'None':
                self.trigger(utilities.emotion_by_name(emotion))

            if impulse != 0:
                print 'IMPULSE IS NEG', impulse
                self.impulse(impulse)
        else:
            self.show_static_emotion(utilities.emotion_by_name(emotion, impulse))

        # TODO(How to wait here until first wasabi message is received?)
        return self.get_primary_emotion()


    def impulse(self, impulse):
        ''' Send the given impulse to wasabi.
        '''
        self.logger.log('  Wasabi: Impulse {}'.format(impulse))
        self.send_to_wasabi("JohnDoe&IMPULSE&1&" + str(impulse))

    def trigger(self, emotion):
        ''' Trigger the given emotion in wasabi.
        '''
        self.logger.log('  Wasabi: Trigger {}'.format(emotion.name))
        self.send_to_wasabi("JohnDoe&TRIGGER&1&" + emotion.name)

    def send_to_wasabi(self, message):
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_out.sendto(message, (EmoModule.WASABI_IP,
                                  EmoModule.WASABI_PORT_IN))

    def show_static_emotion(self, emotion):
        if emotion:
            self.logger.log('Show static emotion {} {}'.format(emotion.name, emotion.impulse))
            self.wasabi.show_static_emotion(emotion)

    def start_expressing(self):
        self.wasabi.clear_static_emotion()
        self.wasabi.start_expressing()

    def start_hearing(self):
        ''' Starts the connectivity to WASABI.
        '''
        self.wasabi.start()

    def end_hearing(self):
        ''' Ends the connectivity to WASABI
        '''
        self.wasabi.end()

    def is_dynamic(self):
        if self.wasabi.expressing:
            return True
        return False


class WasabiListener():
    ''' Class for recieving input by WASABI

    '''
    def __init__(self, marc, logger):
        self.marc = marc
        self.logger = logger
        self.count = 0
        self.emo_status = {'happy': 0, 'concentrated': 0, 'depressed': 0,
                           'sad': 0, 'angry': 0, 'annoyed': 0, 'bored': 0}
        self.hearing = False
        self.expressing = False
        self.static_emotion = None

        self.dominating_emo = None

        self.log_wasabi=False

        self.thread = None

    def start(self):
        ''' Starts the thread and waits for WASABI messages
        '''
        print 'Listener started'
        self.hearing = True
        def run():
            ''' Wait for wasabi messages. Everytime one is received, update
                current emotional status.
            '''
            print 'THREAD STARTET'
            sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #sock_in.bind((EmoModule.WASABI_IP, EmoModule.WASABI_PORT_OUT))
            #sock_in.bind(('192.168.0.46', EmoModule.WASABI_PORT_OUT))
            sock_in.bind(('132.230.17.153', EmoModule.WASABI_PORT_OUT))

            print 'start hearing'
            while self.hearing:
                data = sock_in.recvfrom(1024)[0]
                if self.log_wasabi:
                    self.logger.save_wasabi(data)
                if self.expressing:
                    self.update_emo_status(data)
                elif self.static_emotion:
                    self.show_static()



        self.thread = Thread(target=run, args=())
        self.thread.start()

    def end(self):
        ''' Ends hearing for wasabi messages
        '''
        self.hearing = False

    def start_expressing(self):
        self.expressing = True

    def stop_expressing(self):
        self.expressing = False

    def show_static_emotion(self, emotion):
        self.expressing = False
        self.static_emotion = emotion

    def clear_static_emotion(self):
        self.static_emotion = None

    def show_static(self):
        # Send to MARC:
        if self.marc and self.static_emotion:
            if self.static_emotion.FREQUENCE <= self.count:
                self.count = 0
                self.marc.show(self.static_emotion)
            else:
                self.count += 1

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

        if self.expressing:
            primary_emo = ''
            highest_imp = 0
            for emotion in self.emo_status.keys():
                if math.fabs(self.emo_status[emotion]) >= math.fabs(highest_imp):
                    primary_emo = emotion
                    highest_imp = self.emo_status[emotion]
            if highest_imp == 0:
                primary_emotion = 'concentrated'
            return utilities.emotion_by_name(primary_emo, impulse = highest_imp)
        else:
            return self.static_emotion

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
        # Check for change:
        if (not self.dominating_emo or (primary_emo and self.dominating_emo
            and primary_emo.name != self.dominating_emo.name)):
            #self.logger.log('  Dominating emotion changed to {}'.format(primary_emo))
            self.dominating_emo = primary_emo

        emotion = utilities.emotion_by_name(primary_emo.name)

        # Send to MARC:
        if self.marc:
            if emotion.FREQUENCE <= self.count:
                self.count = 0
                self.marc.show(emotion)
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

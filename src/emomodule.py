''' The emotion module

    Contains class definitions for all available emotions and the emotional
    module which manages all emotional reactions.
'''

import socket
import threading
import math

#from wasabi import Wasabi

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

    WASABI = False
    WASABI_IP = ''
    WASABI_PORT_IN = 0
    WASABI_PORT_OUT = 0

    
    def __init__(self, marc = None):
        self.marc = marc
        print 'EmoModuleEmoModuleEmoModule:', EmoModule.WASABI
        if EmoModule.WASABI:
            self.wasabi = WasabiListener(EmoModule.WASABI_IP, EmoModule.WASABI_PORT_IN, EmoModule.WASABI_PORT_OUT)
            self.start_hearing()
        
    
    def check(self, task):
        ''' Task evaluation according to the emotional reaction.

            Sends an emotional input to wasabi and text back to the agent
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

        if EmoModule.wasabi:
            self.send(emotion.name, emotion.impulse)

        return emotion

    def send(self, emotion, intensity):
        ''' Possible emotions are:
            happy, angry, annoyed, surprised, bored, sad, depressed, fearful
        '''
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        message = "JohnDoe&TRIGGER&1&" + emotion
        sock_out.sendto(message, (self.ip_addr, self.port_out))

        message = "JohnDoe&IMPULSE&1&" + str(intensity)
        sock_out.sendto(message, (self.ip_addr, self.port_out))

    def start_hearing(self):
        ''' Starts the connectivity to WASABI.
        '''
        self.wasabi.start()

    def end_hearing(self):
        ''' Ends the connectivity to WASABI
        '''
        self.wasabi.end()


class WasabiListener(threading.Thread):
    ''' Class for recieving input by WASABI
    '''

    def __init__(self, ip_addr, port, marc):
        threading.Thread.__init__(self)
        self.ip_addr = ip_addr
        self.port = port
        self.marc = marc
        self.hearing = True
        self.emotions = {'happy': 0, 'concentrated': 0, 'depressed': 0,
                         'sad': 0, 'angry': 0, 'annoyed': 0, 'bored': 0}
        self.blocked = False

    def run(self):
        ''' Starts the thread and waits for WASABI messages
        '''
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_in.bind((self.ip_addr, self.port))

        while self.hearing:
            data = sock_in.recvfrom(1024)[0]
            self.update_emotions(data)

    def update_emotions(self, data):
        ''' Gets a string of emotion values received from wasabi
            and updates the internal emotion dictionary

            1. Try: Always show dominating emotion
        '''
        # get the single emotion assignments
        values = data.split(" ")
        # remove eventually empty entries
        values = [val for val in values if val != ""]

        remaining_keys = self.emotions.keys()
        for value in values:
            value = value.replace(' ', '')
            if len(value.split('=')) != 2:
                print 'strange', data, '-', value
            else:
                emotion = value.split('=')[0]
                remaining_keys.remove(emotion)
                # get the first two digits
                intensity = int(float(value.split('=')[1]) * 100)

                # check for emotion update:
                if intensity != self.emotions[emotion]:
                    self.emotions[emotion] = intensity

        # Update emotions with new value 0
        for key in remaining_keys:
            self.emotions[key] = 0


        # Get dominating emotion:
        primary_emo = ''
        highest_imp = 0
        for emotion in self.emotions.keys():
            if math.fabs(self.emotions[emotion]) > math.fabs(highest_imp):
                primary_emo = emotion
                highest_imp = self.emotions[emotion]

        print 'domoinating is ', primary_emo, ' with ', highest_imp

        # MARC:
        if self.marc and not self.blocked:
            self.blocked = True
            if primary_emo == Emotion.WASABI_ANGER:
                self.marc.perform('Ekman-Colere', Emotion('Ekman-Colere', impulse = highest_imp/3*2).get_bml_code())
            elif primary_emo == 'annoyed':
                self.marc.perform('Ekman-Colere', Emotion('Ekman-Colere', impulse = highest_imp/2).get_bml_code())
            elif primary_emo == 'bored':
                self.marc.perform('Ekman-Colere', Emotion('MindReading - Interet', impulse = highest_imp/3).get_bml_code())
            elif primary_emo == 'concentrated':
                self.marc.perform('Ekman-Colere', Emotion('AC-Mind Reading-interested vid8-fascinated', impulse = highest_imp/4).get_bml_code())
            elif primary_emo == Emotion.WASABI_JOY:
                self.marc.perform('Ekman-Joie', Emotion('Ekman-Joie', impulse = highest_imp/3*2).get_bml_code())
    
        elif self.marc and self.blocked:
            self.blocked = False

    def print_emotions(self):
        ''' Prints the current emotion status
        '''
        output = ''
        for emotion in self.emotions.keys():
            intensity = self.emotions[emotion]
            if intensity != 0:
                output += emotion + '=' + str(intensity) + " "
        print output

    def end(self):
        ''' Ends the thread
        '''
        self.hearing = False

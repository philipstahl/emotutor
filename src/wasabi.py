''' Class interface for WASABi software

    Possible emotion matchings:
    happy
    angry
    annoyed
    surprised
    bored
    sad
    depressed
    fearful


    AC - Mind Reading - angry vid1 - angry
    AC - Mind Reading - happy vid16 - happy
    AC - Mind Reading - interested vid10 - interested
    AC - Mind Reading - surprised vid7 - surprised
    AC-Mind Reading-affraid vid19-Vulnerable


    Ekman-Joie
    Ekman-Colere
    Ekman-Surprise
    Ekman-Tristesse
    Ekman-Disgust
    Ekman-Peur
'''

import socket
import threading
import math

class ThreadClassHear(threading.Thread):
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

        self.print_emotions()
        print 'domoinating is ', primary_emo, ' with ', highest_imp

        # MARC:
        if self.marc and not self.blocked:
            self.blocked = True
            if primary_emo == Wasabi.ANGER:
                self.marc.perform('Ekman-Colere', Emotion('Ekman-Colere', impulse = highest_imp/3*2).get_bml_code())
            elif primary_emo == 'annoyed':
                self.marc.perform('Ekman-Colere', Emotion('Ekman-Colere', impulse = highest_imp/2).get_bml_code())
            elif primary_emo == 'bored':
                self.marc.perform('Ekman-Colere', Emotion('MindReading - Interet', impulse = highest_imp/3).get_bml_code())
            elif primary_emo == 'concentrated':
                self.marc.perform('Ekman-Colere', Emotion('AC-Mind Reading-interested vid8-fascinated', impulse = highest_imp/4).get_bml_code())
            elif primary_emo == Wasabi.JOY:
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


class Wasabi:
    ''' Interface for Wasabi: Sending and Receiving messages.
    '''

    JOY = 'happy'
    RELAX = 'happy'
    ANGER = 'angry'

    def __init__(self, ip_addr, port_in, port_out, marc = None):
        self.ip_addr = ip_addr
        self.port_in = port_in
        self.port_out = port_out
        self.marc = marc
        self.input = ThreadClassHear(ip_addr, port_in, marc)

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
        self.input.start()

    def end_hearing(self):
        ''' Ends the connectivity to WASABI
        '''
        self.input.end()

    def get_primary_emotion(self):
        ''' Returns the strongest emotion of the current emotion status
        '''
        if self.input.emotions['angry'] > self.input.emotions['happy']:
            return ('angry', self.input.emotions['angry'])
        else:
            return ('happy', self.input.emotions['happy'])


if __name__ == '__main__':
    import sys
    from emomodule import *
    if len(sys.argv) == 4 and sys.argv[1] == 'send':
        wasabi = Wasabi('192.168.0.46', 42424, 42425)
        wasabi.send(sys.argv[2], sys.argv[3])
    else:
        from marc import Marc
        marc = Marc('localhost', 4014, 4013)
        wasabi = Wasabi('192.168.0.46', 42424, 42425, marc)
        wasabi.start_hearing()

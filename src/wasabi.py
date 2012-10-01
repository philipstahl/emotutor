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
        '''
        # get the single emotion assignments
        values = data.split(" ")
        # remove eventually empty entries
        values = [val for val in values if val != ""]
        for value in values:
            value = value.replace(' ', '')
            if len(value.split('=')) != 2:
                print 'strange', data, '-', value
            else:
                emotion = value.split('=')[0]
                # get the first digit after the
                intensity = int(float(value.split('=')[1]) * 10)

                # check for emotion update:
                if intensity != self.emotions[emotion]:
                    self.emotions[emotion] = intensity
                    self.print_emotions()

                    # MARC:
                    if self.marc:
                        if emotion == Wasabi.JOY:
                            self.marc.show(Emotion.JOY, float(intensity) / 10)
                        elif emotion == Wasabi.ANGER:
                            self.marc.show(Emotion.ANGER, float(intensity) / 10)

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

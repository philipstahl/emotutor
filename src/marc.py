''' Interface to MARC software
'''
import socket

class Marc:
    ''' An interface to interact with an agent represented by MARC
    '''

    IP = 'localhost'
    PORT_OUT = 4010
    PORT_IN = 4011

    def __init__(self):
        self.sock_out = socket.socket(socket.AF_INET,
                                      socket.SOCK_DGRAM)
        self.sock_in = socket.socket(socket.AF_INET,
                              socket.SOCK_DGRAM)
        self.sock_in.bind((Marc.IP, Marc.PORT_IN))

    def _perform(self, name, bml_code):
        ''' Performs the action specified in the bml code
        '''
        self.sock_out.sendto(bml_code, (Marc.IP, Marc.PORT_OUT))

    def show(self, emotion):
        ''' Sends the BML Code of the given facial expression to MARC.

            MARC will perform the expression, if the expression is in the
            database of the selected agent.

        '''
        self._perform(emotion.name, emotion.get_bml_code())

    def speak(self, speech):
        ''' Sends the BML Code for speacking the given wave file to MARC.
        '''
        print 'MARC says', speech.text
        self._perform(speech.name, speech.get_bml_code())


if __name__ == '__main__':

    '''
        (bank, 0), (card, 1), (dart, 2), (face, 3), (game, 4)
        (hand, 5), (jack, 6), (king, 7), (lamb, 8), (mask, 9)
        (neck, 0), (pipe, 1), (guip, 2), (rope, 3), (sock, 4)
        (tent, 5), (vent, 6), (wall, 7), (xray, 8), (zinc, 9)
    '''
    words = ['Bank', 'Pfeil', 'Gesicht', 'Spiel', 'Hand', 'Jacke', 'Lamm',
             'Maske', 'Nacken', 'Pfeife', 'Mantel', 'Socke', 'Zelt', 'Wand', 'Zink']

    import time
    from emomodule import Happy, Angry
    from speechmodule import Speech
    marc = Marc()

    for word in words:
        speech_happy = Speech('test', word, Happy())
        speech_neutral = Speech('test', word, None)
        speech_angry = Speech('test', word, Angry())    
        marc.speak(speech_happy)
        time.sleep(2)
        marc.speak(speech_neutral)
        time.sleep(2)
        marc.speak(speech_angry)
        time.sleep(2)    

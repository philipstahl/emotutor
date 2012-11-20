''' Interface to MARC software
'''
import socket

class Marc:
    ''' An interface to interact with an agent represented by MARC
    '''

    IP = 'localhost'
    PORT_OUT = 4013
    PORT_IN = 4014

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
    from emomodule import Happy
    from speechmodule import Speech
    marc = Marc()
    speech_output = Speech('introduction', 'Das ist ein Test. Test Test Check.',
                     Happy())
    marc.show(Happy())
    marc.speak(speech_output)
    marc.show(Happy())

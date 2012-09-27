''' Interface to MARC software
'''
import socket
from globalsettings import MARC_IP, MARC_PORT_IN, MARC_PORT_OUT


class Marc:
    ''' An interface to interact with an agent represented by MARC
    '''
    def __init__(self):
        self.sock_out = socket.socket(socket.AF_INET,       # Internet
                                      socket.SOCK_DGRAM)    # UDP
        self.sock_in = socket.socket(socket.AF_INET,        # Internet
                              socket.SOCK_DGRAM)            # UDP
        self.sock_in.bind((MARC_IP, MARC_PORT_IN))

    def perform(self, name, bml_code):
        ''' Performs the action specified in the bml code
        '''
        self.sock_out.sendto(bml_code, (MARC_IP, MARC_PORT_OUT))
        # TODO: Wait via Thread for End of Emotion?
        # while True:
        #     data, address = self.sock_in.recvfrom(4096)
        #     print data
        #     # data is <event id=\"Perform_{expression}:end\"/>
        #     if data.split("\"")[1] == "Perform" + name + ":end":
        #         break

    def show(self, emotion):
        ''' Sends the BML Code of the given facial expression to MARC.

            MARC will perform the expression, if the expression is in the database
            of the selected agent.

        '''
        print 'Showing', emotion.name
        self.perform(emotion.name, emotion.getBMLCode())

    def speak(self, speech):
        ''' Sends the BML Code for speacking the given wave file to MARC.
        '''
        print 'Saying', speech.name
        self.perform(speech.name, speech.getBMLCode())

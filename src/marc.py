''' Interface to MARC software
'''
import socket

class Marc:
    ''' An interface to interact with an agent represented by MARC
    '''

    JOY = ''
    RELAX = ''
    ANGER = ''

    def __init__(self, ip_addr, port_in, port_out, emotions):
        self.ip_addr = ip_addr
        self.port_in = port_in
        self.port_out = port_out
        self.emotions = emotions
        JOY = emotions['joy']
        RELAX = emotions['relax']
        ANGER = emotions['anger']

        self.sock_out = socket.socket(socket.AF_INET,       # Internet
                                      socket.SOCK_DGRAM)    # UDP
        self.sock_in = socket.socket(socket.AF_INET,        # Internet
                              socket.SOCK_DGRAM)            # UDP
        self.sock_in.bind((self.ip_addr, self.port_in))

    def perform(self, name, bml_code):
        ''' Performs the action specified in the bml code
        '''
        self.sock_out.sendto(bml_code, (self.ip_addr, self.port_out))
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
        self.perform(emotion.name, emotion.get_bml_code())

    def speak(self, speech):
        ''' Sends the BML Code for speacking the given wave file to MARC.
        '''
        print 'Saying', speech.name
        self.perform(speech.name, speech.get_bml_code())

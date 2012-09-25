import socket
import argparse
import ftplib
from expression import Expression
from speech import Speech

UDP_IP="localhost"
UDP_PORT_OUT=4013
UDP_PORT_IN=4014


class Marc:
    def __init__(self):
        
        self.sock_out = socket.socket( socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM ) # UDP
        self.sock_in = socket.socket( socket.AF_INET, # Internet
                              socket.SOCK_DGRAM ) # UDP
        self.sock_in.bind( (UDP_IP,UDP_PORT_IN) )


    def perform(self, name, bmlCode):
        self.sock_out.sendto(bmlCode, (UDP_IP, UDP_PORT_OUT))
        #while True:
        #    data, address = self.sock_in.recvfrom(4096)
        #    print data
        #    # data is <event id=\"Perform_{expression}:end\"/>
        #    if data.split("\"")[1] == "Perform" + name + ":end":
        #        break

    ''' Sends the BML Code of the given facial expression to MARC.
        MARC will perform the expression, if the expression is in the database
        of the selected agent.
    '''
    def show(self, expression):
        print 'Showing', expression.name
        self.perform(expression.name, expression.getBMLCode())            
        print 'Finished showing',expression.name

    ''' Sends the BML Code for speacking the given wave file to MARC.
    '''
    def speak(self, speech):
        print 'Saying', speech.name
        self.perform(speech.name, speech.getBMLCode())
        print 'Finished saying', speech.name

    def show_joy(self, intensity):
        exp = Expression("CASA_Joy_01", wait = 0.0, intensity = intensity, interpolate = 1.0)
        self.show(exp)

        
    def show_anger(self, intensity):
        exp = Expression("CASA_Anger_01", wait = 0.0, intensity = intensity, interpolate = 1.0)
        self.show(exp)

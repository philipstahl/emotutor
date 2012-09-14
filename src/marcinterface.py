import socket
import argparse
import ftplib
from expression import Expression
from speech import Speech

UDP_IP="localhost"
UDP_PORT_OUT=4013
UDP_PORT_IN=4014

sock_out = socket.socket( socket.AF_INET, # Internet
                         socket.SOCK_DGRAM ) # UDP
sock_in = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock_in.bind( (UDP_IP,UDP_PORT_IN) )

exp_joy = Expression("CASA_Joy_01")
exp_relax = Expression("CASA_Relax_01")
exp_anger = Expression("CASA_Anger_01")

speech_posright = Speech("positive_right")
speech_right = Speech("neutral_right")
speech_wrong = Speech("neutral_wrong")
speech_negwrong = Speech("negative_wrong")

def perform(name, bmlCode):
    sock_out.sendto(bmlCode, (UDP_IP, UDP_PORT_OUT))
    while True:
        data, address = sock_in.recvfrom(4096)
        print data
        # data is <event id=\"Perform_{expression}:end\"/>
        if data.split("\"")[1] == "Perform" + name + ":end":
            break

''' Sends the BML Code of the given facial expression to MARC.
    MARC will perform the expression, if the expression is in the database
    of the selected agent.
'''
def show(expression):
    print 'Showing', expression.name
    perform(expression.name, expression.getBMLCode())            
    print 'Finished showing',expression.name

''' Sends the BML Code for speacking the given wave file to MARC.
'''
def speak(speech):
    print 'Saying', speech.name
    perform(speech.name, speech.getBMLCode())
    print 'Finished saying', speech.name
    
amour = Expression("Amour")
speechWelcome = Speech("mary_test")
#show(amour)
#speak(speechWelcome)

show(exp_anger)
show(exp_relax)
show(exp_joy)

speak(speech_right)
speak(speech_wrong)
speak(speech_posright)
speak(speech_negwrong)

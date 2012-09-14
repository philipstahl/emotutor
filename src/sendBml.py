import socket
import argparse
import ftplib
from facialExpression import FacialExpression

UDP_IP="localhost"
UDP_PORT_OUT=4010
UDP_PORT_IN=4011
#UDP_PORT_OUT=4013
#UDP_PORT_IN=4014

parser = argparse.ArgumentParser(description='Sends the BML Code of the given \
                                              facial expression to MARC.')
parser.add_argument('expression')
args = parser.parse_args()

EMO = FacialExpression(args.expression)

#EMO_ANGER = FacialExpression("Ekman-Surprise")
#EMO_JOY = FacialExpression("Joy")

emotionNames = []

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT_OUT
message = EMO.getBMLCode()
print "message:", message

sock_out = socket.socket( socket.AF_INET, # Internet
                         socket.SOCK_DGRAM ) # UDP
sock_out.sendto( message, (UDP_IP, UDP_PORT_OUT) )

print "\ndone"

sock_in = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock_in.bind( (UDP_IP,UDP_PORT_IN) )

'''
while True:
    data, addr = sock_in.recvfrom( 1024 ) # buffer size is 1024 bytes
    print "received message:", data
    if data.split("\"")[1] == "Show_Anger:end":
        print "SHOW JOY", EMO_JOY.getBMLCode()
        sock_out.sendto( EMO_JOY.getBMLCode(), (UDP_IP, UDP_PORT_OUT) )
    if data.split("\"")[1] == "Show_Joy:end":
        break
'''

print "finished"

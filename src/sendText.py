import socket
import argparse
import ftplib
from facialExpression import FacialExpression

UDP_IP="localhost"
UDP_PORT_OUT=4013
UDP_PORT_IN=4014

parser = argparse.ArgumentParser(description='Sends the BML Code of the given \
                                              facial expression to MARC.')
parser.add_argument('expression')
args = parser.parse_args()

EMO = FacialExpression(args.expression)

emotionNames = []

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT_OUT
message = EMO.getBMLCode()

message = "<bml id=\"Track_0\"> \
               <marc:fork id=\"Track_0_fork_1\"> \
               <face id=\"bml_item_1\" > \
               <description level=\"1\" type=\"marcbml\"> \
               <facial_animation name=\"Amour\" interpolate=\"0.0\" loop=\"false\"  intensity=\"1.0\" /> \
               </description> \
               </face> \
               </marc:fork> \
               <marc:fork id=\"Track_0_fork_2\"> \
               <wait duration=\"1.017\" /> \
               <speech id=\"bml_item_2\"  marc:file=\"C:\\Program Files\\LIMSI\\MARC\\10.4.0\\mary_test.wav\" marc:articulate=\"0.4\" /> \
               </marc:fork></bml>"

sock_out = socket.socket( socket.AF_INET, # Internet
                         socket.SOCK_DGRAM ) # UDP
sock_out.sendto( message, (UDP_IP, UDP_PORT_OUT) )


sock_in = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock_in.bind( (UDP_IP,UDP_PORT_IN) )

print "finished"

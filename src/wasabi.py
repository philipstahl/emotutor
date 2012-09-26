import socket
import threading
from decimal import Decimal

#from marc import *


''' Hearing for emotional status in wasabi.
    Sending emotions to wasabi via commandline.


    We expect messages (i.e. strings with a maximum length of 100 characters) that conform the following BNF:
 * <message>  ::= <senderID> '&' <command>
 * <senderID> ::= (any non-empty string)
 * <command>  ::= <add> | <trigger> | <impulse> | <dominance>
 * <add>      ::= 'ADD' '&' <name> [ '&' <globalID> '&' <initfile> ]
 * <trigger>  ::= 'TRIGGER' '&' <targetID> '&' <affectiveStateName> [ '&' <lifetime> ]
 * <impulse>  ::= 'IMPULSE' '&' <targetID> '&' <impvalue>
 * <dominance>::= 'DOMINANCE' '&' <targetID> '&' <domvalue>
 * <name>     ::= (any non-empty string)
 * <initfile> ::= (any non-empty string, defaults to 'init', if not found)
 * <globalID> ::= (any non-empty string)
 * <targetID> ::= (any non-empty string)
 * <affectiveStateName> ::= (any non-empty string, must match a name of an emotion, though)
 * <lifetime> ::= (any double d with 0 <= d <= 100 or d == -1)
 * <impvalue> ::= (any integer i with -100 <= i <= 100 and i != 0)
 * <domvalue> ::= (any integer i with -100 <= i <= 100)
 * ------------------------------------------------------------------------------------------
 * ADD: Adds a new EmotionalAttendee (EA) to the simulation.
 *      For each EA an independent reference point (XYZ) is created
 *      The affective states are loaded from file <initfile>, if provided, or else from the default file 'init'.
 *      A globalID can optionally be provided as well, but an internal uid (int) is created as well.
 *      Returns: 'REPLY&ADD&OK&' <localID> only in case of success.
 * TRIGGER: Is used whenever an affective state's intensity is to be set to maximum for a certain amount of (life)time.
 *          For example, 'surprise' is initialized to have a baseIntensity of zero and, thus, needs to be triggered,
 *          before it can gain a positive awareness likelihood.
 *          Only triggering an emotion, however, might not be sufficient to 'activate' this emotion with a certain awareness likelihood.
 *          The PAD values of the reference point must be close enough to the emotion in question as well, while it has a non-zero intensity.
 *          This is what it means to have an 'emotion dynamics' instead of a purely rule-based and direct emotion elicitation.
 *          You need to provide the <targetID>, which is the uid returned by the ADD command or '1' for the default simulation of 'John Doe'.
 *          By specifying the <affectiveStateName> you tell the system, which "affective state" (i.e. primary or secondary emotion) to TRIGGER.
 *          Take care yourself that this affective state has been loaded from <initfile>.emo_pad before.
 *          Optionally, you might provide a lifetime (double) for this emotion. If no lifetime is given, the emotions standardLifetime will be used.
 * IMPULSE: Is used to drive the emotion dynamics in XYZ space itself.
 *          As soon as something positive or negative is detected to happen, you might use this command to tell the WASABI engine.
 *          Of course, the event can have happend to the agent/robot itself or to another person, i.e. another EmotionalAttendee (EA).
 *          In the former case, <targetID> should be set to '1', in the latter case, to that uid, which was returned after ADDing this EA to the simulation.
 *          The impulse must be within the range [-100,100] and should be an integer.
 * DOMINANCE: Is used to set the dominance value of the EA with ID <targetID> to any value
 *            between 100 (dominant) and -100 (submissive). As of June 2012 only the two extreme values make sense, though.
 *            Concerning the value of <targetID> the same applies as in case of IMPULSE explained above.
 */
'''

'''
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

class ThreadClassHear(threading.Thread):

    def __init__(self, marc):
        threading.Thread.__init__(self)
        self.marc = marc
        self.hearing = True
    
    def run(self):
        UDP_IP_IN = "192.168.0.46"
        UDP_PORT_IN=42424
        sock_in = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
        sock_in.bind( (UDP_IP_IN,UDP_PORT_IN) )

        self.emotions = {'happy': 0, 'concentrated': 0, 'depressed': 0, 'sad': 0, 'angry': 0, 'annoyed': 0, 'bored': 0}
        
        while self.hearing:
            data, addr = sock_in.recvfrom(1024) # buffer size is 1024 bytes
            
            self.update_emotions(data)
            

    ''' Gets a string of emotion values received from wasabi
        and updates the internal emotion dictionary
    '''
    def update_emotions(self, data):
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
                        if emotion == "happy":
                            self.marc.show_joy(float(intensity) / 10)
                        elif emotion == "angry":
                            self.marc.show_anger(float(intensity) / 10)

    def print_emotions(self):
        output = ''
        for emotion in self.emotions.keys():
            intensity = self.emotions[emotion]
            if intensity != 0:
                output += emotion + '=' + str(intensity) + " "
        print output

    def end(self):
        self.hearing = False


class Wasabi():
    def __init__(self, marc = None):
        self.marc = marc
        self.input = ThreadClassHear(self.marc)

    ''' Possible emotions are:
        happy, angry, annoyed, surprised, bored, sad, depressed, fearful
    '''
    def send(self, emotion, intensity):
        UDP_IP_OUT = "localhost"
        UDP_PORT_OUT=42425
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        message = "JohnDoe&TRIGGER&1&" + emotion
        sock_out.sendto(message, (UDP_IP_OUT, UDP_PORT_OUT))
        
        message = "JohnDoe&IMPULSE&1&" + str(intensity)
        sock_out.sendto(message, (UDP_IP_OUT, UDP_PORT_OUT))
        
    def start_hearing(self):
        self.input.start()

    def end_hearing(self):
        self.input.end()

    def get_primary_emotion(self):
        if self.input.emotions['angry'] > self.input.emotions['happy']:
            return ('angry', self.input.emotions['angry'])
        else:
            return ('happy', self.input.emotions['happy'])

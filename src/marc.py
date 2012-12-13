''' Interface to MARC software
'''
import socket

class Marc:
    ''' An interface to interact with an agent represented by MARC
    '''

    IP = 'localhost'
    PORT_OUT = 4010
    PORT_IN = 4011

    def __init__(self, logger=None):
        self.sock_out = socket.socket(socket.AF_INET,
                                      socket.SOCK_DGRAM)
        self.sock_in = socket.socket(socket.AF_INET,
                              socket.SOCK_DGRAM)
        self.sock_in.bind((Marc.IP, Marc.PORT_IN))
        self.logger = logger
        
    def _perform(self, name, bml_code):
        ''' Performs the action specified in the bml code
        '''
        self.sock_out.sendto(bml_code, (Marc.IP, Marc.PORT_OUT))

    def show(self, emotion):
        ''' Sends the BML Code of the given facial expression to MARC.

            MARC will perform the expression, if the expression is in the
            database of the selected agent.

        '''
        #print 'marc shows', emotion.name
        #self._perform(emotion.name, emotion.get_bml_code())
        pass

    def speak(self, speech):
        ''' Sends the BML Code for speacking the given wave file to MARC.
        '''
        if self.logger:
            self.logger.log('  Marc: Say {0}'.format(speech.text))
        self._perform(speech.name, speech.get_bml_code())

    def endRound(self, round_nr):
        bml_code = '<bml id="Track_0"> \
                    <marc:fork id="Track_0_fork_1"> \
                    <marc:subtitles id="bml_item_2" align="DOWN" duration="10.0">' \
                    + 'Ende Runde ' + str(round_nr) \
                    + '</marc:subtitles></marc:fork></bml>'
        self._perform('end round', bml_code)


    def subtitle(self, text, duration='2.0'):
        bml_code = '<bml id="Track_0"> \
                    <marc:fork id="Track_0_fork_1"> \
                    <marc:subtitles id="bml_item_2" align="DOWN" duration="'+duration+'">' \
                    + str(text) \
                    + '</marc:subtitles></marc:fork></bml>'
        self._perform('end round', bml_code)

    def headYes(self):
        if self.logger:
            self.logger.log('  Marc: Shake head YES')
        print 'MARC HEAD YES'
        self.headDown(wait=0.0, amount=0.1, interpolate=0.3)
        self.headClear(wait=0.3, interpolate=0.3)

    def headNo(self):
        if self.logger:
            self.logger.log('  Marc: Shake head NO')
        self.headClear(wait=0.0, interpolate=1.0)
        self.headLeft(wait=0.1, amount=0.2, interpolate=0.3)
        self.headClear(wait=0.3, interpolate=0.3)
        self.headRight(wait=0.6, amount=0.2, interpolate=0.3)
        self.headClear(wait=0.9, interpolate=0.5)

    def headClear(self, wait=0.0, interpolate=1.0):
        bml_code = '<bml id="Track_0"><marc:fork id="Track_0_fork_1">' \
                + '<wait duration="' + str(wait) + '" />' \
                 + '<face id="bml_item_1" type="FACS" side="BOTH" amount="0" au="marc:ALL" marc:interpolate="' + str(interpolate) + '" />' \
                 + '</marc:fork></bml>'
        
        self._perform('clear', bml_code)


    def headUp(self, wait=0.0, amount=0.5, interpolate=1.0):
        bml_code = '<bml id="Track_0"><marc:fork id="Track_0_fork_1">' \
                 + '<wait duration="' + str(wait) + '" />' \
                 + '<face id="bml_item_1_au52"  type="FACS" side="BOTH" amount="' + str(amount) + '" au="53" marc:interpolate="' + str(interpolate) + '" marc:interpolation_type="linear" />' \
                 + '</marc:fork></bml>'
        self._perform('head_up', bml_code)


    def headDown(self, wait=0.0, amount=0.5, interpolate=1.0):
        bml_code = '<bml id="Track_0"><marc:fork id="Track_0_fork_1">' \
                 + '<wait duration="' + str(wait) + '" />' \
                 + '<face id="bml_item_1_au53"  type="FACS" side="BOTH" amount="' + str(amount) + '" au="54" marc:interpolate="' + str(interpolate) + '" marc:interpolation_type="linear" />' \
                 + '</marc:fork></bml>'
        self._perform('head_down', bml_code)

    def headLeft(self, wait=0.0, amount=0.5, interpolate=1.0):
        bml_code = '<bml id="Track_0"><marc:fork id="Track_0_fork_1">' \
                 + '<wait duration="' + str(wait) + '" />' \
                 + '<face id="bml_item_2_au50"  type="FACS" side="BOTH" amount="' + str(amount) + '" au="51" marc:interpolate="' + str(interpolate) + '" marc:interpolation_type="linear" />' \
                 + '</marc:fork></bml>'
        self._perform('head_left', bml_code)

    def headRight(self, wait=0.0, amount=0.5, interpolate=1.0):
        bml_code = '<bml id="Track_0"><marc:fork id="Track_0_fork_1">' \
                 + '<wait duration="' + str(wait) + '" />' \
                 + '<face id="bml_item_5_au51"  type="FACS" side="BOTH" amount="' + str(amount) + '" au="52" marc:interpolate="' + str(interpolate) + '" marc:interpolation_type="linear" />' \
                 + '</marc:fork></bml>'
        self._perform('head_right', bml_code)

if __name__ == '__main__':

    '''
        (bank, 0), (card, 1), (dart, 2), (face, 3), (game, 4)
        (hand, 5), (jack, 6), (king, 7), (lamb, 8), (mask, 9)
        (neck, 0), (pipe, 1), (guip, 2), (rope, 3), (sock, 4)
        (tent, 5), (vent, 6), (wall, 7), (xray, 8), (zinc, 9)


        Arzt,Arm,Art,Ast
        Baum,Brot,Bank,Bett,Berg,Bein,Blatt,Bus,Ball,Busch,Band,Brett,Bild
        Eis,
        Frau,Fisch,Fleck,Freund
        Gas,Glas
        Hand,Herbst,Hund,Haus,Hemd,Hahn,Herz,Hut,Hof,Kahn
        Kamm,Kopf,Kind,Knopf,Kran
        Lamm,Land,Laub,Laus
        Mann,Milch,Mond,Mann,Meer,Moor
        Nacht,
        Pfeil,Pelz,Pilz
        Rad,Rat
        Salz,Spiel,Schrank,Stift,Stuhl,Saft,Stern,Sieb,Schuh,Stirn,Sieg,Seil,Stein,Sand,Schwein,Schaf,Schuss,Schluss,Schatz,Stahl
        Tee,Tisch,Text,Taxi,Topf
        Uhr,
        Wand,Wurst,Wal,Wald
        Zelt,Zink,Zug,Zahl,Zahn
'''


    all_words = 'Arzt,Arm,Art,Ast,\
             Baum,Brot,Bank,Bett,Berg,Bein,Blatt,Bus,Ball,Busch,Band,Brett,Bild,\
             Cafe,Carl,Chip,Clip,\
             Deo,Damm,Dieb,Dock,Dorf,Dachs,Dampf,Deich,Dolch,Dreck,\
             Eis,\
             Frau,Fisch,Fleck,Freund,\
             Gas,Glas,Geld,Grund,Grill\
             Hand,Herbst,Hund,Haus,Hemd,Hahn,Herz,Hut,Hof,Kahn,\
             Jod, Jagd,Jahr,\
             Kamm,Kopf,Kind,Knopf,Kran,\
             Lamm,Land,Laub,Laus,\
             Mann,Milch,Mond,Mann,Meer,Moor,\
             Nacht,\
             Pfeil,Pelz,Pilz,Pfeil,Pilz,Paar,Park,Pelz,Pfad,Pils,Pult,\
             Quark,Quiz,Qualm,\
             Rad,Rat,Rad,Rat,Reh,Rast,Reis,Reim,Rock,\
             Salz,Spiel,Schrank,Stift,Stuhl,Saft,Stern,Sieb,Schuh,Stirn,Sieg,Seil,Stein,Sand,Schwein,Schaf,Schuss,Schluss,Schatz,Stahl,\
             Tee,Tisch,Text,Taxi,Topf,\
             Uhr,\
             Verb,Vers,Vieh,Volk,\
             Wand,Wurst,Wal,Wald,\
             Yen,Yeti,Yak,Yacht,\
             Zelt,Zink,Zug,Zahl,Zahn'


    good_words = 'Baum,Bank,Bett,Bein,Blatt,Bus,Busch,Band,Bild,\
             Carl,Chip,\
             Damm,Dorf,Dampf,\
             Frau,Fisch,Freund,\
             Geld,\
             Hand,Hemd,Herz,\
             Jod, Jagd,Jahr,\
             Kamm,Kopf,Kind,Knopf,\
             Lamm,Land,Laub,Laus,\
             Mann,Milch,Mond,Mann,Meer,\
             Nacht,\
             Pfeil,Pilz,Pfeil,Paar,Pfad,Pult,\
             Quark,\
             Rock,\
             Schrank,Stift,Stuhl,Stern,Schuh,Stirn,Sieg,Stein,Schluss,Schatz,\
             Tisch,Text,Taxi,Topf,\
             Vers,Vieh,\
             Wand,Wal,Wald,\
             Zelt,Zink,Zahl'

    good_words = 'Xanten,Yeti'
    
    words = good_words.split(',')


    import time
    #from emomodule import Happy, Angry
    from speechmodule import Speech
    marc = Marc()

    marc.headNo()
    marc.endRound(1)

    '''
    for word in words:
        #speech_happy = Speech('test', word, Happy())
        speech_neutral = Speech('test', word, None)
        #speech_angry = Speech('test', word, Angry())    
        #marc.speak(speech_happy)
        #time.sleep(2)
        marc.speak(speech_neutral)
        time.sleep(2)
        #marc.speak(speech_angry)
        #time.sleep(2)
    '''

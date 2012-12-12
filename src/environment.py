''' The environment for the trainig scenario.

    Connects the agent with the gui.

'''
import random
import datetime
from agent import Agent
from marc import Marc
from logger import Logger
import utilities
from emomodule import WasabiListener, EmoModule


class Word:
    ''' Class representing a single word.
    '''
    def __init__(self, word):
        self.word = word
        self.times = []

    def add(self, time):
        self.times.append(time)

    def time(self, i):
        return self.times[i]


class Pair:
    ''' Class representing a pair of a word associated with a number.
    '''
    def __init__(self, word, number):
        self.word = Word(word)
        self.number = Word(number)
        self.answers = []

    def word_called(self, time):
        self.word.add(time)

    def number_called(self, time):
        self.number.add(time)

    def answer_given(answer):
        self.answers.append(answer)


class TestEnvironment:
    ''' Class for testing settings.
    '''
    def __init__(self):
        pass
    
    def test(self, emotion, iterations):
        ''' Simulate a facial expression for a certain time
        '''
        marc = Marc(Logger(path='', write=False))
        from threading import Thread
        import socket
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #sock_in.bind((EmoModule.WASABI_IP, EmoModule.WASABI_PORT_OUT))
        sock_in.bind(('132.230.17.153', EmoModule.WASABI_PORT_OUT))

        def show(emotion, iterations):
            ''' Shows iteration many times the emotion
            '''
            count = 0
            while iterations > 0:
                sock_in.recvfrom(1024)[0]
                if count >= emotion.FREQUENCE:
                    print 'Test: Marc shows', emotion.name, emotion.marc, emotion.intensity
                    marc.show(emotion)
                    iterations -= 1
                    count = 0
                else:
                    count += 1

        thread = Thread(target=show, args=(emotion, iterations))
        thread.start()

    def test_wasabi(self):
        ''' Simulate a facial expression for a certain time
        '''
        marc = Marc()

        listener = WasabiListener(marc)
        listener.start()


class Environment:
    ''' The class for the experimental environment
    '''

    def __init__(self, use_wasabi=False):
        ''' vars indicate the use of marc, wasabi and open mary
        
            Original pairs:
            (bank, 0), (card, 1), (dart, 2), (face, 3), (game, 4)
            (hand, 5), (jack, 6), (king, 7), (lamb, 8), (mask, 9)
            (neck, 0), (pipe, 1), (guip, 2), (rope, 3), (sock, 4)
            (tent, 5), (vent, 6), (wall, 7), (xray, 8), (zinc, 9)



             good_words =
             'Baum,Bank,Bett,Bein,Blatt,Bus,Busch,Band,Bild,\
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

            
        '''
        
        self.pairs = [Pair('Baum', '0'),
                      Pair('Dorf', '1'),
                      Pair('Frau', '2'),
                      Pair('Kopf', '3'),
                      Pair('Land', '4'),
                      Pair('Mond', '5'),
                      Pair('Paar', '6'),
                      Pair('Stern', '7'),
                      Pair('Wald', '8'),
                      Pair('Zahl', '9')]

        self.pairs = [Pair('Baum', '0'),
                      Pair('Frau', '2')]

        random.shuffle(self.pairs)

        self.index = 0
        self.runs = 3
        self.total_runs = self.runs

        self.logger = Logger('logfile.csv')
        self.agent = Agent(use_wasabi, self.logger)
        self.start_time = 0


    def save_start_time(self):
        self.start_time = utilities.milliseconds(datetime.datetime.now())
        self.logger.log('Start time: ' + str(self.start_time))


    def start(self):
        ''' Show init text and wait for start button.
        '''
        return self.agent.start()

    
    def present_word(self):
        if 0 <= self.index and self.index <= len(self.pairs):
            word = self.pairs[self.index].word
            number = self.pairs[self.index].number
            now = utilities.milliseconds(datetime.datetime.now())

            self.logger.log('\nTask [{0} : {1}] @ {2:.2f}s'.format(
                            word.word, number.word, (now - self.start_time)/1000))
            
            self.pairs[self.index].word_called(now)
            return self.agent.present_word(word, number)
        else:
            print 'Index Error'

    def present_number(self):
        if 0 <= self.index and self.index <= len(self.pairs):
            number = self.pairs[self.index].number
            now = utilities.milliseconds(datetime.datetime.now())
            self.pairs[self.index].number_called(now)
            self.index += 1
            return self.agent.present_number(number)
        else:
            print 'Index Error'


    def wait(self):
        ''' Waits for user input and returns current emotional status
        '''
        return self.agent.wait(self.words[self.index])

    def check(self, received):
        ''' Checks if the given word matches the current word in the list
        '''
        received = received.replace('\n', '')

        return correct

    def evaluate(self, received):
        ''' Show feedback of task and wait for next button
        '''
        correct = 0
        if received == self.pairs[self.index].number.word:
            correct = 1
                
        now = utilities.milliseconds(datetime.datetime.now())

        word = self.pairs[self.index].word
        emotion, cog, speech = self.agent.evaluate(word, correct)
        word.add(now)

        # log answer:
        time = now - word.time(0)
        self.logger.save(word.word, received, correct, time)

        return (emotion, cog, speech)


    def reset(self):
        ''' Reset the current word index to start
        '''
        self.runs = self.runs - 1
        random.shuffle(self.pairs)
        self.agent.marc.endRound(self.total_runs - self.runs)
        self.index = 0
        

    def has_next(self):
        ''' Checks if words remains to present
        '''
        if self.index <= len(self.pairs) - 1:
            return True
        return False

    def end(self):
        ''' Ends the trainig
        '''
        return ('.', 'Experiment finished')

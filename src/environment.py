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
    def __init__(self, nr, word, number):
        self.nr = nr
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
        '''
        self.pairs = [Pair(1, 'Baum', '0'),
                     Pair(2, 'Chip', '1'),
                     Pair(3, 'Dorf', '2'),
                     Pair(4, 'Frau', '3'),
                     Pair(5, 'Geld', '4'),
                     Pair(6, 'Herz', '5'),
                     Pair(7, 'Jahr', '6'),
                     Pair(8, 'Kopf', '7'),
                     Pair(9, 'Land', '8'),
                     Pair(10, 'Mond', '9'),
                     Pair(11, 'Nacht', '0'),
                     Pair(12, 'Paar', '1'),
                     Pair(13, 'Quark', '2'),
                     Pair(14, 'Rock', '3'),
                     Pair(15, 'Stuhl', '4'),
                     Pair(16, 'Schrank', '5'),
                     Pair(17, 'Tisch', '6'),
                     Pair(18, 'Vieh', '7'),
                     Pair(19, 'Wand', '8'),
                     Pair(20, 'Zelt', '9')]


        random.shuffle(self.pairs)

        self.index = 0
        self.current_run = 0
        self.total_runs = 8
        self.round_data = [[] for r in range(self.total_runs)]

        now = datetime.datetime.now()
        log_name = 'log\log-' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second) + '.csv'
        self.logger = Logger(log_name)

        self.logger.save('run', 'task','word','number','answer','correct','responsetime','timestamp')

        self.agent = Agent(use_wasabi, self.logger)
        self.start_time = 0
        self.start_time_answer = 0
        self.answer_given = False

        self.test_nr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.test_correct = 0
        self.test_nr_index = -1


    def train_number(self):
        self.test_nr_index = self.test_nr_index + 1
        self.agent.marc.subtitle(self.test_nr[self.test_nr_index])


    def check_nr(self, received):
        if received != str(self.test_nr[self.test_nr_index]):
            self.agent.marc.headNo()
            print 'received is false'
        else:
            self.agent.marc.headYes()
            self.test_correct += 1
            print 'recieved is corrrect'

    def subtitle(self, text, duration='2.0'):
        self.agent.marc.subtitle(text,duration)


    def save_start_time(self):
        self.start_time = datetime.datetime.now()
        self.agent.emo_module.wasabi.log_wasabi=True
        


    def start(self):
        ''' Show init text and wait for start button.
        '''
        return self.agent.start()

    
    def present_word(self, now):
        '''
        '''
        time_delta = now-self.start_time
        print time_delta, ': PRESENT WORD', time_delta.seconds
        
        if self.has_next():
            word = self.pairs[self.index].word
            number = self.pairs[self.index].number
            
            self.logger.log('\nTask [{0} : {1}] @ {2}s'.format(
                            word.word, number.word, time_delta))
            
            self.pairs[self.index].word_called(utilities.milliseconds(now))
            self.start_time_answer = now
            self.answer_given = False

            return self.agent.present_word(word, number)
        else:
            print 'Index Error'

    def present_number(self, now):
        '''
        '''
        time_delta = now-self.start_time
        print time_delta, ': PRESENT NR', time_delta.seconds
        # Check if answer has been given. If not evaluate.
        if not self.answer_given:
            self.logger.log('  No answer given')
            self.evaluate('-1', now)        
        
        if 0 <= self.index and self.index <= len(self.pairs):
            number = self.pairs[self.index].number
            self.pairs[self.index].number_called(utilities.milliseconds(now))
            self.index += 1

            return self.agent.present_number(number)
        else:
            print 'Index Error'


    def evaluate(self, received, now):
        ''' 
        '''
        time_delta = now-self.start_time
        print time_delta, 'EVALUATE', now-self.start_time_answer
        self.answer_given = True
        
        correct = 0
        if received == self.pairs[self.index].number.word:
            correct = 1
        elif received == '-1':
            correct = 2
                
        word = self.pairs[self.index].word
        number = self.pairs[self.index].number
        emotion, cog, speech = self.agent.evaluate(correct)

        # ADD OR ADD NOT??
        #word.add(now)
        log_correct = {0:0, 1:1, 2:0}[correct]
        time = now - self.start_time_answer
        self.round_data[self.current_run].append((correct, now-self.start_time_answer))
        self.logger.save(self.current_run, self.pairs[self.index].nr, word.word, number.word, received, log_correct, now-self.start_time_answer, now-self.start_time)

        return (emotion, cog, speech)


    def reset(self):
        ''' Reset the current word index to start
        '''
        random.shuffle(self.pairs)
        self.agent.marc.endRound(self.current_run+1)
        self.current_run = self.current_run + 1
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
        print 'Round data:', self.round_data

        # compute average:
        average_data = []

        for run in self.round_data:
            correctness = 0.0
            latency = 0.0
            for item in run:
                if item[0] == 1:
                    correctness += 1
                 
                plus = item[1].seconds
                print '+', plus
                latency += plus
                
            average_data.append((correctness / len(self.pairs), latency / len(self.pairs)))

        self.agent.emo_module.wasabi.log_wasabi=False
        print average_data
        self.subtitle('Ende Experiment', duration='20.0')
        return ('.', 'Experiment finished')

''' The environment for the trainig scenario.

    Connects the agent with the gui.

'''
import datetime
from agent import Agent
from marc import Marc
from logger import Logger
from emomodule import WasabiListener, EmoModule


class Word:
    ''' Class representing a single word from a list of words the user has to
        memorize.
    '''
    def __init__(self, word):
        self.word = word
        self.times = []

    def add(self, time):
        self.times.append(time)

    def time(self, i):
        return self.times[i]


class Environment:
    ''' The class for the experimental environment
    '''

    def __init__(self, marc=False, wasabi=False, mary=False):
        ''' vars indicate the use of marc, wasabi and open mary
        '''
        self.words = [Word('Haus'), Word('Baum'), Word('Auto')]
        import random
        random.shuffle(self.words)

        self.index = 0

        self.agent = Agent(marc, wasabi, mary)
        self.logger = Logger('logfile.csv')


    def test(self, emotion, iterations):
        ''' Simulate a facial expression for a certain time
        '''
        marc = Marc()

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

    def seconds(self, time):
        ''' Returns the given time in seconds
        '''
        return time.second + 60 * time.minute + 60 * 60 * time.hour

    def start(self):
        ''' Show init text and wait for start button.
        '''
        return self.agent.start()

    def introduce(self):
        ''' Returns the introduction text for the presentation of the list of
            words.
        '''
        return self.agent.introduce()

    def present_next(self):
        ''' Present next task. The one with index + 1
        '''
        return self.present_current()

    def present_current(self):
        ''' Presents the current task.
        '''
        now = self.seconds(datetime.datetime.now())
        # TODO: check if this line could be in one unequality
        if 0 <= self.index and self.index <= len(self.words):
            word = self.words[self.index]
            word.add(now)
            self.index += 1
            return self.agent.present(word)
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

        correct = False
        if received == self.words[self.index].word:
            correct = True

        return correct

    def evaluate(self, answer, correct):
        ''' Show feedback of task and wait for next button
        '''
        now = self.seconds(datetime.datetime.now())

        word = self.words[self.index]
        emotion, cog, speech = self.agent.evaluate(word, correct)
        word.add(now)

        # log answer:
        time = now - word.time(0)
        self.logger.save(word.word, answer, correct, time)

        if correct:
            self.index += 1
        else:
            self.reset()

        return (emotion, cog, speech)


    def reset(self):
        ''' Reset the current word index to start
        '''
        self.index = 0

    def has_next(self):
        ''' Checks if words remains to present
        '''
        if self.index <= len(self.words) - 1:
            return True
        return False

    def end(self):
        ''' Ends the trainig
        '''
        return ('.', 'Experiment finished')

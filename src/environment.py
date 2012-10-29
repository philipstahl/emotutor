''' The environment for the trainig scenario.

    Connects the agent with the gui.

'''
import datetime
from agent import Agent, ListAgent
from marc import Marc

from emomodule import WasabiListener, EmoModule


class Task:
    ''' Class representing a single task in the experimental environment
    '''
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.trials = []

    def last_trial(self):
        ''' Return the values of the last trial of the task
        '''
        return(self.trials[-1])

    def misses(self):
        ''' Counts how many times the task was answered wrong
        '''
        misses = 0
        for trial in self.trials:
            if not trial[0]:
                misses += 1
        return misses

class Word:
    ''' Class representing a single word from a list of words the user has to
        memorize.
    '''
    def __init__(self, word):
        self.word = word
        self.times = []

    def add(self, time):
        self.times.append(time)

    def time(i):
        return self.times[i]

class Environment:
    ''' The class for the experimental environment
    '''

    def __init__(self, marc=False, wasabi=False, mary=False):
        ''' vars indicate the use of marc, wasabi and open mary
        '''
        self.tasks = [Task("Auto", "Car"), Task("Haus", "House"),
                      Task("Stuhl", "Chair"), Task("Messer", "Knife")]
        self.solved_tasks = []
        self.task = None
        self.time_start = 0

        self.agent = Agent(marc, wasabi, mary)

    def test(self, emotion, iterations):
        ''' Simulate a facial expression for a certain time
        '''
        marc = Marc()

        from threading import Thread
        import socket
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_in.bind((EmoModule.WASABI_IP, EmoModule.WASABI_PORT_OUT))

        def show(emotion, iterations):
            ''' Shows iteration many times the emotion
            '''
            count = 0
            while iterations > 0:
                sock_in.recvfrom(1024)[0]
                if count >= emotion.FREQUENCE:
                    marc.perform(emotion.name, emotion.get_bml_code())
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

    def start(self):
        ''' Show init text and wait for start button.
        '''
        return self.agent.introduce()

    def present(self):
        ''' Show next task and wait for answer.
        '''
        self.task = self.tasks.pop()
        self.time_start = datetime.datetime.now().replace(microsecond=0)
        return self.agent.present(self.task)

    def evaluate(self, answer):
        ''' Show feedback of task and wait for next button
        '''
        time_end = datetime.datetime.now().replace(microsecond=0)
        time_diff = time_end - self.time_start

        solved = False
        if self.task.check(answer, time_diff.seconds):
            self.solved_tasks.append(self.task)
            solved = True
        else:
            self.tasks.insert(0, self.task)

        emotion, speech = self.agent.evaluate(self.task)
        return (emotion, speech, solved)

    def end(self):
        ''' Show final text
        '''
        return self.agent.end(self.solved_tasks)


class ListEnvironment:
    ''' The class for the experimental environment
    '''

    def __init__(self, marc=False, wasabi=False, mary=False):
        ''' vars indicate the use of marc, wasabi and open mary
        '''
        self.words = [Word('Haus'), Word('Baum'), Word('Auto'),
                      Word('Schule'), Word('Apfel'), Word('Mann'),
                      Word('Vogel'), Word('Professor'), Word('Regen')]
        import random
        random.shuffle(self.words)

        self.index = 0

        self.agent = ListAgent(marc, wasabi, mary)

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
        # TODO: check is this line could be in one unequality
        if 0 <= self.index and self.index <= len(self.words):
            word = self.words[self.index]
            word.add(self.seconds(datetime.datetime.now()))
            self.index += 1
            return self.agent.present(word)
        else:
            print 'Index Error'

    def wait(self):
        ''' Waits for user input and returns current emotional status
        '''
        print 'WAIT CALLED WITH INDEX', self.index
        return self.agent.wait(self.words[self.index])

    def check(self, received):
        ''' Checks if the given word matches the current word in the list
        '''
        received = received.replace('\n', '')

        correct = False
        if received == self.words[self.index].word:
            correct = True

        return correct

    def evaluate(self, correct):
        ''' Show feedback of task and wait for next button
        '''

        word = self.words[self.index]
        emotion, cog, speech = self.agent.evaluate(word, correct)

        word.add(self.seconds(datetime.datetime.now()))

        if correct:
            self.index += 1
        else:
            self.reset()

        return (emotion, cog, speech)


    def reset(self):
        ''' Reset the current word index to start
        '''
        print 'INDEX RESET'
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

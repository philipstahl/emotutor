''' The environment for the trainig scenario.

    Connects the agent with the gui.

'''
import datetime
from agent import Agent
from marc import Marc

from emomodule import WasabiListener, EmoModule


class Task:
    ''' Class representing a single task in the experimental environment
    '''
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.trials = []

    def check(self, answer, time):
        ''' checks if the given answer is correct
        '''
        correct = self.answer == answer
        self.trials.append((correct, time))
        return correct

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


class Environment:
    ''' The class for the experimental environment
    '''

    def __init__(self, marc=False, wasabi=False, mary=False):
        ''' vars indicate the use of marc, wasabi and open mary
        '''
        self.tasks = [Task("Car", "Auto"), Task("House", "Haus"),
                      Task("Chair", "Stuhl"), Task("Knife", "Messer")]
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

        listener = WasabiListener(EmoModule.WASABI_IP,
                                  EmoModule.WASABI_PORT_OUT, marc)
        listener.start()

    def start(self):
        ''' Show init text and wait for start button.
        '''
        return self.agent.introduce()

    def present_task(self):
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

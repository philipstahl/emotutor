''' The environment for the trainig scenario.

    Connects the agent with the gui.

'''
import datetime
from agent import Agent

MARC = False
MARY = False
WASABI = False

MARC_IP = 'localhost'
MARC_PORT_OUT = 4013
MARC_PORT_IN = 4014
WASABI_IP = '192.168.0.46'
WASABI_PORT_OUT = 42425
WASABI_PORT_IN = 42424
MARY_VOICE = 'dfki-obadiah'
MARY_IP = 'http://localhost:59125/'
MARY_PATH = 'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\'


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

    def __init__(self, marc=None, mary=None, wasabi=None):
        ''' settings must be a dict with the following keys:
                marc_ip, marc_port_in, marc_port_out, marc_emotions,
                mary_ip, mary_voice, mary_path,
                wasabi_ip, wasabi_port_in, wasabi_port_out, wasabi_emotions
        '''
        self.tasks = [Task("Car", "Auto"), Task("House", "Haus"),
                      Task("Chair", "Stuhl"), Task("Knife", "Messer")]
        self.solved_tasks = []
        self.task = None
        self.time_start = 0
        self.agent = Agent(self.tasks)
        '''
        if marc:
            self.agent.enable_marc(marc['ip'], marc['port_in'],
                                   marc['port_out'], marc['emotions'])
        if mary:
            self.agent.enable_open_mary(mary['ip'], mary['voice'], mary['path'])
        if wasabi:
            self.agent.enable_wasabi(wasabi['ip'], wasabi['port_in'],
                                     wasabi['port_out'], wasabi['emotions'])
        '''
        if MARC:
            self.agent.enable_marc(MARC_IP, MARC_PORT_IN, MARC_PORT_OUT,
                         {Emotion.JOY: MARC_JOY, Emotion.ANGER: MARC_ANGER,
                         Emotion.RELAX: MARC_RELAX})
        if MARY:
            self.agent.enable_open_mary(MARY_IP, MARY_PATH, MARY_VOICE)
        if WASABI:
            self.agent.enable_wasabi(WASABI_IP, WASABI_PORT_IN, WASABI_PORT_OUT,
                          {Emotion.JOY: WASABI_JOY, Emotion.ANGER: WASABI_ANGER,
                                       Emotion.RELAX: WASABI_RELAX})

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

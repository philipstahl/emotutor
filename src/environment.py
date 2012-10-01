''' The environment for the trainig scenario.

    Connects the agent with the gui.

'''
import datetime
from agent import Agent


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

    MARC = True
    MARY = True
    WASABI = True

    MARC_IP = 'localhost'
    MARC_PORT_OUT = 4013
    MARC_PORT_IN = 4014
    WASABI_IP = '192.168.0.46'
    WASABI_PORT_OUT = 42425
    WASABI_PORT_IN = 42424
    MARY_VOICE = 'dfki-obadiah'
    MARY_IP = 'http://localhost:59125/'
    MARY_PATH = 'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\'

    def __init__(self):
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
        self.agent = Agent()
        
        if Environment.MARC:
            self.agent.enable_marc(Environment.MARC_IP,
                                   Environment.MARC_PORT_IN,
                                   Environment.MARC_PORT_OUT)
        if Environment.MARY:
            self.agent.enable_open_mary(Environment.MARY_IP,
                                        Environment.MARY_VOICE,
                                        Environment.MARY_PATH)
        if Environment.WASABI:
            self.agent.enable_wasabi(Environment.WASABI_IP,
                                     Environment.WASABI_PORT_IN,
                                     Environment.WASABI_PORT_OUT)
        '''
        if Environment.MARC:
            Marc.IP = Environment.MARC_IP
            Marc.PORT_IN = MARC_PORT_IN
            Marc.PORT_OUT = Environment.MARC_PORT_OUT,
            Marc.JOY = Environment.MARC_JOY,
            Marc.ANGER: Environment.MARC_ANGER,
            Marc.RELAX: Environment.MARC_RELAX
        if Environment.MARY:
            OpenMary.IP = Environment.MARY_IP,
            OpenMary.PATH = Environment.MARY_PATH,
            OpenMary.VOICE = Environment.MARY_VOICE
        if Environment.WASABI:
            Wasabi.IP = Environment.WASABI_IP,
            Wasabi.PORT_IN = Environment.WASABI_PORT_IN,
            Wasabi.PORT_OUT = Environment.WASABI_PORT_OUT,
            Wasabi.JOY = Environment.WASABI_JOY,
            Wasabi.ANGER = Environment.WASABI_ANGER,
            Wasabi.Relax = Environment.WASABI_RELAX
        self.agent = Agent(self.tasks, Environment.MARC, Environment.MARY,
                           Environment.WASABI)
        '''

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

import datetime
from agent import Agent
from task import Task

class ExpEnvironment:
    def __init__(self, MARC = False):
        self.tasks = [Task("Car", "Auto"), Task("House", "Haus"),
                      Task("Chair", "Stuhl"), Task("Knife", "Messer")]
        # create needed sound files:
        '''
        tts = TextToSpeech()
        tts.save("introduction", "Welcome to the vocabulary training!")
        tts.save("positive_right", "Well done!")
        tts.save("neutral_right", "You have choosen the right answer.")
        tts.save("neutral_wrong", "Your answer is wrong")
        tts.save("negative_wrong", "Annoying. That is not the correct answer!")
        tts.save("question", "What is the german word for:")
        tts.save("chair", "Chair")
        tts.save("knife", "Knife")
        tts.save("car", "Car")
        tts.save("house", "House")
        '''
        self.solved_tasks = []        
        self.agent = Agent(self.tasks, MARC = MARC)

    ''' Show init text and wait for start button.
    '''
    def start(self):
        return self.agent.introduce()
        

    ''' Show next task and wait for answer.
    '''
    def present_task(self):        
        if len(self.tasks) > 0:
            self.task = self.tasks.pop()
            self.time_start = datetime.datetime.now().replace(microsecond=0)
            return self.agent.present(self.task)
            #answer = self.gui.write(self.agent.present(task))
            #time_end = datetime.datetime.now().replace(microsecond=0)
            #time_diff = time_end - time_start
            #self.evaluate(task, answer, time_diff.seconds)
        else:
            self.end()

    ''' Show feedback of task and wait for next button
    '''
    def evaluate(self, answer):
        time_end = datetime.datetime.now().replace(microsecond=0)
        time_diff = time_end - self.time_start


        if self.task.check(answer, time_diff.seconds):
            self.solved_tasks.append(self.task)
        else:
            self.tasks.insert(0, self.task)

        return self.agent.evaluate(self.task)

    ''' Show final text   
    '''
    def end(self):
        self.gui.write(self.agent.end(self.solved_tasks))

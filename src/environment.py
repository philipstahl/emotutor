import datetime
from agent import Agent
from task import Task

class ExpEnvironment:
    def __init__(self):
        self.tasks = [Task("Car", "Auto"), Task("House", "Haus"),
                      Task("Chair", "Stuhl"), Task("Knife", "Messer")]
        self.solved_tasks = []        
        self.agent = Agent(self.tasks)


    ''' Show init text and wait for start button.
    '''
    def start(self):
        return self.agent.introduce()
        

    ''' Show next task and wait for answer.
    '''
    def present_task(self):
        self.task = self.tasks.pop()
        self.time_start = datetime.datetime.now().replace(microsecond=0)
        return self.agent.present(self.task)
            

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
        return self.agent.end(self.solved_tasks)

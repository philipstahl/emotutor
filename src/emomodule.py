from wasabi import *

class EmoModule:


    def __init__(self, marc = None):
        self.marc = marc
        self.wasabi = Wasabi(self.marc)
        self.wasabi.start_hearing()


    ''' task evaluation according to the emotional reaction
    '''
    def check(self, task):
        correct, time = task.last_trial()
        if correct and time < 5 and task.misses() == 0:
            self.wasabi.send('happy', 100)
            #return "[very happy]"
        elif correct and time < 5:
            #return "[happy]"
            self.wasabi.send('happy', 50)
        elif correct:
            #return "[normal]"
            self.wasabi.send('happy', 10)
        elif not correct and task.misses() < 2:
            #return "[angry]"
            self.wasabi.send('angry', -50)
        else:
            #return "[very angry]"
            self.wasabi.send('angry', -100)

        return self.wasabi.get_primary_emotion()

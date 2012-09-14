class EmoModule:

    def __init__(self):
        pass
        
    def check(self, task):
        correct, time = task.last_trial()
        if correct and time < 5 and task.misses() == 0:
            return "[very happy]"
        elif correct and time < 5:
            return "[happy]"
        elif correct:
            return "[normal]"
        elif not correct and task.misses() < 2:
            return "[angry]"
        else:
            return "[very angry]"

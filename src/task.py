class Task:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.trials = []
        
    def check(self, answer, time):
        correct = self.answer == answer
        self.trials.append((correct, time))
        return correct

    def last_trial(self):
        return(self.trials[-1])

    def misses(self):
        misses = 0
        for trial in self.trials:
            if not trial[0]:
                misses += 1
        return misses

class Logger:

    def __init__(self, path):
        self.path = path
        log = open(self.path, 'w')
        log.write('Word, Answer, Correct, time\n')
        log.close()

    def save(self, word, answer, correct, sec):
        log_string = str(word) + ',' + str(answer) + ',' + str(correct) + ',' \
                   + str(sec) + ',' + '\n'

        print 'LOG', log_string
        log = open(self.path, 'a')
        if correct:
            correct = 1
        else:
            correct = 0
        log.write(log_string)
        log.close()

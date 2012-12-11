class Logger:

    def __init__(self, path, write=True):
        self.path = path
        self.exp_path = 'exp_log.txt'
        self.write = write

        if self.write:
            self.init_file(self.path)
            self.init_file(self.exp_path)


    def init_file(self, path):
        f = open(path, 'w')
        f.write('')
        f.close()

    def log(self, log_string):
        print log_string
        if not self.write:
            return
        
        exp_log = open(self.exp_path, 'a')
        exp_log.write(log_string + '\n')
        exp_log.close()


    def save(self, word, answer, correct, sec):
        if not self.write:
            return
        
        log_string = str(word) + ',' + str(answer) + ',' + str(correct) + ',' \
                   + str(sec) + '\n'

        log = open(self.path, 'a')
        if correct:
            correct = 1
        else:
            correct = 0
        log.write(log_string)
        log.close()

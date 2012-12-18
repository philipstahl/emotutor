class Logger:

    def __init__(self, path, write=True):
        self.path = path
        self.wasabi = path.split('-')[0] + 'wasabi_' + path.split('-')[1]
        
        self.exp_path = path.split('-')[0] + 'messages_' + path.split('-')[1]
        self.write = write

        if self.write:
            self.init_file(self.path)
            self.init_file(self.exp_path)
            self.init_file(self.wasabi)


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


    def save(self, run, nr, word, number, answer, correct, sec, timestamp):
        if not self.write:
            return
        
        log_string = str(run)+ ',' + str(nr) + ',' + str(word) + ',' + str(number) + ',' + str(answer) + ',' + str(correct) + ',' \
                   + str(sec) + ',' + str(timestamp) + '\n'

        log = open(self.path, 'a')
        log.write(log_string)
        log.close()

    def save_wasabi(self, text):
        log = open(self.wasabi, 'a')
        log.write(text + '\n')
        log.close()

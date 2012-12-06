from dragonfly.all import Grammar, CompoundRule

# Voice command rule combining spoken form and recognition processing.
class ExampleRule(CompoundRule):
    spec = "do something computer"                  # Spoken form of command.
    print 'Command created'
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        print "Voice command spoken."

class NumberNullRule(CompoundRule):
    spec = "0"

    def __init__(self, function):
        super(NumberNullRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(0)
        print "Null spoken."

class NumberOneRule(CompoundRule):
    spec = "1"

    def __init__(self, function):
        super(NumberOneRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(1)
        print "Eins spoken."
        
class NumberTwoRule(CompoundRule):
    spec = "2"
    
    def __init__(self, function):
        super(NumberTwoRule, self).__init__()
        self.function = function
                      
    def _process_recognition(self, node, extras):
        self.function(2)
        print "Zwei spoken."

class NumberThreeRule(CompoundRule):
    spec = "3"

    def __init__(self, function):
        super(NumberThreeRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(3)
        print "Drei spoken."

class NumberFourRule(CompoundRule):
    spec = "4"

    def __init__(self, function):
        super(NumberFourRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(4)
        print "4 spoken."

class NumberFiveRule(CompoundRule):
    spec = "5"

    def __init__(self, function):
        super(NumberFiveRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(5)
        print "5 spoken"

class NumberSixRule(CompoundRule):
    spec = "6"

    def __init__(self, function):
        super(NumberSixRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(6)
        print "6 spoken."

class NumberSevenRule(CompoundRule):
    spec = "7"

    def __init__(self, function):
        super(NumberSevenRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(7)
        print "Sieben spoken."

class NumberEightRule(CompoundRule):
    spec = "8"

    def __init__(self, function):
        super(NumberEightRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(8)
        print "Acht spoken."

class NumberNineRule(CompoundRule):
    spec = "9"

    def __init__(self, function):
        super(NumberNineRule, self).__init__()
        self.function = function
        
    def _process_recognition(self, node, extras):
        self.function(9)
        print "Neun spoken."

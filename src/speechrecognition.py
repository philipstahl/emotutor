# -*- coding: utf-8 -*-

from dragonfly.all import Grammar, CompoundRule

# Voice command rule combining spoken form and recognition processing.
class ExampleRule(CompoundRule):
    spec = "do something computer"                  # Spoken form of command.
    print 'Command created'
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        print "Voice command spoken."



class NumberNullRule(CompoundRule):
    spec = "null"                  
    def _process_recognition(self, node, extras):
        print "Null spoken."

class NumberOneRule(CompoundRule):
    spec = "eins"                  
    def _process_recognition(self, node, extras):
        print "Eins spoken."
        
class NumberTwoRule(CompoundRule):
    spec = "zwei"                  
    def _process_recognition(self, node, extras):
        print "Zwei spoken."

class NumberThreeRule(CompoundRule):
    spec = "drei"                  
    def _process_recognition(self, node, extras):
        print "Drei spoken."

class NumberFourRule(CompoundRule):
    spec = "4"                  
    def _process_recognition(self, node, extras):
        print "4 spoken."

class NumberFiveRule(CompoundRule):
    spec = "5"                  
    def _process_recognition(self, node, extras):
        print "5 spoken"

class NumberSixRule(CompoundRule):
    spec = "6"                  
    def _process_recognition(self, node, extras):
        print "6 spoken."

class NumberSevenRule(CompoundRule):
    spec = "sieben"                  
    def _process_recognition(self, node, extras):
        print "Sieben spoken."

class NumberEightRule(CompoundRule):
    spec = "acht"                  
    def _process_recognition(self, node, extras):
        print "Acht spoken."

class NumberNineRule(CompoundRule):
    spec = "neun"                  
    def _process_recognition(self, node, extras):
        print "Neun spoken."

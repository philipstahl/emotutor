from globalsettings import *

class Expression:
    def __init__(self, name, wait = 0.0, intensity = 1.0, interpolate = 1.0):
        self.name = name
        self.wait = wait
        self.intensity = intensity
        self.interpolate = interpolate

    def getBMLCode(self):
        return "<bml id=\"Perform{0}\"> \
                <marc:fork id=\"Show_{1}_fork_1\"> \
                <wait duration=\"{2}\" /> \
                <face id=\"bml_item_2\" > \
                <description level=\"1\" type=\"marcbml\"> \
                <facial_animation name=\"{3}\" \
                    interpolate=\"{4}\" \
                    loop=\"false\"  \
                    intensity=\"{5}\" /> \
                </description> </face> </marc:fork> \
                </bml>".format(self.name, self.name, self.wait, self.name,
                               self.interpolate, self.intensity)

class Anger(Expression):
    def __init__(self):
        Expression.__init__(self, ANGER)
        self.name = ANGER

class Joy(Expression):
    def __init__(self):
        Expression.__init__(self, JOY)
        self.name = JOY
        
class Relax(Expression):
    def __init__(self):
        Expression.__init__(self, RELAX)
        self.name = RELAX

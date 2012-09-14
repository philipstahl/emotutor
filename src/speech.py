class Speech:
    def __init__(self, name):
        self.name = name

    #<speech id=\"bml_item_2\"  marc:file=\"C:\\Program Files\\LIMSI\\MARC\\10.4.0\\{1}.wav\" marc:articulate=\"0.4\" /> \
    def getBMLCode(self):
        return "<bml id=\"Perform{0}\"> \
               <marc:fork id=\"Track_0_fork_2\"> \
               <wait duration=\"0.00\" /> \
               <speech id=\"bml_item_2\"  marc:file=\"C:\\Users\\User\\Desktop\\MARC_python\\sounds\\{1}.wav\" marc:articulate=\"0.4\" /> \
               </marc:fork></bml>".format(self.name, self.name)


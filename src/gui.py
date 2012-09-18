'''
import optparse

class Gui:
    def __init__(self):
        pass

    def write(self, text):
        var = raw_input(text)
        return var
'''

from PyQt4 import QtCore, QtGui

from environment import *

class VocabTrainer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(VocabTrainer, self).__init__(parent)

        self.agentOutput = QtGui.QLabel('')
        self.userInput = QtGui.QLineEdit()
        self.userInput.hide()

        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.hide()

        self.nextButton = QtGui.QPushButton("&Start")
        self.nextButton.show()

        self.submitButton.clicked.connect(self.submit)
        self.nextButton.clicked.connect(self.next)        

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.agentOutput, 0, 0)
        mainLayout.addWidget(self.userInput, 1, 0, )
        mainLayout.addWidget(self.submitButton, 1, 1)
        mainLayout.addWidget(self.nextButton,1,1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Vocabulary Trainer")
        self.center()

        self.exp = ExpEnvironment(MARC = False)
        self.agentOutput.setText(self.exp.start())

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


    def submit(self):
        answer = self.userInput.text()
        
        if answer == "":
            QtGui.QMessageBox.information(self, "Empty Field",
                    "Please enter a name and address.")
            return
        
        self.agentOutput.setText(self.exp.evaluate(answer))
        self.submitButton.hide()
        self.userInput.setReadOnly(True)
        self.nextButton.show()

    def next(self):
        if self.userInput.isHidden():
            self.nextButton.setText("Next")
            self.userInput.show()

        self.agentOutput.setText(self.exp.present_task())
        self.nextButton.hide()
        self.userInput.setText('')
        self.userInput.setReadOnly(False)
        self.submitButton.show()


    def cancel(self):
        '''
        self.nameLine.setText(self.oldName)
        self.nameLine.setReadOnly(True)

        self.addressText.setText(self.oldAddress)
        self.addressText.setReadOnly(True)

        self.addButton.setEnabled(True)
        self.submitButton.hide()
        self.cancelButton.hide()
        '''
        pass


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    addressBook = VocabTrainer()
    addressBook.show()

    sys.exit(app.exec_())

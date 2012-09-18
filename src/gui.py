from PyQt4 import QtCore, QtGui

from environment import *

class VocabTrainer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(VocabTrainer, self).__init__(parent)

        self.resize(600, 100)

        self.labelEmoOutput = QtGui.QLabel('Emotional Output:')
        self.labelSpeechOutput = QtGui.QLabel('Speech Output:')

        self.labelEmoOutput.width = 100
        self.labelSpeechOutput.width = 100

        self.emoOutput = QtGui.QLabel('')
        self.speechOutput = QtGui.QLabel('')

        self.userInput = QtGui.QLineEdit()
        self.userInput.hide()

        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.resize(100, 20)
        self.submitButton.hide()

        self.nextButton = QtGui.QPushButton("&Start")
        self.nextButton.resize(100,20)        
        self.nextButton.show()

        self.submitButton.clicked.connect(self.submit)
        self.nextButton.clicked.connect(self.next)        

        mainLayout = QtGui.QGridLayout()
        # column 0
        mainLayout.addWidget(self.labelEmoOutput, 0, 0)
        mainLayout.addWidget(self.labelSpeechOutput, 1, 0)
        # column 1
        mainLayout.addWidget(self.emoOutput, 0, 1)
        mainLayout.addWidget(self.speechOutput, 1, 1)
        # column 2
        mainLayout.addWidget(self.userInput, 2, 1, )
        mainLayout.addWidget(self.submitButton, 2, 2)
        mainLayout.addWidget(self.nextButton,2,2)

        mainLayout.setColumnMinimumWidth(0, 100)
        mainLayout.setColumnMinimumWidth(1, 400)
        mainLayout.setColumnMinimumWidth(2, 100)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Vocabulary Trainer")
        self.center()

        self.exp = ExpEnvironment()
        emotion, speech = self.exp.start()        
        self.emoOutput.setText(emotion)
        self.speechOutput.setText(speech)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


    def submit(self):
        answer = self.userInput.text()
        
        if answer == "":
            QtGui.QMessageBox.information(self, "Empty Field",
                    "Please enter a word")
            return
        
        emotion, speech = self.exp.evaluate(answer) 
        self.emoOutput.setText(emotion)
        self.speechOutput.setText(speech)

        self.submitButton.hide()
        self.userInput.setReadOnly(True)
        self.nextButton.show()

    def next(self):
        if self.userInput.isHidden():
            self.nextButton.setText("Next")
            self.userInput.show()

        if len(self.exp.tasks) == 0:
            self.end()
        else:
            emotion, speech = self.exp.present_task()
                
            self.emoOutput.setText(emotion)
            self.speechOutput.setText(speech)

            self.nextButton.hide()
            self.userInput.setText('')
            self.userInput.setReadOnly(False)
            self.submitButton.show()

    def end(self):
        emotion, speech = self.exp.end()
        self.emoOutput.setText(emotion)
        self.speechOutput.setText(speech)

        self.nextButton.hide()
        self.userInput.setText('')
        self.userInput.hide()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            if ((self.userInput.isHidden()
                 and not self.nextButton.isHidden()) or
               (not self.userInput.isHidden() and self.userInput.isReadOnly())):
                self.next()
            elif (not self.userInput.isHidden() and
                  not self.userInput.isReadOnly()):
                self.submit()
            

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    addressBook = VocabTrainer()
    addressBook.show()

    sys.exit(app.exec_())

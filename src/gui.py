import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from environment import *
from globalsettings import *


class VocabTrainer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(VocabTrainer, self).__init__(parent)
        # Create widgets:
        labelEmoOutput = QtGui.QLabel('Emotional Output:')
        labelSpeechOutput = QtGui.QLabel('Speech Output:')

        self.emoOutput = QtGui.QLabel('')
        self.speechOutput = QtGui.QLabel('')

        self.userInput = QtGui.QLineEdit()
        self.userInput.hide()

        self.labelSolution = QtGui.QLabel('')
        self.labelSolution.show()

        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.hide()

        self.nextButton = QtGui.QPushButton("&Start")
        self.nextButton.show()

        # Define button functionality:
        self.submitButton.clicked.connect(self.submit)
        self.nextButton.clicked.connect(self.next)

        # Design layout:
        agentLayout = QtGui.QGridLayout()
        agentLayout.addWidget(labelEmoOutput, 0, 0)
        agentLayout.addWidget(self.emoOutput, 0, 1)
        agentLayout.addWidget(labelSpeechOutput, 1, 0)
        agentLayout.addWidget(self.speechOutput, 1, 1)

        agentLayout.setColumnMinimumWidth(0, 100)
        agentLayout.setColumnMinimumWidth(1, 500)

        agent = QtGui.QWidget()
        agent.setLayout(agentLayout)

        userLayout = QtGui.QGridLayout()
        userLayout.addWidget(self.userInput, 0, 0)
        userLayout.addWidget(self.submitButton, 0, 1)
        userLayout.addWidget(self.nextButton, 0, 1)
        userLayout.addWidget(self.labelSolution, 1, 0)
        userLayout.setColumnMinimumWidth(0, 500)
        userLayout.setColumnMinimumWidth(1, 100)

        user = QtGui.QWidget()
        user.setLayout(userLayout)

        mainLayout = QtGui.QBoxLayout(2)
        mainLayout.addWidget(agent)
        mainLayout.addWidget(user)

        self.setLayout(mainLayout)
        self.resize(600, 200)

        # Setup experimental environment:
        self.exp = ExpEnvironment()
        emotion, speech = self.exp.start()
        self.emoOutput.setText(emotion)
        self.speechOutput.setText(speech)

    def submit(self):
        answer = self.userInput.text()

        if answer == "":
            QtGui.QMessageBox.information(self, "Empty Field",
                    "Please enter a word")
            return

        emotion, speech, solved = self.exp.evaluate(answer)

        if solved:
            self.userInput.setStyleSheet('QLineEdit {color: green}')
        else:
            self.userInput.setStyleSheet('QLineEdit {color: red}')
            self.labelSolution.setText(self.exp.tasks[0].answer)

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

            self.labelSolution.setText('')
            self.nextButton.hide()
            self.userInput.setStyleSheet('QLineEdit {color: black}')
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
               (not self.userInput.isHidden()
                and self.userInput.isReadOnly())):
                self.next()
            elif (not self.userInput.isHidden() and
                  not self.userInput.isReadOnly()):
                self.submit()


class Settings(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        # Create widgets:
        labelUDP = QtGui.QLabel('UDP Communication:')
        labelUDP.setStyleSheet('QLabel {font-weight:bold}')

        labelIP = QtGui.QLabel('IP:')
        labelInputPort = QtGui.QLabel('Input Port:')
        labelOutputPort = QtGui.QLabel('Output Port:')

        labelEmotions = QtGui.QLabel('Emotions:')
        labelEmotions.setStyleSheet('QLabel {font-weight:bold}')
        labelAnger = QtGui.QLabel('Anger:')
        labelRelax = QtGui.QLabel('Relax:')
        labelJoy = QtGui.QLabel('Joy:')

        labelMary = QtGui.QLabel('MARY:')
        labelMary.setStyleSheet('QLabel {font-weight:bold}')
        labelVoice = QtGui.QLabel('Voice:')

        self.inputIP = QtGui.QLineEdit(UDP_IP)
        self.inputInputPort = QtGui.QLineEdit(str(UDP_PORT_IN))
        self.inputOutputPort = QtGui.QLineEdit(str(UDP_PORT_OUT))

        self.inputAnger = QtGui.QLineEdit(ANGER)
        self.inputRelax = QtGui.QLineEdit(RELAX)
        self.inputJoy = QtGui.QLineEdit(JOY)

        self.inputVoice = QtGui.QLineEdit(VOICE)

        self.buttonSave = QtGui.QPushButton("&Save")
        self.buttonReset = QtGui.QPushButton("&Reset")
        self.buttonCancel = QtGui.QPushButton("&Cancel")

        # Define button functionality:
        self.buttonSave.clicked.connect(self.save)
        self.buttonReset.clicked.connect(self.reset)
        self.buttonCancel.clicked.connect(self.cancel)

        # Design layout:
        settingsLayout = QtGui.QGridLayout()

        # column 0
        settingsLayout.addWidget(labelUDP, 0, 0)
        settingsLayout.addWidget(labelIP, 1, 0)
        settingsLayout.addWidget(labelInputPort, 2, 0)
        settingsLayout.addWidget(labelOutputPort, 3, 0)
        settingsLayout.addWidget(labelEmotions, 4, 0)
        settingsLayout.addWidget(labelAnger, 5, 0)
        settingsLayout.addWidget(labelRelax, 6, 0)
        settingsLayout.addWidget(labelJoy, 7, 0)
        settingsLayout.addWidget(labelMary, 8, 0)
        settingsLayout.addWidget(labelVoice, 9, 0)

        # column 1
        settingsLayout.addWidget(self.inputIP, 1, 1)
        settingsLayout.addWidget(self.inputInputPort, 2, 1)
        settingsLayout.addWidget(self.inputOutputPort, 3, 1)
        settingsLayout.addWidget(self.inputAnger, 5, 1)
        settingsLayout.addWidget(self.inputRelax, 6, 1)
        settingsLayout.addWidget(self.inputJoy, 7, 1)
        settingsLayout.addWidget(self.inputVoice, 9, 1)

        buttonLayout = QtGui.QBoxLayout(0)          # 0 = LeftToRight
        buttonLayout.addWidget(self.buttonCancel)
        buttonLayout.addWidget(self.buttonReset)
        buttonLayout.addWidget(self.buttonSave)

        buttons = QtGui.QWidget()
        buttons.setLayout(buttonLayout)

        values = QtGui.QWidget()
        values.setLayout(settingsLayout)

        mainLayout = QtGui.QBoxLayout(2)
        mainLayout.addWidget(values)
        mainLayout.addWidget(buttons)
        self.setLayout(mainLayout)
        self.resize(600, 100)

    def save(self):
        #MARC = False
        #MARY = False

        global UDP_IP
        global UDP_PORT_OUT
        global UDP_PORT_IN
        global ANGER
        global JOY
        global RELAX
        global VOICE

        UDP_IP = self.inputIP.text()
        UDP_PORT_OUT = int(self.inputInputPort.text())
        UDP_PORT_IN = int(self.inputOutputPort.text())

        JOY = self.inputJoy.text()
        RELAX = self.inputRelax.text()
        ANGER = self.inputAnger.text()

        VOICE = self.inputVoice.text()
        self.emit(SIGNAL('quit'))

    def cancel(self):
        self.emit(SIGNAL("quit"))

    def reset(self):
        self.inputIP.setText('localhost')
        self.inputInputPort.setText('4013')
        self.inputOutputPort.setText('4014')

        self.inputAnger.setText('CASA_Anger_01')
        self.inputRelax.setText('CASA_Relax_01')
        self.inputJoy.setText('CASA_Joy_01')

        self.inputVoice.setText('dfki-obadiah')


class Welcome(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Welcome, self).__init__(parent)

        # Create widgets:
        desc = QtGui.QLabel('Welcome to the vocabulary trainer.')

        buttonSettings = QtGui.QPushButton("&Edit settings")
        buttonStart = QtGui.QPushButton('&Start training')

        # Define button funcionalty:
        buttonSettings.clicked.connect(self.options)
        buttonStart.clicked.connect(self.start)

        # Design Layout:
        optionLayout = QtGui.QBoxLayout(0)
        optionLayout.addWidget(buttonSettings)
        optionLayout.addWidget(buttonStart)
        options = QtGui.QWidget()
        options.setLayout(optionLayout)

        mainLayout = QtGui.QBoxLayout(2)
        mainLayout.addWidget(desc)
        mainLayout.addWidget(options)
        self.setLayout(mainLayout)
        self.resize(600, 100)

    def options(self):
        self.emit(SIGNAL('settings'))

    def start(self):
        self.emit(SIGNAL('training'))


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(600, 400)
        self.setWindowTitle('Vocabulary Trainer')

        new = QtGui.QAction(QtGui.QIcon('icons/icon.png'), 'New training',
                                        self)
        self.connect(new, QtCore.SIGNAL('triggered()'), self.showTraining)

        exit = QtGui.QAction(QtGui.QIcon('icons/icon.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'),
                     QtCore.SLOT('close()'))

        settings = QtGui.QAction(QtGui.QIcon('icons/icon.png'),
                                 'Settings', self)
        self.connect(settings, QtCore.SIGNAL('triggered()'), self.showOptions)

        self.statusBar()

        menubar = self.menuBar()

        menuFile = menubar.addMenu('&File')
        menuFile.addAction(new)
        menuFile.addAction(exit)

        options = menubar.addMenu('&Options')
        options.addAction(settings)

        self.setMenuBar(menubar)
        self.showWelcome()
        self.center()

    def showWelcome(self):
        welcome = Welcome()
        self.connect(welcome, SIGNAL('settings'), self.showOptions)
        self.connect(welcome, SIGNAL('training'), self.showTraining)
        welcome.show()
        self.setCentralWidget(welcome)

    def showOptions(self):
        settings = Settings()
        self.connect(settings, SIGNAL("quit"), self.showWelcome)
        settings.show()
        self.setCentralWidget(settings)

    def showTraining(self):
        trainer = VocabTrainer()
        trainer.show()
        self.setCentralWidget(trainer)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

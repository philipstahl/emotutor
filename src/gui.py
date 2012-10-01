''' The gui implimentation in pyqt4
'''

import sys
import PyQt4.QtGui
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, \
                        QBoxLayout, QMainWindow, QAction, QIcon, \
                        QApplication, QDesktopWidget, QMessageBox
import PyQt4.QtCore
from PyQt4.QtCore import SIGNAL, Qt

from environment import Environment
from emomodule import Emotion


class VocabTrainer(QWidget):
    ''' Gui for a simple vocabulary trainer
    '''
    def __init__(self, parent=None):
        super(VocabTrainer, self).__init__(parent)
        # Create widgets:
        label_emo_output = QLabel('Emotional Output:')
        label_speech_output = QLabel('Speech Output:')

        self.emo_output = QLabel('')
        self.speech_output = QLabel('')

        self.user_input = QLineEdit()
        self.user_input.hide()

        self.label_solution = QLabel('')
        self.label_solution.show()

        self.submit_button = QPushButton("&Submit")
        self.submit_button.hide()

        self.next_button = QPushButton("&Start")
        self.next_button.show()

        # Define button functionality:QtCore
        self.submit_button.clicked.connect(self.submit)
        self.next_button.clicked.connect(self.next)

        # Design layout:
        agent_layout = QGridLayout()
        agent_layout.addWidget(label_emo_output, 0, 0)
        agent_layout.addWidget(self.emo_output, 0, 1)
        agent_layout.addWidget(label_speech_output, 1, 0)
        agent_layout.addWidget(self.speech_output, 1, 1)

        agent_layout.setColumnMinimumWidth(0, 100)
        agent_layout.setColumnMinimumWidth(1, 500)

        agent = QWidget()
        agent.setLayout(agent_layout)

        user_layout = QGridLayout()
        user_layout.addWidget(self.user_input, 0, 0)
        user_layout.addWidget(self.submit_button, 0, 1)
        user_layout.addWidget(self.next_button, 0, 1)
        user_layout.addWidget(self.label_solution, 1, 0)
        user_layout.setColumnMinimumWidth(0, 500)
        user_layout.setColumnMinimumWidth(1, 100)

        user = QWidget()
        user.setLayout(user_layout)

        main_layout = QBoxLayout(2)
        main_layout.addWidget(agent)
        main_layout.addWidget(user)

        self.setLayout(main_layout)
        self.resize(600, 200)

        # Setup experimental environment:
        #self.exp = Environment(marc = settings_marc, mary = settings_mary,
        #                           wasabi = settings_wasabi)
        self.exp = Environment()

        emotion, speech = self.exp.start()
        self.emo_output.setText(emotion)
        self.speech_output.setText(speech)

    def submit(self):
        ''' Submit an answer by the user
        '''
        answer = self.user_input.text()

        if answer == "":
            QMessageBox.information(self, "Empty Field",
                    "Please enter a word")
            return

        emotion, speech, solved = self.exp.evaluate(answer)

        if solved:
            self.user_input.setStyleSheet('QLineEdit {color: green}')
        else:
            self.user_input.setStyleSheet('QLineEdit {color: red}')
            self.label_solution.setText(self.exp.tasks[0].answer)

        self.emo_output.setText(emotion)
        self.speech_output.setText(speech)

        self.submit_button.hide()
        self.user_input.setReadOnly(True)
        self.next_button.show()

    def next(self):
        ''' Show next task
        '''
        if self.user_input.isHidden():
            self.next_button.setText("Next")
            self.user_input.show()

        if len(self.exp.tasks) == 0:
            self.end()
        else:
            emotion, speech = self.exp.present_task()

            self.emo_output.setText(emotion)
            self.speech_output.setText(speech)

            self.label_solution.setText('')
            self.next_button.hide()
            self.user_input.setStyleSheet('QLineEdit {color: black}')
            self.user_input.setText('')
            self.user_input.setReadOnly(False)
            self.submit_button.show()

    def end(self):
        ''' End vocabulary test
        '''
        emotion, speech = self.exp.end()
        self.emo_output.setText(emotion)
        self.speech_output.setText(speech)

        self.next_button.hide()
        self.user_input.setText('')
        self.user_input.hide()

    def keyPressEvent(self, event):
        ''' Handles key events
        '''
        if event.key() == Qt.Key_Return:
            if ((self.user_input.isHidden()
                 and not self.next_button.isHidden()) or
               (not self.user_input.isHidden()
                and self.user_input.isReadOnly())):
                self.next()
            elif (not self.user_input.isHidden() and
                  not self.user_input.isReadOnly()):
                self.submit()


class Settings(QWidget):
    ''' Frame showing all program settings
    '''

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        self.marc_settings = \
            {'ip': QLineEdit(Environment.MARC_IP),
             'port_in': QLineEdit(str(Environment.MARC_PORT_IN)),
             'port_out': QLineEdit(str(Environment.MARC_PORT_OUT)),
             'anger': QLineEdit(Emotion.MARC_ANGER),
             'relax': QLineEdit(Emotion.MARC_RELAX),
             'joy': QLineEdit(Emotion.MARC_JOY)}

        self.wasabi_settings = \
            {'ip': QLineEdit(Environment.WASABI_IP),
             'port_in': QLineEdit(str(Environment.WASABI_PORT_IN)),
             'port_out': QLineEdit(str(Environment.WASABI_PORT_OUT)),
             'anger': QLineEdit(Emotion.WASABI_ANGER),
             'relax': QLineEdit(Emotion.WASABI_RELAX),
             'joy':QLineEdit(Emotion.WASABI_JOY)}

        self.mary_settings = \
            {'ip': QLineEdit(Environment.MARY_IP),
             'voice': QLineEdit(Environment.MARY_VOICE),
             'path': QLineEdit(Environment.MARY_PATH)}


        self.setLayout(self.init_ui())
        self.resize(600, 100)

    def init_ui(self):
        ''' Creates the layout of the settings screen
        '''
        layout1 = QGridLayout()

        layout1.addWidget(QLabel('MARC:'), 0, 1)
        layout1.addWidget(QLabel('WASABI:'), 0, 2)

        label_network = QLabel('Network:')
        label_network.setStyleSheet('QLabel {font-weight:bold}')
        layout1.addWidget(label_network, 1, 0)

        layout1.addWidget(QLabel('IP:'), 2, 0)
        layout1.addWidget(self.marc_settings['ip'], 2, 1)
        layout1.addWidget(self.wasabi_settings['ip'], 2, 2)

        layout1.addWidget(QLabel('Input Port:'), 3, 0)
        layout1.addWidget(self.marc_settings['port_in'], 3, 1)
        layout1.addWidget(self.wasabi_settings['port_in'], 3, 2)

        layout1.addWidget(QLabel('Output Port:'), 4, 0)
        layout1.addWidget(self.marc_settings['port_out'], 4, 1)
        layout1.addWidget(self.wasabi_settings['port_out'], 4, 2)

        label_emotions = QLabel('Emotions:')
        label_emotions.setStyleSheet('QLabel {font-weight:bold}')
        layout1.addWidget(label_emotions, 5, 0)

        layout1.addWidget(QLabel('Anger:'), 6, 0)
        layout1.addWidget(self.marc_settings['anger'], 6, 1)
        layout1.addWidget(self.wasabi_settings['anger'], 6, 2)

        layout1.addWidget(QLabel('Relax:'), 7, 0)
        layout1.addWidget(self.marc_settings['relax'], 7, 1)
        layout1.addWidget(self.wasabi_settings['relax'], 7, 2)

        layout1.addWidget(QLabel('Joy:'), 8, 0)
        layout1.addWidget(self.marc_settings['joy'], 8, 1)
        layout1.addWidget(self.wasabi_settings['joy'], 8, 2)

        values = QWidget()
        values.setLayout(layout1)

        # Open Mary:
        label_mary = QLabel('Open Mary:')
        label_mary.setStyleSheet('QLabel {font-weight:bold}')

        layout_mary = QGridLayout()
        layout_mary.addWidget(label_mary, 0, 0)
        layout_mary.addWidget(QLabel('Request:'), 1, 0)
        layout_mary.addWidget(QLabel('Voice:'), 2, 0)
        layout_mary.addWidget(QLabel('Path:'), 3, 0)
        layout_mary.addWidget(self.mary_settings['ip'], 1, 1)
        layout_mary.addWidget(self.mary_settings['voice'], 2, 1)
        layout_mary.addWidget(self.mary_settings['path'], 3, 1)
        widget_mary = QWidget()
        widget_mary.setLayout(layout_mary)

        # Define button functionality:
        button_save = QPushButton("&Save")
        button_reset = QPushButton("&Reset")
        button_cancel = QPushButton("&Cancel")

        button_save.clicked.connect(self.save)
        button_reset.clicked.connect(self.reset)
        button_cancel.clicked.connect(self.cancel)

        button_layout = QBoxLayout(0)
        button_layout.addWidget(button_cancel)
        button_layout.addWidget(button_reset)
        button_layout.addWidget(button_save)

        buttons = QWidget()
        buttons.setLayout(button_layout)

        main_layout = QBoxLayout(2)
        main_layout.addWidget(values)
        main_layout.addWidget(widget_mary)
        main_layout.addWidget(buttons)
        return main_layout

    def save(self):
        ''' Save changed settings
        '''
        Environment.MARC_IP = self.marc_settings['ip'].text()
        Environment.MARC_PORT_OUT = self.marc_settings['port_out'].text()
        Environment.MARC_PORT_IN = self.marc_settings['port_in'].text()
        Environment.WASABI_IP = self.wasabi_settings['ip'].text()
        Environment.WASABI_PORT_IN = self.wasabi_settings['port_in'].text()
        Environment.WASABI_PORT_OUT = self.wasabi_settings['port_out'].text()
        Environment.MARY_VOICE = self.mary_settings['voice'].text()
        Environment.MARY_IP = self.mary_settings['ip'].text()
        Environment.MARY_PATH = self.mary_settings['path'].text()
        Emotion.WASABI_JOY = self.wasabi_settings['joy'].text()
        Emotion.WASABI_ANGER = self.wasabi_settings['anger'].text()
        Emotion.WASABI_RELAX = self.wasabi_settings['relax'].text()
        Emotion.MARC_JOY = self.marc_settings['joy'].text()
        Emotion.MARC_RELAX = self.marc_settings['relax'].text()
        Emotion.MARC_ANGER = self.marc_settings['anger'].text()

        self.emit(SIGNAL('quit'))

    def cancel(self):
        ''' Exit settings without saving
        '''
        self.emit(SIGNAL("quit"))

    def reset(self):
        ''' Reset settins to original values

        '''
        self.marc_settings['ip'].setText('localhost')
        self.marc_settings['port_in'].setText('4014')
        self.marc_settings['port_out'].setText('4013')
        self.marc_settings['anger'].setText('CASA_Anger_01')
        self.marc_settings['relax'].setText('CASA_Relax_01')
        self.marc_settings['joy'].setText('CASA_Joy_01')

        self.wasabi_settings['ip'].setText('192.168.0.46')
        self.wasabi_settings['port_in'].setText('42424')
        self.wasabi_settings['port_out'].setText('42425')
        self.wasabi_settings['anger'].setText('happy')
        self.wasabi_settings['relax'].setText('happy')
        self.wasabi_settings['joy'].setText('angry')

        self.mary_settings['ip'].setText('http://localhost:59125/')
        self.mary_settings['voice'].setText('dfki-obadiah')
        self.mary_settings['path'].setText(
                            'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\')


class Welcome(QWidget):
    ''' Frame at the start of the vocabulary trainer
    '''
    def __init__(self, parent=None):
        super(Welcome, self).__init__(parent)

        # Create widgets:
        desc = QLabel('Welcome to the vocabulary trainer.')

        button_settings = QPushButton("&Edit settings")
        button_start = QPushButton('&Start training')

        # Define button funcionalty:
        button_settings.clicked.connect(self.options)
        button_start.clicked.connect(self.start)

        # Design Layout:
        option_layout = QBoxLayout(0)
        option_layout.addWidget(button_settings)
        option_layout.addWidget(button_start)
        options = QWidget()
        options.setLayout(option_layout)

        main_layout = QBoxLayout(2)
        main_layout.addWidget(desc)
        main_layout.addWidget(options)
        self.setLayout(main_layout)
        self.resize(600, 100)

    def options(self):
        ''' Show options
        '''
        self.emit(SIGNAL('settings'))

    def start(self):
        ''' Start test
        '''
        self.emit(SIGNAL('training'))


class MainWindow(QMainWindow):
    ''' Main window of the vocabulary trainer
    '''

    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(600, 400)
        self.setWindowTitle('Vocabulary Trainer')

        new = QAction(QIcon('icons/icon.png'), 'New training',
                                        self)
        self.connect(new, SIGNAL('triggered()'), self.show_training)

        settings = QAction(QIcon('icons/icon.png'),
                                 'Settings', self)
        self.connect(settings, SIGNAL('triggered()'), self.show_options)

        self.statusBar()

        menubar = self.menuBar()

        menuFile = menubar.addMenu('&File')
        menuFile.addAction(new)

        options = menubar.addMenu('&Options')
        options.addAction(settings)

        self.setMenuBar(menubar)
        self.show_welcome()
        self.center()

    def show_welcome(self):
        ''' Shows the welcome screen
        '''
        welcome = Welcome()
        self.connect(welcome, SIGNAL('settings'), self.show_options)
        self.connect(welcome, SIGNAL('training'), self.show_training)
        welcome.show()
        self.setCentralWidget(welcome)

    def show_options(self):
        ''' Shows the option screen
        '''
        settings = Settings()
        self.connect(settings, SIGNAL("quit"), self.show_welcome)
        settings.show()
        self.setCentralWidget(settings)

    def show_training(self):
        ''' Starts the training

        '''
        trainer = VocabTrainer()
        trainer.show()
        self.setCentralWidget(trainer)

    def center(self):
        ''' Centers the current window
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    MAIN = MainWindow()
    MAIN.show()
    sys.exit(APP.exec_())

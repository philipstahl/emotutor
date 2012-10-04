''' The gui implimentation in pyqt4
'''

import sys
import PyQt4.QtGui
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, \
                        QBoxLayout, QMainWindow, QAction, QIcon, \
                        QApplication, QDesktopWidget, QMessageBox, QDoubleSpinBox, QSpinBox
import PyQt4.QtCore
from PyQt4.QtCore import SIGNAL, Qt

from environment import Environment
from emomodule import EmoModule, Happy, Concentrated, Bored, Annoyed, Angry


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

        wasabi      ->  emotion  intensity  interpolate  hz/trigger
        happy           
        concentrated    
        bored
        annoyed
        angry
    '''

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        self.marc_settings = \
            {'ip': QLineEdit(Environment.MARC_IP),
             'port_in': QLineEdit(str(Environment.MARC_PORT_IN)),
             'port_out': QLineEdit(str(Environment.MARC_PORT_OUT)),

             'happy': QLineEdit('Ekman-Joie'),
             'concentrated': QLineEdit('AC-Mind Reading-interested vid8-fascinated'),
             'bored': QLineEdit('MindReading - Interet'),
             'annoyed': QLineEdit('Ekman-Colere'),
             'angry': QLineEdit('Ekman-Colere'),

             'happy_imp': self.get_float_widget(0.66, 0.01, 2.00, 0.01),
             'concentrated_imp': self.get_float_widget(0.25, 0.01, 2.00, 0.01),
             'bored_imp': self.get_float_widget(0.33, 0.01, 2.00, 0.01),
             'annoyed_imp': self.get_float_widget(0.5, 0.01, 2.00, 0.01),
             'angry_imp': self.get_float_widget(0.66, 0.01, 2.00, 0.01),

             'happy_int': self.get_float_widget(1.0, 0.01, 2.00, 0.01),
             'concentrated_int': self.get_float_widget(1.0, 0.01, 2.00, 0.01),
             'bored_int': self.get_float_widget(1.0, 0.01, 2.00, 0.01),
             'annoyed_int': self.get_float_widget(1.0, 0.01, 2.00, 0.01),
             'angry_int': self.get_float_widget(1.0, 0.01, 2.00, 0.01),

             'happy_freq': self.get_int_widget(2, 1, 20, 1),
             'concentrated_freq': self.get_int_widget(2, 1, 20, 1),
             'bored_freq': self.get_int_widget(2, 1, 20, 1),
             'annoyed_freq': self.get_int_widget(2, 1, 20, 1),
             'angry_freq': self.get_int_widget(2, 1, 20, 1)}
        

        self.wasabi_settings = \
            {'ip': QLineEdit(Environment.WASABI_IP),
             'port_in': QLineEdit(str(Environment.WASABI_PORT_IN)),
             'port_out': QLineEdit(str(Environment.WASABI_PORT_OUT))}

        self.mary_settings = \
            {'ip': QLineEdit(Environment.MARY_IP),
             'voice': QLineEdit(Environment.MARY_VOICE),
             'path': QLineEdit(Environment.MARY_PATH)}


        self.setLayout(self.init_ui())
        self.resize(600, 100)

    def get_float_widget(self, start_val, min_val, max_val, step):
        box = QDoubleSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def get_int_widget(self, start_val, min_val, max_val, step):
        box = QSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def init_ui(self):
        ''' Creates the layout of the settings screen
        '''
        # network settings
        net_layout = QGridLayout()

        net_layout.addWidget(QLabel('MARC:'), 0, 1)
        net_layout.addWidget(QLabel('WASABI:'), 0, 2)

        label_network = QLabel('Network:')
        label_network.setStyleSheet('QLabel {font-weight:bold}')
        net_layout.addWidget(label_network, 1, 0)

        net_layout.addWidget(QLabel('IP:'), 2, 0)
        net_layout.addWidget(self.marc_settings['ip'], 2, 1)
        net_layout.addWidget(self.wasabi_settings['ip'], 2, 2)

        net_layout.addWidget(QLabel('Input Port:'), 3, 0)
        net_layout.addWidget(self.marc_settings['port_in'], 3, 1)
        net_layout.addWidget(self.wasabi_settings['port_in'], 3, 2)

        net_layout.addWidget(QLabel('Output Port:'), 4, 0)
        net_layout.addWidget(self.marc_settings['port_out'], 4, 1)
        net_layout.addWidget(self.wasabi_settings['port_out'], 4, 2)
        
        net_values = QWidget()
        net_values.setLayout(net_layout)

        #emotion settings
        emo_layout = QGridLayout()

        label_emotions = QLabel('Emotions:')
        label_emotions.setStyleSheet('QLabel {font-weight:bold}')
        emo_layout.addWidget(label_emotions, 0, 0)

        emo_layout.addWidget(QLabel('Wasabi:'), 1, 0)
        emo_layout.addWidget(QLabel('Marc:'), 1, 1)
        emo_layout.addWidget(QLabel('Impulse:'), 1, 2)
        emo_layout.addWidget(QLabel('Interpolate:'), 1, 3)
        emo_layout.addWidget(QLabel('Frequence:'), 1, 4)

        emo_layout.addWidget(QLabel('Happy:'), 2, 0)
        emo_layout.addWidget(self.marc_settings['happy'], 2, 1)
        emo_layout.addWidget(self.marc_settings['happy_imp'], 2, 2)
        emo_layout.addWidget(self.marc_settings['happy_int'], 2, 3)
        emo_layout.addWidget(self.marc_settings['happy_freq'], 2, 4)

        emo_layout.addWidget(QLabel('Concentrated:'), 3, 0)
        emo_layout.addWidget(self.marc_settings['concentrated'], 3, 1)
        emo_layout.addWidget(self.marc_settings['concentrated_imp'], 3, 2)
        emo_layout.addWidget(self.marc_settings['concentrated_int'], 3, 3)
        emo_layout.addWidget(self.marc_settings['concentrated_freq'], 3, 4)
        
        emo_layout.addWidget(QLabel('Bored:'), 4, 0)
        emo_layout.addWidget(self.marc_settings['bored'], 4, 1)
        emo_layout.addWidget(self.marc_settings['bored_imp'], 4, 2)
        emo_layout.addWidget(self.marc_settings['bored_int'], 4, 3)
        emo_layout.addWidget(self.marc_settings['bored_freq'], 4, 4)
        
        emo_layout.addWidget(QLabel('Annoyed:'), 5, 0)
        emo_layout.addWidget(self.marc_settings['annoyed'], 5, 1)
        emo_layout.addWidget(self.marc_settings['annoyed_imp'], 5, 2)
        emo_layout.addWidget(self.marc_settings['annoyed_int'], 5, 3)
        emo_layout.addWidget(self.marc_settings['annoyed_freq'], 5, 4)
        
        emo_layout.addWidget(QLabel('Angry:'), 6, 0)
        emo_layout.addWidget(self.marc_settings['angry'], 6, 1)
        emo_layout.addWidget(self.marc_settings['angry_imp'], 6, 2)
        emo_layout.addWidget(self.marc_settings['angry_int'], 6, 3)
        emo_layout.addWidget(self.marc_settings['angry_freq'], 6, 4)

        button_test_happy = QPushButton("&Test")
        button_test_happy.clicked.connect(self.test_happy)
        button_test_concentrated = QPushButton("&Test")
        button_test_concentrated.clicked.connect(self.test_concentrated)
        button_test_bored = QPushButton("&Test")
        button_test_bored.clicked.connect(self.test_bored)
        button_test_annoyed = QPushButton("&Test")
        button_test_annoyed.clicked.connect(self.test_annoyed)
        button_test_angry = QPushButton("&Test")
        button_test_angry.clicked.connect(self.test_angry)

        emo_layout.addWidget(button_test_happy, 2, 5)
        emo_layout.addWidget(button_test_concentrated, 3, 5)
        emo_layout.addWidget(button_test_bored, 4, 5)
        emo_layout.addWidget(button_test_annoyed, 5, 5)
        emo_layout.addWidget(button_test_angry, 6, 5)

        emo_values = QWidget()
        emo_values.setLayout(emo_layout)

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
        main_layout.addWidget(net_values)
        main_layout.addWidget(emo_values)
        main_layout.addWidget(widget_mary)
        main_layout.addWidget(buttons)
        return main_layout

    def set_settings(self):
        Environment.MARC_IP = self.marc_settings['ip'].text()
        Environment.MARC_PORT_OUT = int(self.marc_settings['port_out'].text())
        Environment.MARC_PORT_IN = int(self.marc_settings['port_in'].text())

        EmoModule.WASABI = True
        EmoModule.WASABI_IP = self.wasabi_settings['ip'].text()
        EmoModule.WASABI_PORT_IN = int(self.wasabi_settings['port_in'].text())
        EmoModule.WASABI_PORT_OUT = int(self.wasabi_settings['port_out'].text())
        
        Environment.MARY_VOICE = self.mary_settings['voice'].text()
        Environment.MARY_IP = self.mary_settings['ip'].text()
        Environment.MARY_PATH = self.mary_settings['path'].text()

        Happy.MARC = self.marc_settings['happy'].text()
        Happy.IMPULSE = self.marc_settings['happy_imp'].value()
        Happy.INTERPOLATE = self.marc_settings['happy_int'].value()
        Happy.FREQUENCE = self.marc_settings['happy_freq'].value()
        print 'set happy frequence to', self.marc_settings['happy_freq'].value()
        
        Concentrated.MARC = self.marc_settings['concentrated'].text()
        Concentrated.IMPULSE = self.marc_settings['concentrated_imp'].value()
        Concentrated.INTERPOLATE = self.marc_settings['concentrated_int'].value()
        Concentrated.FREQUENCE = self.marc_settings['concentrated_freq'].value()
        
        Bored.MARC = self.marc_settings['bored'].text()
        Bored.IMPULSE = self.marc_settings['bored_imp'].value()
        Bored.INTERPOLATE = self.marc_settings['bored_int'].value()
        Bored.FREQUENCE = self.marc_settings['bored_freq'].value()
        
        Annoyed.MARC = self.marc_settings['annoyed'].text()
        Annoyed.IMPULSE = self.marc_settings['annoyed_imp'].value()
        Annoyed.INTERPOLATE = self.marc_settings['annoyed_int'].value()
        Annoyed.FREQUENCE = self.marc_settings['annoyed_freq'].value()
        
        Angry.MARC = self.marc_settings['angry'].text()
        Angry.IMPULSE = self.marc_settings['angry_imp'].value()
        Angry.INTERPOLATE = self.marc_settings['angry_int'].value()
        Angry.FREQUENCE = self.marc_settings['angry_freq'].value()

    def test_happy(self):
        self.test(Happy())
    def test_concentrated(self):
        self.test(Concentrated())
    def test_bored(self):
        self.test(Bored())
    def test_annoyed(self):
        self.test(Annoyed())
    def test_angry(self):
        self.test(Angry())

    def test(self, emotion):
        ''' Test current settings
        '''
        Environment.MARC = False
        Environment.WASABI = False
        self.set_settings()
        e = Environment()
        e.test(emotion, 10)

    def save(self):
        ''' Save changed settings
        '''
        self.set_settings()
        self.emit(SIGNAL('quit'))

    def cancel(self):
        ''' Exit settings without saving
        '''
        self.emit(SIGNAL("quit"))

    def reset(self):
        ''' Reset settins to original values

        '''
        self.wasabi_settings['ip'].setText('192.168.0.46')
        self.wasabi_settings['port_in'].setText('42424')
        self.wasabi_settings['port_out'].setText('42425')
        
        self.marc_settings['ip'].setText('localhost')
        self.marc_settings['port_in'].setText('4014')
        self.marc_settings['port_out'].setText('4013')
        
        self.marc_settings['happy'].setText('Ekman-Joie')
        self.marc_settings['happy_imp'].setValue(0.66)
        self.marc_settings['happy_int'].setValue(1.0)
        self.marc_settings['happy_freq'].setValue(2)

        self.marc_settings['concentrated'].setText('AC-Mind Reading-interested vid8-fascinated')
        self.marc_settings['concentrated_imp'].setValue(0.25)
        self.marc_settings['concentrated_int'].setValue(1.0)
        self.marc_settings['concentrated_freq'].setValue(2)

        self.marc_settings['bored'].setText('MindReading - Interet')
        self.marc_settings['bored_imp'].setValue(0.33)
        self.marc_settings['bored_int'].setValue(1.0)
        self.marc_settings['bored_freq'].setValue(2)

        self.marc_settings['annoyed'].setText('Ekman-Colere')
        self.marc_settings['annoyed_imp'].setValue(0.5)
        self.marc_settings['annoyed_int'].setValue(1.0)
        self.marc_settings['annoyed_freq'].setValue(2)

        self.marc_settings['angry'].setText('Ekman-Colere')
        self.marc_settings['angry_imp'].setValue(0.66)
        self.marc_settings['angry_int'].setValue(1.0)
        self.marc_settings['angry_freq'].setValue(2)

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

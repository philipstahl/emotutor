''' The gui implimentation in pyqt4
'''

import sys
import ConfigParser
import datetime

from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, \
                        QBoxLayout, QMainWindow, QAction, QIcon, \
                        QApplication, QDesktopWidget, QMessageBox, \
                        QDoubleSpinBox, QSpinBox, QComboBox, QCheckBox

from PyQt4.QtCore import SIGNAL, Qt, QTimer

from agent import Agent
from environment import Environment, TestEnvironment
from emomodule import EmoModule, Happy, Concentrated, Bored, Annoyed, Angry, \
                      Surprise
from marc import Marc
from cogmodule import CogModule
from speechmodule import OpenMary
from speechrecognition import *
import utilities

DEBUG = False



class AssociatedPair(QWidget):
    ''' Gui for a simple vocabulary trainer
    '''
    def __init__(self, use_wasabi=False):
        super(AssociatedPair, self).__init__()

        # Speech recognition:
        grammar = Grammar("example grammar")
        #rules = [NumberNullRule, NumberOneRule, NumberTwoRule, NumberThreeRule,
        #         NumberFourRule, NumberFiveRule, NumberSixRule,
        #         NumberSevenRule, NumberEightRule, NumberNineRule]

        #for rule in rules:
        #    grammar.add_rule(rule(self.answer_given))
            
        #grammar.load()

        grammar.add_rule(NumberNullRule(self.answer_given))
        grammar.add_rule(NumberOneRule(self.answer_given))
        grammar.add_rule(NumberTwoRule(self.answer_given))
        grammar.add_rule(NumberThreeRule(self.answer_given))
        grammar.add_rule(NumberFourRule(self.answer_given))
        grammar.add_rule(NumberFiveRule(self.answer_given))
        grammar.add_rule(NumberSixRule(self.answer_given))
        grammar.add_rule(NumberSevenRule(self.answer_given))
        grammar.add_rule(NumberEightRule(self.answer_given))
        grammar.add_rule(NumberNineRule(self.answer_given))

        grammar.load()
        self.training = True

        if DEBUG:
            self.emo_output = QLabel('')
            self.cog_output = QLabel('')
            self.speech_output = QLabel('')

            agent_layout = QGridLayout()
            agent_layout.addWidget(QLabel('Emotional Output:'), 0, 0)
            agent_layout.addWidget(self.emo_output, 0, 1)
            agent_layout.addWidget(QLabel('Cognition Output:'), 1, 0)
            agent_layout.addWidget(self.cog_output, 1, 1)
            agent_layout.addWidget(QLabel('Speech Output:'), 2, 0)
            agent_layout.addWidget(self.speech_output, 2, 1)

            agent_layout.setColumnMinimumWidth(0, 100)
            agent_layout.setColumnMinimumWidth(1, 500)
            agent = QWidget()
            agent.setLayout(agent_layout)

            self.start_button = QPushButton("&Start")
            self.start_button.clicked.connect(self.start_button_clicked)

            main_layout = QBoxLayout(2)
            main_layout.addWidget(agent)
            main_layout.addWidget(self.start_button)
            self.input_widget = self.get_input_widget()
            self.input_widget.hide()
            main_layout.addWidget(self.input_widget)

            self.setLayout(main_layout)
            self.resize(600, 400)
            #192.168.0.46
            self.exp = Environment(use_wasabi)
            self.waiting_for_answer = False

            #emotion, cog, speech = self.exp.start()
            #self.update_output(emotion, cog, speech)
            self.phase = 0
        else:
            self.speech_output = QLabel('')

            self.start_button = QPushButton("&Start")
            self.start_button.clicked.connect(self.start_button_clicked)

            main_layout = QBoxLayout(2)
            main_layout.addWidget(self.start_button)
            self.input_widget = self.get_input_widget()
            self.input_widget.hide()
            main_layout.addWidget(self.input_widget)

            self.setLayout(main_layout)
            self.resize(300, 300)
            self.width = 300
            self.height = 300
            #192.168.0.46

            self.exp = Environment(use_wasabi)
            self.waiting_for_answer = False

            #emotion, cog, speech = self.exp.start()
            #self.update_output(emotion, cog, speech)
            self.phase = 0
            QTimer.singleShot(4000, self.second_introduction)

    def second_introduction(self):

        self.exp.agent.say('Bitte sprechen Sie die folgenden Zahlen nach.')
        QTimer.singleShot(6000, self.train_number)

    def train_number(self):
        if self.exp.test_nr_index < len(self.exp.test_nr)-1:
            self.exp.train_number()
            QTimer.singleShot(3000, self.train_number)
        else:
            print 'training finished'
            if self.exp.test_correct >= 9:
                self.exp.agent.say('Alles richtig. Starten Sie den Test.')
                print 'Alles ok'
            else:
                print 'Nochmal'
                self.exp.test_correct = 0
                self.exp.test_nr_index = -1
                self.exp.agent.say('Mehr als ein Wort falsch. Noch ein Durchgang.')
                QTimer.singleShot(6000, self.train_number)
        

    def get_input_widget(self):
        # Nr layout:      
        button0 = QPushButton("&0")
        button1 = QPushButton("&1")
        button2 = QPushButton("&2")
        button3 = QPushButton("&3")
        button4 = QPushButton("&4")
        button5 = QPushButton("&5")
        button6 = QPushButton("&6")
        button7 = QPushButton("&7")
        button8 = QPushButton("&8")
        button9 = QPushButton("&9")

        button0.clicked.connect(self.bu0_clicked)
        button1.clicked.connect(self.bu1_clicked)
        button2.clicked.connect(self.bu2_clicked)
        button3.clicked.connect(self.bu3_clicked)
        button4.clicked.connect(self.bu4_clicked)
        button5.clicked.connect(self.bu5_clicked)
        button6.clicked.connect(self.bu6_clicked)
        button7.clicked.connect(self.bu7_clicked)
        button8.clicked.connect(self.bu8_clicked)
        button9.clicked.connect(self.bu9_clicked)

        nr_layout = QGridLayout()
        nr_layout.addWidget(button7, 0, 0)
        nr_layout.addWidget(button8, 0, 1)
        nr_layout.addWidget(button9, 0, 2)
        nr_layout.addWidget(button4, 1, 0)
        nr_layout.addWidget(button5, 1, 1)
        nr_layout.addWidget(button6, 1, 2)
        nr_layout.addWidget(button1, 2, 0)
        nr_layout.addWidget(button2, 2, 1)
        nr_layout.addWidget(button3, 2, 2)
        nr_layout.addWidget(button0, 3, 0)
        nr_widget = QWidget()
        nr_widget.setLayout(nr_layout)
        return nr_widget

    def start_button_clicked(self):
        self.start_button.hide()
        self.input_widget.show()
        self.training = False
        self.exp.save_start_time()
        self.exp.start()
        QTimer.singleShot(6000, self.present_word)

    def bu0_clicked(self):
        self.answer_given(0)

    def bu1_clicked(self):
        self.answer_given(1)

    def bu2_clicked(self):
        self.answer_given(2)

    def bu3_clicked(self):
        self.answer_given(3)

    def bu4_clicked(self):
        self.answer_given(4)

    def bu5_clicked(self):
        self.answer_given(5)

    def bu6_clicked(self):
        self.answer_given(6)

    def bu7_clicked(self):
        self.answer_given(7)

    def bu8_clicked(self):
        self.answer_given(8)

    def bu9_clicked(self):
        self.answer_given(9)

    def answer_given(self, nr):
        if self.training:
            self.exp.check_nr(str(nr))
        else:
       
            if self.waiting_for_answer:
                #print '  @', now - self.exp.start_time, 'answer received: Took', now - self.exp.start_time_answer
                self.exp.evaluate(str(nr), datetime.datetime.now())

            self.waiting_for_answer = False

    def update_output(self, emotion, cog, speech):
        ''' Updates the text output of the agent.
        '''
        self.speech_output.setText(speech)
        if DEBUG:
            self.emo_output.setText(emotion)
            self.cog_output.setText(cog)


    def present_word(self):

        if self.exp.has_next():
            
            #print '@', now - self.exp.start_time, 'present word called'
            
            emotion, cog, speech = self.exp.present_word(datetime.datetime.now())
            self.update_output(emotion, cog, speech)
            self.waiting_for_answer = True
            QTimer.singleShot(5000, self.present_number)
        else:
            if self.exp.current_run < self.exp.total_runs-1:
                self.exp.reset()
                QTimer.singleShot(10000, self.present_word)
            else:
                self.end()

    def present_number(self):

        
        #print '@', now-self.exp.start_time, 'present number called'
        
        self.waiting_for_answer = False
        emotion, cog, speech = self.exp.present_number(datetime.datetime.now())
        self.update_output(emotion, cog, speech)
        QTimer.singleShot(5000, self.present_word)

    def end(self):
        ''' End vocabulary test
        '''
        emotion, speech = self.exp.end()
        if DEBUG:
            self.emo_output.setText(emotion)
        self.speech_output.setText(speech)
        self.input_widget.hide()


class Settings(QWidget):
    ''' Abstract Frame showing the program settings
    '''

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        self.setLayout(self.init_ui())
        self.environment = None

    def init_ui(self):
        ''' Creates the layout of the settings screen.
            Basic button functionality is designed here. Parameter settings
            have to be overwritten in init_parameters
        '''
        button_layout = QBoxLayout(0)
        button_layout.addWidget(self.button('&Reset', self.reset))
        button_layout.addWidget(self.button('&Cancel', self.cancel))
        button_layout.addWidget(self.button('&Save', self.save))

        buttons = QWidget()
        buttons.setLayout(button_layout)

        main_layout = QBoxLayout(2)
        main_layout.addWidget(self.init_parameters())
        main_layout.addWidget(buttons)
        return main_layout

    def init_parameters(self):
        ''' Has to be overwritten
        '''
        pass

    def apply_settings(self):
        ''' Has to be overwritten.
        '''
        pass

    def save(self):
        ''' Save changed settings
        '''
        self.apply_settings()
        self.emit(SIGNAL('quit'))

    def cancel(self):
        ''' Exit settings without saving
        '''
        self.emit(SIGNAL("quit"))

    def reset(self):
        ''' Has to be overwritten
        '''
        pass

    def button(self, name, function):
        ''' Returns a button with the given name and function.
        '''
        button = QPushButton(name)
        button.clicked.connect(function)
        return button


    def combo_box(self, selected, items=['None', 'Happy', 'Concentrated', 'Bored', 'Annoyed', 'Angry']):
        ''' Returns a combo box of the available emotions.
        '''
        combo = QComboBox()
        combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        combo.addItems(items)

        if selected in items:
            combo.setCurrentIndex(items.index(selected))

        combo.resize(300, 30)
        return combo

    def float_widget(self, start_val, min_val, max_val, step):
        ''' Returns a float widget with the given values.
        '''
        box = QDoubleSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def int_widget(self, start_val, min_val=-100, max_val=100, step=1):
        ''' Returns an int widget with the given values.
        '''
        box = QSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def add_line(self, layout, values, line_index):
        ''' Adds a line containing the given values into the given grid layout.
        '''
        for i in range(len(values)):
            layout.addWidget(values[i], line_index, i)


class TestEmoButton(QWidget):
    def __init__(self, emo, parent=None):
        QWidget.__init__(self, parent)
        self.button = QPushButton('&Test', self)
        self.name='me'
        self.emo = emo()
        self.button.clicked.connect(self.calluser)
        
    def calluser(self):
        print(self.name)
        environment = TestEnvironment()
        environment.test(self.emo, 5)


class NetworkSettings(Settings):
    ''' Frame showing all network settings
    '''

    def __init__(self, parent=None):
        self.marc_settings = \
            {'ip': QLineEdit(Marc.IP),
             'port_in': QLineEdit(str(Marc.PORT_IN)),
             'port_out': QLineEdit(str(Marc.PORT_OUT))}

        self.wasabi_settings = \
            {'ip': QLineEdit(EmoModule.WASABI_IP),
             'port_in': QLineEdit(str(EmoModule.WASABI_PORT_IN)),
             'port_out': QLineEdit(str(EmoModule.WASABI_PORT_OUT))}

        self.mary_settings = \
            {'ip': QLineEdit(OpenMary.IP),
             'voice': QLineEdit(OpenMary.VOICE),
             'path': QLineEdit(OpenMary.PATH)}

        super(NetworkSettings, self).__init__(parent)


    def init_parameters(self):
        ''' Creates the layout of the settings screen
        '''
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

        button_test_wasabi = QPushButton("&Test")
        button_test_wasabi.clicked.connect(self.test_wasabi)

        net_layout.addWidget(button_test_wasabi, 4, 3)

        net_values = QWidget()
        net_values.setLayout(net_layout)

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

        main_layout = QBoxLayout(2)
        main_layout.addWidget(net_values)
        main_layout.addWidget(widget_mary)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        return main_widget

    def apply_settings(self):
        ''' apply settings loaded from the gui
        '''
        Marc.IP = self.marc_settings['ip'].text()
        Marc.PORT_IN = int(self.marc_settings['port_in'].text())
        Marc.PORT_OUT = int(self.marc_settings['port_out'].text())

        EmoModule.WASABI_IP = self.wasabi_settings['ip'].text()
        EmoModule.WASABI_PORT_IN = int(self.wasabi_settings['port_in'].text())
        EmoModule.WASABI_PORT_OUT = int(self.wasabi_settings['port_out'].text())

        OpenMary.VOICE = self.mary_settings['voice'].text()
        OpenMary.IP = self.mary_settings['ip'].text()
        OpenMary.PATH = self.mary_settings['path'].text()

        self.environment = Environment()

    def test_wasabi(self):
        ''' Tests if messages are received from wasabi.
        '''
        self.apply_settings()

        environment = TestEnvironment()
        environment.test_wasabi()

    def reset(self):
        ''' Reset settins to original values

        '''
        self.wasabi_settings['ip'].setText('192.168.0.46')
        self.wasabi_settings['port_in'].setText('42425')
        self.wasabi_settings['port_out'].setText('42424')

        self.marc_settings['ip'].setText('localhost')
        self.marc_settings['port_in'].setText('4014')
        self.marc_settings['port_out'].setText('4013')

        self.mary_settings['ip'].setText('http://localhost:59125/')
        self.mary_settings['voice'].setText('dfki-obadiah')
        self.mary_settings['path'].setText(
                            'C:\\Users\\User\\Desktop\\emotutor\\src\\sounds\\')


class Emotions(Settings):
    ''' Frame showing the emotion mapping from wasabi to marc.
    '''

    def __init__(self, parent=None):

        def init(Emotion):
            return [QLineEdit(Emotion.MARC),
                    self.float_widget(Emotion.INTENSE, 0.01, 2.00, 0.01),
                    self.float_widget(Emotion.INTERPOLATE, 0.01, 2.00, 0.01),
                    self.int_widget(Emotion.FREQUENCE, 1, 20, 1)]

        self.emo_settings = \
            {'happy': init(Happy),
             'concentrated': init(Concentrated),
             'bored': init(Bored),
             'annoyed': init(Annoyed),
             'angry': init(Angry),
             'surprise': init(Surprise)}



        super(Emotions, self).__init__(parent)

    def init_parameters(self):
        ''' Creates the layout of the settings screen
        '''
        layout = QGridLayout()

        label_emotions = QLabel('Emotions:')
        label_emotions.setStyleSheet('QLabel {font-weight:bold}')
        layout.addWidget(label_emotions, 0, 0)

        self.add_line(layout, [QLabel('Wasabi:'), QLabel('Marc:'),
                               QLabel('Impulse'), QLabel('Interpolate'),
                               QLabel('Frequence')], 1)
        self.add_line(layout, [QLabel('Happy')] + self.emo_settings['happy'], 2)
        self.add_line(layout, [QLabel('Concentrated')]
                              + self.emo_settings['concentrated'], 3)
        self.add_line(layout, [QLabel('Bored')] + self.emo_settings['bored'], 4)
        self.add_line(layout, [QLabel('Annoyed')]
                              + self.emo_settings['annoyed'], 5)
        self.add_line(layout, [QLabel('Angry')] + self.emo_settings['angry'], 6)
        self.add_line(layout, [QLabel('Surprise')]
                              + self.emo_settings['surprise'], 7)

        #layout.addWidget(TestEmoButton(Happy), 2, 5)
        #layout.addWidget(TestEmoButton(Concentrated), 3, 5)
        #layout.addWidget(TestEmoButton(Bored), 4, 5)
        #layout.addWidget(TestEmoButton(Annoyed), 5, 5)
        #layout.addWidget(TestEmoButton(Angry), 6, 5)
        #layout.addWidget(TestEmoButton(Surprise), 7, 5)
        layout.addWidget(self.button('&Test', self.test_happy), 2, 5)
        layout.addWidget(self.button('&Test', self.test_concentrated), 3, 5)
        layout.addWidget(self.button('&Test', self.test_bored), 4, 5)
        layout.addWidget(self.button('&Test', self.test_annoyed), 5, 5)
        layout.addWidget(self.button('&Test', self.test_angry), 6, 5)
        layout.addWidget(self.button('&Test', self.test_surprise), 7, 5)

        emo_values = QWidget()
        emo_values.setLayout(layout)

        main_layout = QBoxLayout(2)
        main_layout.addWidget(emo_values)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        return main_widget

    def apply_settings(self):
        ''' apply settings loaded from the gui
        '''
        def apply_emo(emo_class, emo_key):
            ''' Applies the specified values to the given emotion class.
            '''
            emo_class.MARC = self.emo_settings[emo_key][0].text()
            emo_class.INTENSE = self.emo_settings[emo_key][1].value()
            emo_class.INTERPOLATE = self.emo_settings[emo_key][2].value()
            emo_class.FREQUENCE = self.emo_settings[emo_key][3].value()

        apply_emo(Happy, 'happy')
        apply_emo(Concentrated, 'concentrated')
        apply_emo(Bored, 'bored')
        apply_emo(Annoyed, 'annoyed')
        apply_emo(Angry, 'angry')
        apply_emo(Surprise, 'surprise')
        #self.environment = Environment()

    def get_function(self, combo_box):
        ''' Returns the keyword of the selected function in the given combobox.
        '''
        functions = ['baselevel', 'optimized']
        if combo_box.currentIndex() >= len(functions):
            print 'COMBOBOX: INDEX ERROR'
        else:
            return functions[combo_box.currentIndex()]

    def reset(self):
        ''' Reset settings.
        '''
        self.emo_settings['happy'][0].setText('CASA_Joy_01')
        self.emo_settings['happy'][1].setValue(0.66)
        self.emo_settings['happy'][2].setValue(1.0)
        self.emo_settings['happy'][3].setValue(2)

        self.emo_settings['concentrated'][0].setText('CASA_Relax_01')
        self.emo_settings['concentrated'][1].setValue(0.25)
        self.emo_settings['concentrated'][2].setValue(1.0)
        self.emo_settings['concentrated'][3].setValue(2)

        self.emo_settings['bored'][0].setText('CASA_Relax_01')
        self.emo_settings['bored'][1].setValue(0.33)
        self.emo_settings['bored'][2].setValue(1.0)
        self.emo_settings['bored'][3].setValue(2)

        self.emo_settings['annoyed'][0].setText('CASA_Sadness_01')
        self.emo_settings['annoyed'][1].setValue(0.5)
        self.emo_settings['annoyed'][2].setValue(1.0)
        self.emo_settings['annoyed'][3].setValue(2)

        self.emo_settings['angry'][0].setText('CASA_Anger_01')
        self.emo_settings['angry'][1].setValue(0.66)
        self.emo_settings['angry'][2].setValue(1.0)
        self.emo_settings['angry'][3].setValue(2)

        self.emo_settings['surprise'][0].setText('Surprise - CubeEmotion')
        self.emo_settings['surprise'][1].setValue(0.66)
        self.emo_settings['surprise'][2].setValue(1.0)
        self.emo_settings['surprise'][3].setValue(2)

    def test_happy(self):
        ''' Test happy emotion settings
        '''
        self.apply_settings()
        self.test(Happy())

    def test_concentrated(self):
        ''' Test concentrated emotion settings
        '''
        self.apply_settings()
        self.test(Concentrated())

    def test_bored(self):
        ''' Test bored emotion settings
        '''
        self.apply_settings()
        self.test(Bored())

    def test_annoyed(self):
        ''' Test annoyed emotion settings
        '''
        self.apply_settings()
        self.test(Annoyed())

    def test_angry(self):
        ''' Test angry emotion settings
        '''
        self.apply_settings()
        self.test(Angry())

    def test_surprise(self):
        ''' Test surprise emotion settings
        '''
        self.apply_settings()
        self.test(Surprise())

    def test(self, emotion):
        ''' Test current settings
        '''
        environment = TestEnvironment()
        environment.test(emotion, 5)


class Parameters(Settings):
    ''' Frame showing the activation function and emotional reactions according
        to the given activation.
    '''

    def __init__(self, parent=None):
        self.init = self.combo_box(Agent.INIT_EMOTION,
                                   items=['Happy', 'Neutral', 'Angry', 'Wasabi'])

        self.function = self.function_box(CogModule.FUNCTION)
        self.decay_rate = self.float_widget(CogModule.DECAY_RATE, 0.0, 1.0, 0.1)
        self.activation_noise = self.float_widget(CogModule.NOISE, 0.0, 1.0, 0.1)
        self.threshold = self.float_widget(CogModule.THRESHOLD, -10.0, 10.0, 0.1)
        self.latency = self.float_widget(CogModule.LATENCY, 0.0, 2.0, 0.1)
        
        self.activations = \
            [self.int_widget(CogModule.ACT_HIGH, 0, 100, 1),
             self.int_widget(CogModule.ACT_NONE, 0, 100, 1)]

        # Map expectation {Neg, Pos} to
        #       [emotion to trigger before event,
        #        emotion to trigger if event occurs,
        #        emotion to trigger if event does not occur]
        before = ['None', 'Fear', 'Hope']
        after = ['None', 'Relief', 'Fears-Confirmed']
        self.expectation = {
            'Neg': [self.combo_box(CogModule.EXPECT_NEG[0], items=before),
                    self.combo_box(CogModule.EXPECT_NEG[1], items=after),
                    self.combo_box(CogModule.EXPECT_NEG[2], items=after)],
            'Pos': [self.combo_box(CogModule.EXPECT_POS[0], items=before),
                    self.combo_box(CogModule.EXPECT_POS[1], items=after),
                    self.combo_box(CogModule.EXPECT_POS[2], items=after)]}

        self.surprise = [
            {'Neg': self.check_box(EmoModule.REACT_NEG_WRONG[0]),
             'None': self.check_box(EmoModule.REACT_NONE_WRONG[0]),
             'Pos': self.check_box(EmoModule.REACT_POS_WRONG[0])},
            {'Neg': self.check_box(EmoModule.REACT_NEG_RIGHT[0]),
             'None': self.check_box(EmoModule.REACT_NONE_RIGHT[0]),
             'Pos': self.check_box(EmoModule.REACT_POS_RIGHT[0])},
            {'Neg': self.check_box(EmoModule.REACT_NEG_NONE[0]),
             'None': self.check_box(EmoModule.REACT_NONE_NONE[0]),
             'Pos': self.check_box(EmoModule.REACT_POS_NONE[0])}]


        self.emotion = [\
            {'Neg': self.combo_box(EmoModule.REACT_NEG_WRONG[1]),
             'None': self.combo_box(EmoModule.REACT_NONE_WRONG[1]),
             'Pos': self.combo_box(EmoModule.REACT_POS_WRONG[1])},
            {'Neg': self.combo_box(EmoModule.REACT_NEG_RIGHT[1]),
             'None': self.combo_box(EmoModule.REACT_NONE_RIGHT[1]),
             'Pos': self.combo_box(EmoModule.REACT_POS_RIGHT[1])},
            {'Neg': self.combo_box(EmoModule.REACT_NEG_NONE[1]),
             'None': self.combo_box(EmoModule.REACT_NONE_NONE[1]),
             'Pos': self.combo_box(EmoModule.REACT_POS_NONE[1])}]

        self.impulse = [\
            {'Neg': self.int_widget(EmoModule.REACT_NEG_WRONG[2]),
             'None': self.int_widget(EmoModule.REACT_NONE_WRONG[2]),
             'Pos': self.int_widget(EmoModule.REACT_POS_WRONG[2])},
            {'Neg': self.int_widget(EmoModule.REACT_NEG_RIGHT[2]),
             'None': self.int_widget(EmoModule.REACT_NONE_RIGHT[2]),
             'Pos': self.int_widget(EmoModule.REACT_POS_RIGHT[2])},
            {'Neg': self.int_widget(EmoModule.REACT_NEG_NONE[2]),
             'None': self.int_widget(EmoModule.REACT_NONE_NONE[2]),
             'Pos': self.int_widget(EmoModule.REACT_POS_NONE[2])}]

        super(Parameters, self).__init__(parent)


    def check_box(self, selected):
        box = QCheckBox()
        if selected:
            box.nextCheckState()
        return box

    def function_box(self, selected):
        ''' Returns the combo box of the available functions.
        '''
        items = ['B_i = ln(sum_from_j=1_to_n(t_j^(-d)))',
                 'B_i = ln(n / (1-d)) - d * ln(L)']

        combo = QComboBox()
        combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        combo.addItems(items)

        names = ['baselevel', 'optimized']
        if selected in names:
            combo.setCurrentIndex(names.index(selected))

        combo.resize(300, 30)
        return combo

    def init_parameters(self):
        ''' Creates the layout of the settings screen
        '''
        main_layout = QBoxLayout(2)

        desc1 = QLabel('Intructions:')
        desc2 = QLabel('Map activation to expectation:')
        desc3 = QLabel('Map expectation to emotion:')
        desc4 = QLabel('Map expectation + answer to reaction:')
        for desc in [desc1, desc2, desc3, desc4]:
            desc.setStyleSheet('QLabel {font-weight:bold}')

        main_layout.addWidget(desc1)
        main_layout.addWidget(self.get_init_emotion_widget())
        main_layout.addWidget(desc2)
        main_layout.addWidget(self.get_function_widget())
        main_layout.addWidget(self.get_activation_widget())
        main_layout.addWidget(desc3)
        main_layout.addWidget(self.get_expectation_widget())
        main_layout.addWidget(desc4)
        main_layout.addWidget(self.get_reaction_widget())
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        return main_widget

    def get_init_emotion_widget(self):
        layout = QGridLayout()
        layout.addWidget(QLabel('Show emotion:'), 0, 0)
        layout.addWidget(self.init, 0, 1)
        widget = QWidget()
        widget.setLayout(layout)
        return widget


    def get_function_widget(self):
        ''' Returns the widget containing the function settings
        '''
        layout = QGridLayout()
        layout.addWidget(QLabel('Baselevel:'), 0, 0)
        layout.addWidget(self.function, 0, 1)

        layout.addWidget(QLabel('Decay rate d:'), 0, 2)
        layout.addWidget(QLabel('Activation noise s:'), 1, 2)
        layout.addWidget(QLabel('Latency factor'), 2, 2)
        layout.addWidget(QLabel('Retrieval threshold'), 1, 0)

        layout.addWidget(self.decay_rate, 0, 3)
        layout.addWidget(self.activation_noise, 1, 3)
        layout.addWidget(self.latency, 2, 3)
        layout.addWidget(self.threshold, 1, 1)        

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def get_activation_widget(self):
        ''' Returns the widget containint the activation settings.
        '''
        layout = QGridLayout()
        layout.addWidget(QLabel('Expection:'), 0, 0)
        layout.addWidget(QLabel('Negative'), 1, 0)
        layout.addWidget(QLabel(' < '), 1, 1)
        layout.addWidget(self.activations[1], 1, 2)
        layout.addWidget(QLabel('%'), 1, 3)
        layout.addWidget(QLabel(' < '), 1, 4)
        layout.addWidget(QLabel('None'), 1, 5)
        layout.addWidget(QLabel(' < '), 1, 6)
        layout.addWidget(self.activations[0], 1, 7)
        layout.addWidget(QLabel('%'), 1, 8)
        layout.addWidget(QLabel(' < '), 1, 9)
        layout.addWidget(QLabel('Positive'), 1, 10)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def get_expectation_widget(self):
        items = ['None', 'Fear', 'Hope']
        layout = QGridLayout()
        layout.addWidget(QLabel('Expectation:'), 0, 0)
        layout.addWidget(QLabel('Trigger before Event:'), 0, 1)
        layout.addWidget(QLabel('Trigger if occured:'), 0, 2)
        layout.addWidget(QLabel('Trigger if not occured:'), 0, 3)

        layout.addWidget(QLabel('Negative:'), 1, 0)
        layout.addWidget(QLabel('Positive:'), 2, 0)

        layout.addWidget(self.expectation['Neg'][0], 1, 1)
        layout.addWidget(self.expectation['Neg'][1], 1, 2)
        layout.addWidget(self.expectation['Neg'][2], 1, 3)

        layout.addWidget(self.expectation['Pos'][0], 2, 1)
        layout.addWidget(self.expectation['Pos'][1], 2, 2)
        layout.addWidget(self.expectation['Pos'][2], 2, 3)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def get_reaction_widget(self):
        ''' Different cases:
            - Expectation was negative and answer negative
            - Expectation was none and answer was negative
            - Expectation was positive and answer was negative
            - Expectation was negative and answer was negative
            - Expectation was none and answer was negative
            - Expectation was positive and answer was negative

            mapping to
            - Surprise yes/no, Trigger Emotion, Impulse
        '''
        layout = QGridLayout()
        layout.addWidget(QLabel('Expectation:'), 0, 0)
        layout.addWidget(QLabel('Answer:'), 0, 1)
        layout.addWidget(QLabel('Surprise:'), 0, 2)
        layout.addWidget(QLabel('Emotion:'), 0, 3)
        layout.addWidget(QLabel('Impulse:'), 0, 4)

        def add(layout, expectation, answer, correct, expect, line):
            layout.addWidget(QLabel(expectation), line, 0)
            layout.addWidget(QLabel(answer), line, 1)
            layout.addWidget(self.surprise[correct][expect], line, 2)
            layout.addWidget(self.emotion[correct][expect], line, 3)
            layout.addWidget(self.impulse[correct][expect], line, 4)

        add(layout, 'Negative', 'None', 2, 'Neg', 1)
        add(layout, 'Negative', 'Wrong', 0, 'Neg', 2)
        add(layout, 'Negative', 'Correct', 1, 'Neg', 3)

        add(layout, 'None', 'None', 2, 'None', 4)
        add(layout, 'None', 'Wrong', 0, 'None', 5)
        add(layout, 'None', 'Correct', 1, 'None', 6)
        
        add(layout, 'Positive', 'None', 2, 'Pos', 7)
        add(layout, 'Positive', 'Wrong', 0, 'Pos', 8)
        add(layout, 'Positive', 'Correct', 1, 'Pos', 9)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def apply_settings(self):
        ''' apply settings loaded from the gui
        '''
        Agent.INIT_EMOTION = str(self.init.currentText())

        CogModule.ACT_HIGH = self.activations[0].value()
        CogModule.ACT_LOW = self.activations[1].value()
        
        CogModule.DECAY_RATE = self.decay_rate.value()
        CogModule.NOISE = self.activation_noise.value()
        CogModule.LATENCY = self.latency.value()
        CogModule.THRESHOLD = self.threshold.value()        

        CogModule.FUNCTION = self.get_function(self.function)

        CogModule.EXPECT_NEG = (str(self.expectation['Neg'][0].currentText()),
                                str(self.expectation['Neg'][1].currentText()),
                                str(self.expectation['Neg'][2].currentText()))

        CogModule.EXPECT_POS = (str(self.expectation['Pos'][0].currentText()),
                                str(self.expectation['Pos'][1].currentText()),
                                str(self.expectation['Pos'][2].currentText()))

        def get_reaction(correct, expect):
            return (bool(self.surprise[correct][expect].isChecked()),
                    str(self.emotion[correct][expect].currentText()),
                    int(self.impulse[correct][expect].value()))

        EmoModule.REACT_NEG_NONE = get_reaction(2, 'Neg')
        EmoModule.REACT_NEG_WRONG = get_reaction(0, 'Neg')
        EmoModule.REACT_NEG_RIGHT = get_reaction(1, 'Neg')
        EmoModule.REACT_NONE_NONE = get_reaction(2, 'None')
        EmoModule.REACT_NONE_WRONG = get_reaction(0, 'None')
        EmoModule.REACT_NONE_RIGHT = get_reaction(1, 'None')
        EmoModule.REACT_POS_NONE = get_reaction(2, 'Pos')
        EmoModule.REACT_POS_WRONG = get_reaction(0, 'Pos')
        EmoModule.REACT_POS_RIGHT = get_reaction(1, 'Pos')

        self.environment = Environment()

    def get_function(self, combo_box):
        ''' Returns the selected function in the combo_box.
        '''
        functions = ['baselevel', 'optimized']
        if combo_box.currentIndex() >= len(functions):
            print 'COMBOBOX: INDEX ERROR'
        else:
            return functions[combo_box.currentIndex()]


    def get_class(self, combo_box):
        ''' Returns the selected class type in the combo_box.
        '''
        classes = ['Happy', 'Concentrated', 'Bored', 'Annoyed', 'Angry']
        if combo_box.currentIndex() >= len(classes):
            print 'COMBOBOX: INDEX ERROR'
        else:
            return classes[combo_box.currentIndex()]

    def reset(self):
        ''' Resets the settings.
        '''
        pass


class Welcome(QWidget):
    ''' Frame at the start of the vocabulary trainer
    '''
    def __init__(self, parent=None):
        super(Welcome, self).__init__(parent)

        button_settings = QPushButton("&Edit settings")
        button_emotions = QPushButton('&Edit emotions')
        button_mapping = QPushButton('&Edit mapping')
        button_start = QPushButton('&Start training')
        
        button_start_user = QPushButton('&Start with applied settings.')
        button_start_neutral = QPushButton('&Start with neutral agent.')
        button_start_rulebased = QPushButton('&Start with rulebased agent.')
        button_start_wasabi = QPushButton('&Start with wasabi based agent.')

        # Define button funcionalty:
        button_settings.clicked.connect(self.options)
        button_emotions.clicked.connect(self.emotions)
        button_mapping.clicked.connect(self.mapping)
        
        button_start_user.clicked.connect(self.start_user)
        button_start_neutral.clicked.connect(self.start_neutral)
        button_start_rulebased.clicked.connect(self.start_rulebased)
        button_start_wasabi.clicked.connect(self.start_wasabi)

        button_layout = QBoxLayout(2)
        button_layout.addWidget(button_settings)
        button_layout.addWidget(button_emotions)
        button_layout.addWidget(button_mapping)
        buttons = QWidget()
        buttons.setLayout(button_layout)

        left_top = QWidget()
        left_bottom = QWidget()
        right_top = QWidget()
        right_bottom = QWidget()

        layout = QGridLayout()
        layout.addWidget(left_top, 0, 0)
        layout.addWidget(buttons, 0, 1)
        layout.addWidget(right_top, 0, 2)

        layout.addWidget(QLabel('Paired Associate Task:'), 1, 1)
        layout.addWidget(button_start_user, 2, 1)
        layout.addWidget(button_start_neutral, 3, 1)
        layout.addWidget(button_start_rulebased, 4, 1)
        layout.addWidget(button_start_wasabi, 5, 1)

        self.setLayout(layout)
        self.resize(600, 100)

    def options(self):
        ''' Show options
        '''
        self.emit(SIGNAL('settings'))

    def emotions(self):
        ''' Show emotions
        '''
        self.emit(SIGNAL('emotions'))

    def mapping(self):
        ''' Show mapping
        '''
        self.emit(SIGNAL('mapping'))

    def start_user(self):
        ''' Start task with user specified agent.
        '''
        self.emit(SIGNAL('start_user'))

    def start_neutral(self):
        ''' Start task with neutral agent.
        '''
        self.emit(SIGNAL('start_neutral'))

    def start_rulebased(self):
        ''' Start task with rulebased agent.
        '''
        self.emit(SIGNAL('start_rulebased'))

    def start_wasabi(self):
        ''' Start task with wasabi based agent.
        '''
        self.emit(SIGNAL('start_wasabi'))


class MainWindow(QMainWindow):
    ''' Main window of the vocabulary trainer
    '''
    MARC = None
    WASABI = None
    MARY = None
    EMOTIONS = None

    def __init__(self):
        QMainWindow.__init__(self)

        self.resize(600, 400)
        self.setWindowTitle('Vocabulary Trainer')

        new = QAction(QIcon('icons/icon.png'), 'New training',
                                        self)
        settings = QAction(QIcon('icons/icon.png'),
                                 'NetworkSettings', self)
        self.connect(settings, SIGNAL('triggered()'), self.show_options)

        self.statusBar()

        menubar = self.menuBar()

        menuFile = menubar.addMenu('&File')
        menuFile.addAction(new)

        options = menubar.addMenu('&Options')
        options.addAction(settings)


        self.load_config()
        self.setMenuBar(menubar)
        self.show_welcome()
        self.move(0, 0)

    def load_config(self, configfile='emotutor.cfg'):
        ''' loads the init values from the config file
        '''
        config = ConfigParser.SafeConfigParser()
        config.read(configfile)
        # TODO(path is relative to the path gui.py is called.)
        Marc.IP = config.get('Marc', 'ip')
        Marc.PORT_IN = config.getint('Marc', 'port_in')
        Marc.PORT_OUT = config.getint('Marc', 'port_out')

        EmoModule.WASABI_IP = config.get('Wasabi', 'ip')
        EmoModule.WASABI_PORT_IN = config.getint('Wasabi', 'port_in')
        EmoModule.WASABI_PORT_OUT = config.getint('Wasabi', 'port_out')

        OpenMary.IP = config.get('Mary', 'ip')
        OpenMary.VOICE = config.get('Mary', 'voice')
        OpenMary.PATH = config.get('Mary', 'path')

        def apply_emo(emo_class, emo_name):
            ''' Apply the specified settings to the program.
            '''
            emo_class.MARC = config.get(emo_name, 'marc')
            emo_class.INTENSE = config.getfloat(emo_name, 'impulse')
            emo_class.INTERPOLATE = config.getfloat(emo_name, 'interpolate')
            emo_class.FREQUENCE = config.getint(emo_name, 'frequence')

        apply_emo(Happy, 'Happy')
        apply_emo(Concentrated, 'Concentrated')
        apply_emo(Bored, 'Bored')
        apply_emo(Annoyed, 'Annoyed')
        apply_emo(Angry, 'Angry')
        apply_emo(Surprise, 'Surprise')

        Agent.INIT_EMOTION = config.get('Init', 'emotion')

        CogModule.ACT_HIGH = config.getint('Activation', 'high')
        CogModule.ACT_NONE = config.getint('Activation', 'low')
        CogModule.DECAY_RATE = config.getfloat('Activation', 'decay')
        CogModule.NOISE = config.getfloat('Activation', 'noise')
        CogModule.LATENCY = config.getfloat('Activation', 'latency')
        CogModule.THRESHOLD =config.getfloat('Activation', 'threshold')

        CogModule.EXPECT_NEG = (config.get('Neg_Expectation', 'before'),
                                config.get('Neg_Expectation', 'after'),
                                config.get('Neg_Expectation', 'after_not'))
        CogModule.EXPECT_POS = (config.get('Pos_Expectation', 'before'),
                                config.get('Pos_Expectation', 'after'),
                                config.get('Pos_Expectation', 'after_not'))

        def get_config(name):
            ''' Returns the values for the given emotion specifictation.
            '''
            return (config.getboolean(name, 'surprise'),
                    config.get(name, 'emotion'),
                    config.getint(name, 'impulse'))
        
        EmoModule.REACT_NEG_NONE = get_config('React_Neg_None')
        EmoModule.REACT_NEG_WRONG = get_config('React_Neg_Wrong')
        EmoModule.REACT_NEG_RIGHT = get_config('React_Neg_Right')
        EmoModule.REACT_NONE_NONE = get_config('React_None_None') 
        EmoModule.REACT_NONE_WRONG = get_config('React_None_Wrong')
        EmoModule.REACT_NONE_RIGHT = get_config('React_None_Right')
        EmoModule.REACT_POS_NONE = get_config('React_Pos_None')
        EmoModule.REACT_POS_WRONG = get_config('React_Pos_Wrong')
        EmoModule.REACT_POS_RIGHT = get_config('React_Pos_Right')


    def show_welcome(self):
        ''' Shows the welcome screen
        '''
        welcome = Welcome()
        self.connect(welcome, SIGNAL('settings'), self.show_options)
        self.connect(welcome, SIGNAL('emotions'), self.show_emotions)
        self.connect(welcome, SIGNAL('mapping'), self.show_mapping)
        
        self.connect(welcome, SIGNAL('start_user'), self.start_user)
        self.connect(welcome, SIGNAL('start_neutral'), self.start_neutral)
        self.connect(welcome, SIGNAL('start_rulebased'), self.start_rulebased)
        self.connect(welcome, SIGNAL('start_wasabi'), self.start_wasabi)

        welcome.show()
        self.setCentralWidget(welcome)

    def show_options(self):
        ''' Shows the option screen
        '''
        settings = NetworkSettings()
        self.connect(settings, SIGNAL("quit"), self.show_welcome)
        settings.show()
        self.setCentralWidget(settings)

    def show_emotions(self):
        ''' Shows the option screen
        '''
        emotions = Emotions()
        self.connect(emotions, SIGNAL("quit"), self.show_welcome)
        emotions.show()
        self.setCentralWidget(emotions)

    def show_mapping(self):
        ''' Shows the option screen
        '''
        mapping = Parameters()
        self.connect(mapping, SIGNAL("quit"), self.show_welcome)
        mapping.show()
        self.setCentralWidget(mapping)

    
    def start_user(self):
        self.load_config('emotutor.cfg')
        self.start_trainer(use_wasabi=True)

    def start_neutral(self):
        self.load_config('emotutor_neutral.cfg')
        self.start_trainer(use_wasabi=False)

    def start_rulebased(self):
        self.load_config('emotutor_rulebased.cfg')
        self.start_trainer(use_wasabi=False)

    def start_wasabi(self):
        self.load_config('emotutor_wasabi.cfg')
        self.start_trainer(use_wasabi=True)
           
    def start_trainer(self, use_wasabi):
        trainer = AssociatedPair(use_wasabi)
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

''' The gui implimentation in pyqt4
'''

import sys
import ConfigParser
import time # sound for ubuntu

import PyQt4.QtGui
from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, \
                        QBoxLayout, QMainWindow, QAction, QIcon, \
                        QApplication, QDesktopWidget, QMessageBox, \
                        QDoubleSpinBox, QSpinBox, QComboBox
import PyQt4.QtCore
from PyQt4.QtCore import SIGNAL, Qt, QTimer

from environment import Environment, ListEnvironment
from emomodule import EmoModule, Happy, Concentrated, Bored, Annoyed, Angry, \
                      Surprise
from marc import Marc
from cogmodule import CogModule
from speechmodule import OpenMary

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
        self.exp = Environment(False, False, True)

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

import signal

class TimeoutException(Exception):
    pass

class ListTrainer(QWidget):
    ''' Gui for a simple vocabulary trainer
    '''
    def __init__(self, parent=None):
        super(ListTrainer, self).__init__(parent)
        # Create widgets:
        label_emo_output = QLabel('Emotional Output:')
        label_cog_output = QLabel('Cognition Output:')
        label_speech_output = QLabel('Speech Output:')

        self.emo_output = QLabel('')
        self.cog_output = QLabel('')
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
        agent_layout.addWidget(label_cog_output, 1, 0)
        agent_layout.addWidget(self.cog_output, 1, 1)
        agent_layout.addWidget(label_speech_output, 2, 0)
        agent_layout.addWidget(self.speech_output, 2, 1)

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
        self.exp = ListEnvironment(False, False, False)

        emotion, cog, speech = self.exp.start()
        self.update_output(emotion, cog, speech)
        self.phase = 0

        # test: throw a signal that will change the display in 2 seconds.

        print 'start timer'


    def update(self):
        print 'TIME FOR AN UPDARTE!'

    def update_output(self, emotion, cog, speech):
        self.emo_output.setText(emotion)
        self.cog_output.setText(cog)
        self.speech_output.setText(speech)

    def present(self):
        if self.exp.has_next():
            emotion, cog, speech = self.exp.present_next()
            self.update_output(emotion, cog, speech)
            QTimer.singleShot(1000, self.present)
        else:
            self.speech_output.setText('')
            self.next_button.show()
            self.exp.reset()

    def next(self):
        ''' Show next task
        '''
        if self.phase == 0:
            self.phase += 1
            self.next_button.hide()
            emotion, cog, speech = self.exp.introduce()

            self.update_output(emotion, cog, speech)

            # present word list
            timer = QTimer();

            QTimer.singleShot(6000, self.present);
        else:
            if self.user_input.isHidden():
                self.next_button.setText("Next")
                self.user_input.show()

            if not self.exp.has_next():
                self.end()
            else:
                # wait for user input
                # show cognitive expecation here
                emotion, cog, speech = self.exp.wait()

                self.update_output(emotion, cog, speech)

                self.label_solution.setText('')
                self.next_button.hide()
                self.user_input.setStyleSheet('QLineEdit {color: black}')
                self.user_input.setText('')
                self.user_input.setReadOnly(False)
                self.submit_button.show()

    def submit(self):
        ''' Submit an answer by the user
        '''
        word = self.user_input.text()

        if word == "":
            QMessageBox.information(self, "Empty Field", "Please enter a word")
            return

        self.user_input.setReadOnly(True)
        correct = self.exp.check(word)


        emotion, cog, speech = self.exp.evaluate(correct)

        if correct:
            self.user_input.setStyleSheet('QLineEdit {color: green}')
        else:
            self.user_input.setStyleSheet('QLineEdit {color: red}')
            #self.label_solution.setText(self.exp.words[self.exp.index].word)

        self.update_output(emotion, cog, speech)

        self.submit_button.hide()
        self.next_button.show()

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
        self.setLayout(self.init_ui())
        #self.resize(600, 100)
        self.e = None

    def init_ui(self):
        ''' Creates the layout of the settings screen
        '''
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


class NetworkSettings(Settings):
    ''' Frame showing all program settings

        wasabi      ->  emotion  intensity  interpolate  hz/trigger
        happy
        concentrated
        bored
        annoyed
        angry
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
        # Network settings
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

        self.e = Environment(False, False, False)

    def test_wasabi(self):
        self.apply_settings()
        self.e.test_wasabi()

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


class Parameters(Settings):
    ''' Frame showing all program variables

        Matching: Baselevel activation  -> surprise, emotion, intense

        Expectations:
            - high
            - low
            - none
            - negative
    '''

    def __init__(self, parent=None):
        def init(Emotion):
            return [QLineEdit(Emotion.MARC),
                    self.float_widget(Emotion.IMPULSE, 0.01, 2.00, 0.01),
                    self.float_widget(Emotion.INTERPOLATE, 0.01, 2.00, 0.01),
                    self.int_widget(Emotion.FREQUENCE, 1, 20, 1)]

        self.emo_settings = \
            {'happy': init(Happy),
             'concentrated': init(Concentrated),
             'bored': init(Bored),
             'annoyed': init(Annoyed),
             'angry': init(Angry),
             'surprise': init(Surprise)}

        self.function = self.function_box(CogModule.FUNCTION)

        self.activations = \
            [self.float_widget(CogModule.ACT_HIGH, -10.0, 10.0, 0.1),
             self.float_widget(CogModule.ACT_LOW, -10.0, 10.0, 0.1)]
             #self.float_widget(CogModule.ACT_NONE, -10.0, 10.0, 0.1)]

        self.emotion = {'Happy': [self.combo_box(EmoModule.REACT_NEG_HAPPY[0]), self.combo_box(EmoModule.REACT_POS_HAPPY[0])],
                   'Concentrated': [self.combo_box(EmoModule.REACT_NEG_CONCENTRATED[0]), self.combo_box(EmoModule.REACT_POS_CONCENTRATED[0])],
                   'Bored': [self.combo_box(EmoModule.REACT_NEG_BORED[0]), self.combo_box(EmoModule.REACT_POS_BORED[0])],
                   'Annoyed': [self.combo_box(EmoModule.REACT_NEG_ANNOYED[0]), self.combo_box(EmoModule.REACT_POS_ANNOYED[0])],
                   'Angry': [self.combo_box(EmoModule.REACT_NEG_ANGRY[0]), self.combo_box(EmoModule.REACT_POS_ANGRY[0])]}

        self.intense = {\
            'Happy': [[self.wIntense(100), self.wIntense(100), self.wIntense(100)],
                [self.wIntense(100), self.wIntense(100), self.wIntense(100)]],
            'Concentrated': [[self.wIntense(100), self.wIntense(100), self.wIntense(100)],
                [self.wIntense(100), self.wIntense(100), self.wIntense(100)]],
            'Bored': [[self.wIntense(100), self.wIntense(100), self.wIntense(100)],
                [self.wIntense(100), self.wIntense(100), self.wIntense(100)]],
            'Annoyed': [[self.wIntense(100), self.wIntense(100), self.wIntense(100)],
                [self.wIntense(100), self.wIntense(100), self.wIntense(100)]],
            'Angry': [[self.wIntense(100), self.wIntense(100), self.wIntense(100)],
                [self.wIntense(100), self.wIntense(100), self.wIntense(100)]]}


        super(Parameters, self).__init__(parent)


    def get_emo_values(self):
        # Emotion settings
        layout = QGridLayout()

        label_emotions = QLabel('Emotions:')
        label_emotions.setStyleSheet('QLabel {font-weight:bold}')
        layout.addWidget(label_emotions, 0, 0)

        def add_line(layout, values, line):
            for i in range(len(values)):
                layout.addWidget(values[i], line, i)
        add_line(layout, [QLabel('Wasabi:'), QLabel('Marc:'), QLabel('Impulse'),
                          QLabel('Interpolate'), QLabel('Frequence')], 1)
        add_line(layout, [QLabel('Happy')] + self.emo_settings['happy'], 2)
        add_line(layout, [QLabel('Concentrated')] + self.emo_settings['concentrated'], 3)
        add_line(layout, [QLabel('Bored')] + self.emo_settings['bored'], 4)
        add_line(layout, [QLabel('Annoyed')] + self.emo_settings['annoyed'], 5)
        add_line(layout, [QLabel('Angry')] + self.emo_settings['angry'], 6)
        add_line(layout, [QLabel('Surprise')] + self.emo_settings['surprise'], 7)

        def add_test_button(layout, line, function):
            button = QPushButton('&Test')
            button.clicked.connect(function)
            layout.addWidget(button, line, 5)

        add_test_button(layout, 2, self.test_happy)
        add_test_button(layout, 3, self.test_concentrated)
        add_test_button(layout, 4, self.test_bored)
        add_test_button(layout, 5, self.test_annoyed)
        add_test_button(layout, 6, self.test_angry)
        add_test_button(layout, 7, self.test_surprise)

        emo_values = QWidget()
        emo_values.setLayout(layout)
        return emo_values

    def combo_box(self, selected):
        items = ['Happy', 'Concentrated', 'Bored', 'Annoyed', 'Angry']
        combo = QComboBox()
        combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        combo.addItems(items)

        if selected in items:
            combo.setCurrentIndex(items.index(selected))
        print 'init combo box with ', selected

        combo.resize(300, 30)
        return combo


    def function_box(self, selected):
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

    def float_widget(self, start_val, min_val, max_val, step):
        box = QDoubleSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def int_widget(self, start_val, min_val, max_val, step):
        box = QSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def wIntense(self, start_val):
        box = QSpinBox()
        box.setRange(0, 100)
        box.setValue(start_val)
        box.setSingleStep(1)
        return box


    def init_parameters(self):
        ''' Creates the layout of the settings screen
        '''
        names = ['Happy', 'Concentrated', 'Bored', 'Annoyed', 'Angry']

        desc_layout = QBoxLayout(2)
        desc_layout.addWidget(QLabel('Current emotion:'))
        for name in names:
            desc_layout.addWidget(QLabel(name + ':'))
        desc_widget = QWidget()
        desc_widget.setLayout(desc_layout)

        def get_emo_widget(correct):
            layout = QBoxLayout(2)
            layout.addWidget(QLabel('Emotion:'))
            for name in names:
                layout.addWidget(self.emotion[name][correct])
            widget = QWidget()
            widget.setLayout(layout)
            return widget

        def get_int_widget(correct):
            layout = QGridLayout()
            self.add_line(layout, [QLabel('None'), QLabel('Low'), QLabel('High')], 0)
            for name in names:
                self.add_line(layout, self.intense[name][correct], names.index(name) + 1)
            widget = QWidget()
            widget.setLayout(layout)
            return widget

        map_layout = QGridLayout()
        map_layout.addWidget(desc_widget, 0, 0)
        map_layout.addWidget(get_emo_widget(0), 0, 1)
        map_layout.addWidget(get_int_widget(0), 0, 2)
        map_layout.addWidget(get_emo_widget(1), 0, 3)
        map_layout.addWidget(get_int_widget(1), 0, 4)

        map_widget = QWidget()
        map_widget.setLayout(map_layout)



        main_layout = QBoxLayout(2)
        #main_layout.addWidget(self.get_emo_values())
        main_layout.addWidget(self.get_activation_widget())
        main_layout.addWidget(map_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        return main_widget

    def add_line(self, layout, values, line):
        for i in range(len(values)):
            layout.addWidget(values[i], line, i)

    def get_activation_widget(self):

        desc = QLabel('Activation:')
        desc.setStyleSheet('QLabel {font-weight:bold}')

        function_layout = QBoxLayout(0)
        function_layout.addWidget(QLabel('Function:'))
        function_layout.addWidget(self.function)
        function_widget = QWidget()
        function_widget.setLayout(function_layout)

        exp_layout = QBoxLayout(0)
        exp_layout.addWidget(QLabel('Expection:'))
        exp_layout.addWidget(QLabel('Not expected'))
        exp_layout.addWidget(QLabel(' < '))
        exp_layout.addWidget(self.activations[1])
        exp_layout.addWidget(QLabel(' < '))
        exp_layout.addWidget(QLabel('Expected'))
        exp_layout.addWidget(QLabel(' < '))
        exp_layout.addWidget(self.activations[0])
        exp_layout.addWidget(QLabel(' < '))
        exp_layout.addWidget(QLabel('Highly expected'))
        exp_widget = QWidget()
        exp_widget.setLayout(exp_layout)

        layout = QBoxLayout(2)
        layout.addWidget(desc)
        layout.addWidget(function_widget)
        layout.addWidget(exp_widget)
        widget = QWidget()
        widget.setLayout(layout)

        extra_layout = QBoxLayout(0)
        extra_layout.addWidget(widget)
        extra_layout.addWidget(QLabel(''))
        extra_widget = QWidget()
        extra_widget.setLayout(extra_layout)
        return extra_widget


    def apply_settings(self):
        ''' apply settings loaded from the gui
        '''
        def apply_emo(emo_class, emo_key):
            emo_class.MARC = self.emo_settings[emo_key][0].text()
            emo_class.IMPULSE = self.emo_settings[emo_key][1].value()
            emo_class.INTERPOLATE = self.emo_settings[emo_key][2].value()
            emo_class.FREQUENCE = self.emo_settings[emo_key][3].value()

        CogModule.ACT_HIGH = self.activations[0].value()
        CogModule.ACT_LOW = self.activations[0].value()

        CogModule.FUNCTION = self.get_function(self.function)

        pos_emotion = {'Happy': EmoModule.REACT_POS_HAPPY,
                        'Concentrated': EmoModule.REACT_POS_CONCENTRATED,
                        'Bored': EmoModule.REACT_POS_BORED,
                        'Annoyed': EmoModule.REACT_POS_ANNOYED,
                        'Angry': EmoModule.REACT_POS_ANGRY}

        neg_emotion = {'Happy': EmoModule.REACT_NEG_HAPPY,
                        'Concentrated': EmoModule.REACT_NEG_CONCENTRATED,
                        'Bored': EmoModule.REACT_NEG_BORED,
                        'Annoyed': EmoModule.REACT_NEG_ANNOYED,
                        'Angry': EmoModule.REACT_NEG_ANGRY}

        def apply_emotion(VAR, name, correct):
            EmoModule.VAR = (self.get_class(self.emotion[name][correct]),
                             self.intense[name][correct][0].value(),
                             self.intense[name][correct][1].value(),
                             self.intense[name][correct][2].value())

        for name in pos_emotion.keys():
            apply_emotion(pos_emotion[name], name, 1)

        for name in neg_emotion.keys():
            apply_emotion(neg_emotion[name], name, 0)

        self.e = Environment(False, False, False)

    def get_function(self, combo_box):
        functions = ['baselevel', 'optimized']
        if combo_box.currentIndex() >= len(functions):
            print 'COMBOBOX: INDEX ERROR'
        else:
            return functions[combo_box.currentIndex()]


    def get_class(self, combo_box):
        classes = ['Happy', 'Concentrated', 'Bored', 'Annoyed', 'Angry']
        if combo_box.currentIndex() >= len(classes):
            print 'COMBOBOX: INDEX ERROR'
        else:
            return classes[combo_box.currentIndex()]

    def reset(self):
        '''
        '''
        self.emo_settings['happy'][0].setText('CASA_Joy_01')
        self.emo_settings['happy'][1].setValue(0.66)
        self.emo_settings['happy'][2].setValue(1.0)
        self.emo_settings['happy'][3].setValue(2)

        self.emo_settings['concentrated'][0].setText(CASA_Relax_01)
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
        pass


class Emotions(Settings):
    ''' Frame showing all program variables

        Matching: Baselevel activation  -> surprise, emotion, intense

        Expectations:
            - high
            - low
            - none
            - negative
    '''

    def __init__(self, parent=None):
        def init(Emotion):
            return [QLineEdit(Emotion.MARC),
                    self.float_widget(Emotion.IMPULSE, 0.01, 2.00, 0.01),
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

    def get_emo_values(self):
        # Emotion settings
        layout = QGridLayout()

        label_emotions = QLabel('Emotions:')
        label_emotions.setStyleSheet('QLabel {font-weight:bold}')
        layout.addWidget(label_emotions, 0, 0)

        def add_line(layout, values, line):
            for i in range(len(values)):
                layout.addWidget(values[i], line, i)
        add_line(layout, [QLabel('Wasabi:'), QLabel('Marc:'), QLabel('Impulse'),
                          QLabel('Interpolate'), QLabel('Frequence')], 1)
        add_line(layout, [QLabel('Happy')] + self.emo_settings['happy'], 2)
        add_line(layout, [QLabel('Concentrated')] + self.emo_settings['concentrated'], 3)
        add_line(layout, [QLabel('Bored')] + self.emo_settings['bored'], 4)
        add_line(layout, [QLabel('Annoyed')] + self.emo_settings['annoyed'], 5)
        add_line(layout, [QLabel('Angry')] + self.emo_settings['angry'], 6)
        add_line(layout, [QLabel('Surprise')] + self.emo_settings['surprise'], 7)

        def add_test_button(layout, line, function):
            button = QPushButton('&Test')
            button.clicked.connect(function)
            layout.addWidget(button, line, 5)

        add_test_button(layout, 2, self.test_happy)
        add_test_button(layout, 3, self.test_concentrated)
        add_test_button(layout, 4, self.test_bored)
        add_test_button(layout, 5, self.test_annoyed)
        add_test_button(layout, 6, self.test_angry)
        add_test_button(layout, 7, self.test_surprise)

        emo_values = QWidget()
        emo_values.setLayout(layout)
        return emo_values

    def combo_box(self, selected):
        items = ['Happy', 'Concentrated', 'Bored', 'Annoyed', 'Angry']
        combo = QComboBox()
        combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        combo.addItems(items)

        if selected in items:
            combo.setCurrentIndex(items.index(selected))
        print 'init combo box with ', selected

        combo.resize(300, 30)
        return combo

    def float_widget(self, start_val, min_val, max_val, step):
        box = QDoubleSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def int_widget(self, start_val, min_val, max_val, step):
        box = QSpinBox()
        box.setRange(min_val, max_val)
        box.setValue(start_val)
        box.setSingleStep(step)
        return box

    def wIntense(self, start_val):
        box = QSpinBox()
        box.setRange(0, 100)
        box.setValue(start_val)
        box.setSingleStep(1)
        return box


    def init_parameters(self):
        ''' Creates the layout of the settings screen
        '''
        main_layout = QBoxLayout(2)
        main_layout.addWidget(self.get_emo_values())
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        return main_widget

    def apply_settings(self):
        ''' apply settings loaded from the gui
        '''
        def apply_emo(emo_class, emo_key):
            emo_class.MARC = self.emo_settings[emo_key][0].text()
            emo_class.IMPULSE = self.emo_settings[emo_key][1].value()
            emo_class.INTERPOLATE = self.emo_settings[emo_key][2].value()
            emo_class.FREQUENCE = self.emo_settings[emo_key][3].value()

        apply_emo(Happy, 'happy')
        self.e = Environment(False, False, False)

    def get_function(self, combo_box):
        functions = ['baselevel', 'optimized']
        if combo_box.currentIndex() >= len(functions):
            print 'COMBOBOX: INDEX ERROR'
        else:
            return functions[combo_box.currentIndex()]

    def reset(self):
        '''
        '''
        self.emo_settings['happy'][0].setText('CASA_Joy_01')
        self.emo_settings['happy'][1].setValue(0.66)
        self.emo_settings['happy'][2].setValue(1.0)
        self.emo_settings['happy'][3].setValue(2)

        self.emo_settings['concentrated'][0].setText(CASA_Relax_01)
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
        pass

    def test_wasabi(self):
        self.apply_settings()
        self.e.test_wasabi()

    def test_happy(self):
        self.apply_settings()
        self.test(Happy())

    def test_concentrated(self):
        self.apply_settings()
        self.test(Concentrated())

    def test_bored(self):
        self.apply_settings()
        self.test(Bored())

    def test_annoyed(self):
        self.apply_settings()
        self.test(Annoyed())

    def test_angry(self):
        self.apply_settings()
        self.test(Angry())

    def test_surprise(self):
        self.apply_settings()
        self.test(Surprise())

    def test(self, emotion):
        ''' Test current settings
        '''
        self.e.test(emotion, 10)


class Welcome(QWidget):
    ''' Frame at the start of the vocabulary trainer
    '''
    def __init__(self, parent=None):
        super(Welcome, self).__init__(parent)

        # Create widgets:
        desc = QLabel('Welcome to the vocabulary trainer.')

        button_settings = QPushButton("&Edit settings")
        button_emotions = QPushButton('&Edit emotions')
        button_mapping = QPushButton('&Edit mapping')
        button_start = QPushButton('&Start training')
        button_list = QPushButton('&Start list training')

        # Define button funcionalty:
        button_settings.clicked.connect(self.options)
        button_emotions.clicked.connect(self.emotions)
        button_mapping.clicked.connect(self.mapping)
        button_start.clicked.connect(self.start)
        button_list.clicked.connect(self.list_test)

        # Design Layout:
        option_layout = QBoxLayout(2)
        option_layout.addWidget(button_settings)
        option_layout.addWidget(button_emotions)
        option_layout.addWidget(button_mapping)
        option_layout.addWidget(button_start)
        option_layout.addWidget(button_list)
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

    def emotions(self):
        ''' Show emotions
        '''
        self.emit(SIGNAL('emotions'))

    def mapping(self):
        ''' Show mapping
        '''
        self.emit(SIGNAL('mapping'))

    def start(self):
        ''' Start test
        '''
        self.emit(SIGNAL('training'))

    def list_test(self):
        ''' Start list test
        '''
        self.emit(SIGNAL('list_test'))


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
        self.connect(new, SIGNAL('triggered()'), self.show_training)

        settings = QAction(QIcon('icons/icon.png'),
                                 'NetworkSettings', self)
        self.connect(settings, SIGNAL('triggered()'), self.show_options)

        self.statusBar()

        menubar = self.menuBar()

        menuFile = menubar.addMenu('&File')
        menuFile.addAction(new)

        options = menubar.addMenu('&Options')
        options.addAction(settings)

        self.setMenuBar(menubar)
        self.load_config()
        print 'EmoModule.REACT_POS_ANGRY:', EmoModule.REACT_POS_ANGRY
        self.show_welcome()
        print 'EmoModule.REACT_POS_ANGRY:', EmoModule.REACT_POS_ANGRY
        self.move(0, 0)

    def load_config(self):
        ''' loads the init values from the config file
        '''
        config = ConfigParser.SafeConfigParser()
        config.read('emotutor.cfg')
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
            emo_class.MARC = config.get(emo_name, 'marc')
            emo_class.IMPULSE = config.getfloat(emo_name, 'impulse')
            emo_class.INTERPOLATE = config.getfloat(emo_name, 'interpolate')
            emo_class.FREQUENCE = config.getint(emo_name, 'frequence')

        apply_emo(Happy, 'Happy')
        apply_emo(Concentrated, 'Concentrated')
        apply_emo(Bored, 'Bored')
        apply_emo(Annoyed, 'Annoyed')
        apply_emo(Angry, 'Angry')
        apply_emo(Surprise, 'Surprise')

        CogModule.ACT_HIGH = config.getfloat('Activation', 'high')
        CogModule.ACT_LOW = config.getfloat('Activation', 'low')

        def get_config(name):
            return (config.get(name, 'emotion'),
                     config.getint(name, 'none'),
                     config.getint(name, 'low'),
                     config.getint(name, 'high'))

        EmoModule.REACT_NEG_HAPPY = get_config('Map_Happy_Neg')
        EmoModule.REACT_NEG_CONCENTRATED = get_config('Map_Concentrated_Neg')
        EmoModule.REACT_NEG_BORED = get_config('Map_Bored_Neg')
        EmoModule.REACT_NEG_ANNOYED = get_config('Map_Annoyed_Neg')
        EmoModule.REACT_NEG_ANGRY = get_config('Map_Angry_Neg')

        EmoModule.REACT_POS_HAPPY = get_config('Map_Happy_Pos')
        EmoModule.REACT_POS_CONCENTRATED = get_config('Map_Concentrated_Pos')
        EmoModule.REACT_POS_BORED = get_config('Map_Bored_Pos')
        EmoModule.REACT_POS_ANNOYED = get_config('Map_Annoyed_Pos')
        EmoModule.REACT_POS_ANGRY = get_config('Map_Angry_Pos')

    def show_welcome(self):
        ''' Shows the welcome screen
        '''
        welcome = Welcome()
        self.connect(welcome, SIGNAL('settings'), self.show_options)
        self.connect(welcome, SIGNAL('emotions'), self.show_emotions)
        self.connect(welcome, SIGNAL('mapping'), self.show_mapping)
        self.connect(welcome, SIGNAL('training'), self.show_training)
        self.connect(welcome, SIGNAL('list_test'), self.show_list_training)
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

    def show_training(self):
        ''' Starts the training

        '''
        print 'start button pressed'
        trainer = VocabTrainer()
        trainer.show()
        self.setCentralWidget(trainer)

    def show_list_training(self):
        ''' Starts the list training

        '''
        trainer = ListTrainer()
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

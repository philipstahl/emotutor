''' The gui implimentation in pyqt4
'''

import sys
import ConfigParser

from PyQt4.QtGui import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, \
                        QBoxLayout, QMainWindow, QAction, QIcon, \
                        QApplication, QDesktopWidget, QMessageBox, \
                        QDoubleSpinBox, QSpinBox, QComboBox, QCheckBox

from PyQt4.QtCore import SIGNAL, Qt, QTimer

from environment import Environment
from emomodule import EmoModule, Happy, Concentrated, Bored, Annoyed, Angry, \
                      Surprise
from marc import Marc
from cogmodule import CogModule
from speechmodule import OpenMary


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
        #192.168.0.46
        self.exp = Environment(False, True, False)

        emotion, cog, speech = self.exp.start()
        self.update_output(emotion, cog, speech)
        self.phase = 0

    def update_output(self, emotion, cog, speech):
        ''' Updates the text output of the agent.
        '''
        self.emo_output.setText(emotion)
        self.cog_output.setText(cog)
        self.speech_output.setText(speech)

    def present(self):
        ''' Presents a single word.
        '''
        if self.exp.has_next():
            emotion, cog, speech = self.exp.present_next()
            self.update_output(emotion, cog, speech)
            QTimer.singleShot(1000, self.present)
        else:
            self.speech_output.setText('')
            self.next_button.show()
            self.exp.reset()

    def next(self):
        ''' Introduce or show next task
        '''
        if self.phase == 0:
            self.phase += 1
            self.next_button.hide()
            emotion, cog, speech = self.exp.introduce()

            self.update_output(emotion, cog, speech)

            # present word list
            QTimer.singleShot(6000, self.present)
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

        self.environment = Environment(False, False, False)

    def test_wasabi(self):
        ''' Tests if messages are received from wasabi.
        '''
        self.apply_settings()
        self.environment.test_wasabi()

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
        self.environment = Environment(False, False, False)

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
        self.environment.test(emotion, 5)


class Parameters(Settings):
    ''' Frame showing the activation function and emotional reactions according
        to the given activation.
    '''

    def __init__(self, parent=None):
        self.function = self.function_box(CogModule.FUNCTION)

        self.activations = \
            [self.float_widget(CogModule.ACT_HIGH, -10.0, 10.0, 0.1),
             self.float_widget(CogModule.ACT_NONE, -10.0, 10.0, 0.1)]

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
             'Pos': self.check_box(EmoModule.REACT_POS_RIGHT[0])}]


        self.emotion = [\
            {'Neg': self.combo_box(EmoModule.REACT_NEG_WRONG[1]),
             'None': self.combo_box(EmoModule.REACT_NONE_WRONG[1]),
             'Pos': self.combo_box(EmoModule.REACT_POS_WRONG[1])},
            {'Neg': self.combo_box(EmoModule.REACT_NEG_RIGHT[1]),
             'None': self.combo_box(EmoModule.REACT_NONE_RIGHT[1]),
             'Pos': self.combo_box(EmoModule.REACT_POS_RIGHT[1])}]

        self.impulse = [\
            {'Neg': self.int_widget(EmoModule.REACT_NEG_WRONG[2]),
             'None': self.int_widget(EmoModule.REACT_NONE_WRONG[2]),
             'Pos': self.int_widget(EmoModule.REACT_POS_WRONG[2])},
            {'Neg': self.int_widget(EmoModule.REACT_NEG_RIGHT[2]),
             'None': self.int_widget(EmoModule.REACT_NONE_RIGHT[2]),
             'Pos': self.int_widget(EmoModule.REACT_POS_RIGHT[2])}]

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


        desc1 = QLabel('Map activation to expectation:')
        desc2 = QLabel('Map expectation to emotion:')
        desc3 = QLabel('Map expectation + answer to reaction:')
        for desc in [desc1, desc2, desc3]:
            desc.setStyleSheet('QLabel {font-weight:bold}')

        main_layout.addWidget(desc1)
        main_layout.addWidget(self.get_function_widget())
        main_layout.addWidget(self.get_activation_widget())
        main_layout.addWidget(desc2)
        main_layout.addWidget(self.get_expectation_widget())
        main_layout.addWidget(desc3)
        main_layout.addWidget(self.get_reaction_widget())
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        return main_widget

    def get_function_widget(self):
        ''' Returns the widget containing the function settings
        '''
        layout = QBoxLayout(0)
        layout.addWidget(QLabel('Function:'))
        layout.addWidget(self.function)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def get_activation_widget(self):
        ''' Returns the widget containint the activation settings.
        '''
        layout = QGridLayout()
        layout.addWidget(QLabel('Expection:'), 0, 0)
        layout.addWidget(QLabel('Negative'), 0, 1)
        layout.addWidget(QLabel(' < '), 0, 2)
        layout.addWidget(self.activations[1], 0, 3)
        layout.addWidget(QLabel(' < '), 0, 4)
        layout.addWidget(QLabel('None'), 0, 5)
        layout.addWidget(QLabel(' < '), 0, 6)
        layout.addWidget(self.activations[0], 0, 7)
        layout.addWidget(QLabel(' < '), 0, 8)
        layout.addWidget(QLabel('Positive'), 0, 9)

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
        layout.addWidget(QLabel('Intense:'), 0, 4)

        def add(layout, expectation, answer, correct, expect, line):
            layout.addWidget(QLabel(expectation), line, 0)
            layout.addWidget(QLabel(answer), line, 1)
            layout.addWidget(self.surprise[correct][expect], line, 2)
            layout.addWidget(self.emotion[correct][expect], line, 3)
            layout.addWidget(self.impulse[correct][expect], line, 4)

        add(layout, 'Negative', 'Wrong', 0, 'Neg', 1)
        add(layout, 'Negative', 'Correct', 1, 'Neg', 2)
        add(layout, 'None', 'Wrong', 0, 'None', 3)
        add(layout, 'None', 'Correct', 1, 'None', 4)
        add(layout, 'Positive', 'Wrong', 0, 'Pos', 5)
        add(layout, 'Positive', 'Correct', 1, 'Pos', 6)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def apply_settings(self):
        ''' apply settings loaded from the gui
        '''
        CogModule.ACT_HIGH = self.activations[0].value()
        CogModule.ACT_LOW = self.activations[1].value()

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

        EmoModule.REACT_NEG_WRONG = get_reaction(0, 'Neg')
        EmoModule.REACT_NONE_WRONG = get_reaction(0, 'None')
        EmoModule.REACT_POS_WRONG = get_reaction(0, 'Pos')
        EmoModule.REACT_NEG_RIGHT = get_reaction(1, 'Neg')
        EmoModule.REACT_NONE_RIGHT = get_reaction(1, 'None')
        EmoModule.REACT_POS_RIGHT = get_reaction(1, 'Pos')

        self.environment = Environment(False, False, False)

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
        button_list = QPushButton('&Start list training')

        # Define button funcionalty:
        button_settings.clicked.connect(self.options)
        button_emotions.clicked.connect(self.emotions)
        button_mapping.clicked.connect(self.mapping)
        button_start.clicked.connect(self.start)
        button_list.clicked.connect(self.list_test)

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
        layout.addWidget(left_bottom, 1, 0)
        layout.addWidget(button_list, 1, 1)
        layout.addWidget(right_bottom, 1, 2)

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
        self.show_welcome()
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

        CogModule.ACT_HIGH = config.getfloat('Activation', 'high')
        CogModule.ACT_NONE = config.getfloat('Activation', 'low')

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

        EmoModule.REACT_NEG_WRONG = get_config('React_Neg_Wrong')
        EmoModule.REACT_NEG_RIGHT = get_config('React_Neg_Right')
        EmoModule.REACT_NONE_WRONG = get_config('React_None_Wrong')
        EmoModule.REACT_NONE_RIGHT = get_config('React_None_Right')
        EmoModule.REACT_POS_WRONG = get_config('React_Pos_Wrong')
        EmoModule.REACT_POS_RIGHT = get_config('React_Pos_Right')

        
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

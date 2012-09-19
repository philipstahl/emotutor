class SpeachModule:
    def __init__(self):
        pass

    def get_verbal_reaction(self, correct, surprise, mood):
        reaction = ""
        if surprise == "[very surprised]":
            reaction += "Unbelievable! "
        elif surprise == "[surprised]":
            reaction += "Oh! "
        if correct and mood == "[very happy]":
            reaction += "Absolutely correct! You are doing a fantastic job!"
        elif correct and mood == "[happy]":
            reaction += "Well done my friend, your answer is correct."
        elif correct and mood == "[normal]":
            reaction += "Allright, your answer is correct."
        elif not correct and mood == "[normal]":
            reaction += "Your answer is wrong."
        elif not correct and mood == "[angry]":
            reaction += "No, that's definitely not the right answer."
        elif not correct and mood == "[very angry]":
            reaction += "What are you doing? Your answer is really annoying!"
        else:
            reaction += "Wrong mood or surprise"
        return reaction

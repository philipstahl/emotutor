import datetime
from emomodule import Happy, Concentrated, Bored, Annoyed, Angry, Fear, \
                      FearsConfirmed, Hope, Relief


def milliseconds(time):
    ''' Returns the given time in milli seconds.
    '''
    seconds = (time.second + 60 * time.minute + 60 * 60 * time.hour)
    milliseconds = seconds * 1000
    return time.microsecond / 100 + milliseconds

def emotion_by_name(name, impulse=100):
    ''' Returns an emotion object with the given impulse.
    '''
    if not name or name == 'None' or impulse == 0:
        return None

    con = Concentrated()

    name = name.lower()
    name_to_emotion = {'happy': Happy(impulse=impulse),
                       'concentrated': Concentrated(impulse=impulse),
                       'bored': Bored(impulse=impulse),
                       'annoyed': Annoyed(impulse=impulse),
                       'angry': Angry(impulse=impulse),
                       'fear': Fear(),
                       'fears-confirmed': FearsConfirmed(),
                       'hope': Hope(),
                       'relief': Relief()}

    if name in name_to_emotion.keys():
        return name_to_emotion[name]
    else:
        return None

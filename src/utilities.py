import datetime
from emomodule import Happy, Concentrated, Bored, Annoyed, Angry

def seconds(time):
    ''' Returns the given time in seconds.
    '''
    return (time.second + 60 * time.minute + 60 * 60 * time.hour)

def milliseconds(time):
    ''' Returns the given time in milli seconds.
    '''
    return time.microsecond / 100 + seconds(time) * 1000

def emotion_by_name(name, impulse=100):
    ''' Returns an emotion object with the given impulse.
    '''
    if name == 'None' or impulse == 0:
        return None

    name = name.lower()
    name_to_emotion = {'happy': Happy(impulse=impulse), 'concentrated': Concentrated(impulse=impulse),
                       'bored': Bored(impulse=impulse), 'annoyed': Annoyed(impulse=impulse), 'angry': Angry(impulse=impulse)}
    if name in name_to_emotion.keys():
        return name_to_emotion[name]
    else:
        return None

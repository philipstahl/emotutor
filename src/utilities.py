import datetime
from emomodule import Happy, Concentrated, Bored, Annoyed, Angry

def seconds(time):
    ''' Returns the given time in seconds.
    '''
    return (time.second + 60 * time.minute + 60 * 60 * time.hour) * 1000 + time.microsecond / 100

def millisecond(time):
    ''' Returns the given time in milli seconds.
    '''
    return time.microsecond / 100 + seconds(time) * 1000

def emotion_by_name(name, impulse=100):
    ''' Returns an emotion object with the given impulse.
    '''
    if name == 'None' or impulse == 0:
        return None

    name = name.lower()
    name_to_emotion = {'happy': Happy, 'concentrated': Concentrated,
                       'bored': Bored, 'annoyed': Annoyed, 'angry': Angry}
    if name in name_to_emotion.keys():
        return name_to_emotion[name](impulse=impulse)
    else:
        return None

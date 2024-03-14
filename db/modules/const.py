
class Error():
    def dbDoesNotExist(self):
        return 'Данная база данных не существует.'

    def gestureDoesNotExist(self):
        return 'Данный жест не существует в указанном словаре.'

class Path():
    def __init__(self):
        self.gestures = 'db/gestures/'
        self.dictionaries = 'db/gestures/dictionaries/'

class ConstPlenty():
    def __init__(self):
        self.commonPath = '/'.join(__file__.split('/')[:-2]) + '/'
        self.mainPath = '/'.join(__file__.split('/')[:-3]) + '/'
        self.path = Path()
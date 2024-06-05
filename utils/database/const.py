
from utils.const import GlobalConstPlenty
from utils.funcs import joinPath

class Error():
    def __init__(self):
        self.doesNotExist = 'Данная база данных не существует.'

class Names():
    def __init__(self):
        self.dbFolder = 'gestures'
        self.dbFile = 'indexations.json'

class ConstPlenty(GlobalConstPlenty):
    def __init__(self):
        super().__init__()
        self.error = Error()
        self.path.file.indexations = joinPath(self.path.gestures, 'indexations.json')
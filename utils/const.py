
from utils.funcs import joinPath

class LmList:
    def __init__(self):
        self.parentPoints = (-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9,
                             10, 11, 0, 13, 14, 15, 0, 17, 18, 19)

class Bones:
    def __init__(self):
        self.parentPoints = (-1, 0, 1, 2, -1, 4, 5, 6, -1, 8, 9,
                             10, -1, 12, 13, 14, -1, 16, 17, 18)

class Palm:
    def __init__(self):
        self.centerPoints = (0, 5, 17)
        self.centerBones = (4, 8, 12, 16)

class Hands:
    def __init__(self):
        self.lmList = LmList()
        self.bones = Bones()
        self.palm = Palm()
        self.right = 'right'
        self.left = 'left'

class File:
    def __init__(self):
        pass

class Camera:
    def __init__(self):
        self.index = 0

class Path:
    def __init__(self):
        self.project = joinPath('/', *__file__.split('/')[:-2])
        self.assets = joinPath(self.project, 'assets')
        self.db = joinPath(self.project, 'db')
        self.gestures = joinPath(self.db, 'gestures')
        self.dictionaries = joinPath(self.gestures, 'dictionaries')
        self.generator = joinPath(self.project, 'generator')
        self.server = joinPath(self.project, 'server')
        self.service = joinPath(self.project, 'service')
        self.utils = joinPath(self.project, 'utils')
        self.web = joinPath(self.project, 'web')
        self.file = File()

class GlobalConstPlenty:
    def __init__(self):
        self.path = Path()
        self.hands = Hands()
        self.camera = Camera()
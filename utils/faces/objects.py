
class Face:
    def __init__(self, lmList: tuple = None):
        if lmList is None: self.lmList = []
        else: self.lmList = lmList
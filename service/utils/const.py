from pydantic import BaseModel

class Position(BaseModel):
    x: int
    y: int

class Point(BaseModel):
    pos: Position
    color: list
    radius: float

class Line(BaseModel):
    start: Position
    end: Position
    color: list
    thickness: float

class Path():
    def __init__(self):
        self.gestures = 'db/gestures/'
        self.dictionaries = 'db/gestures/dictionaries/'

class Hands():
    def __init__(self):
        self.parentPoints = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
        self.right = 'right'
        self.left = 'left'

class ConstPlenty():
    def __init__(self):
        self.commonPath = '/'.join(__file__.split('/')[:-2]) + '/'
        self.mainPath = '/'.join(__file__.split('/')[:-3]) + '/'
        self.hands = Hands()
        self.path = Path()
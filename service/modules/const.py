
from utils.const import GlobalConstPlenty

from pydantic import BaseModel

class WebPosition(BaseModel):
    x: int
    y: int

class WebPoint(BaseModel):
    pos: WebPosition
    color: list
    radius: float

class WebLine(BaseModel):
    start: WebPosition
    end: WebPosition
    color: list
    thickness: float

class ConstPlenty(GlobalConstPlenty):
    def __init__(self):
        super().__init__()
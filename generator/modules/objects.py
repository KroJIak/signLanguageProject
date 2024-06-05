
class GestureImage:
    def __init__(self, name: str, format: str, path: str):
        self.name = name
        self.format = format
        self.path = path

    def __str__(self):
        return f'[GestureImage] name: {self.name} format: {self.format}'

class DictionaryInfo:
    def __init__(self, name: str, command: str, path: str, images: tuple = None):
        self.name = name
        self.command = command
        self.path = path
        if images is None: self.images = []
        else: self.images = images

    def __str__(self):
        return f'[DictionaryInfo] name: {self.name} command: {self.command}'

from utils.const import GlobalConstPlenty
from utils.funcs import joinPath

class Files():
    def __init__(self):
        self.allowedFormats = ('png', 'jpg', 'jpeg')

class ConstPlenty(GlobalConstPlenty):
    def __init__(self):
        super().__init__()
        self.files = Files()
        self.path.images = joinPath(self.path.generator, 'images')

class Messages:
    def __init__(self):
        self.start = 'Приветствую в программе для генерации базы жестов. Выберите папки, из которых нужно добавить или переустановить жесты.'

    def getInstruction(self, folderName):
        return f'> {folderName} | [Enter - skip; A - add; R - replace]: '
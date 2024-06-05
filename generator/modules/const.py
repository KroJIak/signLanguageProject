
from utils.const import GlobalConstPlenty

class Files():
    def __init__(self):
        self.allowedFormats = ('png', 'jpg', 'jpeg')

class ConstPlenty(GlobalConstPlenty):
    def __init__(self):
        super().__init__()
        self.files = Files()

class Messages:
    def __init__(self):
        self.start = 'Приветствую в программе для генерации базы жестов. Выберите папки, из которых нужно добавить или переустановить жесты.'

    def getInstruction(self, folderName):
        return f'> {folderName} | [Enter - skip; A - add; R - replace]: '
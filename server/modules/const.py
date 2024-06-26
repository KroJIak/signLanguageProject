
from utils.const import GlobalConstPlenty
from utils.funcs import joinPath

class Certificates:
    def __init__(self, webPath):
        self.keyfile = joinPath(webPath, 'certificates', 'signlanguageproject.key')
        self.certfile = joinPath(webPath, 'certificates', 'signlanguageproject.crt')

class ConstPlenty(GlobalConstPlenty):
    def __init__(self):
        super().__init__()
        self.cert = Certificates(self.path.web)
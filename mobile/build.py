import os

def findFileByExt(extension):
    curNameFile = os.path.basename(__file__)
    files = os.listdir()
    files.pop(files.index(curNameFile))
    extFiles = [file for file in files if file[file.rfind('.'):] == extension]
    return extFiles[0]

#nameScript = findFileByExt('.py')
nameScript = 'mapp.py'
#nameImage = findFileByExt('.png')
nameImage = 'icon.png'

os.system(f'flet publish {nameScript} --web-render html')
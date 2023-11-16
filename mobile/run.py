import os

def findFileByExt(extension):
    curNameFile = os.path.basename(__file__)
    files = os.listdir()
    files.pop(files.index(curNameFile))
    extFiles = [file for file in files if file[file.rfind('.'):] == extension]
    return extFiles[0]

#nameScript = findFileByExt('.py')
nameScript = 'mapp.py'

os.system(f'flet -r {nameScript}')
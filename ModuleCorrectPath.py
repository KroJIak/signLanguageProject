
def getCorrectPathByPyScript(file):
    mainPath = '/'.join(file.split('/')[:-1])
    return mainPath

def main():
    mainPath = getCorrectPathByPyScript(__file__)
    print(mainPath)

if __name__ == '__main__':
    main()


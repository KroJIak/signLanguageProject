import os

from generator.modules.const import ConstPlenty, Messages
from generator.modules.objects import GestureImage, DictionaryInfo
from generator.modules.database.worker import dbDictWorker, dbGestureWorker
from utils.hands.detector import HandDetector
from utils.hands.objects import BoneVector, Gesture
from utils.funcs import joinPath

import cv2

const = ConstPlenty()
messages = Messages()

detHands = HandDetector(detectionCon=0.6, minTrackCon=0.6, staticImage=True)
dbDictionaries = dbDictWorker()

def getFolderNames():
    folders = os.listdir(const.path.assets)
    return tuple(folders)

def getCommandsForFolders(folderNames):
    commands = {}
    for name in folderNames:
        while True:
            command = input(messages.getInstruction(name)).lower()
            if command in ['', 'a', 'r']: break
        if command != '': commands[name] = command
    return commands

def getImagesFromDict(dictionary):
    return tuple(os.listdir(joinPath(const.path.assets, dictionary)))

def getDictionariesInfo(commands):
    dictionariesInfo = []
    for dictionary, com in commands.items():
        dictInfo = DictionaryInfo(dictionary, com, joinPath(const.path.assets, dictionary))
        imageFiles = getImagesFromDict(dictionary)
        for file in imageFiles:
            splitedFile = file.split('.')
            name, format = '.'.join(splitedFile[:-1]), splitedFile[-1]
            if format not in const.files.allowedFormats: continue
            gestureImage = GestureImage(name, format, joinPath(const.path.assets, dictionary, file))
            dictInfo.images.append(gestureImage)
        dictionariesInfo.append(dictInfo)
    return dictionariesInfo

def main():
    folderNames = getFolderNames()
    commands = getCommandsForFolders(folderNames)
    dictionariesInfo = getDictionariesInfo(commands)
    for dictionary in dictionariesInfo:
        match commands[dictionary.name]:
            case 'a': dbDictionaries.addNewDictionary(dictionary.name)
            case 'r': dbDictionaries.replaceDictionary(dictionary.name)
        dictionaryPath = dbDictionaries.getDictionaryPath(dictionary.name)
        dbGesture = dbGestureWorker(dictionaryPath)
        for image in dictionary.images:
            img = cv2.imread(image.path)
            hands = detHands.findHands(img)
            gesture = Gesture(image.name, hands)
            match commands[dictionary.name]:
                case 'a': dbGesture.addNewGesture(gesture)
                case 'r': dbGesture.replaceGesture(gesture)

if __name__ == '__main__':
    main()
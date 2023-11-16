from ModuleCorrectPath import getCorrectPathByPyScript
import json
import os

MAIN_PATH = getCorrectPathByPyScript(__file__)

class dbWorker:
	def __init__(self, databaseFilePath):
		self.databaseFilePath = databaseFilePath
		filePathArr = self.databaseFilePath.split('/')
		fileName = filePathArr[-1]
		if len(filePathArr) > 1: databaseFoldersPath = '/'.join(filePathArr[:-1])
		else: databaseFoldersPath = ''
		files = os.listdir(databaseFoldersPath)
		if fileName not in files:
			print('[NOT FOUND DATABASE]')
			dbData = self.getDefaultdbData()
			self.save(dbData)

	def get(self):
		with open(self.databaseFilePath) as file:
			dbData = json.load(file)
		return dbData

	def save(self, dbData):
		with open(self.databaseFilePath, 'w') as file:
			json.dump(dbData, file, indent=4, ensure_ascii=False)

	def getStaticGesturesNames(self):
		dbData = self.get()
		staticGestures = [gesture for gesture in dbData['static']['gestures'].keys()]
		return staticGestures

	def addStaticGesture(self, name, hands, useFace=False, linkedPointsWithFace=None):
		dbData = self.get()
		dbData['static']['gestures'][name] = dict(hands=hands,
									   useFace=useFace,
									   linkedPointsWithFace=linkedPointsWithFace)
		self.save(dbData)

	def getStaticGesture(self, name):
		dbData = self.get()
		hands = dbData['static']['gestures'][name]
		return hands

	def addNameStaticGestureToTwoHandsList(self, gestureName):
		dbData = self.get()
		dbData['static']['info']['twoHands'].append(gestureName)
		self.save(dbData)

	def addNameStaticGestureToOneHandsList(self, gestureName):
		dbData = self.get()
		dbData['static']['info']['oneHand'].append(gestureName)
		self.save(dbData)

	def getStaticInfo(self):
		dbData = self.get()
		staticInfo = dbData['static']['info']
		return staticInfo

	def getDefaultdbData(self):
		return {
				"static": {
					"info": {
						"twoHands": [],
						"oneHand": []
					},
					"gestures": {}
				},
				"dynamic": {}
			}

def main():
	db = dbWorker(f'{MAIN_PATH}/database.json')
	print(db.get())

if __name__ == '__main__':
	main()


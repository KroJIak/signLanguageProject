#ModuleHandWorking -> globalHandWorker
def filteringlmListByAverageValue(self, realHands, confidence, filterPower=0, handsOldArr=[]):
    if len(handsOldArr) <= filterPower: return realHands

    resultHands = {}
    countHands = dict(Right=0, Left=0)
    for hands in handsOldArr:
        for typeHand in hands:
            if hands[typeHand]['score'] < confidence: continue
            countHands[typeHand] = countHands[typeHand] + 1
            if typeHand not in resultHands:
                resultHands[typeHand] = {
                    'lmList': hands[typeHand]['lmList'],
                    'score': hands[typeHand]['score']
                }
            else:
                lmListHand = hands[typeHand]['lmList']
                for posId in range(len(lmListHand)):
                    curX = resultHands[typeHand]['lmList'][posId]['x']
                    curY = resultHands[typeHand]['lmList'][posId]['y']
                    curZ = resultHands[typeHand]['lmList'][posId]['z']
                    resultHands[typeHand]['lmList'][posId]['x'] = curX + lmListHand[posId]['x']
                    resultHands[typeHand]['lmList'][posId]['y'] = curY + lmListHand[posId]['y']
                    resultHands[typeHand]['lmList'][posId]['z'] = curZ + lmListHand[posId]['z']
                scoreHand = hands[typeHand]['score']
                curScoreHand = resultHands[typeHand]['score']
                resultHands[typeHand]['score'] = curScoreHand + scoreHand

    popHand = dict(Right=False, Left=False)
    for typeHand in resultHands:
        countCurTypeHand = countHands[typeHand]
        lmListResultHand = resultHands[typeHand]['lmList']
        if filterPower - countCurTypeHand > min(3, filterPower):
            popHand[typeHand] = True
            continue
        for posId in range(len(lmListResultHand)):
            curX = lmListResultHand[posId]['x']
            curY = lmListResultHand[posId]['y']
            curZ = lmListResultHand[posId]['z']
            resultHands[typeHand]['lmList'][posId]['x'] = curX // countCurTypeHand
            resultHands[typeHand]['lmList'][posId]['y'] = curY // countCurTypeHand
            resultHands[typeHand]['lmList'][posId]['z'] = curZ // countCurTypeHand
        scoreResultHand = resultHands[typeHand]['score']
        resultHands[typeHand]['score'] = scoreResultHand / countCurTypeHand
    for typeHand in popHand:
        if popHand[typeHand]:
            resultHands.pop(typeHand)
    return resultHands

#ModuleHandWorking -> globalHandWorker
def getOnlyMainHands(self, hands):
    if hands is None: return None
    newHands = {}
    for hand in hands:
        newHands[hand['type']] = {
            'lmList': hand['lmList'],
            'score': hand['score']
        }
    return newHands

#ModuleFaceWorking -> globalFaceWorker
def onlyOneFace2LmList(self, face):
    lmList = face['lmList']
    return lmList

#ModuleFaceWorking -> globalFaceWorker
def filteringlmListByAverageValue(self, realFace, filterPower=0, facesOldArr=[]):
    if len(facesOldArr) <= filterPower: return realFace

    resultFace = {}
    countFullFace = 0
    for face in facesOldArr:
        if face:
            countFullFace += 1
            if 'lmList' not in resultFace:
                resultFace = face
            else:
                lmListFace = face['lmList']
                for posId in range(len(lmListFace)):
                    curX = resultFace['lmList'][posId]['x']
                    curY = resultFace['lmList'][posId]['y']
                    curZ = resultFace['lmList'][posId]['z']
                    resultFace['lmList'][posId]['x'] = curX + lmListFace[posId]['x']
                    resultFace['lmList'][posId]['y'] = curY + lmListFace[posId]['y']
                    resultFace['lmList'][posId]['z'] = curZ + lmListFace[posId]['z']

    if resultFace:
        for posId in range(len(resultFace['lmList'])):
            curX = resultFace['lmList'][posId]['x']
            curY = resultFace['lmList'][posId]['y']
            curZ = resultFace['lmList'][posId]['z']
            resultFace['lmList'][posId]['x'] = curX // countFullFace
            resultFace['lmList'][posId]['y'] = curY // countFullFace
            resultFace['lmList'][posId]['z'] = curZ // countFullFace

    return resultFace

#ModuleImageWorking
def alphaMergeImage3D(background, foreground, top=0, left=0):
    if foreground is None: return background
    resultImg = background.copy()
    tmp = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    _, fgAlpha = cv2.threshold(tmp, 100, 255, cv2.THRESH_BINARY)
    fgBColor, fgGColor, fgRColor = cv2.split(foreground)
    labelRGB = cv2.merge([fgBColor * fgAlpha, fgGColor * fgAlpha, fgRColor * fgAlpha])
    height, width = foreground.shape[:2]
    bgPart = resultImg[top:top + height, left:left + width, :]
    bgBColor, bgGColor, bgRColor = cv2.split(bgPart)
    bgPart = cv2.merge([bgBColor * (1 - fgAlpha), bgGColor * (1 - fgAlpha), bgRColor * (1 - fgAlpha)])
    cv2.add(labelRGB, bgPart, bgPart)
    resultImg[top:top + height, left:left + width, :] = bgPart
    return resultImg

#ModuleImageWorking
def get4DImageWithText(shape, text, pos, scale, color, thickness, alpha=255):
    resultImg = getZero4DImage(shape)
    cv2.putText(resultImg, text, pos, cv2.FONT_HERSHEY_COMPLEX, scale, color, thickness)
    mask = np.all(resultImg[:, :, :3] == color, axis=-1)
    resultImg[mask, 3] = alpha
    return resultImg

#serverSide
'''
fps = round(1000 / userData['responseTime'] if userData['responseTime'] else 0, 2)
cv2.putText(mainImg, str(fps), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 2)
imgShape = mainImg.shape[:2]
cutImgShape = (userData['windowSize']['height'], userData['windowSize']['width'])
startHeightPos, endHeightPos = max(0, round(imgShape[0] / 2 - cutImgShape[0] / 2)), min(imgShape[0], round(imgShape[0] / 2 + cutImgShape[0] / 2))
startWidthPos, endWidthPos = max(0, round(imgShape[1] / 2 - cutImgShape[1] / 2)), min(imgShape[1], round(imgShape[1] / 2 + cutImgShape[1] / 2))
cutImg = mainImg[startHeightPos:endHeightPos, startWidthPos:endWidthPos, :]
'''

#handWorking

def findWorldHands(self, img, flipType=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    processFinding = multiprocessing.Process(self.getResults(imgRGB))
    while processFinding.is_alive(): pass
    self.height, self.width = img.shape[:2]
    allHands = []
    if self.results.multi_hand_world_landmarks:
        for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_world_landmarks):
            lmList = []
            for lm in handLms.landmark:
                multip = 2000
                px, py, pz = self.width // 2 + lm.x * multip, self.height // 2 + lm.y * multip, self.width // 2 + lm.z * multip
                lmList.append(dict(x=px, y=py, z=pz))

            typeHand = handType.classification[0].label
            scoreHand = handType.classification[0].score
            if flipType: typeHand = flipHand(typeHand)
            allHands.append({
                'lmList': lmList,
                'type': typeHand,
                'score': scoreHand
            })
    return allHands

#handWorkng - drawHandWorker
    def drawLine(self, img, posPoints, prePoint, curPoint, color, thickness):
        resultImg = copy(img)
        pos1 = dict(x=int(posPoints[prePoint]['x']), y=int(posPoints[prePoint]['y']))
        pos2 = dict(x=int(posPoints[curPoint]['x']), y=int(posPoints[curPoint]['y']))
        cv2.line(resultImg, (pos1['x'], pos1['y']), (pos2['x'], pos2['y']), color, thickness)
        return resultImg

    def drawLinesOnImgFromPoints(self, img, lmList, colorLines, thickness):
        resultImg = copy(img)
        for point in range(1, 21):
            resultImg = self.drawLine(resultImg, lmList, PARENT_POINTS[point], point, colorLines[point], thickness)
        return resultImg
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
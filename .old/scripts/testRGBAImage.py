import cv2

def alphaMerge(foreground, background, top=0, left=0):
    if foreground is None: return background
    result = background.copy()

    fgBColor, fgGColor, fgRColor, fgAlpha = cv2.split(foreground)
    fgAlpha //= 255

    labelRGB = cv2.merge([fgBColor * fgAlpha, fgGColor * fgAlpha, fgRColor * fgAlpha])
    height, width = foreground.shape[:2]

    bgPart = result[top:top + height, left:left + width, :]
    bgBColor, bgGColor, bgRColor = cv2.split(bgPart)
    bgPart = cv2.merge([bgBColor * (1 - fgAlpha), bgGColor * (1 - fgAlpha), bgRColor * (1 - fgAlpha)])

    cv2.add(labelRGB, bgPart, bgPart)
    result[top:top + height, left:left + width, :] = bgPart
    return result

'''


def alphaMerge(foreground, background, top=0, left=0):
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

'''
image = cv2.imread('DOYOE.jpg')
label = cv2.imread('ава в кружочке.png', cv2.IMREAD_UNCHANGED)
result = alphaMerge(label, image, 100, 200)
cv2.imshow('Image', result)

while cv2.waitKey(1) != 27: pass
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
import cv2
 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
 
detector = HandDetector(detectionCon=0.65)

# img1 = cv2.imread("/Users/dabbi/Desktop/dlproject/project/Image/1.png", cv2.IMREAD_UNCHANGED)
# ox , oy = 500, 200  # x,y의 시작점

class DragImg():
    def __init__(self, path, posOrigin, imgType):
 
        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path
 
        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)
 
        # self.img = cv2.resize(self.img, (0,0),None,0.4,0.4)
        self.size = self.img.shape[:2]
 
    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size
 
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
 
path = "/Users/dabbi/Desktop/dlproject/project/Image"
myList = os.listdir(path)
print(myList)
 
listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 300, 50], imgType))
 
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img,flipType=False )
 
    if hands:
        lmList = hands[0]['lmList']  #손의 랜드마크 목록
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        # print(length)
        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

    try:
        for imgObject in listImg:
            imgObject.update(cursor)
 
        for imgObject in listImg:
 
            # JPG 
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # PNG 
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass

    #jpeg 해당
    # h, w, _ = img1.shape
    # img[oy:oy + h, ox:ox + w] = img1  #원점에 이미지 크기만큼 더해줘야 좌표값 일치

 
    cv2.imshow("Image", img)
    cv2.waitKey(1)


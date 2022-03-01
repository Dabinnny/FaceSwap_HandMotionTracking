import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import HandTrackingModule as htm
import time
import autopy
 

wCam, hCam = 640, 480
frameR = 100 # 프레임 축소
smoothening = 7
 
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)   #한손만 인식
wScr, hScr = autopy.screen.size()
#print(wScr, hScr)
 
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 검지와 중지의 인덱스의 끝을 클릭으로 감지
    if len(lmList) != 0:  #검지와 중지의 인덱스 tip을 좌표로 인식했다면 
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1, y1, x2, y2)
    
        # 어떤 손가락이 위에 위치했는지? 
        fingers = detector.fingersUp()
        #print(fingers)

        # 프레임을 벗어나면 손인식을 하기 힘들어지므로 특정영역을 지정(=프레임축소)하여 안에서만 작동하게 설정
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # 검지손가락이 위로 올라와있을때만 이동인식
        if fingers[1] == 1 and fingers[2] == 0:
            # 화면 크기를 조정했기때문에 그에 맞는 좌표로 변환 해줘야함
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 커서가 따라오는 속도 조절
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
    
            # 실제 움직이는 방향으로 움직이도록 좌우반전
            autopy.mouse.move(wScr - clocX, clocY) 
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        
        # 검지와 중지 모두 올라와 있는 경우는 두 손가락사이의 길이에 따라 인식되게끔
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            #print(length)

            # 두손가락의 거리가 40이하일때 클릭으로 인식
            if length < 40:
                # 손가락거리를 인식하는 모듈에서 lineInfo 인덱스 좌표를 지정하면 손가락 중앙으로 지정
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
    
    #적절한 프레임 속도를 유지
    # cTime = time.time()
    # fps = 1 / (cTime - pTime) #현재시간-이전시간
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    # (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

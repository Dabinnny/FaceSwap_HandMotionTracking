import cv2
from cvzone.HandTrackingModule import HandDetector
import time
 
class Button:
    def __init__(self, pos, width, height, value): #(생성자, 위치, 너비, 높이, 텍스트)
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
 
    def draw(self, img):
        # 사각형을 생성(화면에 출력, 좌표, 너비와 높이, 색상, 채우기효과) 
        # x,y 좌표값에다가 너비 높이를 지정해줘야 화면의 좌표에 찍힘
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        # 생성한 사각형에 테두리 그리기
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        # 사각형안에 글자 넣기 (화면, 텍스트, 좌표, 글꼴, 크기, 색상, 두께)
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
 
    def checkClick(self, x, y):   # 검지의 x,y의 값 기준
        # 초기값과 초기값+너비 안에 검지가 위치한다면
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            # 계산기에 검지가 위치한다면 사각형의 색깔을 변환해서 클릭이 되었는지 표시
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), 
                        cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            return True
        else:
            return False
 
 
# 버튼 생성 및 입력리스트
buttonValues = [['7', '8', '9', '*'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['0', '/', '.', '=']]

buttonList = []
for x in range(4):  # 4*4 계산기
    for y in range(4):
        xpos = x * 100 + 800   # x좌표에 100*100 정사각형 크기 지정, 화면 위 위치조정
        ypos = y * 100 + 150
        # [y][x]로 지정해야 수평 그대로 출력 / [x][y]는 수직으로 flip되어 출력
        buttonList.append(Button((xpos, ypos), 100, 100, buttonValues[y][x]))
 
# 수학 계산수행 변수지정
myEquation = ''
delayCounter = 0

cap = cv2.VideoCapture(0)
cap.set(3,1280) #너비
cap.set(2,720)  #높이

#손 탐지시 신뢰도 설정, 80% 확신해야 손으로 인식 / 여러개의 손 말고 하나만 인식
detector = HandDetector(detectionCon=0.8, maxHands=1) 
 
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)  # 카메라이기 때문에 좌우반전, 수직으로 뒤집을땐 0
    hands, img = detector.findHands(img)

    cv2.rectangle(img, (800,50), (800+400, 70+100), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800,50), (800+400, 70+100), (50, 50, 50), 3)
 
    # 카메라가 켜지면 화면에 버튼리스트만큼 버튼 생성
    for button in buttonList:
        button.draw(img)
 
    # 손이 클릭을 했는지 확인
    if hands:  # hands == True :
        lmList = hands[0]['lmList']  # 손을 인식한 포인트 좌표에서 랜드마크 목록을 가져오기 위함
        len, _ , img = detector.findDistance(lmList[8], lmList[12], img) # 8 = 검지, 12 = 중지 인덱스
        #print(len)
        x, y = lmList[8]  # 손가락 포인트는 검지기준으로 인식
 
        # 검지와 중지를 딱 붙였을때 거리가 대략 40이므로 50이하로 지정, 손가락을 벌리면 클릭인식x
        if len < 50 :
            # 16개 버튼의 클릭여부를 확인하려면 이 시점의 버튼클릭이 true여야 함
            # 해당 버튼의 번호를 행번호, 열번호로 계산식에 입력
            # 리스트형태이기 때문에 1차원으로 버튼 변환
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    # y값을 0으로 만들어줘야 버튼하나만 출력/아니면 열전체같이 클릭
                    myValue = buttonValues[int(i % 4)][int(i / 4)]  
                    if myValue == '=':   # '='은 문자 그대로 출력해라
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue # 5다음에 6을 입력하면 56으로 받아라
                    delayCounter = 1
 
    # 계산식 입력 중복 방지 / 카운터가 실행중이면 계산마칠때까지 다음 동작 미실행
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0
 
    # 계산식 값 넣기
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN,
                3, (50, 50, 50), 3)
 
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''
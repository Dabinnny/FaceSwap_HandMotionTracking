# FaceSwap & HandMotionTracking System

OpenCV, Dlib, Mediapipe 활용 얼굴 및 핸드모션 인식시스템 구현

</br> 

## ✔️ FaceSwap

### 진행 내용  

**1. Swapping 하고자 하는 Source 이미지에서 Dlib 기반 Face Landmark 추출 후 Segmentation을 실시합니다.**

<div align="center">
<img src="https://user-images.githubusercontent.com/90162819/160758500-b0fa295f-7e7d-4472-bec3-4907e4640e8a.png" width="500"></div>  

</br> 
</br> 

**2. Source 이미지를 세부 분할하여 Target이미지의 크기와 비율에 맞게 동일한 Landmark Index에 Swapping을 수행합니다.**  

<div align="center">
<img src="https://user-images.githubusercontent.com/90162819/160758534-2b8392b1-53df-4fd3-b934-a687ce132ca9.png" width="700"></div> 

</br> 
</br> 

**3. Target이미지에 색상과 경계가 자연스럽게 연결되도록 seamlessClone을 적용합니다.** 

<div align="center">
<img src="https://user-images.githubusercontent.com/90162819/160758545-dace1f46-008d-4f88-a34b-d47a07d25b74.png" width="200"></div> 

</br> 
</br> 
</br> 

## ✔️ Hand Motion Tracking

### 진행 내용  

**1. 손 Landmark기반 인식시스템 마우스 구현**  
  **- 검지와 중지의 Index를 기반으로 손가락사이의 좌표 거리를 조정하여 마우스 커서를 움직이고 클릭을 수행합니다.**

</br> 

<div align="center">
<img src="https://user-images.githubusercontent.com/90162819/160759270-a02beb52-038f-4918-ab36-5770f2b62ed1.gif" ></div> 

</br> 
</br> 
</br> 

**2. 손 인식 마우스 활용 가상의 계산기 사용** 
**- 도형을 활용해 계산기 객체를 생성하고 계산기능과 인식 마우스를 연결합니다.** 

</br> 

<div align="center">
<img src="https://user-images.githubusercontent.com/90162819/160759308-e506a85c-050b-41c8-8772-e9ee639faee0.gif" ></div> 



 
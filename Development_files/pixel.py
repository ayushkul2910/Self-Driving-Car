import cv2
cap=cv2.VideoCapture(0)

ret,img = cap.read()
x=0
while x<100:

    img[100][x][2]=255
    x=x+1
cv2.imshow('img',img)



cap.release()


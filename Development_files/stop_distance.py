import cv2
import numpy as np

stop_cascade = cv2.CascadeClassifier('stop_sign.xml')


cap = cv2.VideoCapture(0)

width=6.8
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    stop = stop_cascade.detectMultiScale(gray, 1.3, 5)
    for(x,y,w,h) in stop:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0),2)
        dist=((width*668.748634441)/w)
        print(dist)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = img[y:y+h,x:x+w]
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break


cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np

stop_cascade = cv2.CascadeClassifier('stop_sign.xml')


cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.uint8)
    tophat=cv2.morphologyEx(gray,cv2.MORPH_TOPHAT,kernel)
    (thresh, im_bw) = cv2.threshold(tophat, 25, 255, cv2.THRESH_BINARY)
    minLineLength = 2000
    half=300
    maxLineGap = 0
    crp=im_bw[half:483,0:644]
    lines = cv2.HoughLinesP(crp,1,np.pi/180,15,minLineLength,maxLineGap)
    if lines != None:
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(img,(x1,y1+half),(x2,y2+half),(0,0,255),2)
                #cv2.line(crp,(x1,y1),(x2,y2),(0,0,255),2)
        y=350
        for x in range(0,479):
            if img[x][y][2]==255:
                x1=x
                break
        for x in range(479,0):
            if img[x][y][2]==255:
                x2=x
                break
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()

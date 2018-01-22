import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt

cap=cv2.VideoCapture(0)

#img = cv2.imread('road.jpg')






while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur1=cv2.GaussianBlur(gray,(5,5),0)
    blur=cv2.GaussianBlur(blur1,(5,5),0)
    kernel = np.ones((5,5),np.uint8)
    di = cv2.dilate(blur,kernel,iterations = 1)
    (thresh, im_bw) = cv2.threshold(di, 128, 255, cv2.THRESH_BINARY)
    (thresh1, im_bw_blur) = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY)
    img2=di-blur
    img1=im_bw-im_bw_blur
    img1=img1**2.8
##    cv2.imshow('img',di)
##    minLineLength = 30
##    maxLineGap = 10
##    lines = cv2.HoughLinesP(img2,1,np.pi/180,15,minLineLength,maxLineGap)
##    for x in range(0, len(lines)):
##        for x1,y1,x2,y2 in lines[x]:
##            cv2.line(img2,(x1,y1),(x2,y2),(0,255,0),2)
##
##
##    
    #img2=cv2.Canny(img1,100,200)
    #img3=cv2.GaussianBlur(img1,(5,5),0)
    #img4=cv2.GaussianBlur(img2,(5,5),0)
    #for i in range(0, gray.shape[0]):
        #for j in range(0, gray.shape[1]):
                #if gray[i][j]>100 and gray[i][j]<175:
                    #gray[i][j]=0
    
    #cv2.namedWindow('img1',cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('img1',1370,700)
    cv2.imshow('img1',img1)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break





cap.release()
cv2.destroyAllWindows()

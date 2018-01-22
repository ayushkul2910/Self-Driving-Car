import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt

cap=cv2.VideoCapture(0)

#img = cv2.imread('road.jpg')






while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blur=cv2.GaussianBlur(gray,(5,5),0)
    #kernel = np.ones((5,5),np.uint8)
    #di = cv2.dilate(blur,kernel,iterations = 1)
    #(thresh, im_bw) = cv2.threshold(di, 128, 255, cv2.THRESH_BINARY)
    #(thresh1, im_bw_blur) = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY)
    #img1=im_bw-im_bw_blur


    edges = cv2.Canny(gray,100,200,apertureSize = 3)
    cv2.imshow('edges',edges)
    
    minLineLength=img.shape[1]-300
    lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, threshold=10,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)

    
    for i in range(2):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)


    #cv2.waitKey(0)

    
    #img2=cv2.Canny(img1,100,200)
    #img3=cv2.GaussianBlur(img1,(5,5),0)
    #img4=cv2.GaussianBlur(img2,(5,5),0)
    #for i in range(0, gray.shape[0]):
        #for j in range(0, gray.shape[1]):
                #if gray[i][j]>100 and gray[i][j]<175:
                    #gray[i][j]=0
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break





cap.release()
cv2.destroyAllWindows()

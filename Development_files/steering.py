import cv2
import numpy as np
import time



cap=cv2.VideoCapture(0)



while True:
    ret,img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur2=cv2.GaussianBlur(gray,(5,5),0)
    kernel = np.ones((5,5),np.uint8)
    tophat=cv2.morphologyEx(blur2,cv2.MORPH_TOPHAT,kernel)
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
                cv2.line(gray,(x1,y1+half),(x2,y2+half),(0,0,255),2)
                #cv2.line(crp,(x1,y1),(x2,y2),(0,0,255),2)
    x1=x2=0    
    for x in range(0,639):
        if img[350][x][2]==255:
            x1=x
            break
    for x in range(0,639):
        if img[350][x][2]==255:
            x2=x
    #distance=x2-x1
    avg=(x2+x1)/2
    if avg!=0:
        print(x1,x2)
        print(avg)
        if avg<250:
            print("turn left")
            time.sleep(0.01)
        if avg in range (250,394):
            print("In range!")
            time.sleep(0.01)
        if avg>394:
            print("turn right")
            time.sleep(0.01)
    #print(distance)
    cv2.line(img,(0,350),(644,350),(255,0,0),2)
    cv2.line(img,(322,360),(322,340),(0,255,0),2)
    cv2.line(img,(int(round(avg)),350),(int(round(avg)),350),(0,255,0),5)
    cv2.line(img,(250,355),(250,345),(0,255,0),2)
    cv2.line(img,(394,355),(394,345),(0,255,0),2)        
    cv2.imshow('img',img)

##    crp=img[242:483,0:322]
##    crp1=img[242:483,322:644]
##    flp=cv2.flip(crp,1)
##    if flp==crp1:
##        print("Hi")
##    #cv2.imshow('img1',gray1)
##    cv2.imshow('crp1',crp1)
##    #cv2.imshow('crp',crp)
##    cv2.imshow('flip',flp)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break


cap.release()
cv2.destroyAllWindows()

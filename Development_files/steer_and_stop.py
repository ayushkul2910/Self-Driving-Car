import cv2
import numpy as np
import urllib.request
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
stop_cascade = cv2.CascadeClassifier('stop_sign.xml')

width=6.8
centre_pin=9
left_pin=22
right_pin=24


while True:
    GPIO.setup([centre_pin,left_pin,right_pin],GPIO.OUT)
    GPIO.output(centre_pin,GPIO.HIGH)
    URL='http://192.168.43.1:8080/shot.jpg'
    request=urllib.request.urlopen(URL)
    array=np.array(bytearray(request.read()),dtype=np.uint8)
    img=cv2.imdecode(array,-1)
    img1=cv2.imdecode(array,-1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    stop = stop_cascade.detectMultiScale(gray1, 1.3, 5)
    for(x,y,w,h) in stop:
        cv2.rectangle(img1, (x,y), (x+w,y+h), (255,0,0),2)
        dist=((width*668.748634441)/w)
        print("Distance from stop:",dist)
        if dist<10:
            GPIO.output(centre_pin,GPIO.LOW)
            GPIO.output(left_pin,GPIO.LOW)
            GPIO.output(right_pin,GPIO.LOW)
        roi_gray = gray1[y:y+h,x:x+w]
        roi_color = img1[y:y+h,x:x+w]
    cv2.imshow('img_stop',img1)
    #blur2=cv2.GaussianBlur(gray,(5,5),0)
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
            GPIO.output(left_pin,GPIO.HIGH)
            GPIO.output(right_pin,GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(left_pin,GPIO.LOW)
        if avg in range (250,394):
            print("In range!")
            GPIO.output(9,GPIO.HIGH)
            time.sleep(0.01)
        if avg>394:
            print("turn right")
            GPIO.output(right_pin,GPIO.HIGH)
            GPIO.output(left_pin,GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(right_pin,GPIO.LOW)
    GPIO.cleanup(9)
    #print(distance)
    cv2.line(img,(0,350),(644,350),(255,0,0),2)
    cv2.line(img,(322,360),(322,340),(0,255,0),2)
    cv2.line(img,(int(round(avg)),350),(int(round(avg)),350),(0,255,0),5)
    cv2.line(img,(250,355),(250,345),(0,255,0),2)
    cv2.line(img,(394,355),(394,345),(0,255,0),2)        
    cv2.imshow('img',img)


    k = cv2.waitKey(30) & 0xff
    if k==27:
        break


cap.release()
cv2.destroyAllWindows()

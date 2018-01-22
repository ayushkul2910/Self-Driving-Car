import RPi.GPIO as GPIO
import time
import signal
import sys
import cv2
import numpy as np
import urllib.request
stop_cascade = cv2.CascadeClassifier('stop_sign.xml')
GPIO.setmode(GPIO.BOARD)
pinTrigger = 12
pinEcho = 16
m11=18
m12=22

centre_pin=9
left_pin=38
right_pin=40



width=6.1
GPIO.setup(7,GPIO.OUT)
	
def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup() 
	sys.exit(0)

signal.signal(signal.SIGINT, close)
def forward():
        GPIO.output(m11,True)
        GPIO.output(m12,False)
        time.sleep(0.01)
def reverse():
        GPIO.output(m11,False)
        GPIO.output(m12,True)
        time.sleep(0.01)
def stop_():
        GPIO.output(m11,False)
        GPIO.output(m12,False)
        time.sleep(0.01)
# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
kernel = np.ones((5,5),np.uint8)
while True:
    GPIO.setup([centre_pin,left_pin,right_pin],GPIO.OUT)
    URL='http://192.168.43.1:8080/shot.jpg'
    request=urllib.request.urlopen(URL)
    array=np.array(bytearray(request.read()),dtype=np.uint8)
    img=cv2.imdecode(array,-1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
            forward()
            time.sleep(0.01)
        if avg>394:
            print("turn right")
            GPIO.output(right_pin,GPIO.HIGH)
            GPIO.output(left_pin,GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(right_pin,GPIO.LOW)

    cv2.line(img,(0,350),(644,350),(255,0,0),2)
    cv2.line(img,(322,360),(322,340),(0,255,0),2)
    cv2.line(img,(int(round(avg)),350),(int(round(avg)),350),(0,255,0),5)
    cv2.line(img,(250,355),(250,345),(0,255,0),2)
    cv2.line(img,(394,355),(394,345),(0,255,0),2)
    
    stop = stop_cascade.detectMultiScale(gray, 1.3, 5)
    if stop==():
	    a= 32000
    for(x,y,w,h) in stop:
	    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0),2)
	    dist=((width*668.748634441)/w)
	    a= dist
	    roi_gray = gray[y:y+h,x:x+w]
	    roi_color = img[y:y+h,x:x+w]
        
    



    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    # set Trigger to HIGH
    GPIO.output(pinTrigger, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)

    startTime = time.time()
    stopTime = time.time()

    # save start time
    while 0 == GPIO.input(pinEcho):
	    startTime = time.time()

    # save time of arrival
    while 1 == GPIO.input(pinEcho):
    	stopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    print ("Distance: %.1f cm" % distance)
    time.sleep(0.1)
    print (a)
    if (a<=100):
    	reverse()
    	print ('Stop detected')
    	time.sleep(0.01)
    	stop_()
    if (a==32000):
    	forward()
    if (distance<=10):
    	#reverse()
    	print ('Reverse')
    	stop_()
    else:
    	#forward()
    	print ('Forward')

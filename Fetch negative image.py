import cv2
import os
import urllib.request
def FetchImages():
    if not os.path.exists('J:/IoT Project - A Self-driving-Car/Negative'):
        os.mkdir('Negative')
    Negative_Image_URLs='http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n02960352'
    Negative_Image=urllib.request.urlopen(Negative_Image_URLs).read().decode()
    Negative_Image=Negative_Image.split("\n")
    a= 4000
    
        
    for i in Negative_Image:
        try:
            print (i)
            if a in range(1,389):
                pass
##                print ('a')
##                a+=1
            else:
                urllib.request.urlretrieve(i, 'J:/IoT Project - A Self-driving-Car/Negative/'+str(a)+'.jpg')
                a+=1
        except Exception as e:
            print (str(e))
FetchImages()

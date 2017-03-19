import cv2
import os
import numpy as np

def resize():
    a=1
    path="Negative/"
    for a in range(4000,4500):
        print(a)
        try:
            img=cv2.imread(path+str(a)+'.jpg',cv2.IMREAD_GRAYSCALE)
            resized=cv2.resize(img,(100,100))
            cv2.imwrite(path+str(a)+'.jpg',resized)
            a+=1
        except Exception as e:
            print (str(e))
            a+=1
#resize()
def find_uglies():
    for file_type in ['Negative']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path=str(file_type)+'/'+str(img)
                    ugly=cv2.imread('uglies/'+str(ugly))
                    question=cv2.imread(current_image_path)
                    if ugly.shape==question.shape and not (np.bitwise_xor(ugly,question).any()):
                        os.remove(current_image_path)
                        print ('Ohyeahh')
                except Exception as e:
                    print (str(e))

find_uglies()

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import cv2
from processing_py import *

def core(img,temp) :
    plain = np.full((img.shape[0] , img.shape[1] , 3) , 0 ,dtype=np.uint8)

    for i in range((len(temp)//2),len(img)-(len(temp)//2)) :
        for j in range((len(temp)//2),len(img[0])-(len(temp)//2)) :
            resr = 0
            resg = 0
            resb = 0

            for a in range(-(len(temp)//2),(len(temp)//2)+1) :
                for b in range(-(len(temp)//2),(len(temp)//2)+1) :
                    resr += temp[a+(len(temp)//2)][b+(len(temp)//2)] * img[i+a][j+b][0]
                    resg += temp[a+(len(temp)//2)][b+(len(temp)//2)] * img[i+a][j+b][1]
                    resb += temp[a+(len(temp)//2)][b+(len(temp)//2)] * img[i+a][j+b][2]
                plain[i][j][0] = min(int(resr) , 255)
                plain[i][j][1] = min(int(resg) , 255)
                plain[i][j][2] = min(int(resb) , 255)
    return plain

filter  = fil = np.full((3,3),1) /9


img = cv2.imread("images/city.jpg")
img = np.array(img)

plain = np.full((img.shape[0] , img.shape[1] , 3) , 0 ,dtype=np.uint8)

#cv2.imshow('123' , core(img,filter))
#cv2.waitKey(0)


app = App(800,800)
Image(img,0,0)

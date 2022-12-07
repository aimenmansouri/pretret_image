import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math

fil = np.full((3,3),1) / 9

def core(img,temp) :
    plain = np.full((img.shape[0] , img.shape[1] , 3) , 0 ,dtype=np.uint8)
    for x in range(3) :
        for i in range((len(temp)//2),len(img)-(len(temp)//2)) :
            for j in range((len(temp)//2),len(img[0])-(len(temp)//2)) :
                res = 0
                for a in range(-(len(temp)//2),(len(temp)//2)+1) :
                    for b in range(-(len(temp)//2),(len(temp)//2)+1) :
                        res += temp[a+(len(temp)//2)][b+(len(temp)//2)] * img[i+a][j+b][x]
                plain[i][j][x] = min(int(res) , 255)
    return plain

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import pyplot as plt
import math

#OPEN IMAGE
img = Image.open("images/river.jpg")

#SHOW IMAGE
#plt.imshow(img)
#plt.show()

#IMAGE TO NP ARRAY
img_array = np.array(img)

#PIXEL TO GREY
def to_grey(pixel) :
    col = pixel[0]*0.299 + pixel[1]*0.587 + pixel[2]*0.114
    return [col,col,col] 

def histogram(img_array) :
    histo = np.zeros(256).astype(int)
    for i in range(len(img_array)) :
        for j in range(len(img_array[0])) :
            histo[(img_array[i][j][1])] += 1

    return histo

def histoNorm(histo ,h,w) :
    return [i/(h*w) for i in histo]

def histoCum(histo) :
    return [sum(histo[:i+1]) for i in range(len(histo))]

def histoCumNorm(histoCum,h,w) :
    return [i/(h*w) for i in histoCum]

#PLOT HISTOGRAM
x = ([i for i in range(256)])
plt.plot(x, histoCum(histogram(img_array)))


def core(img,temp) :
    plain = np.full((len(img), len(img[0])), 0)
    for i in range(1,len(img)-1) :
        for j in range(1,len(img[0])-1) :
            res = 0
            for a in range(-1,2) :
                for b in range(-1 ,2) :
                    res += temp[a+1][b+1] * img[i+a][j+b]
            plain[i][j] = int(res)
    return plain

def mdn(arr) :
    return sorted(arr)[math.ceil((len(arr)/2))-1]

def minx(arr) :
    a = arr[len(arr) // 2]
    del(arr[len(arr) // 2])
    if a <= min(arr) or a >= max(arr) :
        return min(arr)
    return a

def maxx(arr) :
    a = arr[len(arr) // 2]
    del(arr[len(arr) // 2])
    if a <= min(arr) or a >= max(arr) :
        return max(arr)
    return a

def gaus(i,sigma) :
    plain = np.zeros((i,i))
    res = 0
    for a in range(i) :
        for j in range(i) :
            b = 1/(sigma*math.sqrt(2*math.pi))
            x = -(((a-(i//2))**2 + (j-(i//2))**2) / (2*(sigma**2)))
            c = math.exp(x)
            plain[a][j] = b*c
            res += plain[a][j]
            
    for g in range(i) :
        for h in range(i) :
            plain[g][h] = plain[g][h]/res 
    return plain

def minmaxmedian(img):
    plain = np.full((len(img), len(img[0])), 0)
    for i in range(1,len(img)-1) :
        for j in range(1,len(img[0])-1) :
            res = []
            for a in range(-1,2) :
                for b in range(-1 ,2) :
                    res.append(img[i+a][j+b])
            plain[i][j] = minx(res)
    return plain

#FILTER IMAGE REAL
def filterRgb(img,temp) :
    plain = np.full((img.shape[0] , img.shape[1] , 3) , 0 ,dtype=np.uint8)
    for x in range(3) :
        for i in range((len(temp[x])//2),len(img)-(len(temp[x])//2)) :
            for j in range((len(temp[x])//2),len(img[0])-(len(temp[x])//2)) :
                res = 0
                for a in range(-(len(temp[x])//2),(len(temp[x])//2)+1) :
                    for b in range(-(len(temp[x])//2),(len(temp[x])//2)+1) :
                        res += temp[x][a+(len(temp[x])//2)][b+(len(temp[x])//2)] * img[i+a][j+b][x]
                plain[i][j][x] = min(int(res) , 255)
    return plain


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

#HISTOGRAM IMAGE REAL
def histo(img_array) :
    r = np.zeros(256).astype(int)
    g = np.zeros(256).astype(int)
    b = np.zeros(256).astype(int)
    for i in range(len(img_array)) :
        for j in range(len(img_array[0])) :
            r[(img_array[i][j][0])] += 1
            g[(img_array[i][j][1])] += 1
            b[(img_array[i][j][2])] += 1
            
    return [r,g,b]

plt.plot([i for i in range(256)], histo(img_array)[0])
plt.show()

def contrast(n,maxx,minn):
    return np.clip(int((n-minn)*(255/(maxx-minn))) , 0,255)


def minmax(arr) :
    min = 0
    max = 255
    
    for i in range(len(arr)) :
        if arr[i] != 0:
            min  = i
    for i in range(len(arr)-1,-1,-1) :
        if arr[i] != 0:
            max  = i
    return [min,max]
            
#CREATE TABLE
def contrastDecs(img) :
    histos = histo(img)
    mm = []
    for i in range(3):
        mm.append([0,0])
        mm[i] = minmax(histos[i])
    decs = [{},{},{}]
    for i in range(256) :

        decs[0][str(i)] = contrast(i, mm[0][0], mm[0][1])
        decs[1][str(i)] = contrast(i, mm[1][0], mm[1][1])
        decs[2][str(i)] = contrast(i, mm[2][0], mm[2][1])
    return decs

#METHODE TABLE
def applyDecRGB(img ,decs) :
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            img[i][j][0] = decs[0][str(img[i][j][0])]
            img[i][j][1] = decs[1][str(img[i][j][1])]
            img[i][j][2] = decs[2][str(img[i][j][2])]
    return img


plt.imshow(filterRgb(img, filter))
plt.show()
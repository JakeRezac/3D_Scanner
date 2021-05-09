from PIL import Image
import glob
from array import *
import math 
from mpl_toolkits import mplot3d
import numpy as np
#import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

imgArr = []
silhouette = []
foreground = []
intersect = []
zList=[]
col=800
row=600

cmToPixel=37.7952755906
camD=10*cmToPixel
silToSilD=20*cmToPixel
totAngleY=2*math.atan(col/(2*camD))
totAngleZ=2*math.atan(row/(2*camD))
numAngle=40
picCount=0;
thetaY=totAngleY/numAngle
thetaZ=totAngleZ/numAngle
imgIndex=0

adjustedX=0
adjustedY=0

class vhull:
    coord = []
    projections = []
    def __init__(self, coord):
        self.coord = coord    # instance variable unique to each instance  
        
for filename in glob.glob('C:/Users/derek/Desktop/pics/*.png'):
    baseImage = Image.open(filename)
    mask = baseImage.point(lambda i: i > 230 and 255)
    newImage = mask.convert("1")
    newImage.show() 
    imgArr.append(newImage)
    picCount += 1
    
   # panda1 = pd.DataFrame(np.array(newImage.getdata()))
    #print(panda1.head(20))
    #for p in panda1.iterrows():
    #    print(p)

#shift=2*math.pi/picCount
shift=math.pi/4
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111, projection='3d')

for img in imgArr:
    foreground = []
    rgb = img.convert("RGB")                
    for z in np.arange(-totAngleZ/2,totAngleZ/2+thetaZ/2,thetaZ):
        for y in np.arange(-totAngleY/2,totAngleY/2+thetaY/2,thetaY):
            yLoc=(col/2+round(camD*math.tan(y)))
            zLoc=(row/2+round(camD*math.tan(z)))
            
            a=rgb.getpixel((yLoc-1,zLoc-1))
            if(a==(0, 0, 0)):
                hull=vhull([round(camD*math.tan(y)),round(camD*math.tan(z))])
                
                yLocSpace=camD*math.tan(y)
                zLocSpace=-camD*math.tan(z)
                
                for x in np.arange(10):
                    #a=x-camD-silToSilD/2
                    a=x-5
                    b=x*yLocSpace
                    c=x*zLocSpace
                    if(imgIndex==0):
                        adjustedX=a*math.cos(shift*imgIndex)-b*math.sin(shift*imgIndex)
                        adjustedY=b*math.cos(shift*imgIndex)+a*math.sin(shift*imgIndex)
                        hull.projections.append([adjustedX,adjustedY,c])
                        ax.scatter(adjustedX,adjustedY,c)
                foreground.append(hull)
    silhouette.append(foreground)
    print("newimg")
    imgIndex+=1
print("--------------------------------------------------------")
print(len(silhouette))  
for x in range(len(silhouette)):
   print(len(silhouette[x]))  
#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')
#plt.show()

for x in range(x,len(silhouette)):
    for y in range(len(silhouette[x])
    


#print(silhouette[0][1].hullList)#image num, index of foreground pixel, the coordinate of it on image
#print(silhouette[0][1])#object location
#print(silhouette[0][0].projections)
#print(silhouette[0][0].hullList)
#print(silhouette[0][1].coord[1])
#print(silhouette[0][1].printl())
#print(silhouette[0][300][273].coord)
#print(silhouette[0][300][274].coord)
#print(hullGen(silhouette[0]))
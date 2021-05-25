from PIL import Image
import glob
from array import *
import math 
from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
#print(dir_path)
imgArr = []
silhouette = []
foreground = []
intersect = []
zList=[]
combinedprojections = []
combinedprojectionsList = []
col=133
row=125

cmToPixel=37.7952755906
camD=10*cmToPixel
silToSilD=20*cmToPixel
totAngleY=2*math.atan(col/(2*camD))
totAngleZ=2*math.atan(row/(2*camD))
numAngle=30
projD=6
threshold=.001
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
#C:\Users\DerekS\Desktop\3D_Scanner\pics
#'C:/Users/derekS/Desktop/pics/*.png'   
dir_path=dir_path.replace("\\","/")     
imgPath=dir_path+'/*.png'
print(imgPath)
for filename in glob.glob(imgPath):
    baseImage = Image.open(filename)
    mask = baseImage.point(lambda i: i > 230 and 255)
    newImage = mask.convert("1")
    #newImage.show() 
    imgArr.append(newImage)
    picCount += 1
    
    #panda1 = pd.DataFrame(np.array(newImage.getdata()))
    #print(panda1.head(20))
    #for p in panda1.iterrows():
    #    print(p)

shift=2*math.pi/picCount
#shift=math.pi/4
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
                
                for x in np.arange(projD):
                    #a=x-camD-silToSilD/2
                    a=x-projD/2
                    b=x*yLocSpace
                    c=x*zLocSpace
                    #if(imgIndex==0):
                    
                    adjustedX=a*math.cos(shift*imgIndex)-b*math.sin(shift*imgIndex)
                    adjustedY=b*math.cos(shift*imgIndex)+a*math.sin(shift*imgIndex)
                    #print(a," ",b," ",c)
                    #print(adjustedX,",",adjustedY,",",c)
                    print("-------------------------")
                    #listproj=[str(adjustedX),str(adjustedY),str(c)]
                    #proj = ",".join(listproj)
                    hull.projections.append([adjustedX,adjustedY,c])
                    # if(imgIndex==0):
                        # ax.scatter(adjustedX,adjustedY,c,color='red')
                    # else:
                        # ax.scatter(adjustedX,adjustedY,c,color='blue')
                foreground.append(hull)
    silhouette.append(foreground)
    print("newimg")
    imgIndex+=1
print("--------------------------------------------------------")
# for a in range(len(silhouette)):
    # print("left sil ",a)
    # for a2 in range(a+1,len(silhouette)):
        # print("right sil ",a2)
        # for b in range(len(silhouette[a])):
            # #print("left sil fore",b)
            # for b2 in range(len(silhouette[a2])):
                # #print("right sil fore",b2)
                # for loc in range(len(silhouette[a][b].projections)):
                    # #print("left sil fore loc",loc)
                    # for loc2 in range(len(silhouette[a2][b2].projections)):
                        # #print("right sil fore loc",loc2)
                        # coord=silhouette[a][b].projections[loc].split(",")
                        # x1=float(coord[0])
                        # y1=float(coord[1])
                        # z1=float(coord[2])
                        # coord2=silhouette[a2][b2].projections[loc2].split(",")
                        # x2=float(coord2[0])
                        # y2=float(coord2[1])
                        # z2=float(coord2[2])
                        # print(x2,",",y2,",",z2)
                        # #if(loc==0 and loc2==0):
                            # #print("sil ",a,"-",b,":",x1,",",y1,",",z1," with sil ",a2,"-",b2,":",x2,",",y2,",",z2)
                        # print(a2,"-",b2,":",x2,",",y2,",",z2)
                        # if(math.sqrt(pow(x2-x1,2)+pow(y2-y1,2)+pow(z2-z1,2))<.01):
                            # #print(x1,",",y1,",",z1," with ",x2,",",y2,",",z2)
                            # intersect.append([x2,y2,z2])
                            # ax.scatter(x2,y2,z2,color='green')
                            
#for a in range(len(silhouette)):
    #for b in range(len(silhouette[a])):
        #print(len(silhouette[a]))
        
#for a in range(0,combinedprojections):
combinedprojections.extend(silhouette[0][0].projections)    
print("--------------------------------------------------------")
# print(len(silhouette))
# for x in range(len(silhouette)):
    # print("-------------------------")
    # print(len(silhouette[x]))
    # print("-------------------------")    
    # for y in range(len(silhouette[x])):
        # print(len(silhouette[x][y].projections)) 
 
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# ax.scatter(2.0,-2.4492935982947064e-16,0.0,color='green')
# ax.scatter(1.0,-1.2246467991473532e-16,31.039235711498588,color='green')
# ax.scatter(-0.0,0.0,62.078471422997175,color='green')
# ax.scatter(-1.0,1.2246467991473532e-16,93.11770713449576,color='green')
# ax.scatter(2.0,-2.4492935982947064e-16,-0.0,color='green')
# ax.scatter(0.999999999999996,-32.996572190998265,-0.0,color='green')
# ax.scatter(-8.081829303308119e-15,-65.99314438199653,-0.0,color='green')
# ax.scatter(-1.0000000000000122,-98.9897165729948,-0.0,color='green')
# ax.scatter(2.0,-2.4492935982947064e-16,-0.0,color='green')
# ax.scatter(1.000000000000004,32.996572190998265,-31.03923571149859,color='green')
# ax.scatter(8.081829303308119e-15,65.99314438199653,-62.07847142299718,color='green')
# ax.scatter(-0.9999999999999879,98.9897165729948,-93.11770713449577,color='green')
# ax.scatter(2.0,-2.4492935982947064e-16,-0.0,color='green')
# ax.scatter(0.999999999999996,-32.996572190998265,-31.03923571149859,color='green')
# ax.scatter(-8.081829303308119e-15,-65.99314438199653,-62.07847142299718,color='green')
# ax.scatter(-1.0000000000000122,-98.9897165729948,-93.11770713449577,color='green')
#print(combinedprojections)
#print(len(combinedprojections))

interval=int(len(combinedprojections)/len(silhouette))
print(interval)
for a in range(len(silhouette)):
    for x in range(a*interval,a*interval+interval):
        for y in range(a*interval+interval,len(combinedprojections)):
            x1=combinedprojections[x][0]
            y1=combinedprojections[x][1]
            z1=combinedprojections[x][2]
            x2=combinedprojections[y][0]
            y2=combinedprojections[y][1]
            z2=combinedprojections[y][2]
            if(math.sqrt(pow(x2-x1,2)+pow(y2-y1,2)+pow(z2-z1,2))<threshold):
                #print(x1,",",y1,",",z1," with ",x2,",",y2,",",z2)
                intersect.append([x2,y2,z2])
                ax.scatter(x2,y2,z2,color='green')
# print(combinedprojections[1][0])
# print(combinedprojections[1][1])
# print(combinedprojections[1][2])
print(intersect)
ax.set_xlim3d(-2, 2)
ax.set_ylim3d(-150, 150)
ax.set_zlim3d(-150, 150)
plt.show()


#print(silhouette[0][1].hullList)#image num, index of foreground pixel, the coordinate of it on image
#print(silhouette[0][1])#object location

#print(silhouette[0][0].hullList)
#print(silhouette[0][1].coord[1])
#print(silhouette[0][1].printl())
#print(silhouette[0][300][273].coord)
#print(silhouette[0][300][274].coord)
#print(hullGen(silhouette[0]))


"""
Given an image, it generate files containing individual puzzle pieces
@author: Hana
"""

#open image
from classes_generator import PuzzlePiece
from classes_generator import Edge
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import random
from create_edge import create_edge
from matplotlib import path
import os

DEBUG=0

#Input data/parameters
imgfilename='sheet_music.jpg'
ncols=3 #nunber of columns
nrows=4 #number of rows
jitter=0.125 #Measure of the random variation for the location of the corners of each piece
bkgcolor=(0,255,0) #Greenscreen colour for the background of the pieces

#Load image and convert to rgb. imread and imwrite use BGR but matplotlib uses RGB
img = cv.imread(imgfilename,cv.IMREAD_COLOR)
img = cv.cvtColor(img,cv.COLOR_BGR2RGB) #Convert to RGB


if DEBUG:
    plt.imshow(img)
    plt.show()

#Select coordinates for the corners of the pieces
imgheight,imgwidth,channel=img.shape #Dimension of the original image
pheight=int(imgwidth/ncols) #average height of a piece
pwidth=int(imgheight/nrows) #average width of a piece

X=np.zeros((nrows+1,ncols+1)) #Array containing the x-coordinate of all the corners
Y=np.zeros((nrows+1,ncols+1)) #Array containing the y-coordinate of all the corners
for j in range(0,ncols+1):
    for i in range(0,nrows+1):
        if j==0 or j==ncols: #Corner on the edge of the puzzle => No jitter
            X[i,j]=pheight*j
        else: #Corner in the middle of the puzzle => Add jitter
            X[i,j]=pheight*(j+random.randrange(-1,1)*jitter)
        if i==0 or i==nrows:
            Y[i,j]=pwidth*i
        else:
            Y[i,j]=pwidth*(i+random.randrange(-1,1)*jitter)

if DEBUG:
    plt.plot(X,Y,'ro')

#Create an empty array of pieces.
pieces=[]

#Add pieces to the array of pieces and store the coordinates of the centre of each piece
for i in range(0,nrows):
    for j in range(0,ncols):
        newpiece= PuzzlePiece()
        newpiece.centre=np.array([pheight*(j+0.5),pwidth*(i+0.5)])
        newpiece.alledges=[Edge(),Edge(),Edge(),Edge()]
        pieces.append(newpiece)

#Store the coordinates of the 4 corners of each piece
#Each piece has an array for the X-coordinates (coordx) of the 4 corners and
#an array for the Y-coordinates (coordy)
d=0.25*(pwidth+pheight)/2 #height of the head/hole
npieces=nrows*ncols #Total number of pieces
for p in range(npieces): #For each piece p
    pcol=p%ncols
    prow=p//ncols
    pieces[p].coordx=np.array([X[prow][pcol],X[prow][pcol+1],X[prow+1][pcol+1],X[prow+1][pcol]])
    pieces[p].coordy=np.array([Y[prow][pcol],Y[prow][pcol+1],Y[prow+1][pcol+1],Y[prow+1][pcol]])

#Create edges and contour for each piece based on the coordinates of the corners
for p in range(npieces):
    #allocate 4 edges per piece
    if (p+ncols)>=(npieces): #piece in last row
        pieces[p].alledges[2]=create_edge(pieces[p].coordx[2],pieces[p].coordy[2],pieces[p].coordx[3],pieces[p].coordy[3],0)
    else:
        pieces[p].alledges[2]=create_edge(pieces[p+ncols].coordx[1],pieces[p+ncols].coordy[1],pieces[p+ncols].coordx[0],pieces[p+ncols].coordy[0],d)

    if p>=ncols: #piece not in first row
        pieces[p].alledges[0].points=pieces[p-ncols].alledges[2].points[::-1]
    else:
        pieces[p].alledges[0]=create_edge(pieces[p].coordx[0],pieces[p].coordy[0],pieces[p].coordx[1],pieces[p].coordy[1],0)

    if p%ncols==0: #piece on the left edge
        pieces[p].alledges[3]=create_edge(pieces[p].coordx[3],pieces[p].coordy[3],pieces[p].coordx[0],pieces[p].coordy[0],0)
    else:
        pieces[p].alledges[3].points=pieces[p-1].alledges[1].points[::-1]

    if (p+1)%ncols==0: #piece on right edge
        pieces[p].alledges[1]=create_edge(pieces[p].coordx[1],pieces[p].coordy[1],pieces[p].coordx[2],pieces[p].coordy[2],0)
    else:
        pieces[p].alledges[1]=create_edge(pieces[p].coordx[1],pieces[p].coordy[1],pieces[p].coordx[2],pieces[p].coordy[2],d)

    #Create contour of the piece by concatenating the 4 edges of the piece
    pieces[p].contour=pieces[p].alledges[0].points
    pieces[p].contour=np.concatenate((pieces[p].contour,pieces[p].alledges[1].points))
    pieces[p].contour=np.concatenate((pieces[p].contour,pieces[p].alledges[2].points))
    pieces[p].contour=np.concatenate((pieces[p].contour,pieces[p].alledges[3].points))

    if DEBUG:
        pieces[p].plot()
        plt.ylim([np.max(Y)+100,-100])
        plt.xlim([-100,np.max(X)+100])

# Create image for each piece

# Image for each piece
for p in range(npieces):
    # Create blank image and then add the pixels with the actual image of the piece
    pieces[p].image = np.uint8(np.zeros(img.shape))
    pieces[p].image[:,:,0:3]=bkgcolor
    pieceshape = path.Path((pieces[p].contour))  # Create a 'path' using the contour of the piece
    print('Getting image for piece index '+str(p)+' ('+str(p+1)+' of '+str(npieces)+')')
#    for j in range(int(max([0,pieces[p].centre[0]-w])),int(min([imgwidth,pieces[p].centre[0]+w]))):
#        for i in range(int(max([0,round(pieces[p].centre[1]-h)])),int(min([imgheight,round(pieces[p].centre[1]+h)]))):
#            if pieceshape.contains_points([(j,i)])==True:
#                pieces[p].image[i,j,:]=img[i,j,:]
    j=np.arange(int(max([0,pieces[p].centre[0]-pwidth])),(int(min([imgwidth,pieces[p].centre[0]+pwidth]))))
    i=np.arange(int(max([0,round(pieces[p].centre[1]-pheight)])),(int(min([imgheight,round(pieces[p].centre[1]+pheight)]))))
    J,I = np.meshgrid(j,i,indexing='xy')
    points = np.hstack((J.reshape((-1,1)), I.reshape((-1,1))))
    mask = np.where(pieceshape.contains_points(points),1,0)
    mask.shape=J.shape
    mask_inv= -(mask-1) # Invert the mask
    pieces[p].image[I,J,0]=img[I,J,0]*mask+bkgcolor[0]*mask_inv
    pieces[p].image[I,J,1]=img[I,J,1]*mask+bkgcolor[1]*mask_inv
    pieces[p].image[I,J,2]=img[I,J,2]*mask+bkgcolor[2]*mask_inv

# Move all pieces to (roughly) the centre of a square of size LxL and rotate piece randomly
L=int(np.sqrt(pwidth**2+pheight**2))*2 #integer as 'number of pixels' is integer
for p in range(npieces):
    #Displacement vector
    dx=pieces[p].centre[0]-(L/2)
    dy=pieces[p].centre[1]-(L/2)

    #Displace and crop image
    M = np.float32([[1,0,-(dx)],[0,1,-(dy)]])
    piece_image= cv.warpAffine(pieces[p].image,M,(L,L),borderMode=cv.BORDER_CONSTANT,borderValue=bkgcolor)

    #Rotate image
    alpha=random.random()*360 #rotate clockwise (degrees)
    R = cv.getRotationMatrix2D((L/2,L/2),-alpha,1) # Rotation matrix
    piece_image=cv.warpAffine(piece_image,R,(L,L),borderMode=cv.BORDER_CONSTANT,borderValue=bkgcolor)

    if DEBUG:
        plt.figure()
        plt.imshow(piece_image)

    #save image to file
    #directory name based on the original image file name and the number of pieces
    new_directory=os.path.splitext(imgfilename)[0]+'_'+str(nrows)+'x'+str(ncols);
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
    #filename
    pn=str(p).zfill(len(str(npieces)))
    filename='p'+pn+'.jpg'

    savepath=new_directory+'\\'+filename
    piece_image = cv.cvtColor(piece_image,cv.COLOR_RGB2BGR) #Converting back to BGR for imwrite to create the correct files
    cv.imwrite(savepath,piece_image)
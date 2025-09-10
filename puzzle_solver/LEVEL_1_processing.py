"""
Created on Sun Feb 21 16:56:23 2021

@author: Hana
"""
import os
import cv2 as cv
import numpy as np
from classes_solver import PuzzlePiece
from classes_solver import Edge_S
from scipy.signal import find_peaks
import sys


def Load_pieces(foldername):
    filename=os.listdir(foldername)
    pieces=[]
    for i in range(len(filename)):
        newpiece=PuzzlePiece()
        newpiece.image=cv.imread(foldername +"\\" + filename[i])
        newpiece.image=cv.cvtColor(newpiece.image,cv.COLOR_BGR2RGB)
        #newpiece.image=cv.imread(foldername +"\\" + filename[i])
        pieces.append(newpiece)
    return(pieces,filename)

def Mask(image):
    image = cv.cvtColor(image,cv.COLOR_BGR2RGB)# convert to rgb as cv reads it as bgr
    # make mask of puzzle piece to remove background and create contour
    # make threshold of green colour
    lower_green=np.array([0,220,0])
    upper_green=np.array([100,255,100])

    mask=cv.inRange(image,lower_green,upper_green)

    masked_image=np.copy(image)
    masked_image[mask!=0]=[0,0,0] #not mask=black
    masked_image[mask==0]=[255,255,255] #mask=white
    return(masked_image)

def Remove_bkg(piece):

    height, width = piece.image.shape[:2]

    for r in range(height):
        for c in range(width):
            if piece.mask[r,c][0]==0:
                piece.image[r,c]=np.array([0,0,0])
    return(piece.image)

def Contour(masked_image):
    grayIm = cv.cvtColor(masked_image,cv.COLOR_BGR2GRAY)
    # Handle both OpenCV 3.x and 4.x+ versions
    try:
        # OpenCV 4.x+ returns (contours, hierarchy)
        contours, _ = cv.findContours(np.uint8(grayIm), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    except ValueError:
        # OpenCV 3.x returns (image, contours, hierarchy)
        _, contours, _ = cv.findContours(np.uint8(grayIm), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #pieces[i].contour=np.array(contours[0])[:,0,:]
    return(np.array(contours[0])[:,0,:])

def Corners(piece):
    #finding centre of the piece using the idea of centre of mass
    rows, cols, t = piece.mask.shape
    sum_n=0
    sum_rn=0
    #centre of mass = mass*distance / total mass
    for r in range(rows):
        n=0
        for c in range(cols):
            if piece.mask[r,c][0]==255:
                n=n+1
        sum_n=sum_n+n
        sum_rn=sum_rn+r*n
    cy=sum_rn/sum_n

    sum_cn=0
    for c in range(cols):
        n=0
        for r in range(rows):
            if piece.mask[r,c][0]==255:
                n=n+1
        sum_cn=sum_cn+c*n
    cx=sum_cn/sum_n

    #finding distance from each point on contour to centre of piece
    ar_D=np.array([])
    for j in range(len(piece.contour)):
        p=piece.contour[j,:]
        dy=p[1]-cy
        dx=p[0]-cx
        D=np.sqrt(dy**2+dx**2)
        ar_D=np.append(ar_D,D)

    #plotting on graph, sharp peaks are corners
    shift=np.argsort(ar_D)[0]#sort into order so that graph starts on min
    Ds=np.roll(ar_D,-shift)
    #dont forget to roll Ds back, so that distance correponds to contour point

    #max points
    y=Ds
    peaks,_ = find_peaks(y,prominence=20)

    if len(peaks)<4:
        sys.exit('error, less than 4 peaks detected ')

    #test sharpness of corner points by giving each point a 'quality' value
    #find yPA+yPB
    qual=np.array([])
    w=int(len(piece.contour)*0.008)
    for j in range(len(peaks)):
        py=Ds[peaks[j]]
        Ay=Ds[peaks[j]-w]
        By=Ds[peaks[j]+w]
        qual=np.append(qual,(py-Ay)+(py-By)-abs(Ay-By))

    piece.corners=np.zeros([4,2])
    ar_pos=np.array([])
    for j in range(4):
        p=np.argsort(-qual)[j] #sort so that largest quality value comes first, descending list

        #obtain corner points from contour
        pos=peaks[p]+shift
        ar_pos=np.append(ar_pos,pos)


    for l in range(len(ar_pos)):
        if ar_pos[l]>=len(piece.contour):
            ar_pos[l]=ar_pos[l]-len(piece.contour)

    ar_pos=np.sort(ar_pos)
    for l in range(4):
        piece.corners[l,0]=piece.contour[int(ar_pos[l]),0]
        piece.corners[l,1]=piece.contour[int(ar_pos[l]),1]

    return(ar_pos)

def Edges(piece,ar_pos):
    piece.edges=[]
    ar_pos=np.sort(ar_pos)
    for j in range(4):
        new_edge=Edge_S()
        if j==3:
            new_edge.points=piece.contour[int(ar_pos[j]):]
            piece.edges.append(new_edge)
            if int(ar_pos[0])!=0:
                new_edge.points=np.concatenate(([piece.edges[j].points],[piece.contour[0:int(ar_pos[0])]]),axis=1)[0]
                piece.edges.append(new_edge)
        else:
            new_edge.points=piece.contour[int(ar_pos[j]):int(ar_pos[j+1])]
            piece.edges.append(new_edge)

    if len(piece.edges)==5:
        piece.edges=np.delete(piece.edges,4)

def Edge_type(piece):
    for e in range(4):
        #finding perpendincular distance from curve to line corner to corner using cross product
        A=piece.corners[e]
        type_v=0
        if e==3:
            B=piece.corners[0]
        else:
            B=piece.corners[e+1]
        a=B-A
        u=a/(np.sqrt(a[0]**2+a[1]**2))#unitary vector AB
        for m in range(len(piece.edges[e].points)):
            M=piece.edges[e].points[m]
            MA=A-M
            d=(MA[0]*u[1])-(MA[1]*u[0])
            type_v=type_v+d

#        UB=200
#        LB=-200

#        UB=520
#        LB=-520


        B=(np.sqrt(a[0]*a[0]+a[1]*a[1])*0.03)*len(piece.edges[e].points) #'pixels along one edge times 0.3' error allowed per point , times number of points along edge
        UB=B
        LB=(-1)*B

        piece.edges[e].type=[]

        if type_v>UB:
            piece.edges[e].type=+1
        elif type_v<LB:
            piece.edges[e].type=-1
        else:
            piece.edges[e].type=0

"""
Created on Sun Feb 21 19:40:06 2021

@author: Hana
"""
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


#used in Test_cand to rotate only the relevant edges
#despite name also, translates edge to correct point
def Rotate_edge_e1(aw,n,edge,corner_point,corner_point_coord,bb_pieces,piece):
    if aw==0:
        dv_piece_a=np.array([1,0])
    else:
        dv_piece_a=bb_pieces[n-aw-1].corners[2]-bb_pieces[n-aw-1].corners[3]

    A_coord=corner_point_coord
    B=corner_point+1
    if B==4:
        B=0
    B_coord=piece.corners[B]
    dv_piece_b=B_coord-A_coord#direction vector of piece_b

    dot=np.dot(dv_piece_a,dv_piece_b)
    cross=np.cross(dv_piece_a,dv_piece_b)
    theta=np.arctan2(cross, dot)

    #rotate edge
    rot_point=corner_point_coord
    angle=theta*180/np.pi
    R=cv.getRotationMatrix2D((rot_point[0],rot_point[1]),angle,1)#point of rotation, angle, scale

    points=piece.edges[edge].points
    ones = np.ones([len(points), 1])
    points_ones= np.hstack([points, ones])
    check_edge = R.dot(points_ones.T).T#after rotation

    ccx=corner_point_coord[0]
    ccy=corner_point_coord[1]
    if aw==0:
        fx=int(bb_pieces[n-2].corners[1][0])
        fy=int(bb_pieces[n-2].corners[1][1])
    else:
        fx=int(bb_pieces[n-aw-1].corners[3][0])
        fy=int(bb_pieces[n-aw-1].corners[3][1])


    dx=fx-ccx
    dy=fy-ccy

    for j in range(len(check_edge[:,0])):#after translation
        check_edge[j,0]=check_edge[j,0]+dx
        check_edge[j,1]=check_edge[j,1]+dy


    return(check_edge,angle)



#used in Test_cand to rotate only the relevant edges
#despite name also, translates edge to correct point
def Rotate_edge_e2(aw,n,edge,corner_point,corner_point_coord,bb_pieces,piece):
    if aw==0:
        if n-1==0:
            dv_piece_a=np.array([0,-1])
        else:
            dv_piece_a=bb_pieces[n-2].corners[2]-bb_pieces[n-2].corners[1]
    else:
        if (n-1)%aw==0:
            dv_piece_a=np.array([0,-1])
        else:
            dv_piece_a=bb_pieces[n-2].corners[2]-bb_pieces[n-2].corners[1]

    A_coord=corner_point_coord
    B=corner_point-1
    if B==-1:
        B=3
    B_coord=piece.corners[B]
    dv_piece_b=B_coord-A_coord#direction vector of piece_b

    dot=np.dot(dv_piece_a,dv_piece_b)
    cross=np.cross(dv_piece_a,dv_piece_b)
    theta=np.arctan2(cross, dot)

    #rotate edge
    rot_point=corner_point_coord
    angle=theta*180/np.pi
    R=cv.getRotationMatrix2D((rot_point[0],rot_point[1]),angle,1)#point of rotation, angle, scale

    points=piece.edges[edge].points
    ones = np.ones([len(points), 1])
    points_ones= np.hstack([points, ones])
    check_edge = R.dot(points_ones.T).T#after rotation

    ccx=corner_point_coord[0]
    ccy=corner_point_coord[1]
    if aw==0:
        fx=int(bb_pieces[n-2].corners[1][0])
        fy=int(bb_pieces[n-2].corners[1][1])
    else:
        fx=int(bb_pieces[n-aw-1].corners[3][0])
        fy=int(bb_pieces[n-aw-1].corners[3][1])


    dx=fx-ccx
    dy=fy-ccy

    for j in range(len(check_edge[:,0])):#after translation
        check_edge[j,0]=check_edge[j,0]+dx
        check_edge[j,1]=check_edge[j,1]+dy

    return(check_edge,angle)


def Rotate_edge_flat_1(aw,piece,n,corr_e1,e):
    if e+1==4:
        sub=0
    else:
        sub=e+1
    A_coord=corr_e1[0,:]
    B_coord=corr_e1[1,:]
    dv_piece_a=B_coord-A_coord#direction vector of piece_a


    dv_piece_b=piece.corners[sub]-piece.corners[e]

    dot=np.dot(dv_piece_a,dv_piece_b)
    cross=np.cross(dv_piece_a,dv_piece_b)
    theta=np.arctan2(cross, dot)

    angle=theta*180/np.pi


    return(angle)


def Rotate_edge_flat_2(aw,piece,n,corr_e2,ne):
    if ne+1==4:
        sub=0
    else:
        sub=ne+1
    A_coord=corr_e2[0,:]
    B_coord=corr_e2[1,:]
    dv_piece_a=B_coord-A_coord#direction vector of piece_b

    dv_piece_b=piece.corners[ne]-piece.corners[sub]

    dot=np.dot(dv_piece_a,dv_piece_b)
    cross=np.cross(dv_piece_a,dv_piece_b)
    theta=np.arctan2(cross, dot)

    angle=theta*180/np.pi

    return(angle)




#knowing first and second edge,finds corner point of piece which will be pivot for rotation
def Rot_corner(e,ne,piece):
    corners_used=[]
    if e == 3:
        corners_used.append(e)
        corners_used.append(0)
    else:
        corners_used.append(e)
        corners_used.append(e+1)

    if ne ==3:
        corners_used.append(ne)
        corners_used.append(0)
    else:
        corners_used.append(ne)
        corners_used.append(ne+1)
    for i in range(4):
        if corners_used.count(corners_used[i])>1:
            corner_point=corners_used[i]
            corner_point_coord=piece.corners[corner_point]
    return(corner_point,corner_point_coord)



def Extend_board(piece_b,corner_point,piece):
    a=int(piece_b.shape[0]/2)
    e_piece_b=cv.copyMakeBorder(piece_b, a, a, a, a, cv.BORDER_CONSTANT)
    for i in range(4):
        for r in range(len(piece.edges[i].points)):
            piece.edges[i].points[r,0]=piece.edges[i].points[r,0]+a
            piece.edges[i].points[r,1]=piece.edges[i].points[r,1]+a
    for c in range(4):
        piece.corners[c][0]=piece.corners[c][0]+a
        piece.corners[c][1]=piece.corners[c][1]+a
    corner_point_coord=piece.corners[corner_point]
    return(e_piece_b,corner_point_coord)

def Rotate(aw,n,corner_point,corner_point_coord, bb_pieces, e_piece_b,piece):
    if aw==0:
        if n-1==0:
            dv_piece_a=np.array([0,-1])
        else:
            dv_piece_a=bb_pieces[n-2].corners[2]-bb_pieces[n-2].corners[1]
    else:
        if (n-1)%aw==0:
            dv_piece_a=np.array([0,-1])
        else:
            dv_piece_a=bb_pieces[n-2].corners[2]-bb_pieces[n-2].corners[1]


    #find angle of rotation
    #select next corner, going clockwise around the piece
    #A and B are two points on piece b
    A_coord=corner_point_coord
    B=corner_point-1
    if B==-1:
        B=3
    B_coord=piece.corners[B]
    dv_piece_b=B_coord-A_coord#direction vector of piece_b

    dot=np.dot(dv_piece_a,dv_piece_b)
    cross=np.cross(dv_piece_a,dv_piece_b)
    theta=np.arctan2(cross, dot)

    #rotate piece
    rot_point=corner_point_coord
    angle=theta*180/np.pi
    R=cv.getRotationMatrix2D((rot_point[0],rot_point[1]),angle,1)#point of rotation, angle, scale
    rot_piece = cv.warpAffine(e_piece_b, R, e_piece_b.shape[:2], borderMode=cv.BORDER_CONSTANT)
    return(rot_piece,R)

def Onto_bb(size,piece_b,rot_piece):
    #extend canvas to make blackboard
    m=int((piece_b.shape[0]*size)-rot_piece.shape[0])
    n=int((piece_b.shape[1]*size)-rot_piece.shape[1])
    bbp = cv.copyMakeBorder(rot_piece, 0, m, 0, n, cv.BORDER_CONSTANT)
    return(bbp)

def Translate(n,p,aw,size,height,corner_point_coord,bbp,bb_pieces):
    ccx=corner_point_coord[0]
    ccy=corner_point_coord[1]
    if n-1==0:
        fx=100
        fy=int(height*size)-100
    elif aw==0:
        fx=int(bb_pieces[n-2].corners[1][0])
        fy=int(bb_pieces[n-2].corners[1][1])
    else:
        fx=int(bb_pieces[n-aw-1].corners[3][0])
        fy=int(bb_pieces[n-aw-1].corners[3][1])

    rows,cols,c = bbp.shape
    dx=fx-ccx
    dy=fy-ccy
    Trans=np.float32([[1,0,(dx)],[0,1,(dy)]])
    piece_t = cv.warpAffine(bbp,Trans,(cols,rows))
    return(piece_t,dx,dy)

def Rename_edges(R,dx,dy,corner_point,piece):
    for i in range(4):
        points=piece.edges[i].points
        ones = np.ones([len(points), 1])
        points_ones= np.hstack([points, ones])
        piece.edges[i].points = R.dot(points_ones.T).T#after rotation
        for j in range(len(piece.edges[i].points[:,0])):#after translation
            piece.edges[i].points[j,0]=piece.edges[i].points[j,0]+dx
            piece.edges[i].points[j,1]=piece.edges[i].points[j,1]+dy

    piece.edges=np.roll(piece.edges,-corner_point)
    return(piece.edges)

def Rename_corners(R,dx,dy,corner_point,piece):
    points=piece.corners
    ones = np.ones([len(points), 1])
    points_ones= np.hstack([points, ones])
    piece.corners = R.dot(points_ones.T).T#after rotation
    for i in range(4):#after translation
        piece.corners[i,0]=piece.corners[i,0]+dx
        piece.corners[i,1]=piece.corners[i,1]+dy

    temp_corners=np.zeros([4,2])
    for i in range(4):
        temp_corners[i,:]=piece.corners[corner_point]
        if corner_point+i==4:
            temp_corners[i,:]=piece.corners[0]
        elif corner_point+i==5:
            temp_corners[i,:]=piece.corners[1]
        elif corner_point+i==6:
            temp_corners[i,:]=piece.corners[2]
        else:
            temp_corners[i,:]=piece.corners[i+corner_point]
    piece.corners=temp_corners
    return(piece.corners)

def g_Points(edge,g):
    x = edge[:,0]
    y = edge[:,1]

    # Linear length on the line
    distance = np.cumsum(np.sqrt( np.ediff1d(x, to_begin=0)**2 + np.ediff1d(y, to_begin=0)**2 ))
    distance = distance/distance[-1]

    fx, fy = interp1d( distance, x ), interp1d( distance, y )

    alpha = np.linspace(0, 1, g)
    x_regular, y_regular = fx(alpha), fy(alpha)
    return(x_regular,y_regular)

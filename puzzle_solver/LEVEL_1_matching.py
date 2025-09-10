"""
Created on Sun Feb 21 17:23:27 2021

@author: Hana
"""
import numpy as np
import matplotlib.pyplot as plt
from LEVEL_2_matching import Rotate_edge_e1
from LEVEL_2_matching import Rotate_edge_e2
from LEVEL_2_matching import Rot_corner
from LEVEL_2_matching import Extend_board
from LEVEL_2_matching import Rotate
from LEVEL_2_matching import Onto_bb
from LEVEL_2_matching import Translate
from LEVEL_2_matching import Rename_edges
from LEVEL_2_matching import Rename_corners
from LEVEL_2_matching import g_Points
from LEVEL_2_matching import Rotate_edge_flat_1
from LEVEL_2_matching import Rotate_edge_flat_2



def Flat_edge_p(pieces):
    side_p=[] #list of pieces which are side pieces
    corner_p=[]#list of corner pieces
    for i in range(len(pieces)):
        for e in range(4):
            if pieces[i].edges[e].type==0:
                if side_p.count(i)>0: #if piece is already in list for having a side, then it is a corner
                    side_p.remove(i)
                    corner_p.append(i)
                else:
                    side_p.append(i)

    return(side_p,corner_p)





def Crit(n,aw,T,w, bb_pieces,og_list_p,corner_p,side_p,size,pieces):
    cand=np.array([])
    bp=n-1 #board piece
    len_p=len(pieces[0].edges[0].points)

    if aw==0:
        e1=0
        corr_e1=np.array([[(((n+w-1)%w))*len_p,aw*len_p],[(((n+w-1)+1)%w)*len_p,aw*len_p]])
    else:
        e1=(bb_pieces[bp-aw].edges[2].type)*-1
        corr_e1=bb_pieces[bp-aw].edges[2]

    if bp==0:
        e2=0
        corr_e2=np.array([[((n+w-1)%w)*len_p,aw*len_p],[((n+w-1)%w)*len_p,-(aw+1)*len_p]])
    elif aw==0:
        e2=(bb_pieces[bp-1].edges[1].type)*-1
        corr_e2=bb_pieces[bp-1].edges[1]
    elif bp%aw==0:
        e2=0
        corr_e2=np.array([[((n+w-1)%w)*len_p,aw*len_p],[((n+w-1)%w)*len_p,-(aw+1)*len_p]])
    else:
        e2=(bb_pieces[bp-1].edges[1].type)*-1
        corr_e2=bb_pieces[bp-1].edges[1]

    #matching
    if n>=size and aw==0: #if a piece is the bottom right corner
        for i in range(len(corner_p)):
            for e in range(4):
                if e-1==-1:
                    ne=3
                else:
                    ne=e-1

                if pieces[corner_p[i]].edges[e].type==e1 and pieces[corner_p[i]].edges[ne].type==e2:
                    cand=np.append(cand,np.array([corner_p[i],e,ne]))

    elif len(og_list_p)==aw: #if a piece is the top left corner
        for i in range(len(corner_p)):
            for e in range(4):
                if e-1==-1:
                    ne=3
                else:
                    ne=e-1

                if pieces[corner_p[i]].edges[e].type==e1 and pieces[corner_p[i]].edges[ne].type==e2:
                    cand=np.append(cand,np.array([corner_p[i],e,ne]))

    elif aw!=0 and aw%n==0: #if a piece is a side piece on the right
        for i in range(len(side_p)):
            for e in range(4):
                if e-1==-1:
                    ne=3
                else:
                    ne=e-1

                if pieces[side_p[i]].edges[e].type==e1 and pieces[side_p[i]].edges[ne].type==e2:
                    cand=np.append(cand,np.array([side_p[i],e,ne]))

    elif aw!=0 and aw%(n-1)==0: #if a piece is a side piece on the left
        for i in range(len(side_p)):
            for e in range(4):
                if e-1==-1:
                    ne=3
                else:
                    ne=e-1

                if pieces[side_p[i]].edges[e].type==e1 and pieces[side_p[i]].edges[ne].type==e2:
                    cand=np.append(cand,np.array([side_p[i],e,ne]))

    else:
        for i in range(T-(bp)):
            for e in range(0,4):
                if e-1==-1:
                    ne=3
                else:
                    ne=e-1
                if pieces[og_list_p[i]].edges[e].type==e1 and pieces[og_list_p[i]].edges[ne].type==e2:
                    cand=np.append(cand,np.array([og_list_p[i],e,ne]))

    cand=cand.reshape((int(len(cand)/3),3))


#    if aw!=0 and (n-1)%3!=0 and n%aw!=0 and len(og_list_p)!=aw:
#        delete_row=np.array([])
#        range_c =int(len(cand))-1
#        for c in range(range_c):
#            for m in range(0,int(len(side_p))-1):
#                if int(cand[c,0])==int(side_p[m]):
#                    delete_row=np.append(delete_row,c)
#        delete_row=delete_row[::-1] #invert array so that no issues with row number when deleting a row
#        for dp in range(len(delete_row)):
#            dv=int(delete_row[dp])
#            cand=np.delete(cand,dv,0) #remove from array cand, row dv, axis 0 (horizontal)
#
    return(cand,corr_e1,corr_e2,e1,e2)



def Test_cand(cand, corr_e1,corr_e2,e1,e2,n,aw,bb_pieces,pieces):
    total_diffs=np.zeros([len(cand),2])
    A=pieces[0].corners[0]
    B=pieces[0].corners[1]
    a=B-A
    pix=np.sqrt(a[0]**2 + a[1]**2)  #number of points along one edge
    g=int(pix*0.2) #number of comparison points that will be selected, 20% of total points
    CHECKING=np.zeros((len(cand),5))

    for i in range(len(cand)):
        p=int(cand[i][0])
        e=int(cand[i][1])
        ne=int(cand[i][2])

        total_diffs[i,0]=p
        CHECKING[i,0]=p

        angle_1=0
        if e1==0: #type of edge is flat
            angle_1=Rotate_edge_flat_1(aw,pieces[p],n,corr_e1,e)
        else:
            corner_point,corner_point_coord=Rot_corner(e,ne,pieces[p])
            edge=corner_point

            check_edge_x,angle_1=Rotate_edge_e1(aw,n,edge,corner_point,corner_point_coord,bb_pieces,pieces[p])
            new_check_edge_x=np.zeros([g,2])
            x_regular,y_regular=g_Points(check_edge_x,g)
            for gn in range(g):
                new_check_edge_x[gn,0]=x_regular[gn]
                new_check_edge_x[gn,1]=y_regular[gn]

            check_edge_x=new_check_edge_x


            new_corr_e1=np.zeros([g,2])
            x_regular,y_regular=g_Points(corr_e1.points,g)
            for gn in range(g):
                new_corr_e1[gn,0]=x_regular[gn]
                new_corr_e1[gn,1]=y_regular[gn]

            corr_e1.points=new_corr_e1

            k=int(len(check_edge_x)/g)
            check_x=int(len(corr_e1.points)/g)

            #check to see if edge needs inverting
            if check_edge_x[0,0]<check_edge_x[(g*k)-1,0]:
                check_edge_x=check_edge_x[::-1]
            if corr_e1.points[0,0]<corr_e1.points[(g*check_x)-1,0]:
                corr_e1.points=corr_e1.points[::-1]#invert so that first point on corr_e2 is at top

#            plt.plot(check_edge_x[:,0],check_edge_x[:,1],'r')
#            plt.plot(corr_e1.points[:,0],corr_e1.points[:,1],'b')
#

            for j in range(g):
                diffs=abs(check_edge_x[(j*k)-1]-corr_e1.points[(j*check_x)-1])
                total_diffs[i,1]=total_diffs[i,1]+np.sqrt(diffs[0]**2+diffs[1]**2)

#                print('p')
#                print(p)
#                print('adding each time')
#                print(str(np.sqrt(diffs[0]**2+diffs[1]**2)))


#                plt.plot(check_edge_x[j*k][0],check_edge_x[j*k][1],'r.')
#                plt.plot(corr_e1.points[j*check_x][0],corr_e1.points[j*check_x][1],'b.')
#                x_values = [check_edge_x[j*k][0], corr_e1.points[j*check_x][0]]
#                y_values = [check_edge_x[j*k][1], corr_e1.points[j*check_x][1]]
#                plt.plot(x_values, y_values)


        angle_1=angle_1




        angle_2=0
        if e2==0:
            angle_2=Rotate_edge_flat_2(aw,pieces[p],n,corr_e2,ne)
        else:
            corner_point,corner_point_coord=Rot_corner(e,ne,pieces[p])
            if corner_point-1==-1:
                edge=3
            else:
                edge=corner_point-1

            check_edge_y,angle_2=Rotate_edge_e2(aw,n,edge,corner_point,corner_point_coord,bb_pieces,pieces[p])
            new_check_edge_y=np.zeros([g,2])
            x_regular,y_regular=g_Points(check_edge_y,g)
            for gn in range(g):
                new_check_edge_y[gn,0]=x_regular[gn]
                new_check_edge_y[gn,1]=y_regular[gn]

            check_edge_y=new_check_edge_y

            new_corr_e2=np.zeros([g,2])
            x_regular,y_regular=g_Points(corr_e2.points,g)
            for gn in range(g):
                new_corr_e2[gn,0]=x_regular[gn]
                new_corr_e2[gn,1]=y_regular[gn]

            corr_e2.points=new_corr_e2

#            plt.figure()
#            plt.plot(check_edge_y[:,0],check_edge_y[:,1],'m')
#            plt.plot(corr_e2.points[:,0],corr_e2.points[:,1],'g')

            k=int(len(check_edge_y)/g)
            check_y=int(len(corr_e2.points)/g)

            #check to see if edge needs inverting
            if check_edge_y[0,1]<check_edge_y[(g*k)-1,1]:
                check_edge_y=check_edge_y[::-1]
            if corr_e2.points[0,1]<corr_e2.points[(g*check_y)-1,1]:
                corr_e2.points=corr_e2.points[::-1]#invert so that first point on corr_e2 is at top

            #top down
            for j in range(int(g*0.1), int(g-(0.1*g))):
                diffs=abs(check_edge_y[(j*k)-1]-corr_e2.points[(j*check_y)-1])
                total_diffs[i,1]=total_diffs[i,1]+np.sqrt(diffs[0]**2+diffs[1]**2)




#                plt.plot(check_edge_y[j*k][0],check_edge_y[j*k][1],'r.')
#                plt.plot(corr_e2.points[j*check_y][0],corr_e2.points[j*check_y][1],'b.')
#                x_values = [check_edge_y[j*k][0], corr_e2.points[j*check_y][0]]
#                y_values = [check_edge_y[j*k][1], corr_e2.points[j*check_y][1]]
#                plt.plot(x_values, y_values)



        if angle_1<0:
            angle_1=180+angle_1

        angle_2=angle_2
        if angle_2<0:
            angle_2=180+angle_2


        if angle_1-angle_2<-180:
            angle_diff=angle_1-angle_2+180
        elif angle_1-angle_2>180:
            angle_diff=angle_1-angle_2-180
        else:
            angle_diff=angle_1-angle_2


        CHECKING[i,1]=total_diffs[i,1]
        total_diffs[i,1]=total_diffs[i,1]/(g)
        CHECKING[i,2]=total_diffs[i,1]



        scale = (3/2) #good values are 3 points out and 2 degrees for angle

        CHECKING[i,3]=angle_diff
        CHECKING[i,4]=abs(scale*(angle_1 - angle_2))

        total_diffs[i,1]=total_diffs[i,1]+abs(scale*(angle_diff))

#        print(CHECKING)
#        print('angle_1')
#        print(angle_1)
#        print('angle_2')
#        print(angle_2)
#        print('diff')
#        print(angle_1 - angle_2)

#   print(total_diffs)
    #rank diffs
    diffs_val=np.array([])
    for j in range(len(cand)):
        diffs_val=np.append(diffs_val,total_diffs[j,1])
    order=np.argsort(diffs_val)

    ordered_diffs=np.zeros([len(total_diffs),3])
    for k in range(len(total_diffs)):
        ordered_diffs[k][0]=cand[order[k]][0]
        ordered_diffs[k][1]=cand[order[k]][1]
        ordered_diffs[k][2]=cand[order[k]][2]
    p=ordered_diffs[0,0]
    e=ordered_diffs[0,1]
    ne=ordered_diffs[0,2]

    if n==1:
        p=cand[2,0]
        e=cand[2,1]
        ne=cand[2,2]
    return(p,e,ne)





def Place_piece(p,e,ne,size,n,aw,bb_pieces,piece):
    #rotate all points, edges and corners
    #translate
    #return piece[p] with new points
    corner_point,corner_point_coord=Rot_corner(e,ne,piece)
    piece_b=piece.image

    #extend board to make space for rotation
    e_piece_b,corner_point_coord=Extend_board(piece_b,corner_point,piece)

    #rotate piece
    rot_piece,R=Rotate(aw,n,corner_point,corner_point_coord, bb_pieces, e_piece_b,piece)

    #makes canvas size of blackboard so easy to add all layers together
    #background is black as [0,0,0]+[0,0,0]=[0,0,0] so only shows pieces on final board
    bbp=Onto_bb(size,piece_b,rot_piece)
    height, width = piece_b.shape[:2]

    #transaltes piece onto correct position, uses corner point/ pivot point
    piece_t,dx,dy=Translate(n,p,aw,size,height,corner_point_coord,bbp,bb_pieces)


    #rotate and translate the coordinates of the edges
    piece.edges=Rename_edges(R,dx,dy,corner_point,piece)

    #rotate and translate the coordinates of the corners
    piece.corners=Rename_corners(R,dx,dy,corner_point,piece)

    return(piece_t,piece.edges,piece.corners)

#check if final piece is a corner piece
#if it is, make aw (actual width) equal to piece number
def Check_end(og_corner_p,p,aw,n):
    for i in range(len(og_corner_p)):
        if og_corner_p[i]==p:
            aw=n
    return(aw)

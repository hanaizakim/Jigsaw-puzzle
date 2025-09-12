"""
Created on Sun Feb 14 16:28:44 2021

@author: Hana
"""
import numpy as np
import matplotlib.pyplot as plt
from LEVEL_1_processing import Load_pieces
from LEVEL_1_processing import Mask
from LEVEL_1_processing import Remove_bkg
from LEVEL_1_processing import Contour
from LEVEL_1_processing import Corners
from LEVEL_1_processing import Edges
from LEVEL_1_processing import Edge_type
from LEVEL_1_matching import Flat_edge_p
from LEVEL_1_matching import Crit
from LEVEL_1_matching import Test_cand
from LEVEL_1_matching import Place_piece
from LEVEL_1_matching import Check_end


#find files in foldername
foldername='sheet_music_3x4'

#load pieces
pieces,filename=Load_pieces(foldername)

#analyse/process pieces
for i in range(len(pieces)):
    #show which piece working on to track progress when running
    print('Piece ' + str(i) + ' out of ' + str(len(pieces)))

    #find mask of piece on green background
    pieces[i].mask=Mask(pieces[i].image)

    #remove green background
    pieces[i].image=Remove_bkg(pieces[i])

    #find contour
    pieces[i].contour=Contour(pieces[i].mask)

    #find corners
    ar_pos=Corners(pieces[i])

    #create edges for each piece
    #make pieces[i].edges[0].points...etc
    Edges(pieces[i],ar_pos)

    # plt.figure()
    # plt.imshow(pieces[i].image)
    # plt.plot(pieces[i].edges[0].points[:,0],pieces[i].edges[0].points[:,1],'r')
    # plt.plot(pieces[i].edges[1].points[:,0],pieces[i].edges[1].points[:,1],'b')
    # plt.plot(pieces[i].edges[2].points[:,0],pieces[i].edges[2].points[:,1],'g')
    # plt.plot(pieces[i].edges[3].points[:,0],pieces[i].edges[3].points[:,1],'k')

    #find edge type
    Edge_type(pieces[i])

pieces_og= pieces[:].copy()

#match pieces
#prep for matching
#side_p=list of pieces with one flat edge
#corner_p=list of pieces with two consecutive flat edges
side_p,corner_p=Flat_edge_p(pieces)

T=len(pieces) #total number of pieces

E=len(side_p) #flat edge pieces
M=T-4-E #middle pieces with no flat edges

h=int(E/4 +(np.sqrt(abs(E**2-(16*M))))/4 +2) #height of piece
w= int(T/h) #width of piece
og_corner_p=corner_p.copy()
size= max(h,w)
aw=0 #actual width

print(str(h) + ' by ' + str(w) + ' puzzle')

bb_pieces=np.array([]) #array of pieces on blackboard in order
bb_layers=[] #blackboard layers, add layers together at the end
og_list_p=[] #original list of pieces

for i in range(T):
    og_list_p.append(i)

#for n in range(1,6):
for n in range(1,T+1):
    print(n)
    #returns candidate list with piece number, first edge and next edge (second edge is next edge clockwise)
    cand,corr_e1,corr_e2,e1,e2=Crit(n,aw,T,w, bb_pieces,og_list_p,corner_p,side_p,size,pieces)

    #rotate and translate relevant edges, create 'g' points on each edge and compare distances
    #using distances and angle rotated on each edge, select edge with smallest total distance and angle difference for piece p
    p,e,ne=Test_cand(cand, corr_e1,corr_e2,e1,e2,n,aw,bb_pieces,pieces)


    #place piece
    p=int(p) #piece selected
    e=int(e) #first edge, horizontal
    ne=int(ne) #second edge, vertical clockwise


    piece_t,pieces[p].edges,pieces[p].corners=Place_piece(p,e,ne,size,n,aw,bb_pieces,pieces[p])

    bb_layers.append(piece_t)
    bb_pieces=np.append(bb_pieces,pieces[p])
    og_list_p.remove(p)



    #if piece was a corner piece, remove from list
    for corner in range(len(corner_p)):
        if p == corner_p[corner-1]:
            corner_p.remove(p)

    #check to see if reached actual width
    if aw==0:
        if n==1:
            aw=0
        else:
            aw=Check_end(og_corner_p,p,aw,n)

#add layers together
actual_bb=bb_layers[0]
for i in range(1,len(bb_layers)):
    actual_bb=actual_bb+bb_layers[i]
plt.imshow(actual_bb)
plt.show()



# for i in range(T):
#    plt.figure()
#    plt.plot(pieces[i].edges[0].points[:,0],pieces[i].edges[0].points[:,1],'r')
#    plt.plot(pieces[i].corners[0,0],pieces[i].corners[0,1],'rx')
#    plt.plot(pieces[i].edges[1].points[:,0],pieces[i].edges[1].points[:,1],'g')
#    plt.plot(pieces[i].corners[1,0],pieces[i].corners[1,1],'gx')
#    plt.plot(pieces[i].edges[2].points[:,0],pieces[i].edges[2].points[:,1],'b')
#    plt.plot(pieces[i].corners[2,0],pieces[i].corners[2,1],'bx')
#    plt.plot(pieces[i].edges[3].points[:,0],pieces[i].edges[3].points[:,1],'m')
#    plt.plot(pieces[i].corners[3,0],pieces[i].corners[3,1],'mx')




# changes
    #made g not just value
    #made LB and UB of type of edge 'd' percentage
    #weighted value of change of angle, added to quality value of piece

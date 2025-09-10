from classes_generator import Edge
import numpy as np
import random
from interpolation import spcrv

def create_edge(Ax,Ay,Bx,By,d):
    """
    Returns a puzzle edge between two points
    Ax: x-coordinate of the first point
    Ay: y-coordinate of the first point
    Bx: x-coordinate of the second point
    By: y-coordinate of the second point
    d: "height" of the head/hole (0 for straight edge)
    """
    A=[Ax,Ay]
    B=[Bx,By]
    e=Edge()
    if d==0:
        e.guidepoints=np.array([A,B])
        e.points=np.array([A,B])
    else:
        s=0
        while s==0: #s=1 hole, s=-1 head
            s=np.sign(random.random()-0.5)

        e.guidepoints=np.zeros([9,2])
        e.guidepoints[0,:]=np.array(A)
        e.guidepoints[-1,:]=np.array(B)

        AB=e.guidepoints[-1,:]-e.guidepoints[0,:] #vector A to B
        e.guidepoints[1,:]=e.guidepoints[0,:]+AB*0.1*random.randrange(4,5)
        e.guidepoints[-2,:]=e.guidepoints[0,:]+AB*0.1*random.randrange(5,6)

        u=AB/(np.sqrt(AB[0]**2+AB[1]**2)) #unitary vector from A to B
        v=np.array([-u[1],u[0]]) #unitary vector perpendicular to AB

        e.guidepoints[2,:]=e.guidepoints[1,:]+random.randrange(-1,1)*0.05*AB+s*random.randrange(2,5)/10*d*v
        e.guidepoints[-3,:]=e.guidepoints[-2,:]+random.randrange(-1,1)*0.05*AB+s*random.randrange(2,5)/10*d*v

        e.guidepoints[3,:]=e.guidepoints[2,:]-random.randrange(1,2)*0.1*AB+s*random.randrange(1,2)*0.2*d*v
        e.guidepoints[-4,:]=e.guidepoints[-3,:]+random.randrange(1,2)*0.1*AB+s*random.randrange(1,2)*0.2*d*v

        e.guidepoints[4,:]=e.guidepoints[0,:]+AB*0.5+s*v*d

        e.points=(e.guidepoints)
        e.points=spcrv(e.guidepoints)

    return e

def create_edge_s(e):
    e.points=spcrv(e.guidepoints)
    return e
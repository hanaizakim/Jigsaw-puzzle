"""
Created on Mon Oct 19 20:47:38 2020

@author: elfi
"""
import numpy as np
def spcrv(x):
#SPCRV Spline curve by uniform subdivision. (Usign algorithm from matlab)
#
#   CURVE = SPCRV(X)  uses repeated midpoint knot insertion to generate a
#   fine sequence of successive values CURVE(:,i) of the spline
#
#      t |-->  sum  B(t-K/2;j,...,j+k)*X(j)  for  t  in  [K/2 .. n-K/2]
#               j
#
#   from the input (d,n)-array X.
#   For d>1, each CURVE(:,i) is a point on the corresponding spline curve.
#   The insertion process stops as soon as there are >= MAXPNT knots.
#   K is set to 3 and MAXKNT to 100.

    kntstp = 1
    k = 3
    maxpnt = 100

    # Transpose x if necessary to have all the x coordinates of the points
    # in x(0,:) and all the y components in x(:,1)
    [d,n] = x.shape
    transposed=False
    if n<d:
        x=x.T[:]
        [d,n] = x.shape
        transposed=True

    y = x[:]
    while n<maxpnt:
         kntstp = 2*kntstp
         m = 2*n
         yy=np.zeros((d,2*n))
         yy[:,1::2] = y[:]
         yy[:,::2] = y[:]
         for r in range(1,k):
            yy[:,1::] = (yy[:,1::]+yy[:,0:m-1])*.5
         y = yy[:,k-1:m]
         n = m+1-k

    # Include first and last point
    firstpoint=x[::,0]
    lastpoint=x[::,-1]
    #To use np.concatenate, we need to extend the second array to 2D and then concatenate along axis=1
    curve = np.concatenate([firstpoint[:,None], y, lastpoint[:,None]],axis=1)
    if transposed:
        return curve.T
    else:
        return curve
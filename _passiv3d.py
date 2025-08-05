import items
from math import cos, sin
#import matplotlib.pyplot as plt

def projection(X:(float), th:float, ph:float):
    ''' projection 3D into 2D (cf. wiki) 

    X  : (float)*3     < represents the 3d cartesian position of the point to project
    th : float         < the angle theta = the latitude  of the viewer
    ph : float         < the angle phi   = the longitude of the viewer '''

    x, y, z = X

    vx, vy     = -sin(ph)       , cos(ph)
    wx, wy, wz = sin(th)*cos(ph), sin(th)*sin(ph), cos(th)

    x2 = vx*x + vy*y
    y2 = wx*x + wy*y + wz*z

    return x2, y2
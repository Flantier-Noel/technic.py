import items
from math import cos, sin
import heapq
import warnings

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

class Plane():
    ''' class of portions of plane defined by their corners
     
        corners_3D : [(float)*3]    < represents the 3D postions (x, y, z) of the corners defining the portions in the 3D space
        
        corners_2D : [(float)*2]    < represents the 2D positions (x, y)   of the corners defining the portions in the 2D space (projection cf. wiki) '''
    
    def __init__(self, corners_3D:list):
        self.corners_3D = []
        ## supress eventual double in corners_3D
        _dic_double = {}
        for item in corners_3D :
            if item in _dic_double.keys(): warnings.warn("Plane : definition contained repetitions")
            else :
                _dic_double[item] = -1
                self.corners_3D.append(item)
        del _dic_double
        ##

        self.corners_2D = [projection(pos_3D) for pos_3D in corners_3D]

        assert len(corners_3D) > 2, "Plane : must be defined by at least 3 points"

        ## check if the plane portion is well defined ie contained in a plane
        p0x, p0y, p0z = corners_3D[0]
        p1x, p1y, p1z = corners_3D[1]
        p2x, p2y, p2z = corners_3D[2]

        u1x, u1y, u1z = p1x-p0x, p1y-p0y, p1y-p0y
        u2x, u2y, u2z = p2x-p0x, p2y-p0y, p2y-p0y
        
        for (pix, piy, piz) in corners_3D :
            uix, uiy, uiz = pix-p0x, piy-p0y, piy-p0y
            det = u1x*u2y*uiz + u2x*uiy*u1z + uix*u1y*u2z - uix*u2y*u1z- u2x*u1y*uiz - u1x*uiy*u2z
            assert det == 0, "Plane : unplanar definition"
        ##
    
    def __contains__(self, point:(float)):
        ''' check if a 3D point is contained in the plain section 
        
        point : (float)*3       < represents the 3D postion (x, y, z) of the point to check'''


class Scene():
    ''' class of scene constitued of planes in a 3D space 
    
        planes : [Plane]            < represents the list of planes defining the scene'''
    
    def __init__(self, planes:list):
        self.planes = planes.copy()
        
    def priority(self, th:float, ph:float):
        prio = []

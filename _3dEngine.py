#import items
from math import cos, sin, sqrt
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
     
        corners_3D    : [(float)*3]                    < represents the 3D postions (x, y, z) of the corners defining the portions in the 3D space 
        color         : (hex)*3                        < represents the filling rgb color of the plane
        outline       : (hex)*3                        < represents the outline rgg color of the plane - set as same as color by default

        ***
        
        _support_plan : [(float)*3]                    < represents a 3 points defining the plane in which the section is contained'''
    
    def __init__(self, corners_3D:list, color:(hex), outline=None):
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

        self.fill = '#'
        self.outline = '#'
        for ind_col in range(3) :
            fill_val = color[ind_col][2:]
            if len(fill_val) < 2 : fill_val = '0'*(2-len(fill_val)) + fill_val
            if len(fill_val) > 2 : 
                fill_val = fill_val[-2:]
                warnings.warn('Plane : color hex truncated')

            self.fill += fill_val
            if outline == None : self.outline += fill_val
            else :
                outl_val = outline[ind_col][2:]
                if len(outl_val) < 2 : outl_val = '0'*(2-len(outl_val)) + outl_val
                if len(outl_val) > 2 : 
                    outl_val = outl_val[-2:]
                    warnings.warn('Plane : outline hex truncated')

                self.outline += outl_val  

        assert len(corners_3D) > 2, "Plane : must be defined by at least 3 points"

        ## check if the plane portion is well defined ie contained in a plane
        p0x, p0y, p0z = corners_3D[0]
        p1x, p1y, p1z = corners_3D[1]
        p2x, p2y, p2z = corners_3D[2]

        u1x, u1y, u1z = p1x-p0x, p1y-p0y, p1z-p0z
        u2x, u2y, u2z = p2x-p0x, p2y-p0y, p2z-p0z

        self._support_plan = [(p0x, p0y, p0z), (p1x, p1y, p1z), (p2x, p2y, p2z)]
        
        for (pix, piy, piz) in corners_3D :
            uix, uiy, uiz = pix-p0x, piy-p0y, piz-p0z
            det = u1x*u2y*uiz + u2x*uiy*u1z + uix*u1y*u2z - uix*u2y*u1z- u2x*u1y*uiz - u1x*uiy*u2z
            assert det == 0, "Plane : unplanar definition"
        ##

    def to_3D(self, pos_2D:(float), th:float, ph:float):
        ''' give the 3D position of a 2D point projected as described in the wiki 
        
            pos_2D  : (float)*2         < represents the 2D position (x, y) of the projected point
            th      : float             < represents the theta angle of the projection
            ph      : float             < represents the phi   angle of the projection '''
        
        x2, y2 = pos_2D

        [(p0x, p0y, p0z), (p1x, p1y, p1z), (p2x, p2y, p2z)] = self._support_plan
        u1x, u1y, u1z = p1x-p0x, p1y-p0y, p1z-p0z
        u2x, u2y, u2z = p2x-p0x, p2y-p0y, p2z-p0z

        vx, vy     = -sin(ph)       , cos(ph)
        wx, wy, wz = sin(th)*cos(ph), sin(th)*sin(ph), cos(th)

        syst_mat = [[u1x*vx + u1y*vy, u2x*vx + u2y*vy], [u1x*wx + u1y*wy + u1z*wz, u2x*wx + u2y*wy + u2z*wz]]
        det = syst_mat[0][0]*syst_mat[1][1] - syst_mat[0][1]*syst_mat[1][0]
        if det == 0 : raise ArithmeticError ## !! seems to be problematic
        inv_syst_mat = [[syst_mat[1][1]/det, -syst_mat[0][1]/det], [-syst_mat[1][0]/det, syst_mat[0][0]/det]]
        val0 = [x2 - (p0x*vx + p0x*vy), y2 - (p0x*vx + p0y*vy)]

        pln_var0, pln_var1 = inv_syst_mat[0][0]*val0[0] + inv_syst_mat[0][1]*val0[1], inv_syst_mat[1][0]*val0[0] + inv_syst_mat[1][1]*val0[1]
        x3, y3, z3 = pln_var0*u1x + pln_var1*u2x + p0x, pln_var0*u1y + pln_var1*u2y + p0y, pln_var0*u1z + pln_var1*u2z + p0z

        return x3, y3, z3

class Scene():
    ''' class of scene constitued of planes in a 3D space 
    
        planes : [Plane]            < represents the list of planes defining the scene'''
    
    def __init__(self, planes:list):
        self.planes = planes.copy()
        
    def priority(self, th:float, ph:float):
        ''' cf wiki '''

        def are_2Dintersecting(pln1, pln2):
            ''' check if two planes intersects in the projection. Returns an instnace of intersecting 2D point.
            
                pln1, pln2 : Plane  < represents the planes to check '''
            

            for i in range(len(pln1.corners_3D)):
                corners_2D_pln1 = [projection(pos_3D, th , ph) for pos_3D in pln1.corners_3D]

                p11x, p11y = corners_2D_pln1[i]
                p12x, p12y = corners_2D_pln1[(i+1)%len(corners_2D_pln1)]
                u1x, u1y = p12x-p11x, p12y-p11y

                for j in range(len(pln2.corners_3D)):
                    corners_2D_pln2 = [projection(pos_3D, th, ph) for pos_3D in pln2.corners_3D]

                    p21x, p21y = corners_2D_pln2[j]
                    p22x, p22y = corners_2D_pln2[(j+1)%len(corners_2D_pln2)]
                    u2x, u2y = p22x-p21x, p22y-p21y

                    det = u1x*u2y - u1y*u2x
                    if det != 0 :
                        val0x, val0y = u1x*p11x + u2x*p11y, u2y*p11x + u2y*p11y
                        xint, yint = (u2y*val0x - u2x*val0y)/det, (-u1y*val0x + u1x*val0y)/det
                        return True, (xint, yint)
            
            return False, None

        def merge_sort(L:list):
            ''' sort a list of Plane according to their distance from the viewer 
            
            L : [Plane]             < represents the list of planes to sort '''

            def merge(L1:list, L2:list):
                ''' merge function of a merge_sort '''

                i1, i2 = 0,0
                L_merge = []
                while i1 < len(L1) or i2 < len(L2):
                    if i1 >= len(L1) : 
                        L_merge.append(L2[i2])
                        i2 += 1
                    elif i2 >= len(L2) :
                        L_merge.append(L1[i1])
                        i1 += 1
                    else :
                        pln1, pln2 = L1[i1], L2[i2]

                        tst_inter, pt_inter = are_2Dintersecting(pln1, pln2)
                        if tst_inter :
                            ix1, iy1, iz1 = pln1.to_3D(pt_inter, th, ph)
                            ix2, iy2, iz2    = pln2.to_3D(pt_inter, th, ph)

                            vx, vy, vz    = cos(th)*cos(ph), cos(th)*sin(ph), -sin(th)

                            d1 = sqrt((ix1-vx)**2 + (iy1-vy)**2 +(iz1-vz)**2)
                            d2 = sqrt((ix2-vx)**2 + (iy2-vy)**2 +(iz2-vz)**2)

                            if d1 >= d2 :
                                L_merge.append(L1[i1])
                                i1 +=  1
                            else :
                                L_merge.append(L2[i2])
                                i2 += 1
                        else : 
                            L_merge.append(L1[i1])
                            i1 += 1
                return L

            def main_sort(L:(list)):
                ''' main recursive sorting function '''

                if len(L) <= 1 : return L
                else :
                    i_mid = len(L)//2
                    L1, L2 = L[:i_mid], L[i_mid:]
                    return merge(main_sort(L1), main_sort(L2))
                
            return main_sort(L)

        return merge_sort(self.planes)

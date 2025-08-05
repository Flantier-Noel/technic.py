import math
import warnings
import _default_values as dft

class _Hole():
    ''' basic type for connections between _Items 
    
        centerEnt : (float)*3                       < represents the 3d position (x, y, z) of the center of the hole's entry
        centerExt : (float)*3                       < represents the 3d position (x, y, z) of the center of the hole's exit 
        from      : str : 'cross' || 'round'        < defined the form of the hole '''

    def __init__(self, centerEnt:(float), centerExt:(float), form:str):
        pass

class _Items():
    ''' basic type for any objects such as gear, axes, ...
    
        center_pos3d : (float)*3                < represents the 3d position (x, y, z) of the center of the object
        weight       : float                    < represents the mass of the items 
        orient       : (float)*2                < represents the rotation of the object by (theta, phi)'''
    
    def __init__(self, center_pos3d:(float), orient:(float), weight:float):
        self.center_pos3d = center_pos3d
        self.orient = orient
        self.weight = weight

    class Gear():
        ''' gear child class : gear described either by (radius, number of tooth) or by key of _Items.Gear._default_gears
        
            center_pos3d, orient                < super arg
            rad      : float                    < describe the radius of the gear taken into account tooth heigth
            nb_tooth : int                      < describe the number of tooths of the gear 
            dft_gr   : str                      < describe the gear by its key for _Items.Gear._default_gears '''
        
        _default_rads = dft._gear_rads          # [float] < list of radius of default gears
        _default_tths = dft._gear_tths          # [int]   < list of nb_tooth of default gears
        _default_gears = dft._gear_dict         # {(int, int)} < dict of default gear given by index - keys/values given in doc

        def __init__(self, center_pos3d:(float), orient:(float), rad=None, nb_tooth=None, dft_gr=None):
            wgt = dft._wgtGear_fun(rad)
            _Items.__init__(self, center_pos3d, orient, wgt)

            assert (rad != None and nb_tooth != None) or dft_gr != None, "Gear : gear badly defined, either (rad, nb_tooth) or dft_gr must be described"

            if self.rad == None :
                [radInd, tthInd] = _Items.Gear._default_gears[dft_gr]
                self.radius = _Items.Gear._default_rads[radInd]
                self.nb_tth = _Items.Gear._default_rads[tthInd]

            else :
                self.radius = rad
                self.nb_tth = nb_tooth

                if ( rad not in _Items.Gear._default_rads ) or ( nb_tooth not in _Items.Gear._default_tths ): 
                    warnings.warn("Gear : unusual gear described")

    class Axes():
        ''' axes child class : axes described by its length
        
            center_pos3d, orient                < super arg
            length      : int                   < describes the length of the axes by its number of studs '''
        
        def __init__(self, center_pos3d:(float), orient:(float), length:int):
            wgt = dft._wgtAxe_fun(length)
            _Items.__init__(self, center_pos3d, orient, wgt)

            self.lgt = length
    
    class Join():
        ''' join child class :

            center_pos3d, orient                    < super arg
            length      : int                       < describes the length of the join by its number of studs 
            rough       : bool                      < describes either the join could rotate or not 
            form_lst    : ('cross' || 'round') list < describes the formes of each part of the join '''

        def __init__(self, center_pos3d:(float), length:int, rough:bool, form_lst:list, orient:(float)):
            wgt = dft._wgtJoin_fun(length)
            _Items.__init__(self, center_pos3d, orient, wgt)
            
            if length > 3 : warnings.warn("Join : unusual length described")
            assert len(form_lst) == length, "Join : wrong dimension for form_lst"

            self.length = length
            self.rough = rough
            self.form_lst = form_lst

    class Beam(): ## gestion de la forme ??
        ''' beam child class :
        
            center_pos3d, orient                < super arg
            length      : int                   < describes the length of the beam by its number of studs '''

        def __init__(self,center_pos3d:(float), length:int, orient:(float)):
            wgt = dft._wgtBeam_fun(length)
            _Items.__init__(self, center_pos3d, orient, wgt)
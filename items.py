import math
import warnings
import _default_values as dft

class _Items():
    ''' basic type for any objects such as gear, axes, ...
    
        center_pos3d : (float)*3                < represents the 3d position (x, y, z) of the center of the object
        weight       : float                    < represents the mass of the items '''
    
    def __init__(self, center_pos3d:(float), weight:float):
        self.center_pos3d = center_pos3d
        self.weight = weight

    class Gear():
        ''' gear child class : gear described either by (radius, number of tooth) or by key of _Items.Gear._default_gears
        
            center_pos3d                        < super arg
            rad      : float                    < describe the radius of the gear taken into account tooth heigth
            nb_tooth : int                      < describe the number of tooths of the gear 
            dft_gr   : str                      < describe the gear by its key for _Items.Gear._default_gears '''
        
        _default_rads = dft._gear_rads          # [float] < list of radius of default gears
        _default_tths = dft._gear_tths          # [int]   < list of nb_tooth of default gears
        _default_gears = dft._gear_dict         # {(int, int)} < dict of default gear given by index - keys/values given in doc

        def __init__(self, center_pos3d:(float), rad=None, nb_tooth=None, dft_gr=None):
            wgt = 100
            _Items.__init__(self, center_pos3d, wgt)

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
        
            center_pos3d                        < super arg
            length      : int                   < describes the length of the axes by the number of studs '''
        
        def __init__(self, center_pos3d:(float), length:int):
            wgt = 100
            _Items.__init__(self, center_pos3d, wgt)

            self.lgt = length

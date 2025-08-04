# default gears values

_gear_rads = [0.5, 0.9, 1.3, 2.15]
_gear_tths = [8, 16, 24, 40]
_gear_dict = {'gx0001':(0,0), 'gx0002':(1,1), 'gx0002':(2,2), 'gx0003':(3,3)} ## ids referenced in wiki
_wgtGear_fun = lambda rad : 0.825*rad**2 - 0.197*rad + 0.010  ## values explained in wiki

# default axes values

_wgtAxe_fun = lambda lgt : 0.152*lgt - 0.039                  ## values explained in wiki

## default beam values

_wgtBeam_fun = lambda lgt : 0.274*lgt - 0.219                 ## values explained in wiki

## default join values

_wgtJoin_fun = lambda lgt : 0.050*lgt + 0.049                 ## values explained in wiki

#
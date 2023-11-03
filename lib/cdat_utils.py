'''Interfacing netcdf data via CDAT

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2020-12-05 10:28:38.
'''

from __future__ import print_function
import os
import numpy as np
import cdms2 as cdms

current_dir, _=os.path.split(__file__)
DATA_FILE_NAME=os.path.join(current_dir, '../tests/erai_data.nc')

def isInteger(x):
    '''Check an input is integer

    Args:
        x (unknow type): input
    Returns:
        True if <x> is integer type, False otherwise.
    '''
    return isinstance(x, (int, np.integer))

#-------Retrieve required axis from variable-------
def getAxis(axis,ref_var,verbose=True):
    dim_idx=interpretAxis(axis,ref_var)
    try:
        ax=ref_var.getAxis(dim_idx)
    except:
        raise Exception("<axis> %s not found in variable." %str(axis))

    if ax is None:
        raise Exception("<axis> %s not found in variable." %str(axis))

    return ax

#-----------------Change latitude axis to south-to-north---------------------------
def increasingLatitude(slab,verbose=False):
    '''Changes a slab so that is always has latitude running from
    south to north.

    Args:
        slab (TransientVariable): input TransientVariable, need to have a
            proper latitude axis.
    Return:
        slab2 (TransientVariable): if latitude axis is reversed, or <slab>
            otherwise.

    If <slab> has a latitude axis, and the latitudes run from north to south, a
    copy <slab2> is made with the latitudes reversed, i.e., running from south
    to north.
    '''

    latax=getAxis('lat',slab)

    #-----Reverse latitudes if necessary------------------
    if latax[0]>latax[-1]:
        if verbose:
            print('\n# <increasingLatitude>: Reversing latitude axis.')
        slab2=slab(latitude=(latax[-1],latax[0]))
        return slab2
    else:
        if verbose:
            print('\n# <increasingLatitude>: Latitude axis correct. Not changing.')
        return slab

#------Interpret and convert an axis id to index----------
def interpretAxis(axis,ref_var,verbose=True):
    '''Interpret and convert an axis id to index

    Args:
        axis (int or str): axis option, integer (e.g. 0 for 1st dimension) or
            string (e.g. 'x' for x-dimension).
        ref_var (TransientVariable): reference variable.
    Return:
        axis_index (int): the index of required axis in <ref_var>.

    E.g. index=interpretAxis('time',ref_var)
         index=0

         index=interpretAxis(1,ref_var)
         index=1
    '''

    if isInteger(axis):
        return axis
    # interpret string dimension
    elif isinstance(axis,str):
        axis=axis.lower()

        if axis in ['time', 'tim', 't']:
            dim_id = 'time'
        elif axis in ['level', 'lev','z']:
            dim_id = 'level'
        elif axis in ['latitude', 'lat','y']:
            dim_id = 'latitude'
        elif axis in ['longitude', 'long', 'lon','x']:
            dim_id = 'longitude'
        else:
            dim_id = axis

        dim_index = ref_var.getAxisIndex(dim_id)

        if dim_index==-1:
            raise Exception("Required dimension not in <var>.")

        return dim_index
    else:
        raise Exception("<axis> type not recognized.")

def readData(varid):
    '''Read sample netcdf data

    Args:
        varid (str): id of variable to read.
    Returns:
        var (TransientVariable): sample netcdf data.
    '''
    fin=cdms.open(DATA_FILE_NAME,'r')
    var=fin(varid)
    fin.close()
    return var

def checkGeomap(var, x, y):
    '''Check input args suitable for geo plot or not and do some preprocessing

    Args:
        var (TransientVariable): input N-d TransientVariable.
        x (ndarray): 1d array, x-coordinates.
        y (ndarray): 1d array, y-coordinates.
    Returns:
        isgeo (bool): True if inputs are suitable for geographical plot, False
            otherwise.
        var (TransientVariable): input <var> with latitude order reversed if
            needed.
        xx (ndarray): 1d array, use longitude axis of <var> if possible,
            <x> otherwise
        yy (ndarray): 1d array, use latitude axis of <var> if possible,
            <y> otherwise
    '''


    if isinstance(var, cdms.tvariable.TransientVariable) and \
            var.getLatitude() is not None and \
            var.getLongitude() is not None:
        isgeo = True
    elif isinstance(var, np.ndarray) and np.ndim(np.squeeze(var)) > 1\
            and x is not None and y is not None:
        isgeo = True
    else:
        isgeo = False

    try:
        var = increasingLatitude(var)
        yy = var.getLatitude()[:]
        xx = var.getLongitude()[:]
    except:
        xx = x
        yy = y

    return isgeo, var, xx, yy


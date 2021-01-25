'''Interfacing netcdf data via netcdf4

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2021-01-24 17:30:56.
'''

from __future__ import print_function
import numpy as np
from netCDF4 import Dataset

DATA_FILE_NAME='erai_data.nc'

def readData(varid):
    '''Read in a variable from an netcdf file

    Args:
        abpath_in (str): absolute file path to the netcdf file.
        varid (str): id of variable to read.
    Returns:
        ncvarNV (NCVAR): variable stored as an NCVAR obj.
    '''

    fin=Dataset(DATA_FILE_NAME, 'r')
    var=fin.variables[varid][:]

    return var


def checkGeomap(var, xarray, yarray):
    '''Check input args suitable for geo plot or not and do some preprocessing

    Args:
        var (TransientVariable): input N-d TransientVariable.
        xarray (ndarray): 1d array, x-coordinates.
        yarray (ndarray): 1d array, y-coordinates.
    Returns:
        isgeo (bool): True if inputs are suitable for geographical plot, False
            otherwise.
        var (TransientVariable): input <var> with latitude order reversed if
            needed.
        xx (ndarray): 1d array, use longitude axis of <var> if possible,
            <xarray> otherwise
        yy (ndarray): 1d array, use latitude axis of <var> if possible,
            <yarray> otherwise
    '''


    if isinstance(var, np.ndarray) and np.ndim(np.squeeze(var)) > 1\
            and xarray is not None and yarray is not None:
        isgeo=True
    else:
        isgeo=False

    return isgeo, var, xarray, yarray


from __future__ import print_function
from __future__ import absolute_import

#--------------Globals------------------------------------------


#-----------Variable 1----------------------
SOURCEDIR1='/home/guangzhi/datasets/erai/erai_qflux';
U_FILE_NAME='uflux_m1-60_6_2000_cln.nc'
V_FILE_NAME='vflux_m1-60_6_2000_cln.nc'




OUTPUTDIR='outputs1'





#--------Import modules-------------------------
import os
import cdms2 as cdms
#import MV2 as MV
import numpy as np
#from tools.plot import Plot2D, mkscale, Isofill
import matplotlib.pyplot as plt
import gplot


if __name__=='__main__':

    abpath_in=os.path.join(SOURCEDIR1, U_FILE_NAME)
    print('\n### <test>: Read in file:\n',abpath_in)
    fin=cdms.open(abpath_in,'r')
    u=fin('uflux', time=slice(0,10))
    fin.close()

    abpath_in=os.path.join(SOURCEDIR1, V_FILE_NAME)
    print('\n### <test>: Read in file:\n',abpath_in)
    fin=cdms.open(abpath_in,'r')
    v=fin('vflux', time=slice(0,10))
    fin.close()

    #----------------------Tests----------------------
    # default Plot2Quiver
    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)

    quiver=gplot.Quiver(4)
    uslab=np.array(u)[0]
    vslab=np.array(v)[0]

    aa=gplot.Plot2Quiver(uslab, vslab, ax=ax, step=8, keylength=300,
            scale=10000, units='m/s'
            )
    aa.plot()

    figure.show()

    # default basemap
    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)

    #quiver=gplot.Quiver(4)
    uslab=u[0]
    vslab=v[0]

    from basemap_utils import Plot2QuiverBasemap
    aa=Plot2QuiverBasemap(uslab, vslab, u.getLongitude()[:], u.getLatitude()[:], ax=ax, projection='cyl')
    aa.plot()

    figure.show()

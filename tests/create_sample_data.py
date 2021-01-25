'''Create sample data.
'''

from __future__ import print_function

#--------------Globals------------------------------------------
CLUSTERDIR='/home/guangzhi/datasets/'


#-----------------------slp-----------------------
SOURCEDIR1='erai/msl/';
VAR1='msl';VARIN1='msl';LEVELS1='s';LEVEL_TYPE1='s';\
YEARS1=1984;TIME_STEP1='6';SUFFIX1='ori.nc'

#-----------------------sst-----------------------
SOURCEDIR2='erai/newdownload'
VAR2='sst';VARIN2='sst';LEVELS2='s';LEVEL_TYPE2='s';\
YEARS2=1984;TIME_STEP2='6';SUFFIX2='ori.nc'

#-----------------------u850-----------------------
SOURCEDIR3='ERAI/u'
VAR3='u';VARIN3='u';LEVELS3=850;LEVEL_TYPE3='p';\
YEARS3=1984;TIME_STEP3='6';SUFFIX3='ori.nc'

#-----------------------v850-----------------------
SOURCEDIR4='ERAI/v'
VAR4='v';VARIN4='v';LEVELS4=850;LEVEL_TYPE4='p';\
YEARS4=1984;TIME_STEP4='6';SUFFIX4='ori.nc'

#-----------------------lsm-----------------------
SOURCEDIR5='ERAI'
VAR5='lsm';VARIN5='lsm';LEVELS5='s';LEVEL_TYPE5='s';\
YEARS5=1900;TIME_STEP5='a';SUFFIX5='mask-preprocessed.nc'

OUTPUTDIR='.'





#--------Import modules-------------------------
import os
import cdms2 as cdms
import MV2 as MV
import numpy as np
from tools import functions,plot

PLOT,SAVE=functions.isPlotSave(__name__)




#-------------Main---------------------------------
if __name__=='__main__':

    path=os.path.join(CLUSTERDIR, SOURCEDIR1)
    file_in_name=functions.fileName(VAR1,LEVEL_TYPE1,LEVELS1,\
    TIME_STEP1,YEARS1,SUFFIX1)
    abpath_in=os.path.join(path,file_in_name)
    print('\n### <sample>: Read in file:\n',abpath_in)
    fin=cdms.open(abpath_in,'r')
    slp=fin(VARIN1, time=slice(0,4))(squeeze=1)
    fin.close()

    slp=functions.increasingLatitude(slp)

    print('\n# <create_sample_data>: slp.shape', slp.shape)


    path=os.path.join(CLUSTERDIR, SOURCEDIR2)
    file_in_name=functions.fileName(VAR2,LEVEL_TYPE2,LEVELS2,\
    TIME_STEP2,YEARS2,SUFFIX2)
    abpath_in=os.path.join(path,file_in_name)
    print('\n### <sample>: Read in file:\n',abpath_in)
    fin=cdms.open(abpath_in,'r')
    sst=fin(VARIN2, time=slice(0,4))(squeeze=1)
    fin.close()

    sst=functions.increasingLatitude(sst)
    print('\n# <create_sample_data>: sst.shape', sst.shape)

    path=os.path.join(CLUSTERDIR, SOURCEDIR3)
    file_in_name=functions.fileName(VAR3,LEVEL_TYPE3,LEVELS3,\
    TIME_STEP3,YEARS3,SUFFIX3)
    abpath_in=os.path.join(path,file_in_name)
    print('\n### <sample>: Read in file:\n',abpath_in)
    fin=cdms.open(abpath_in,'r')
    u=fin(VARIN3, time=slice(0,4))(squeeze=1)
    fin.close()

    path=os.path.join(CLUSTERDIR, SOURCEDIR4)
    file_in_name=functions.fileName(VAR4,LEVEL_TYPE4,LEVELS4,\
    TIME_STEP4,YEARS4,SUFFIX4)
    abpath_in=os.path.join(path,file_in_name)
    print('\n### <sample>: Read in file:\n',abpath_in)
    fin=cdms.open(abpath_in,'r')
    v=fin(VARIN4, time=slice(0,4))(squeeze=1)
    fin.close()

    path=os.path.join(CLUSTERDIR, SOURCEDIR5)
    file_in_name=functions.fileName(VAR5,LEVEL_TYPE5,LEVELS5,\
    TIME_STEP5,YEARS5,SUFFIX5)
    abpath_in=os.path.join(path,file_in_name)
    print('\n### <sample>: Read in file:\n',abpath_in)
    fin=cdms.open(abpath_in,'r')
    lsm=fin(VARIN5)(squeeze=1)
    fin.close()

    u=functions.increasingLatitude(u)
    v=functions.increasingLatitude(v)

    print('\n# <create_sample_data>: u.shape', u.shape)
    print('\n# <create_sample_data>: v.shape', v.shape)

    #--------Save------------------------------------
    if SAVE:
        file_out_name='erai_data.nc'
        abpath_out=os.path.join('.',file_out_name)
        print('\n### <sample>: Saving output to:\n',abpath_out)
        fout=cdms.open(abpath_out,'w')
        fout.write(slp,typecode='f')
        fout.write(sst,typecode='f')
        fout.write(u,typecode='f')
        fout.write(v,typecode='f')
        fout.write(lsm,typecode='f')
        fout.close()












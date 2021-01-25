from __future__ import print_function
from __future__ import absolute_import

#--------Import modules-------------------------
import numpy as np
import MV2 as MV
import matplotlib
matplotlib.use('Qt4Agg')
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import gplot
import cdat_utils

SAVE=True


def test_cartopy_default():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())
    iso=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, title='Default cartopy', projection='cyl', geo_interface='cartopy')
    figure.show()

    return

def test_cartopy_label_axes_False():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())
    iso=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, title='Cartopy label_axes=False', projection='cyl', label_axes=False,
            geo_interface='cartopy')
    figure.show()

    return

def test_cartopy_axes_grid():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())
    iso=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, title='Cartopy axes_grid=True', projection='cyl', axes_grid=True, geo_interface='cartopy')
    figure.show()

    return

def test_cartopy_vertical_legend():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())
    iso=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, title='Cartopy vertical legend', projection='cyl', legend_ori='vertical', geo_interface='cartopy')
    figure.show()

    return

def test_cartopy_shading():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())

    iso=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, title='Basemap with shading', projection='cyl', geo_interface='cartopy')
    shading=gplot.Shading(color='g', alpha=0.5)

    thres=np.percentile(var1, 80)
    shadevar=MV.where(var1>=thres,1,np.nan)
    shadevar.setAxisList(var1.getAxisList())
    gplot.plot2(shadevar, shading, ax, projection='cyl',
            clean=True, geo_interface='cartopy')

    figure.show()

    return

def test_cartopy_stroke():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())
    iso=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001, stroke=True)
    gplot.plot2(var1, iso, ax, title='Cartopy isofill with stroke', projection='cyl', geo_interface='cartopy')
    figure.show()

    return

def test_cartopy_force_split():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())

    iso=gplot.Isofill(var1, 10, 1, 2, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, title='Cartopy force split', projection='cyl', geo_interface='cartopy')
    figure.show()

    return

def test_cartopy_boxfill():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111, projection=ccrs.PlateCarree())
    box=gplot.Boxfill(var1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, box, ax, title='Default Cartopy boxfill', projection='cyl', geo_interface='cartopy')
    figure.show()

    return

def test_cartopy_subplots():

    figure=plt.figure(figsize=(12,10),dpi=100)
    plot_vars=[var1, var2, var1, var2]
    iso1=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    iso2=gplot.Isofill(var2, 10, 1, 1, ql=0.05, qr=0.05)
    titles=['var1', 'var2', 'var1', 'var2']

    for ii, vii in enumerate(plot_vars):
        ax=figure.add_subplot(2,2,ii+1, projection=ccrs.PlateCarree())
        if ii%2==0:
            gplot.plot2(vii, iso1, ax, title=titles[ii], legend='local', geo_interface='cartopy')
        if ii%2==1:
            gplot.plot2(vii, iso2, ax, title=titles[ii], legend='local', geo_interface='cartopy')

    figure.show()

    return

def test_cartopy_subplots_global_legend():

    figure=plt.figure(figsize=(12,10),dpi=100)
    plot_vars=[var1, var1, var1, var1]
    iso1=gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    titles=['var1', 'var1', 'var1', 'var1']

    for ii, vii in enumerate(plot_vars):
        ax=figure.add_subplot(2,2,ii+1, projection=ccrs.PlateCarree())
        gplot.plot2(vii, iso1, ax, title=titles[ii], legend='global', fix_aspect=False, geo_interface='cartopy')

    figure.show()

    return

if __name__=='__main__':

    var1=cdat_utils.readData('mslp')
    var2=cdat_utils.readData('sst')

    #----------------------Tests----------------------
    test_cartopy_default()
    test_cartopy_label_axes_False()
    test_cartopy_axes_grid()
    test_cartopy_vertical_legend()
    test_cartopy_shading()
    test_cartopy_stroke()
    test_cartopy_force_split()
    test_cartopy_boxfill()
    test_cartopy_subplots()
    test_cartopy_subplots_global_legend()




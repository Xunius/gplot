from __future__ import print_function
from __future__ import absolute_import

#--------Import modules-------------------------
import numpy as np
import MV2 as MV
import matplotlib.pyplot as plt
from gplot.lib import gplot
from gplot.lib import cdat_utils
from gplot.lib.basemap_utils import Plot2Basemap, Plot2QuiverBasemap

SAVE=True


def test_basemap_default():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Default basemap', projection='cyl')
    figure.show()

    return

def test_basemap_default_cdat():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    _, var1b, lons, lats=cdat_utils.checkGeomap(var1, None, None)
    gp=Plot2Basemap(var1b, iso, lons, lats, ax=ax, title='Default basemap', projection='cyl')
    gp.plot()
    figure.show()

    return

def test_basemap_isofill_overflow():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1, num=10, zero=1, split=1, min_level=11000, qr=0.01)
    gplot.plot2(var1, iso, ax, title='Isofill with overflows', projection='cyl')
    figure.show()

    return

def test_basemap_isofill_split():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1, num=10, zero=1, split=2)
    gplot.plot2(var1, iso, ax, title='Isofill with force split', projection='cyl')
    figure.show()

    return

def test_basemap_boxfill():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    box=gplot.Boxfill(var1)
    gplot.plot2(var1, box, ax, title='default Boxfill', projection='cyl')
    figure.show()

    return

def test_basemap_axes_grid():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Plot2D axes_grid=True', axes_grid=True, projection='cyl')
    figure.show()

    return

def test_basemap_label_axes_False():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Basemap label_axes=False', projection='cyl', label_axes=False)
    figure.show()

    return

def test_basemap_vertical_legend():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Basemap vertical legend', projection='cyl', legend_ori='vertical')
    figure.show()

    return

def test_basemap_shading():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)

    iso=gplot.Isofill(var1)
    g1=gplot.plot2(var1, iso, ax, title='Basemap with shading', projection='cyl')

    shading=gplot.Shading(color='g', alpha=0.5)
    thres=np.percentile(var1, 80)
    gplot.plot2(MV.where(var1>=thres,1,np.nan), shading, ax, projection='cyl',
            bmap=g1.bmap,
            clean=True)

    figure.show()

    return

def test_basemap_stroke():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1, stroke=True)
    gplot.plot2(var1, iso, ax, title='Basemap isofill with stroke', projection='cyl')
    figure.show()

    return

def test_basemap_subplots():

    figure=plt.figure(figsize=(12,10),dpi=100)
    plot_vars1=[var1[ii] for ii in range(3)]
    plot_vars2=[var2[ii] for ii in range(3)]
    iso1=gplot.Isofill(plot_vars1, ql=0.005, qr=0.001)
    iso2=gplot.Isofill(plot_vars2, ql=0.05, qr=0.05)
    titles1=['var1-%d' %ii for ii in range(3)]
    titles2=['var2-%d' %ii for ii in range(3)]

    for ii, vii in enumerate(plot_vars1):
        ax=figure.add_subplot(3,2,2*ii+1)
        gplot.plot2(vii, iso1, ax, title=titles1[ii], legend='local', projection='cyl')

    for ii, vii in enumerate(plot_vars2):
        ax=figure.add_subplot(3,2,2*ii+2)
        gplot.plot2(vii, iso2, ax, title=titles2[ii], legend='local', projection='cyl')

    figure.show()

    return

def test_basemap_subplots_global_legend():

    figure=plt.figure(figsize=(12,10),dpi=100)
    plot_vars=[var1[ii] for ii in range(4)]
    iso1=gplot.Isofill(plot_vars, ql=0.005, qr=0.001)
    titles=['var1-%d' %ii for ii in range(4)]

    for ii, vii in enumerate(plot_vars):
        ax=figure.add_subplot(2,2,ii+1)
        gplot.plot2(vii, iso1, ax, title=titles[ii], legend='global', projection='cyl')

    figure.show()

    return

def test_basemap_quiver():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver()
    pquiver=Plot2QuiverBasemap(u, v, q, xarray=lons, yarray=lats,
            ax=ax, title='default quiver', projection='cyl')
    pquiver.plot()

    figure.show()

    return

def test_basemap_quiver2():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver()
    gplot.plot2(u, q, var_v=v, xarray=lons, yarray=lats,
            ax=ax, title='default quiver', projection='cyl')
    figure.show()

    return

def test_basemap_quiver_reso():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(reso=10)
    pquiver=Plot2QuiverBasemap(u, v, q, xarray=lons, yarray=lats,
            ax=ax, title='quiver reso=10', projection='cyl')
    pquiver.plot()

    figure.show()

    return

def test_basemap_quiver_scale():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(reso=5, scale=500)
    pquiver=Plot2QuiverBasemap(u, v, q, xarray=lons, yarray=lats,
            ax=ax, title='quiver step=5, scale=500', projection='cyl')
    pquiver.plot()

    figure.show()

    return

def test_basemap_quiver_scale_keylength():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(reso=5, scale=500, keylength=20)
    pquiver=Plot2QuiverBasemap(u, v, q, xarray=lons, yarray=lats,
            ax=ax, title='quiver step=5, scale=500, keylength=20', projection='cyl')
    pquiver.plot()

    figure.show()

    return

def test_basemap_quiver_overlay():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(reso=5, scale=500)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='default Plot2D', projection='cyl')

    pquiver=Plot2QuiverBasemap(u, v, q, xarray=lons, yarray=lats,
            ax=ax, clean=True, title='quiver overlay', projection='cyl')
    pquiver.plot()
    figure.show()

    return

def test_basemap_quiver_overlay2():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(reso=5, scale=500)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='default Plot2D', projection='cyl')

    gplot.plot2(u, q, var_v=v, xarray=lons, yarray=lats,
            ax=ax, clean=True, title='quiver overlay', projection='cyl')
    figure.show()

    return

if __name__=='__main__':


    var1=cdat_utils.readData('msl')
    var2=cdat_utils.readData('sst')
    u=cdat_utils.readData('u')
    v=cdat_utils.readData('v')
    _, u, lons, lats=cdat_utils.checkGeomap(u, None, None)

    #----------------------Tests----------------------
    test_basemap_default_cdat()
    test_basemap_default()
    test_basemap_isofill_overflow()
    test_basemap_isofill_split()
    test_basemap_boxfill()
    test_basemap_axes_grid()
    test_basemap_label_axes_False()
    test_basemap_vertical_legend()
    test_basemap_shading()
    test_basemap_stroke()
    test_basemap_subplots()
    test_basemap_subplots_global_legend()
    test_basemap_quiver()
    test_basemap_quiver2()
    test_basemap_quiver_reso()
    test_basemap_quiver_scale()
    test_basemap_quiver_scale_keylength()
    test_basemap_quiver_overlay()
    test_basemap_quiver_overlay2()

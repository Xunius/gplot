from __future__ import absolute_import
from __future__ import print_function
import time
import io
#from gplot.lib.cartopy_utils import Plot2QuiverCartopy
from gplot.lib.cartopy_utils import Plot2Cartopy as Plot2Geo
from gplot.lib import netcdf4_utils
import gplot
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# --------Import modules-------------------------
import numpy as np
import matplotlib
#matplotlib.use('Qt4Agg')
matplotlib.use('Agg')

SAVE = True



def test_cartopy_default(idx):

    figure = plt.figure(figsize=(12, 10), dpi=100)
    ax = figure.add_subplot(111, projection=ccrs.PlateCarree())
    iso = gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, x=lons, y=lats, title='Default cartopy',
                projection='cyl', geo_interface='cartopy', nc_interface='netcdf4')
    #figure.show()

    #----------------- Save plot ------------
    if SAVE:
        plot_save_name = f'test_1_{idx}'
        print('\n# <speed_tests>: Save figure to', plot_save_name)
        figure.savefig(plot_save_name+'.png', dpi=100, bbox_inches='tight')
    plt.close(figure)

    return



def test_cartopy_default2(proj, idx):

    figure = plt.figure(figsize=(12, 10), dpi=100)
    ax = figure.add_subplot(111, projection=proj)
    iso = gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)
    gplot.plot2(var1, iso, ax, x=lons, y=lats, title='Default cartopy',
                projection='cyl', geo_interface='cartopy', nc_interface='netcdf4')
    #figure.show()
    #----------------- Save plot ------------
    if SAVE:
        plot_save_name = f'test_2_{idx}'
        print('\n# <speed_tests>: Save figure to', plot_save_name)
        figure.savefig(plot_save_name+'.png', dpi=100, bbox_inches='tight')
    plt.close(figure)

    return


def test_cartopy_default3(proj, idx):

    figure = plt.figure(figsize=(12, 10), dpi=100)
    ax = figure.add_subplot(111, projection=proj)
    iso = gplot.Isofill(var1, 10, 1, 1, ql=0.005, qr=0.001)

    plotobj = Plot2Geo(
        var1, iso, ax=ax, legend='global', x=lons, y=lats,
        title='Default cartopy',
        label_axes=True,
        axes_grid=False,
        fill_color='0.8',
        projection=proj,
        fontsize=9,
        legend_ori='horizontal',
        clean=False, fix_aspect=False)
    cs = plotobj.plot()

    #figure.show()
    #----------------- Save plot ------------
    if SAVE:
        plot_save_name = f'test_3_{idx}'
        print('\n# <speed_tests>: Save figure to', plot_save_name)
        figure.savefig(plot_save_name+'.png', dpi=100, bbox_inches='tight')

    plt.close(figure)

    return cs


def test_cartopy_default4(proj, var_list, ref_var):

    figure = plt.figure(figsize=(12, 10), dpi=100)
    ax = figure.add_subplot(111, projection=proj)
    iso = gplot.Isofill(ref_var, 10, 1, 1, ql=0.005, qr=0.001)

    for ii, varii in enumerate(var_list):

        if ii == 0:

            plotobj = Plot2Geo(
                varii, iso, ax=ax, legend='global', x=lons, y=lats,
                title='Default cartopy',
                label_axes=True,
                axes_grid=False,
                fill_color='0.8',
                projection=proj,
                fontsize=9,
                legend_ori='horizontal',
                clean=False, fix_aspect=False)

            plotobj.plot()
        else:
            '''
            plotobj.var = plotobj.getSlab(varii)
            plotobj.add_cyclic_point(lons)

            clean_up_artists(ax, [cs])

            plotobj._plot()
            cs = plotobj.cs
            '''
            plotobj.update_plot(varii)

        #----------------- Save plot ------------
        if SAVE:
            plot_save_name = f'test_4_{ii}'
            print('\n# <speed_tests>: Save figure to', plot_save_name)
            figure.savefig(plot_save_name+'.png', dpi=100, transparent=False)

        plt.close(figure)

    return


def clean_up_artists(axis, artist_list):

    for artist in artist_list:

        try:
            while artist.collections:
                for col in artist.collections:
                    artist.collections.remove(col)
                    try:
                        axis.collections.remove(col)
                    except ValueError:
                        pass

                artist.collections = []
                axis.collections = []

        except AttributeError:
            pass

        try:
            artist.remove()
        except (AttributeError, ValueError):
            pass

    return


if __name__ == '__main__':

    var1 = netcdf4_utils.readData('msl')
    var2 = netcdf4_utils.readData('sst')
    u = netcdf4_utils.readData('u')
    v = netcdf4_utils.readData('v')
    lats = netcdf4_utils.readData('latitude')
    lons = netcdf4_utils.readData('longitude')

    # ----------------------Tests----------------------
    #test_cartopy_default()
    #proj = ccrs.PlateCarree()
    #cs = test_cartopy_default3(proj)
    t1 = time.perf_counter()
    for ii in range(10):
        test_cartopy_default(ii)

    t2 = time.perf_counter()
    print(f'time: {t2-t1}')

    t1 = time.perf_counter()
    proj = ccrs.PlateCarree()
    for ii in range(10):
        test_cartopy_default2(proj, ii)
    t2 = time.perf_counter()
    print(f'time 2: {t2-t1}')

    t1 = time.perf_counter()
    proj = ccrs.PlateCarree()
    for ii in range(10):
        test_cartopy_default3(proj, ii)
    t2 = time.perf_counter()
    print(f'time 3: {t2-t1}')

    t1 = time.perf_counter()
    proj = ccrs.PlateCarree()
    var_list = [ var1, ] * 10

    test_cartopy_default4(proj, var_list, var_list[0])
    t2 = time.perf_counter()

    print(f'time 4: {t2-t1}')

'''Test Cartopy plots

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2023-11-03 15:16:28.
'''

import os
import shutil
import unittest
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import gplot
from gplot.lib import netcdf4_utils
from gplot.lib.cartopy_utils import Plot2QuiverCartopy


class TestCartopyPlots(unittest.TestCase):
    '''Test Cartopy plots'''

    def setUp(self):
        '''Do preparation before test'''

        self.fixture_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'outputs')

        self.var1 = netcdf4_utils.readData('msl')
        self.var2 = netcdf4_utils.readData('sst')
        self.u    = netcdf4_utils.readData('u')
        self.v    = netcdf4_utils.readData('v')
        self.lats = netcdf4_utils.readData('latitude')
        self.lons = netcdf4_utils.readData('longitude')

    def test_cartopy_default(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        iso = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)

        gplot.plot2(self.var1, iso, ax, x=self.lons, y=self.lats,
                    title='Default cartopy',
                    projection='cyl', geo_interface='cartopy', nc_interface='netcdf4')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_default.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return



    def test_cartopy_label_axes_False(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        iso = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)

        gplot.plot2(self.var1, iso, ax, x=self.lons, y=self.lats,
                    title='Default cartopy', projection='cyl',
                    geo_interface='cartopy', label_axes=False,
                    nc_interface='netcdf4')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_label_axes_False.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_axes_grid(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        iso = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)

        gplot.plot2(self.var1, iso, ax, x=self.lons, y=self.lats,
                    title='Cartopy axes_grid=True', projection='cyl',
                    axes_grid=True, geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_axes_grid.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_vertical_legend(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        iso = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)

        gplot.plot2(self.var1, iso, ax, x=self.lons, y=self.lats,
                    title='Cartopy vertical legend', projection='cyl',
                    legend_ori='vertical', geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_vertical_legend.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_shading(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        iso = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)

        gplot.plot2(self.var1, iso, ax, x=self.lons, y=self.lats,
                    title='Basemap with shading', projection='cyl',
                    geo_interface='cartopy')

        shading = gplot.Shading(color='g', alpha=0.5)

        thres = np.percentile(self.var1, 80)
        shadevar = np.where(self.var1 >= thres, 1, np.nan)

        gplot.plot2(shadevar, shading, ax, x=self.lons, y=self.lats,
                    projection='cyl', clean=True, geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_shading.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_stroke(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        iso = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001, stroke=True)

        gplot.plot2(self.var1, iso, ax, x=self.lons, y=self.lats,
                    title='Cartopy isofill with stroke', projection='cyl',
                    geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_stroke.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_force_split(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        iso = gplot.Isofill(self.var1, 10, 1, 2, ql=0.005, qr=0.001)

        gplot.plot2(self.var1, iso, ax, x=self.lons, y=self.lats,
                    title='Cartopy force split', projection='cyl',
                    geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_force_split.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_boxfill(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        box = gplot.Boxfill(self.var1, 1, ql=0.005, qr=0.001)

        gplot.plot2(self.var1, box, ax, x=self.lons, y=self.lats,
                    title='Default Cartopy boxfill', projection='cyl',
                    geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_boxfill.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_subplots(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        plot_vars = [self.var1, self.var2, self.var1, self.var2]

        iso1 = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)
        iso2 = gplot.Isofill(self.var2, 10, 1, 1, ql=0.05, qr=0.05)

        titles = ['var1', 'var2', 'var1', 'var2']

        for ii, vii in enumerate(plot_vars):
            ax = figure.add_subplot(2, 2, ii+1, projection=ccrs.PlateCarree())

            if ii % 2 == 0:
                isoii = iso1

            if ii % 2 == 1:
                isoii = iso2

            gplot.plot2(vii, isoii, ax, x=self.lons, y=self.lats,
                        title=titles[ii], legend='local',
                        geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_subplots.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))


        return


    def test_cartopy_subplots2(self):

        #figure, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10), dpi=100,
                                    #subplot_kw={'projection': ccrs.PlateCarree()},
                                    #constrained_layout=False)
        figure = plt.figure(figsize=(8, 6), dpi=100)
        plot_vars = [self.var1, self.var2, self.var1, self.var2]

        iso1 = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)
        iso2 = gplot.Isofill(self.var2, 10, 1, 1, ql=0.05, qr=0.05)

        titles = ['var1', 'var2', 'var1', 'var2']

        for ii, vii in enumerate(plot_vars):
            ax = figure.add_subplot(2, 2, ii+1, projection=ccrs.PlateCarree())
            #ax = axes.flatten()[ii]

            if ii % 2 == 0:
                isoii = iso1

            if ii % 2 == 1:
                isoii = iso2

            gplot.plot2(vii, isoii, ax, x=self.lons, y=self.lats,
                        title=titles[ii], legend='local',
                        geo_interface='cartopy')

        figure.tight_layout()

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_subplots2.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_subplots_global_legend(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        plot_vars = [self.var1, self.var1, self.var1, self.var1]

        iso1 = gplot.Isofill(self.var1, 10, 1, 1, ql=0.005, qr=0.001)
        titles = ['var1', 'var1', 'var1', 'var1']

        for ii, vii in enumerate(plot_vars):
            ax = figure.add_subplot(2, 2, ii+1, projection=ccrs.PlateCarree())

            gplot.plot2(vii, iso1, ax, x=self.lons, y=self.lats,
                        title=titles[ii], legend='global', fix_aspect=False,
                        geo_interface='cartopy')

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_subplots_global_legend.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_quiver(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        q = gplot.Quiver(step=5)

        pquiver = Plot2QuiverCartopy(self.u, self.v, q, x=self.lons,
                                     y=self.lats, ax=ax, title='default quiver',
                                     projection='cyl')

        pquiver.plot()

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_quiver.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))



        return


    def tearDown(self):
        '''Do clean up after test'''

        try:
            shutil.rmtree(self.output_dir)
        except:
            pass
        else:
            print('output folder removed: {}'.format(self.output_dir))

        return



if __name__ == '__main__':

    unittest.main()
    # to run in commandline:
    # python -m unittest tests/test_module.py
    # to run all tests in tests/ folder:
    # python -m unittest discover -s tests
    # NOTE: Start directory and subdirectories containing tests must be regular package that have __ini__.py file.

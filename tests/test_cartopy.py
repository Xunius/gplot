'''Test Cartopy plots

Author: guangzhi XU (xugzhi1987@gmail.com)
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
from gplot.lib.cartopy_utils import Plot2Cartopy, Plot2QuiverCartopy


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

        pobj = Plot2Cartopy(self.var1, iso, self.lons, self.lats, ax=ax,
                            title='default cartopy', projection='cyl',)
        pobj.plot()

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

        pobj = Plot2Cartopy(self.var1, iso, self.lons, self.lats, ax=ax,
                            title='label_axes=False', projection='cyl',
                            label_axes=False)
        pobj.plot()

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

        pobj = Plot2Cartopy(self.var1, iso, self.lons, self.lats, ax=ax,
                            title='axes_grid=True', projection='cyl',
                            axes_grid=True)
        pobj.plot()

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

        pobj = Plot2Cartopy(self.var1, iso, self.lons, self.lats, ax=ax,
                            title='legend_ori="vertical"', projection='cyl',
                            legend_ori='vertical')
        pobj.plot()

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

        pobj = Plot2Cartopy(self.var1, iso, self.lons, self.lats, ax=ax,
                            title='Isofill with region shading', projection='cyl',)
        pobj.plot()


        shading = gplot.Shading(color='g', alpha=0.5)
        thres = np.percentile(self.var1, 80)
        shadevar = np.where(self.var1 >= thres, 1, np.nan)

        pobj.method = shading
        pobj.clean = True
        pobj.update_plot(shadevar, del_old=False)

        '''
        pobj = Plot2Cartopy(shadevar, shading, self.lons, self.lats, ax=ax,
                            title='Cartopy with shading', clean=True, projection='cyl',)
        pobj.plot()
        '''

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

        pobj = Plot2Cartopy(self.var1, iso, self.lons, self.lats, ax=ax,
                            title='Isofill with stroke', projection='cyl')
        pobj.plot()

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

        pobj = Plot2Cartopy(self.var1, iso, self.lons, self.lats, ax=ax,
                            title='Isofill force split colors', projection='cyl')
        pobj.plot()

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

        pobj = Plot2Cartopy(self.var1, box, self.lons, self.lats, ax=ax,
                            title='boxfill', projection='cyl')
        pobj.plot()

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

            Plot2Cartopy(vii, isoii, self.lons, self.lats, ax=ax,
                                title=titles[ii], projection='cyl',
                                legend='local', fontsize=5).plot()


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

            Plot2Cartopy(vii, isoii, self.lons, self.lats, ax=ax,
                                title=titles[ii], projection='cyl',
                                legend='local', fontsize=5).plot()

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

            Plot2Cartopy(vii, iso1, self.lons, self.lats, ax=ax,
                                title=titles[ii], projection='cyl',
                                legend='global', fix_aspect=False,
                         fontsize=5).plot()

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_subplots_global_legend.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_update_plot(self):

        proj = ccrs.PlateCarree()
        var_list = [ self.var1, ] * 10
        ref_var = self.var1

        figure = plt.figure(figsize=(12, 10), dpi=100)
        ax = figure.add_subplot(111, projection=proj)
        iso = gplot.Isofill(ref_var, 10, 1, 1, ql=0.005, qr=0.001)

        for ii, varii in enumerate(var_list):

            if ii == 0:

                plotobj = Plot2Cartopy(
                    varii, iso, ax=ax, legend='global', x=self.lons, y=self.lats,
                    title='update_plot',
                    projection=proj)

                plotobj.plot()
            else:
                plotobj.update_plot(varii)

            #----------------- Save plot ------------
            plot_save_name = f'test_cartopy_update_plot_{ii}.png'
            plot_save_name = os.path.join(self.output_dir, plot_save_name)
            os.makedirs(self.output_dir, exist_ok=True)
            print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
            figure.savefig(plot_save_name, dpi=100, transparent=False)

            self.assertTrue(os.path.exists(plot_save_name),
                            msg='{} not created.'.format(plot_save_name))

        plt.close(figure)

        return


    def test_cartopy_quiver(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        q = gplot.Quiver(step=5)

        plotobj = Plot2QuiverCartopy(self.u, self.v, q, x=self.lons,
                                     y=self.lats, ax=ax, title='default quiver',
                                     projection='cyl')

        plotobj.plot()

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_quiver.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_quiver_update_plot(self):

        proj = ccrs.PlateCarree()
        u_list = [ self.u, ] * 10
        v_list = [ self.v, ] * 10

        figure = plt.figure(figsize=(12, 10), dpi=100)
        ax = figure.add_subplot(111, projection=proj)
        q = gplot.Quiver(step=5)

        for ii, (uii, vii) in enumerate(zip(u_list, v_list)):

            uii = uii * (ii+1)
            vii = vii * -1 * (ii+1)

            if ii == 0:

                plotobj = Plot2QuiverCartopy(uii, vii, q, x=self.lons,
                                             y=self.lats, ax=ax,
                                             title='quiver update_plot',
                                             projection=proj)

                plotobj.plot()
            else:
                plotobj.update_plot(uii, vii)

            #----------------- Save plot ------------
            plot_save_name = f'test_cartopy_quiver_update_plot_{ii}.png'
            plot_save_name = os.path.join(self.output_dir, plot_save_name)
            os.makedirs(self.output_dir, exist_ok=True)
            print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
            figure.savefig(plot_save_name, dpi=100, transparent=False)

            self.assertTrue(os.path.exists(plot_save_name),
                            msg='{} not created.'.format(plot_save_name))

        plt.close(figure)

        return


    def test_cartopy_barbs(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111, projection=ccrs.PlateCarree())

        q = gplot.Barbs(step=14, linewidth=0.5, keylength=5)
        uu = self.u * 2
        vv = self.v * 2

        plotobj = Plot2QuiverCartopy(uu, vv, q, x=self.lons,
                                     y=self.lats, ax=ax,
                                     title='Wind barbs',
                                     projection='cyl')

        plotobj.plot()

        #----------------- Save plot ------------
        plot_save_name = 'test_cartopy_barbs.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return


    def test_cartopy_barbs_update_plot(self):

        proj = ccrs.PlateCarree()
        u_list = [ self.u, ] * 10
        v_list = [ self.v, ] * 10

        figure = plt.figure(figsize=(12, 10), dpi=100)
        ax = figure.add_subplot(111, projection=proj)
        q = gplot.Barbs(step=14, linewidth=0.5, keylength=5, standard='cma')

        for ii, (uii, vii) in enumerate(zip(u_list, v_list)):

            uii = uii
            vii = vii * -1 * (ii+1)

            if ii == 0:

                plotobj = Plot2QuiverCartopy(uii, vii, q, x=self.lons,
                                             y=self.lats, ax=ax,
                                             title='barbs update_plot',
                                             projection=proj)

                plotobj.plot()
            else:
                plotobj.update_plot(uii, vii)

            #----------------- Save plot ------------
            plot_save_name = f'test_cartopy_barbs_update_plot_{ii}.png'
            plot_save_name = os.path.join(self.output_dir, plot_save_name)
            os.makedirs(self.output_dir, exist_ok=True)
            print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
            figure.savefig(plot_save_name, dpi=100, transparent=False)

            self.assertTrue(os.path.exists(plot_save_name),
                            msg='{} not created.'.format(plot_save_name))

        plt.close(figure)

        return


    def tearDown(self):
        '''Do clean up after test'''

        try:
            shutil.rmtree(self.output_dir)
            #pass
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

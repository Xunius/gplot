'''Cartopy related utilities

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2020-12-05 10:28:38.
'''

from __future__ import print_function
import numpy as np
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
from gplot.lib.base_utils import Plot2D, Plot2Quiver


class Plot2Cartopy(Plot2D):
    def __init__(self, var, method, xarray, yarray, ax=None,
                 title=None, label_axes=True, axes_grid=False,
                 legend='global', legend_ori='horizontal',
                 clean=False, fontsize=12, projection='cyl', transform=None,
                 fill_color='0.8', fix_aspect=False, isdrawcoastlines=True,
                 isdrawcountries=True, isdrawcontinents=False, isdrawrivers=False,
                 isfillcontinents=False):

        Plot2D.__init__(
            self, var, method, ax=ax, xarray=xarray, yarray=yarray,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            legend=legend, legend_ori=legend_ori, clean=clean,
            fontsize=fontsize, fill_color=fill_color)

        self.projection=projection
        self.transform=transform
        self._projection=self.getProjectionNTransform(projection)
        self._transform=self.getProjectionNTransform(transform)
        self.ax.projection=self._projection

        self.fix_aspect=fix_aspect
        self.isdrawcoastlines=isdrawcoastlines
        self.isdrawcountries=isdrawcountries
        self.isdrawcontinents=isdrawcontinents
        self.isfillcontinents=isfillcontinents
        self.isdrawrivers=isdrawrivers

        try:
            self.var, self.xarray = add_cyclic_point(self.var, self.xarray)
            self.lons, self.lats = np.meshgrid(self.xarray, self.yarray)
        except:
            pass

    def getProjectionNTransform(self, proj):

        if isinstance(proj, ccrs.CRS):
            result=proj
        elif isinstance(proj, str):
            if proj == 'cyl':
                xarray = np.array(self.xarray)
                lon0 = xarray[len(xarray)//2]
                result = ccrs.PlateCarree(central_longitude=lon0)
        elif proj is None:
                result = ccrs.PlateCarree()

        return result

    def plotOthers(self):

        if self.clean:
            return

        # -------------------Draw others-------------------
        if not self.method.method == 'gis':
            self.ax.coastlines()

        return

    # ---------------Draw lat, lon grids---------------
    def plotAxes(self):

        self.plotOthers()

        # --------Turn off lat/lon labels if required--------
        if self.label_axes is False or self.clean:
            self.ax.xaxis.set_ticklabels([])
            self.ax.yaxis.set_ticklabels([])
            return

        if self.label_axes=='all':
            parallels=[1,1,0,0]
            meridians=[0,0,1,1]
        elif isinstance(self.label_axes, (list, tuple)) and len(self.label_axes)==2 and\
                len(self.label_axes[0])==4 and len(self.label_axes[1])==4:
            # TODO: add docstring for this
            parallels,meridians=self.label_axes
        else:
            parallels,meridians=self.getLabelBool(self.geo, self.subidx)

        self.gridliner = self.ax.gridlines(
            draw_labels=True, color=self.fill_color)
        self.gridliner.xlabel_style={'size': self._fontsize}
        self.gridliner.ylabel_style={'size': self._fontsize}

        if meridians[3]==0:
            self.gridliner.bottom_labels=False
        else:
            self.gridliner.bottom_labels=True

        if meridians[2]==0:
            self.gridliner.top_labels=False
        else:
            self.gridliner.top_labels=True

        if parallels[0]==0:
            self.gridliner.left_labels=False
        else:
            self.gridliner.left_labels=True

        if parallels[1]==0:
            self.gridliner.right_labels=False
        else:
            self.gridliner.right_labels=True

        if self.axes_grid:
            #self.ax.grid(True)
            self.gridliner.xlines=True
            self.gridliner.ylines=True
        else:
            self.gridliner.xlines=False
            self.gridliner.ylines=False

        return


class Plot2QuiverCartopy(Plot2Cartopy, Plot2Quiver):

    def __init__(self, u, v, method, xarray, yarray, ax=None,
                 title=None, label_axes=True, axes_grid=False,
                 legend='global', legend_ori='horizontal',
                 units=None,
                 clean=False, fontsize=12, projection='cyl', transform=None,
                 fill_color='0.8', fix_aspect=False, isdrawcoastlines=True,
                 isdrawcountries=True, isdrawcontinents=False, isdrawrivers=False,
                 isfillcontinents=False):


        # basemap obj. When overlaying quiver onto another plot, sometimes
        # the regrid operation will make the data to a slightly different domain,
        # once overlaid, the basemap domain will always be the later plot (quiver).
        # In such cases, pass in a basemap object and use it to generate the
        # plot
        #self.bmap = bmap
        if units is None:
            units=getattr(u, 'units', None)

        Plot2Quiver.__init__(
            self, u, v, method, ax=ax, xarray=xarray, yarray=yarray,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            clean=clean, fontsize=fontsize, units=units, fill_color=fill_color)

        Plot2Cartopy.__init__(
            self, self.var, method, self.xarray, self.yarray, ax=ax,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            legend=None,
            projection=projection, transform=transform,
            clean=clean, fontsize=fontsize, fill_color=fill_color,
            fix_aspect=fix_aspect, isdrawcoastlines=isdrawcoastlines,
            isdrawcountries=isdrawcountries, isdrawcontinents=isdrawcontinents,
            isdrawrivers=isdrawrivers,
            isfillcontinents=isfillcontinents)


    def plot(self):
        self.quiver = self._plot()
        self.plotAxes()
        self.qkey = self.plotkey()
        self.plotTitle()

        return self.quiver

    '''
    def _plot(self):

        # ------------------Create basemap------------------
        self.ax.patch.set_color(self.fill_color)

        # -------------------Plot vectors-------------------
        quiver = self.bmap.quiver(
            self.lons, self.lats, self.var, self.v, scale=self.method.scale,
            width=self.method.linewidth, latlon=True, alpha=self.method.alpha,
            color=self.method.color)

        return quiver
    '''

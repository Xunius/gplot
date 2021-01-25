'''Cartopy related utilities

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2020-12-05 10:28:38.
'''

from __future__ import print_function
import numpy as np
from matplotlib.pyplot import MaxNLocator
import matplotlib
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
from gplot import Plot2D, Plot2Quiver, Quiver, getSlab, regridToReso


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
            self.var, self.lonax = add_cyclic_point(self.var, self.lonax)
            self.lons, self.lats = np.meshgrid(self.lonax, self.latax)
        except:
            pass

    def getProjectionNTransform(self, proj):

        if isinstance(proj, ccrs.CRS):
            result=proj
        elif isinstance(proj, str):
            if proj == 'cyl':
                xarray = np.array(self.lonax)
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

        if meridians[2]==0:
            self.gridliner.top_labels=False

        if parallels[0]==0:
            self.gridliner.left_labels=False

        if parallels[1]==0:
            self.gridliner.right_labels=False

        if self.axes_grid:
            #self.ax.grid(True)
            self.gridliner.xlines=True
            self.gridliner.ylines=True
        else:
            self.gridliner.xlines=False
            self.gridliner.ylines=False

        return


def plot2(var, method, ax=None, legend='global',
          xarray=None, yarray=None,
          title=None, latlon=True, latlongrid=False, fill_color='0.8',
          legend_ori='horizontal', clean=False,
          isbasemap=True,
          fix_aspect=True, verbose=True):

    # ---------------Deal with longitude---------------
    xarray = np.array(xarray)
    lon0 = xarray[len(xarray)//2]
    ax.projection = ccrs.PlateCarree(central_longitude=lon0)

    if np.ndim(var) == 1:
        raise Exception("<var> is 1D")

    if isbasemap and Plot2D.checkBasemap(var, xarray, yarray):
        # try:
        # var=increasingLatitude(var)
        # except:
        # pass
        plotobj = Plot2Cartopy(
            var, method, ax=ax, legend=legend, xarray=xarray, yarray=yarray,
            title=title, latlon=latlon, latlongrid=latlongrid,
            fill_color=fill_color, legend_ori=legend_ori, clean=clean,
            fix_aspect=fix_aspect)
    else:
        plotobj = Plot2D(var, method, ax=ax, legend=legend,
                         xarray=xarray, yarray=yarray,
                         title=title, latlon=latlon, latlongrid=latlongrid,
                         legend_ori=legend_ori, clean=clean)
    cs = plotobj.plot()

    return plotobj

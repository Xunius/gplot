'''Cartopy related utilities

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2020-12-05 10:28:38.
'''

from __future__ import print_function
import numpy as np
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
from gplot.lib.base_utils import Plot2D, Plot2Quiver
from gplot.lib.base_utils import clean_up_artists


class Plot2Cartopy(Plot2D):
    def __init__(self, var, method, x, y, ax=None,
                 title=None, label_axes=True, axes_grid=False,
                 legend='global', legend_ori='horizontal',
                 clean=False, fontsize=12, projection='cyl', transform=None,
                 fill_color='0.8', fix_aspect=False, isdrawcoastlines=True,
                 isdrawcountries=True, isdrawcontinents=False, isdrawrivers=False,
                 isfillcontinents=False):

        Plot2D.__init__(
            self, var, method, ax=ax, x=x, y=y,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            legend=legend, legend_ori=legend_ori, clean=clean,
            fontsize=fontsize, fill_color=fill_color)

        self.projection       = projection
        self.transform        = transform
        self._projection      = self.getProjectionNTransform(projection)
        self._transform       = self.getProjectionNTransform(transform)
        self.ax.projection    = self._projection

        self.fix_aspect       = fix_aspect
        self.isdrawcoastlines = isdrawcoastlines
        self.isdrawcountries  = isdrawcountries
        self.isdrawcontinents = isdrawcontinents
        self.isfillcontinents = isfillcontinents
        self.isdrawrivers     = isdrawrivers

        # save a copy of the old x axis values. This maybe used later in
        # update_plot() to call again the add_cyclic_point() method, re-using
        # this copy of x
        self.old_x = self.x.copy()
        self.add_cyclic_point()

        if not self.fix_aspect:
            self.ax.set_aspect('auto')



    def add_cyclic_point(self, lons=None):

        # allow passing in a new lons arg
        if lons is None:
            lons = self.x

        try:
            self.var, self.x = add_cyclic_point(self.var, lons)
            self.lons, self.lats = np.meshgrid(self.x, self.y)
        except:
            pass

        return

    def getProjectionNTransform(self, proj):

        if isinstance(proj, ccrs.CRS):
            result=proj
        elif isinstance(proj, str):
            if proj == 'cyl':
                x = np.array(self.x)
                lon0 = x[len(x)//2]
                result = ccrs.PlateCarree(central_longitude=lon0)
        elif proj is None:
                result = ccrs.PlateCarree()

        return result


    def update_plot(self, var):
        '''Update an existing plot by re-doing only data plotting, skipping
        axes, colorbar etc.

        Args:
            var (ndarray): new data to plot. Needs to have compatible size
                as self.x, self.y.

        NOTE that this function assumes the new data <var> is compatible in shape
        and value range as the initial data been plotted earlier. This is
        helpful when creating a sequence of time slices of the a variable, e.g.
        SST, with the same resolution as domain size, and using the plotting
        method (e.g isofill, and therefore same colorbar).
        Skipping the init steps and plotting of the axes, colorbar etc. can
        help saving some time.
        '''

        if not hasattr(self, 'cs'):
            return

        self.var = self.getSlab(var)
        self.add_cyclic_point(self.old_x)
        clean_up_artists(self.ax, [self.cs])
        self.cs = self._plot()

        return

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
            parallels,meridians=self.getLabelBool()

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


    def _plotIsofill(self):
        '''Core plotting function, isofill/contourf

        Use this overloading because the transform_first kwarg is unique to
        cartopy's axes.
        '''

        extend = self.method.extend
        transform_first = self._transform is not None

        cs = self.ax.contourf(
            self.lons, self.lats, self.var, self.method.levels,
            cmap=self.method.cmap, extend=extend, norm=self.method.norm,
                transform_first=transform_first,
            transform=self._transform)

        if self.method.stroke:
            nl = len(self.method.levels)
            css = self.ax.contour(
                self.lons, self.lats, self.var, self.method.levels,
                colors=[self.method.stroke_color, ]*nl,
                linestyles=[self.method.stroke_linestyle, ]*nl,
                linewidths=[self.method.stroke_lw, ]*nl,
                transform=self._transform,
                transform_first=transform_first,
            )
            self.css = css

        return cs



    def _plotIsoline(self):
        '''Core plotting function, isoline/contour

        Use this overloading because the transform_first kwarg is unique to
        cartopy's axes.
        '''

        extend = self.method.extend
        transform_first = self._transform is not None

        if self.method.color is not None:
            colors = [self.method.color]*len(self.method.levels)
            cmap = None
        else:
            if self.method.black:
                colors = ['k']*len(self.method.levels)
                cmap = None
            else:
                colors = None
                cmap = None

        cs = self.ax.contour(
            self.lons, self.lats, self.var, self.method.levels,
            colors=colors,
            cmap=cmap, extend=extend,
            linewidths=self.method.linewidth,
            alpha=self.method.alpha,
            transform=self._transform,
            transform_first=transform_first)

        # -----------------Set line styles-----------------
        if self.method.dash_negative:
            for ii in range(len(cs.collections)):
                cii = cs.collections[ii]
                lii = cs.levels[ii]
                if lii < 0:
                    cii.set_linestyle('dashed')
                else:
                    cii.set_linestyle('solid')

        # ----------------Thicken some lines----------------
        if self.method.bold_lines is not None:
            multi = 2.0
            idx_bold = []
            for bii in self.method.bold_lines:
                idxii = np.where(np.array(cs.levels) == bii)[0]
                if len(idxii) > 0:
                    idx_bold.append(int(idxii))

            for bii in idx_bold:
                cs.collections[bii].set_linewidth(
                    self.method.linewidth * multi)

        #-------------------Plot labels-------------------
        if self.method.label:
            self.plotContourLabels(cs)

        return cs

class Plot2QuiverCartopy(Plot2Cartopy, Plot2Quiver):

    def __init__(self, u, v, method, x, y, ax=None,
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
            self, u, v, method, ax=ax, x=x, y=y,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            clean=clean, fontsize=fontsize, units=units, fill_color=fill_color)

        x_old = self.x.copy()

        Plot2Cartopy.__init__(
            self, self.var, method, self.x, self.y, ax=ax,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            legend=None,
            projection=projection, transform=transform,
            clean=clean, fontsize=fontsize, fill_color=fill_color,
            fix_aspect=fix_aspect, isdrawcoastlines=isdrawcoastlines,
            isdrawcountries=isdrawcountries, isdrawcontinents=isdrawcontinents,
            isdrawrivers=isdrawrivers,
            isfillcontinents=isfillcontinents)

        self.v, _ = add_cyclic_point(self.v, x_old)

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

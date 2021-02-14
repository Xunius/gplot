'''Basemap related utilities

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2020-12-05 10:28:38.
'''

from __future__ import print_function
import warnings
import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt
from matplotlib.pyplot import MaxNLocator
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import addcyclic
from gplot.lib.gplot import Plot2D, Plot2Quiver


class Plot2Basemap(Plot2D):
    def __init__(self, var, method,
                 xarray, yarray,
                 ax=None,
                 title=None,
                 label_axes=True,
                 axes_grid=False,
                 legend='global',
                 legend_ori='horizontal',
                 clean=False,
                 fontsize=12,
                 projection='cyl',
                 fill_color='0.8',
                 fix_aspect=False,
                 isdrawcoastlines=True,
                 isdrawcountries=True,
                 isdrawcontinents=False,
                 isdrawrivers=False,
                 bmap=None,
                 isfillcontinents=False):

        Plot2D.__init__(
            self, var, method, ax=ax, xarray=xarray, yarray=yarray,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            legend=legend, legend_ori=legend_ori, clean=clean,
            fontsize=fontsize, fill_color=fill_color)

        self.projection = projection
        self.fix_aspect = fix_aspect
        self.isdrawcoastlines = isdrawcoastlines
        self.isdrawcountries = isdrawcountries
        self.isdrawcontinents = isdrawcontinents
        self.isfillcontinents = isfillcontinents
        self.isdrawrivers = isdrawrivers
        self.bmap=bmap

    def createBmap(self):

        # ------------------Create basemap------------------
        if self.method.method == 'gis':
            self.projection = 'cyl'

        if self.projection in ['cyl', 'merc', 'cea']:
            bmap = Basemap(projection=self.projection,
                           llcrnrlat=self.yarray[0], llcrnrlon=self.xarray[0],
                           urcrnrlat=self.yarray[-1], urcrnrlon=self.xarray[-1],
                           ax=self.ax, fix_aspect=self.fix_aspect)

        elif self.projection in ['npaeqd', 'nplaea', 'npstere']:

            self.var, self.xarray = addcyclic(self.var, self.xarray)
            self.lons, self.lats = np.meshgrid(self.xarray, self.yarray)
            lat_0 = np.min(self.yarray)-5
            lon_0 = 180.

            bmap = Basemap(projection=self.projection,
                           boundinglat=lat_0, lon_0=lon_0,
                           ax=self.ax, fix_aspect=self.fix_aspect)

        elif self.projection in ['spaeqd', 'splaea', 'spstere']:

            self.var, self.xarray = addcyclic(self.var, self.xarray)
            self.lons, self.lats = np.meshgrid(self.xarray, self.yarray)
            lat_0 = np.max(self.yarray)+5
            lon_0 = 180.
            bmap = Basemap(projection=self.projection,
                           boundinglat=lat_0, lon_0=lon_0,
                           ax=self.ax, fix_aspect=self.fix_aspect)

        self.bmap = bmap

    def _plot(self):

        if self.bmap is None:
            self.createBmap()

        # make masked value grey, otherwise they will be white
        self.ax.patch.set_color(self.fill_color)

        # -------------Plot according to method-------------
        # -------------------Contour fill/line-------------------
        if self.method.method == 'isofill':
            cs = self._plotIsofill()

        elif self.method.method == 'isoline':
            cs = self._plotIsoline()

        # ---------------------Boxfill---------------------
        elif self.method.method == 'boxfill':
            cs = self._plotBoxfill()

        # -------------------Pcolor fill-------------------
        elif self.method.method == 'pcolor':
            cs = self._plotPcolor()

        # ------------------Hatch contourf------------------
        elif self.method.method == 'hatch':
            cs = self._plotHatch()

        elif self.method.method == 'gis':
            cs = self._plotGIS()

        elif self.method.method == 'shading':
            cs = self._plotShading()

        return cs

    def _plotIsofill(self):

        extend = Plot2D.getExtend(self.method)
        cs = self.bmap.contourf(
            self.lons, self.lats, self.var, self.method.levels, latlon=True,
            cmap=self.method.cmap, ax=self.ax, extend=extend,
            norm=self.method.norm)

        if self.method.stroke:
            nl = len(self.method.levels)
            css = self.bmap.contour(
                self.lons, self.lats, self.var, self.method.levels,
                latlon=True,
                ax=self.ax,
                colors=[self.method.stroke_color, ]*nl,
                linestyles=[self.method.stroke_linestyle, ]*nl,
                linewidths=self.method.stroke_lw)
            self.css = css

        return cs

    def _plotIsoline(self):

        extend = Plot2D.getExtend(self.method)

        if self.method.color is not None:
            colors = [self.method.color]*len(self.method.levels)
            cs = self.bmap.contour(
                self.lons, self.lats, self.var, self.method.levels,
                latlon=True, colors=colors, ax=self.ax, extend=extend,
                linewidths=self.method.linewidth, alpha=self.method.alpha)
        else:
            if self.method.black:
                colors = ['k']*len(self.method.levels)
                cs = self.bmap.contour(
                    self.lons, self.lats, self.var, self.method.levels,
                    latlon=True, colors=colors, ax=self.ax, extend=extend,
                    linewidths=self.method.linewidth, alpha=self.method.alpha)
            else:
                cs = self.bmap.contour(
                    self.lons, self.lats, self.var, self.method.levels,
                    latlon=True, cmap=self.method.cmap, ax=self.ax,
                    extend=extend, linewidths=self.method.linewidth,
                    alpha=self.method.alpha)

        # -----------------Set line styles-----------------
        # for some reason it's not giving me dashed line for negatives.
        # have to set myself
        for ii in range(len(cs.collections)):
            cii = cs.collections[ii]
            lii = cs.levels[ii]
            if lii < 0:
                if self.method.dash_negative:
                    cii.set_linestyle('dashed')
                else:
                    cii.set_linestyle('solid')

        # For some reason the linewidth keyword in contour doesn't
        # work, has to set again.
        for ii in range(len(cs.collections)):
            cs.collections[ii].set_linewidth(self.method.linewidth)

        if self.method.bold_lines is not None:
            multi = 2.0
            idx_bold = []
            for bii in self.method.bold_lines:
                # idxii=np.where(np.array(self.method.levels)==bii)[0]
                idxii = np.where(np.array(cs.levels) == bii)[0]
                if len(idxii) > 0:
                    idx_bold.append(int(idxii))

            for bii in idx_bold:
                cs.collections[bii].set_linewidth(self.method.linewidth*multi)

        return cs

    def _plotBoxfill(self):

        cs = self.bmap.imshow(
            self.var, cmap=self.method.cmap, ax=self.ax, vmin=self.method.vmin,
            vmax=self.method.vmax, interpolation='nearest')
        return cs

    def _plotPcolor(self):

        cs = self.bmap.pcolormesh(
            self.lons, self.lats, self.var, latlon=True, cmap=self.method.cmap,
            ax=self.ax, vmin=self.method.levels[0],
            vmax=self.method.levels[-1])

        return cs

    def _plotHatch(self):
        # Skip if none == 1
        if np.all(self.var == 0):
            nlevel = 1
        else:
            nlevel = 3
        cs = self.bmap.contourf(
            self.lons, self.lats, self.var, nlevel, latlon=True, colors='none',
            ax=self.ax, hatches=[None, self.method.hatch],
            alpha=0.)
        return cs

    def _plotShading(self):

        pvar = np.where(self.var == 1, 1, np.nan)
        cs = self.bmap.contourf(
            self.lons,
            self.lats,
            pvar, 1, latlon=True, ax=self.ax,
            cmap=self.method.cmap,
            alpha=self.method.alpha)

        return cs

    def _plotGIS(self):

        cs = self.bmap.arcgisimage(
            service='ESRI_Imagery_World_2D', xpixels=self.method.xpixels,
            dpi=self.method.dpi, verbose=self.method.verbose)

        return cs

    def plotOthers(self):

        if self.clean:
            return

        # self.bmap.drawmapboundary(color='k',linewidth=1.0,
            # fill_color=self.fill_color)
        if self.isdrawcoastlines:
            self.bmap.drawcoastlines(
                linewidth=0.5, linestyle='solid', color='k', antialiased=True)
        if self.isdrawcountries:
            self.bmap.drawcountries(
                linewidth=0.5, linestyle='solid', color='k', antialiased=True)
        if self.isfillcontinents:
            self.bmap.fillcontinents(color='w', lake_color=None, alpha=0.2)
        if self.isdrawrivers:
            self.bmap.drawrivers(linewidth=0.5, linestyle='solid', color='b',
                                 antialiased=True)

        return

    # ---------------Draw lat, lon grids---------------

    def plotAxes(self):

        if self.axes_grid:
            self.ax.grid(True)

        if self.clean:
            return

        loclatlon = MaxNLocator(nbins='auto', steps=[
                                1, 2, 2.5, 3, 4, 5, 6, 7, 8, 8.5, 9, 10])
        lat_labels = loclatlon.tick_values(
            np.min(self.yarray), np.max(self.yarray))
        lon_labels = loclatlon.tick_values(
            np.min(self.xarray), np.max(self.xarray))
        idx = np.where((lat_labels >= self.yarray[0]) & (
            lat_labels <= self.yarray[-1]))
        lat_labels = np.array(lat_labels)[idx]
        idx = np.where((lon_labels >= self.xarray[0]) & (
            lon_labels <= self.xarray[-1]))
        lon_labels = np.array(lon_labels)[idx]

        # -----------------Set axes labels-----------------
        if self.label_axes is False or self.clean:
            parallels = [0, 0, 0, 0]
            meridians = [0, 0, 0, 0]
        elif self.label_axes == 'all':
            parallels = [1, 1, 0, 0]
            meridians = [0, 0, 1, 1]
        elif isinstance(self.label_axes, (list, tuple)) and len(self.label_axes) == 4:
            parallels = [0,]*4
            meridians = [0,]*4
            for ii in [0, 1]:
                if self.label_axes[ii]:
                    parallels[ii] = 1
            for ii in [2, 3]:
                if self.label_axes[ii]:
                    meridians[ii] = 1
        else:
            parallels, meridians = self.getLabelBool(self.geo, self.subidx)

        # -----------------format axes/lables/ticks-----------------
        lon_labels_proj, _ = self.bmap(lon_labels, np.zeros(len(lon_labels)))
        _, lat_labels_proj = self.bmap(np.zeros(len(lat_labels)), lat_labels)
        self.ax.set_yticks(lat_labels_proj)
        self.ax.set_xticks(lon_labels_proj)

        lon_default_formatter = self.ax.xaxis.get_major_formatter()
        lon_ticklabels=lon_default_formatter.format_ticks(lon_labels_proj)

        lat_default_formatter = self.ax.yaxis.get_major_formatter()
        lat_ticklabels=lat_default_formatter.format_ticks(lat_labels_proj)

        @ticker.FuncFormatter
        def newformatterlon(x, pos):
            return '' if pos is None else u'%s\u00B0' %(lon_ticklabels[pos])

        @ticker.FuncFormatter
        def newformatterlat(x, pos):
            # latex \circ seems to give a smaller circle than the unicode
            #return '' if pos is None else r'%s$^{\circ}$' %(lat_ticklabels[pos])
            return '' if pos is None else u'%s\u00B0' %(lat_ticklabels[pos])

        self.ax.xaxis.set_major_formatter(newformatterlon)
        self.ax.yaxis.set_major_formatter(newformatterlat)

        if meridians[3] == 1:
            self.ax.set_xticks(lon_labels)
            labelbottom = True
        else:
            labelbottom = False

        if meridians[2] == 1:
            self.ax.set_xticks(lon_labels)
            labeltop = True
        else:
            labeltop = False

        if parallels[0] == 1:
            self.ax.set_yticks(lat_labels)
            labelleft = True
        else:
            labelleft = False

        if parallels[1] == 1:
            self.ax.set_yticks(lat_labels)
            labelright = True
        else:
            labelright = False

        self.ax.tick_params(axis='both', which='major',
                            labelsize=self._fontsize,
                            labelleft=labelleft, labelright=labelright,
                            labeltop=labeltop, labelbottom=labelbottom,
                            left=labelleft, right=labelright,
                            top=labeltop, bottom=labelbottom)

        # -------Label parallels in polar projections-------
        if self.projection in ['npaeqd', 'nplaea', 'npstere', 'spaeqd',
                               'splaea', 'spstere']:
            for ll in lat_labels:
                xll, yll = self.bmap(180., ll)
                self.ax.text(xll, yll, u'%+d\N{DEGREE SIGN}' % ll,
                             fontsize=max(4, int(self._fontsize*0.7)),
                             horizontalalignment='center',
                             verticalalignment='center')

        # NOTE: there is some really weird issue with the bmap.drawmapboundary()
        # (see plotOthers()). The order of calling this func gives different
        # results:
        # calling plotOthers() (therefore drawmapboundary()) before plotting
        # the axes (in plotAxes()) makes the top and left figure frame gone.
        # Setting zorder=-1 in drawmapboundary() won't help. Not giving
        # zorder<=0 will fill the entire figure with fill_color.
        # See https://github.com/matplotlib/basemap/issues/474
        # An alternative fix is to not call drawmapboundary() but use
        # self.ax.set_facecolor(self.fill_color)

        self.plotOthers()

        return


class Plot2QuiverBasemap(Plot2Basemap, Plot2Quiver):

    def __init__(
            self, u, v, method, xarray, yarray, ax=None,
            title=None, label_axes=True, axes_grid=False,
            clean=False, fontsize=12, units=None, fill_color='w', curve=False,
            bmap=None, projection='cyl',
            fix_aspect=False, isdrawcoastlines=True,
            isdrawcountries=True, isdrawcontinents=False, isdrawrivers=False,
            isfillcontinents=False):

        # basemap obj. When overlaying quiver onto another plot, sometimes
        # the regrid operation will make the data to a slightly different domain,
        # once overlaid, the basemap domain will always be the later plot (quiver).
        # In such cases, pass in a basemap object and use it to generate the
        # plot
        self.bmap = bmap
        if units is None:
            units=getattr(u, 'units', None)

        Plot2Quiver.__init__(
            self, u, v, method, ax=ax, xarray=xarray, yarray=yarray,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            clean=clean, fontsize=fontsize, units=units, fill_color=fill_color,
            curve=curve)

        Plot2Basemap.__init__(
            self, self.var, method, self.xarray, self.yarray, ax=ax, title=title,
            label_axes=label_axes, axes_grid=axes_grid, legend=None,
            projection=projection, clean=clean, fontsize=fontsize,
            fill_color=fill_color,
            fix_aspect=fix_aspect, isdrawcoastlines=isdrawcoastlines,
            isdrawcountries=isdrawcountries, isdrawcontinents=isdrawcontinents,
            isdrawrivers=isdrawrivers, isfillcontinents=isfillcontinents)

    def plot(self):
        self.quiver = self._plot()
        self.plotAxes()  # this is Plot2Basemap's
        self.qkey = self.plotkey()
        self.plotTitle()
        # Inside plotAxes() the drawmeridians() uses a grey color as fill.
        # this is to fill in a white:
        #self.ax.patch.set_color('w')

        return self.quiver

    def _plot(self):

        # ------------------Create basemap------------------
        if self.bmap is None:
            self.createBmap()

        self.ax.patch.set_color(self.fill_color)

        if self.curve:
            # modded from: https://stackoverflow.com/a/65607512/2005415
            warnings.warn('#<gplot warning>: The curved quiver functionality is experimental.')
            norm = np.sqrt(self.var**2 + self.v**2)
            norm_flat = norm.flatten()

            start_points = np.array([self.lons.flatten(),self.lats.flatten()]).T
            scale = .2/np.max(norm)

            for i in range(start_points.shape[0]):
                self.bmap.streamplot(self.lons, self.lats, self.var, self.v,
                        color=self.method.color,
                        start_points=np.array([start_points[i,:]]),
                        minlength=.25*norm_flat[i]*scale,
                        maxlength=1.0*norm_flat[i]*scale,
                        integration_direction='backward',
                        density=10, arrowsize=0.0)

        # -------------------Plot vectors-------------------
        quiver = self.bmap.quiver(
            self.lons, self.lats, self.var, self.v, scale=self.method.scale,
            width=self.method.linewidth, latlon=True, alpha=self.method.alpha,
            color=self.method.color,
            headwidth=4)

        return quiver


def blueMarble(
        lat1, lon1, lat2, lon2, fig=None, projection='merc', verbose=True):
    '''Plot bluemarble plot as background.

    <lat1>,<lon1>: float, low-left corner. Longitude range 0-360
    <lat2>,<lon2>: float, upper-right corner.
    <fig>: plt figure. If None, create a new.

    NOTE: due to a bug in basemap, if the plot range is crossing the
    dateline, need to plot 2 separate plots joining at the dateline.

    Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
    Update time: 2017-06-29 12:36:36.
    '''

    from mpl_toolkits.basemap import Basemap

    if fig is None:
        fig = plt.figure()

    if lat1 > lat2:
        lat1, lat2 = lat2, lat1
    if lon1 > lon2:
        lon1, lon2 = lon2, lon1

    if lon1 < 0:
        lon1 += 360.
    if lon2 < 0:
        lon2 += 360.

    # ------------Not crossing the dateline------------
    if (lon1-180.)*(lon2-180.) >= 0:
        if lon1 < 180 and lon2 == 180:
            lon2 = 179.96
        elif lon1 >= 180 and lon2 > 180:
            lon1 = lon1-179.96 if lon1 == 180 else lon1-360.
            lon2 -= 360.

        lats1 = [lat1, lat2]
        lons1 = [lon1, lon2]

        ax1 = fig.add_subplot(111)
        bmap = Basemap(projection='merc',
                       llcrnrlat=lats1[0], llcrnrlon=lons1[0],
                       urcrnrlat=lats1[1], urcrnrlon=lons1[1],
                       lon_0=(lons1[0]+lons1[1])/2.,
                       ax=ax1)

        bmap.bluemarble(ax=ax1)

    else:
        # --------------Crossing the dateline--------------
        proportion1 = (179.96-lon1)/(lon2-lon1)

        # -------------------Western part-------------------
        lats1 = [lat1, lat2]
        lons1 = [lon1, 179.96]

        ax1 = fig.add_subplot(121)

        bmap1 = Basemap(projection='merc',
                        llcrnrlat=lats1[0], llcrnrlon=lons1[0],
                        urcrnrlat=lats1[1], urcrnrlon=lons1[1],
                        lon_0=(lons1[0]+lons1[1])/2.,
                        ax=ax1)

        bmap1.bluemarble(ax=ax1)

        ax1.set_position([0, 0, proportion1, 1])
        ax1.set_aspect('auto')
        ax1.set_adjustable('datalim')
        ax1.axis('off')

        # -------------------Eastern part-------------------
        lats2 = [lat1, lat2]
        lons2 = [-179.96, lon2-360.]

        ax2 = fig.add_subplot(122)

        bmap2 = Basemap(projection='merc',
                        llcrnrlat=lats2[0], llcrnrlon=lons2[0],
                        urcrnrlat=lats2[1], urcrnrlon=lons2[1],
                        lon_0=(lons2[0]+lons2[1])/2.,
                        ax=ax2)

        bmap2.bluemarble(ax=ax2)

        ax2.set_position([proportion1, 0, 1-proportion1, 1])
        ax2.set_aspect('auto')
        ax2.set_adjustable('datalim')
        ax2.axis('off')

    return fig

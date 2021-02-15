'''Basemap 2D plotting functions and classes.

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2021-02-14 13:42:31.
'''

from __future__ import print_function
import warnings
import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt
from matplotlib.pyplot import MaxNLocator
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import addcyclic
from gplot.lib.base_utils import Plot2D, Plot2Quiver, rcParams


class Plot2Basemap(Plot2D):
    def __init__(self, var, method, xarray, yarray, ax=None, title=None,
                 label_axes=True, axes_grid=False, legend=None, legend_ori=None,
                 clean=False, fontsize=None, projection=None, fill_color=None,
                 fix_aspect=False, isdrawcoastlines=True,
                 isdrawcountries=True, isdrawcontinents=False,
                 isdrawrivers=False, isfillcontinents=False, bmap=None):
        '''2D geographical plotting class, using basemap

        Args:
            var (ndarray): input data to plot. Determines what to plot.
                Mush have dimensions >= 2.
                For data with rank>2, take the slab from the last 2 dimensions.
            method (PlotMethod): plotting method. Determines how to plot.
                Could be Isofill, Isoline, Boxfill, Quiver, Shading, Hatch, GIS.
            xarray (1darray or None): array to use as the x-coordinates. If None,
                use the indices of the last dimension: np.arange(slab.shape[-1]).
            yarray (1darray or None): array to use as the y-coordinates. If None,
                use the indices of the 2nd last dimension: np.arange(slab.shape[-2]).
        Keyword Args:
            ax (matplotlib axis or None): axis obj. Determines where to plot.
                If None, create a new.
            title (str or None): text as the figure title if <ax> is the
                single plot in the figure. If None, automatically
                get an alphabetic subtitle if <ax> is a subplot, e.g. '(a)'
                for the 1st subplot, '(d)' for the 4th one. If str and <ax>
                is a subplot, prepend <title> with the alphabetic index.
                One can force overriding the alphabetic index by giving a title
                str in the format of '(x) xxxx', e.g. '(p) subplot-p'.
            label_axes (bool or 'all' or ((left_y, right_y, top_y, top_y),
                (left_x, right_x, top_x, top_x)) or None): controls axis ticks and
                ticklabels. If True, don't exert any inference other than
                changing the ticklabel fontsize, and let matplotlib put the
                ticks and ticklabels (i.e. default only left and bottom axes).
                If False, turn off all ticks and ticklabels.
                If 'all', plot ticks and ticks labels on all 4 sides.
                If ((left_y, right_y, top_y, top_y), (left_x, right_x, top_x, top_x)),
                specify which side to plot ticks/ticklabels. Each swith is a
                bool or binary. If None, will set the ticks/ticklabels such
                that the interior subplots have no ticks/ticklabels, edge
                subplots have ticks/ticklabels on the outer edges, i.e. similar
                as the 'sharex', 'sharey' options. Location of the subplot
                is determined from return of `ax.get_geometry()`.
            axes_grid (bool): whether to add axis grid lines.
            legend (str or None): controls whether to share colorbar or not.
                A colorbar is only plotted for Isofill/Isoline plots.
                If None, don't put colorbar. If 'local', <ax> has its own
                colorbar. If 'global', all subplots in the figure share a
                single colorbar, which is created by the 1st subplot in the
                figure, which is determined from the return of `ax.get_geometry()`.
            legend_ori (str): orientation of colorbar. 'horizontal' or 'vertical'.
            clean (bool): if False, don't plot axis ticks/ticklabels, colorbar,
                axis grid lines or title.
            fontsize (int): font size for ticklabels, title, axis labels, colorbar
                ticklabels.
            projection (str): the map projection.
            fill_color (str or color tuple): color to use as background color.
                If data have missings, they will be shown as this color.
                It is better to use a grey than while to better distinguish missings.
            fix_aspect (bool): passed to the constructor of basemap: `Basemap(xxx,
                fix_aspect=fix_aspect)`.
            isdrawcoastlines (bool): whether to draw continent outlines or not.
            isdrawcountries (bool): whether to draw contry boundaries or not.
            isdrawrivers (bool): whether to draw rivers or not.
            isfillcontinents (bool): whether to fill continents or not.
            bmap (basemap obj or None): reuse an existing basemap obj if not None.
        '''

        fill_color = fill_color or rcParams['fill_color']
        title = title or rcParams['title']
        label_axes = label_axes or rcParams['label_axes']
        axes_grid = axes_grid or rcParams['axes_grid']
        fontsize = fontsize or rcParams['fontsize']
        clean = clean or rcParams['clean']
        legend = legend or rcParams['legend']
        legend_ori = legend_ori or rcParams['legend_ori']

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
        self.bmap = bmap

    def createBmap(self):
        '''Create basemap based on data domain
        '''

        # ------------------Create basemap------------------
        if self.method.method == 'gis':
            self.projection = 'cyl'

        if self.projection in ['cyl', 'merc', 'cea']:
            bmap = Basemap(
                projection=self.projection, llcrnrlat=self.yarray[0],
                llcrnrlon=self.xarray[0],
                urcrnrlat=self.yarray[-1],
                urcrnrlon=self.xarray[-1],
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
        '''Core plotting function

        Create the plot depending on method: isofill, isoline, boxfill, pcolor,
        hatch, or shading.

        Returns:
            self.cs (mappable): the mappable obj, e.g. return value from contour()
                or contourf().
        '''

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
        '''Core plotting function, isofill/contourf'''

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
        '''Core plotting function, isoline/contour'''

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
        for ii in range(len(cs.collections)):
            cii = cs.collections[ii]
            lii = cs.levels[ii]
            if lii < 0:
                if self.method.dash_negative:
                    cii.set_linestyle('dashed')
                else:
                    cii.set_linestyle('solid')

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
        '''Core plotting function, boxfill/imshow'''

        cs = self.bmap.imshow(
            self.var, cmap=self.method.cmap, ax=self.ax, vmin=self.method.vmin,
            vmax=self.method.vmax, interpolation='nearest')
        return cs

    def _plotPcolor(self):
        '''Core plotting function, pcolormesh'''

        cs = self.bmap.pcolormesh(
            self.lons, self.lats, self.var, latlon=True, cmap=self.method.cmap,
            ax=self.ax, vmin=self.method.levels[0],
            vmax=self.method.levels[-1])

        return cs

    def _plotHatch(self):
        '''Core plotting function, pattern hatching'''

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
        '''Core plotting function, color shading'''

        pvar = np.where(self.var == 1, 1, np.nan)
        cs = self.bmap.contourf(
            self.lons,
            self.lats,
            pvar, 1, latlon=True, ax=self.ax,
            cmap=self.method.cmap,
            alpha=self.method.alpha)

        return cs

    def _plotGIS(self):
        '''Core plotting function, ARC GIS image'''

        cs = self.bmap.arcgisimage(
            service='ESRI_Imagery_World_2D', xpixels=self.method.xpixels,
            dpi=self.method.dpi, verbose=self.method.verbose)

        return cs

    def plotOthers(self):
        '''Plot other map information

        Plot continents, contries, rivers if needed.
        '''

        if self.clean:
            return

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
        '''Plot longitude/latitude ticks and ticklabels

        Overwrites parent classes method
        '''

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
        parallels, meridians = self.getLabelBool()

        # -----------------format axes/lables/ticks-----------------
        lon_labels_proj, _ = self.bmap(lon_labels, np.zeros(len(lon_labels)))
        _, lat_labels_proj = self.bmap(np.zeros(len(lat_labels)), lat_labels)
        self.ax.set_yticks(lat_labels_proj)
        self.ax.set_xticks(lon_labels_proj)

        #ter = self.ax.xaxis.get_major_formatter()
        lon_default_formatter = ticker.ScalarFormatter()
        self.ax.xaxis.set_major_formatter(lon_default_formatter)
        lon_ticklabels = lon_default_formatter.format_ticks(lon_labels_proj)

        #lat_default_formatter = self.ax.yaxis.get_major_formatter()
        lat_default_formatter = ticker.ScalarFormatter()
        self.ax.yaxis.set_major_formatter(lat_default_formatter)
        lat_ticklabels = lat_default_formatter.format_ticks(lat_labels_proj)

        @ticker.FuncFormatter
        def newformatterlon(x, pos):
            return '' if pos is None else u'%s\u00B0' % (lon_ticklabels[pos])

        @ticker.FuncFormatter
        def newformatterlat(x, pos):
            # latex \circ seems to give a smaller circle than the unicode
            # return '' if pos is None else r'%s$^{\circ}$' %(lat_ticklabels[pos])
            return '' if pos is None else u'%s\u00B0' % (lat_ticklabels[pos])

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

        #------------------Set grid lines------------------
        if self.label_axes is False or self.clean:
            #linewidth=0
            zorder=-2
        else:
            #linewidth=0.5
            zorder=-2

        #-----------------Draw axes/lables/ticks-----------------
        '''
        self.ax.set_yticks(lat_labels_proj)
        self.ax.set_xticks(lon_labels_proj)
        self.ax.tick_params(axis='both',which='major',labelsize=self.font_size)
        self.ax.xaxis.set_ticklabels([])
        self.ax.yaxis.set_ticklabels([])
        self.ax.xaxis.set_ticks_position('both')
        self.ax.yaxis.set_ticks_position('both')
        '''

        '''
        self.bmap.drawparallels(lat_labels,labels=parallels,linewidth=linewidth,\
                labelstyle='+/-',fontsize=self.font_size,
                xoffset=0.010*abs(self.bmap.xmax-self.bmap.xmin))
        self.bmap.drawmeridians(lon_labels,labels=meridians,linewidth=linewidth,\
                labelstyle='+/-',fontsize=self.font_size,
                yoffset=0.012*abs(self.bmap.ymax-self.bmap.ymin))
        '''

        # NOTE: this is to fix the flawed PDF save issue.
        # for some reason when using linewidth=0 in drawmeridians() or
        # drawparallels(), the saved PDF won't display properly in some PDF
        # viewers (e.g. Xreader or Adobe Reader).
        '''
        self.bmap.drawparallels(lat_labels,labels=[0,0,0,0],
                labelstyle='+/-',fontsize=self._fontsize,
                color=self.fill_color, # to hide the lines where mask is True
                zorder=zorder,
                xoffset=0.010*abs(self.bmap.xmax-self.bmap.xmin))
        self.bmap.drawmeridians(lon_labels,labels=[0,0,0,0],
                labelstyle='+/-',fontsize=self._fontsize,
                zorder=zorder,
                color=self.fill_color,
                yoffset=0.012*abs(self.bmap.ymax-self.bmap.ymin))
        '''

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
            clean=False, fontsize=None,
            projection=None,
            units=None, fill_color='w', curve=False,
            fix_aspect=False, isdrawcoastlines=True,
            isdrawcountries=True, isdrawcontinents=False, isdrawrivers=False,
            isfillcontinents=False, bmap=None):
        '''2D geographical quiver plotting class, using basemap

        Args:
            u,v (ndarray): x- and y-component of velocity to plot.
                Mush have dimensions >= 2. For data with rank>2, take the slab
                from the last 2 dimensions.
            method (Quiver obj): quiver plotting method. Determines how to plot
                the quivers.
            xarray (1darray or None): array to use as the x-coordinates. If None,
                use the indices of the last dimension: np.arange(slab.shape[-1]).
            yarray (1darray or None): array to use as the y-coordinates. If None,
                use the indices of the 2nd last dimension: np.arange(slab.shape[-2]).
        Keyword Args:
            ax (matplotlib axis or None): axis obj. Determines where to plot.
                If None, create a new.
            title (str or None): text as the figure title if <ax> is the
                single plot in the figure. If None, automatically
                get an alphabetic subtitle if <ax> is a subplot, e.g. '(a)'
                for the 1st subplot, '(d)' for the 4th one. If str and <ax>
                is a subplot, prepend <title> with the alphabetic index.
                One can force overriding the alphabetic index by giving a title
                str in the format of '(x) xxxx', e.g. '(p) subplot-p'.
            label_axes (bool or 'all' or ((left_y, right_y, top_y, top_y),
                (left_x, right_x, top_x, top_x)) or None): controls axis ticks and
                ticklabels. If True, don't exert any inference other than
                changing the ticklabel fontsize, and let matplotlib put the
                ticks and ticklabels (i.e. default only left and bottom axes).
                If False, turn off all ticks and ticklabels.
                If 'all', plot ticks and ticks labels on all 4 sides.
                If ((left_y, right_y, top_y, top_y), (left_x, right_x, top_x, top_x)),
                specify which side to plot ticks/ticklabels. Each swith is a
                bool or binary. If None, will set the ticks/ticklabels such
                that the interior subplots have no ticks/ticklabels, edge
                subplots have ticks/ticklabels on the outer edges, i.e. similar
                as the 'sharex', 'sharey' options. Location of the subplot
                is determined from return of `ax.get_geometry()`.
            axes_grid (bool): whether to add axis grid lines.
            clean (bool): if False, don't plot axis ticks/ticklabels, colorbar,
                axis grid lines or title.
            fontsize (int): font size for ticklabels, title, axis labels, colorbar
                ticklabels.
            projection (str): the map projection.
            units (str or None): unit of <u> and <v>. Will be plotted next to
                the reference vector.
            fill_color (str or color tuple): color to use as background color.
                If data have missings, they will be shown as this color.
                It is better to use a grey than while to better distinguish missings.
            curve (bool): whether to plot quivers as curved vectors. Experimental.
            fix_aspect (bool): passed to the constructor of basemap: `Basemap(xxx,
                fix_aspect=fix_aspect)`.
            isdrawcoastlines (bool): whether to draw continent outlines or not.
            isdrawcountries (bool): whether to draw contry boundaries or not.
            isdrawrivers (bool): whether to draw rivers or not.
            isfillcontinents (bool): whether to fill continents or not.
            bmap (basemap obj or None): reuse an existing basemap obj if not None.
        '''

        fill_color = fill_color or rcParams['fill_color']
        title = title or rcParams['title']
        label_axes = label_axes or rcParams['label_axes']
        axes_grid = axes_grid or rcParams['axes_grid']
        fontsize = fontsize or rcParams['fontsize']
        clean = clean or rcParams['clean']

        # basemap obj. When overlaying quiver onto another plot, sometimes
        # the regrid operation will make the data to a slightly different domain,
        # once overlaid, the basemap domain will always be the later plot (quiver).
        # In such cases, pass in a basemap object and use it to generate the
        # plot
        self.bmap = bmap
        if units is None:
            units = getattr(u, 'units', None)

        Plot2Quiver.__init__(
            self, u, v, method, ax=ax, xarray=xarray, yarray=yarray,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            clean=clean, fontsize=fontsize, units=units, fill_color=fill_color,
            curve=curve)

        Plot2Basemap.__init__(
            self, self.var, method, self.xarray, self.yarray, ax=ax,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            legend=None, projection=projection, clean=clean, fontsize=fontsize,
            fill_color=fill_color, fix_aspect=fix_aspect,
            isdrawcoastlines=isdrawcoastlines, isdrawcountries=isdrawcountries,
            isdrawcontinents=isdrawcontinents, isdrawrivers=isdrawrivers,
            isfillcontinents=isfillcontinents)

    def plot(self):
        '''Main plotting interface

        Calls the core plotting function self._plot(), which handles the
        2D plotting using quiver plotting method.
        Then plots axes, quiverkey and title.

        Returns:
            self.quiver (mappable): the quiver obj, i.e. return value quiver().
        '''

        self.quiver = self._plot()
        self.plotAxes()  # this is Plot2Basemap's
        self.qkey = self.plotkey()
        self.plotTitle()

        return self.quiver

    def _plot(self):
        '''Core quiver plotting function

        Returns:
            self.quiver (mappable): the quiver obj, i.e. return value quiver().
        '''

        # ------------------Create basemap------------------
        if self.bmap is None:
            self.createBmap()

        self.ax.patch.set_color(self.fill_color)

        if self.curve:
            # modded from: https://stackoverflow.com/a/65607512/2005415
            warnings.warn(
                '#<gplot warning>: The curved quiver functionality is experimental.')
            norm = np.sqrt(self.var**2 + self.v**2)
            norm_flat = norm.flatten()

            start_points = np.array(
                [self.lons.flatten(),
                 self.lats.flatten()]).T
            scale = .2/np.max(norm)

            for i in range(start_points.shape[0]):
                self.bmap.streamplot(
                    self.lons, self.lats, self.var, self.v,
                    color=self.method.color, start_points=np.array(
                        [start_points[i, :]]),
                    minlength=.25 * norm_flat[i] * scale, maxlength=1.0 *
                    norm_flat[i] * scale, integration_direction='backward',
                    density=10, arrowsize=0.0)

        # -------------------Plot vectors-------------------
        quiver = self.bmap.quiver(
            self.lons, self.lats, self.var, self.v, scale=self.method.scale,
            ax=self.ax,
            width=self.method.linewidth, latlon=True, alpha=self.method.alpha,
            color=self.method.color,
            headwidth=4)

        return quiver


def blueMarble(lat1, lon1, lat2, lon2, fig=None, projection='merc'):
    '''Plot bluemarble plot as background.

    Args:
        lat1,lon1 (floats): low-left corner. Longitude range 0-360
        lat2,lon2 (floats): upper-right corner.
    Keyword Args:
        fig (matplotlib figure or None): If None, create a new.
        projection (str): map projection.

    NOTE: due to a bug in basemap, if the plot range is crossing the
    dateline, need to plot 2 separate plots joining at the dateline.
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

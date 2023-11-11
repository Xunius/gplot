'''Cartopy related utilities

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2023-11-09 10:34:18.
'''

import re
import warnings
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colorbar as mcbar
from matplotlib import ticker
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point

from gplot.lib.base_utils import clean_up_artists, update_kwarg, get_slab, \
        get_ax_geometry, get_colorbar_pad, create_dummy_textbox, index2Letter,\
        alternate_ticks, regrid_to_reso
from gplot.lib import modplot

from gplot.lib import cma_wind_barbs


class Plot2Cartopy(object):
    def __init__(self, var, method, x, y, units=None,
                 ax=None,
                 title=None, label_axes=True, axes_grid=False,
                 legend='global', legend_ori='horizontal',
                 clean=False, fontsize=12, projection='cyl', transform=None,
                 fill_color='0.8', fix_aspect=False, isdrawcoastlines=True,
                 isdrawcountries=True, isdrawcontinents=False, isdrawrivers=False,
                 isfillcontinents=False):

        # get kwargs
        fill_color = update_kwarg('fill_color' , fill_color)
        title      = update_kwarg('title'      , title)
        label_axes = update_kwarg('label_axes' , label_axes)
        axes_grid  = update_kwarg('axes_grid'  , axes_grid)
        fontsize   = update_kwarg('fontsize'   , fontsize)
        clean      = update_kwarg('clean'      , clean)
        legend_ori = update_kwarg('legend_ori' , legend_ori)

        self.method           = method
        self.ax               = ax or plt.subplot(111)
        self.x                = x
        self.y                = y
        self.units            = units

        self.title            = str(title)
        self.label_axes       = label_axes
        self.axes_grid        = axes_grid
        self.legend           = legend
        self.legend_ori       = legend_ori
        self.clean            = clean
        self.fontsize         = fontsize
        self.fill_color       = fill_color

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

        # ---------------------Get slab---------------------
        self.var = self.get_slab(var)

        # ---------------------Get grid---------------------
        self.x, self.y, self.lons, self.lats = self.get_grid()

        # ---------------Get geo and fontsize---------------
        self.geo, self.subidx, self._fontsize = self.get_geo()

        # Store a singleton record to avoid the ax.get_geometry() result
        # get changed after creating a local colorbar:
        if not hasattr(self.ax, '_gplot_geo'):
            self.ax._gplot_geo = self.geo + (self.subidx,)

        # save a copy of the old x axis values. This maybe used later in
        # update_plot() to call again the add_cyclic_point() method, re-using
        # this copy of x
        self.ori_x = self.x.copy()
        self.add_cyclic_point()

        if not self.fix_aspect:
            self.ax.set_aspect('auto')

        # use lib.Colormap.colormap or not
        self.use_custom_cmap = hasattr(self.method, 'colormap')


    @staticmethod
    def get_slab(var):
        return get_slab(var)


    def get_grid(self):
        '''Get x- and y- coordnates

        Returns:
            x (1darray): 1d array of the x-coordinates.
            y (1darray): 1d array of the y-coordinates.
            lons,lats (ndarray): 2d array of the x- and y- coordinates, as
                created from `lons, lats = np.meshgrid(x, y)`.
        '''

        if self.y is None:
            y = np.arange(self.var.shape[0])
        else:
            y = np.array(self.y)

        if self.x is None:
            x = np.arange(self.var.shape[1])
        else:
            x = np.array(self.x)

        if len(y) != self.var.shape[0]:
            raise Exception("X-axis dimention does not match")
        if len(x) != self.var.shape[1]:
            raise Exception("Y-axis dimention does not match")

        lons, lats = np.meshgrid(x, y)

        return x, y, lons, lats


    def get_geo(self):
        '''Get geometry layout of the axis and font size

        Returns:
            geo (nrows, ncols): subplot layout of the figure.
            subidx (int): index of the axis obj in the (nrows, ncols) layout.
                i.e. 1 for the 1st subplot.
            fontsize (int): default font size. This is determined from an
                empirical formula that scales down the default font size
                for a bigger grid layout.
        '''

        if not hasattr(self.ax, '_gplot_geo'):
            #geo = self.ax.get_geometry()[:2]
            #subidx = self.ax.get_geometry()[-1]
            geo, subidx = get_ax_geometry(self.ax)
        else:
            geo = self.ax._gplot_geo[:2]
            subidx = self.ax._gplot_geo[-1]
        scale = 1./max(geo)
        fontsize = 7*scale+self.fontsize  # empirical

        return geo, subidx, fontsize


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



    def plot(self):
        '''Main plotting interface

        Calls the core plotting function self._plot(), which handles the
        2D plotting depending on the plotting method.
        Then plots axes, colorbar and title.

        Returns:
            self.cs (mappable): the mappable obj, e.g. return value from contour()
                or contourf().
        '''

        self.cs = self._plot()
        self.plot_axes()
        self.cbar = self.plot_colorbar()
        self.plot_title()

        return self.cs


    def update_plot(self, var, del_old=True):
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

        if del_old and not hasattr(self, 'cs'):
            return

        self.var = self.get_slab(var)
        self.add_cyclic_point(self.ori_x)
        if del_old:
            clean_up_artists(self.ax, [self.cs])
        self.cs = self._plot()

        return


    def _plot(self):
        '''Core plotting function

        Create the plot depending on method: isofill, isoline, boxfill, pcolor,
        hatch, or shading.

        Returns:
            self.cs (mappable): the mappable obj, e.g. return value from contour()
                or contourf().
        '''

        # make masked value grey, otherwise they will be white
        self.ax.patch.set_color(self.fill_color)

        # -------------------Contour fill/line-------------------
        if self.method.method == 'isofill':
            cs = self._plot_isofill()

        elif self.method.method == 'isoline':
            cs = self._plot_isoline()

        # ---------------------Boxfill---------------------
        elif self.method.method == 'boxfill':
            cs = self._plot_boxfill()

        # -------------------Pcolor fill-------------------
        elif self.method.method == 'pcolor':
            cs = self._plot_pcolormesh()

        # ------------------Hatch contourf------------------
        elif self.method.method == 'hatch':
            cs = self._plot_hatch()

        # ------------------shading contourf------------------
        elif self.method.method == 'shading':
            cs = self._plot_shading()

        return cs


    def _plot_isofill(self):
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



    def _plot_isoline(self):
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
            self.plot_contour_labels(cs)

        return cs


    def plot_contour_labels(self, cs):

        if self.method.label_fmt is None:
            # save the old xaxis formatter
            old_formatter = self.ax.xaxis.get_major_formatter()
            # get a new scalar formatter
            formatter = ticker.ScalarFormatter()
            # for some reason one needs to set as major and call format_ticks()
            # before this thing can do formatter(value)
            self.ax.xaxis.set_major_formatter(formatter)
            formatter.format_ticks(cs.levels)
            clabels = cs.clabel(inline=1, fmt=formatter, fontsize=12)
            # restore old xaxis formatter
            self.ax.xaxis.set_major_formatter(old_formatter)
        else:
            clabels = cs.clabel(inline=1, fmt=self.method.label_fmt, fontsize=12)

        if self.method.label_box:
            [txt.set_bbox(dict(facecolor=self.method.label_box_color,
                edgecolor='none', pad=0)) for txt in clabels]

        return


    def _plot_boxfill(self):
        '''Core plotting function, boxfill/imshow'''

        cs = self.ax.imshow(
            self.var, cmap=self.method.cmap, origin='lower',
            norm=self.method.norm,
            vmin=self.method.vmin, vmax=self.method.vmax,
            interpolation='nearest',
            extent=[self.x.min(),
                    self.x.max(),
                    self.y.min(),
                    self.y.max()],
            aspect='auto')

        return cs

    def _plot_pcolormesh(self):
        '''Core plotting function, pcolormesh'''

        cs = self.ax.pcolormesh(
            self.lons, self.lats, self.var, cmap=self.method.cmap,
            norm=self.method.norm,
            vmin=self.method.vmin,
            vmax=self.method.vmax)

        return cs

    def _plot_hatch(self):
        '''Core plotting function, pattern hatching'''

        # nlevel=3 necessary?
        #if np.all(self.var == 0):
            #nlevel = 1
        #else:
            #nlevel = 3
        cs = self.ax.contourf(
            self.lons[0, :],
            self.lats[:, 0],
            hatches=[None, self.method.hatch],
            alpha=self.method.alpha)

        # For each level, we set the color of its hatch
        for i, collection in enumerate(cs.collections):
            collection.set_edgecolor(self.method.color)
            collection.set_facecolor('none')
        # Doing this also colors in the box around each level
        # We can remove the colored line around the levels by setting the linewidth to 0
        for collection in cs.collections:
            collection.set_linewidth(0.)

        return cs

    def _plot_shading(self):
        '''Core plotting function, color shading'''

        pvar = np.where(self.var == 1, 1, np.nan)
        cs = self.ax.contourf(
            self.lons,
            self.lats,
            pvar, 1, cmap=self.method.cmap,
            alpha=self.method.alpha,
            transform=self._transform)

        return cs


    def plot_others(self):

        if self.clean:
            return

        # -------------------Draw others-------------------
        if not self.method.method == 'gis':
            self.ax.coastlines()

        return


    def get_label_bool_for_sharexy(self, geo, idx):
        '''Decide ticks and ticklabels on the 4 sides with shared x and y.

        Args:
            geo (nrows, ncols): subplot layout of the figure.
            idx (int): index of the axis obj in the (nrows, ncols) layout.
                i.e. 1 for the 1st subplot.
        Returns:
            parallels (list): boolean flag for the x-axis ticks/labels on 4 sides:
                [left, right, top, bottom]
            meridians (list): boolean flag for the y-axis ticks/labels on 4 sides:
                [left, right, top, bottom]
        '''

        if geo[0]*geo[1] == 1:
            parallels = [1, 1, 0, 0]
            meridians = [0, 0, 0, 1]
        else:
            ridx, cidx = np.unravel_index(idx-1, geo)
            parallels = [0, 0, 0, 0]
            meridians = [0, 0, 0, 0]
            if cidx == 0:
                parallels[0] = 1
                if geo[1] == 1:
                    parallels[1] = 1
            elif cidx == geo[1]-1:
                parallels[1] = 1
                if geo[1] == 1:
                    parallels[0] = 1

            if ridx == 0 and geo[0] == 1:
                meridians[3] = 1
            elif ridx == geo[0]-1:
                meridians[3] = 1

        return parallels, meridians


    def get_label_bool(self):
        '''Decide whether to plot axis ticks and ticklabels on the 4 sides.

        Returns:
            parallels (list): boolean flag for the x-axis ticks/labels on 4 sides:
                [left, right, top, bottom]
            meridians (list): boolean flag for the y-axis ticks/labels on 4 sides:
                [left, right, top, bottom]
        '''

        if self.clean or not self.label_axes:
            parallels = [0, 0, 0, 0]
            meridians = [0, 0, 0, 0]

        elif self.label_axes == 'all':
            parallels = [1, 1, 0, 0]
            meridians = [0, 0, 1, 1]

        elif isinstance(self.label_axes, (list, tuple)) and len(self.label_axes) == 4:
            parallels = [0, ]*4
            meridians = [0, ]*4
            for ii in [0, 1]:
                if self.label_axes[ii]:
                    parallels[ii] = 1
            for ii in [2, 3]:
                if self.label_axes[ii]:
                    meridians[ii] = 1
        else:
            parallels, meridians = self.get_label_bool_for_sharexy(
                    self.ax._gplot_geo[:-1], self.subidx)

        return parallels, meridians


    # ---------------Draw lat, lon grids---------------
    def plot_axes(self):

        self.plot_others()

        # --------Turn off lat/lon labels if required--------
        if self.label_axes is False or self.clean:
            self.ax.xaxis.set_ticklabels([])
            self.ax.yaxis.set_ticklabels([])
            return

        if self.label_axes == 'all':
            parallels = [1,1,0,0]
            meridians = [0,0,1,1]

        elif isinstance(self.label_axes, (list, tuple)) and len(self.label_axes)==2 and\
                len(self.label_axes[0])==4 and len(self.label_axes[1])==4:
            # TODO: add docstring for this
            parallels,meridians = self.label_axes
        else:
            parallels,meridians = self.get_label_bool()

        self.gridliner = self.ax.gridlines(
            draw_labels=True, color=self.fill_color)
        self.gridliner.xlabel_style = {'size': self._fontsize}
        self.gridliner.ylabel_style = {'size': self._fontsize}

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


    def get_colorbar_ax(self):
        '''Get axis obj for colorbar'''

        # --------------Create a colorbar axis--------------
        if self.legend == 'local' or (
                self.legend == 'global' and self.geo[0] * self.geo[1] == 1):

            if self.method.method in ['boxfill', 'pcolor']:

                # Adjust position according to the existence of axis ticks
                pad = get_colorbar_pad(self.ax, self.legend_ori, base_pad=0.02)
                # NOTE: mcbar.make_axes() doesn't work well with tight_layout()

            elif self.method.method in ['isofill', 'isoline']:
                if self.legend_ori == 'horizontal':
                    # compute extra padding needed for the top side tick labels
                    dummybox = create_dummy_textbox(self.ax, self._fontsize)
                    pad = get_colorbar_pad(
                        self.ax, self.legend_ori, base_pad=dummybox.height*1.5)
                else:
                    pad = get_colorbar_pad(
                        self.ax, self.legend_ori, base_pad=0.02)

            cax, _ = mcbar.make_axes_gridspec(
                self.ax, orientation=self.legend_ori, shrink=0.85, pad=pad,
                fraction=0.07, aspect=35)

        # -----Use the 1st subplot as global color bar-----
        elif self.legend == 'global' and self.subidx == 1:

            fig = self.ax.get_figure()
            subplots = list(filter(lambda x: isinstance(x, matplotlib.axes.SubplotBase), fig.axes))

            if self.legend_ori == 'horizontal':
                if len(subplots) > 1:
                    if fig.get_constrained_layout():
                        cax, _ = mcbar.make_axes(
                            subplots, orientation=self.legend_ori, shrink=0.85,
                            pad=0.01, fraction=0.07, aspect=35)
                    else:
                        dummybox = create_dummy_textbox(self.ax, self._fontsize)
                        pad = dummybox.height*1.2
                        cax, _ = mcbar.make_axes(
                            subplots, orientation=self.legend_ori, shrink=0.85,
                            pad=pad, fraction=0.07, aspect=35)
                else:
                    dummybox = create_dummy_textbox(self.ax, self._fontsize)
                    pad = dummybox.height*0.85
                    height = 0.02
                    fig.subplots_adjust(bottom=0.18)
                    cax = self.ax.get_figure().add_axes(
                        [0.175, 0.18-height-pad, 0.65, height])

            elif self.legend_ori == 'vertical':
                if len(subplots) > 1:
                    cax, _ = mcbar.make_axes(
                        subplots, orientation=self.legend_ori, shrink=0.85,
                        pad=0.02, fraction=0.07, aspect=35)
                else:
                    fig.subplots_adjust(right=0.90)
                    cax = self.ax.get_figure().add_axes(
                        [0.95, 0.20, 0.02, 0.6])

        return cax


    def plot_colorbar(self):
        '''Plot colorbar

        Returns:
            cbar (matplotlib colorbar obj): colorbar obj.

        Only creates a colorbar for isofill/contourf or isoline/contour plots.
        '''

        if self.method.method in ['hatch', 'shading']:
            return

        if self.legend is None:
            return

        if self.legend in ['off', 'none']:
            return

        if self.method.method in ['isofill', 'isoline']:
            if len(self.cs.levels) < 2:
                return
            if self.method.method == 'isoline' and self.method.black:
                return
            if self.method.method == 'isoline' and self.method.color is not None:
                return
            isdrawedges = True
        else:
            isdrawedges = False

        if self.method.method in ['boxfill', 'pcolor']:
            ticks = None
            #extend = self.method.extend
        else:
            ticks = getattr(self.method, 'levels', None)
            #extend = None

        if self.legend == 'global' and self.subidx > 1:
            return

        #----------------Get colorbar axis----------------
        cax = self.get_colorbar_ax()

        # ------------------Plot colorbar------------------
        if self.use_custom_cmap:
            cbar = self.method.colormap.plot_colorbar(self.ax, cax=cax,
                                               orientation=self.legend_ori)

        else:
            cbar = plt.colorbar(self.cs, cax=cax, orientation=self.legend_ori,
                ticks=ticks, drawedges=isdrawedges)

            # -------------------Re-format ticks-------------------
            if self.method.method in [
                    'isofill', 'isoline'] and self.legend_ori == 'horizontal':
                #cbar = self.alternate_ticks(cbar, ticks)
                cbar = alternate_ticks(cbar, ticks, self._fontsize)
            cbar.ax.tick_params(labelsize=self._fontsize)

            # --------------------Plot unit--------------------
            var_units = getattr(self.var, 'units', '')
            if var_units is None:
                var_units = self.units

            if var_units:
                # option1: plot colorbar units below
                # self.cbar.set_label(var_units,fontsize=self._fontsize)

                # option2: plot colorbar units to the right or below, depending on
                # orientation
                if self.legend_ori == 'horizontal':
                    cbar_ax = cbar.ax
                    cbar_ax.text(1.02, 0.5, var_units, fontsize=self._fontsize,
                                 transform=cbar_ax.transAxes,
                                 horizontalalignment='left',
                                 verticalalignment='center')
                elif self.legend_ori == 'vertical':
                    cbar_ax = cbar.ax
                    cbar_ax.text(
                        0.5, -0.05, var_units, fontsize=self._fontsize,
                        transform=cbar_ax.transAxes,
                        horizontalalignment='left', verticalalignment='top')

        return cbar


    def plot_title(self):
        '''Plot title

        Use self.title as the figure title if self.ax is the single plot in the
        figure. If None, automatically get an alphabetic subtitle if self.ax is
        a subplot, e.g. '(a)' for the 1st subplot, '(d)' for the 4th one.
        If self.title is str and self.ax is a subplot, prepend self.title with
        the alphabetic index. One can force overriding the alphabetic index
        by giving a title str in the format of '(x) xxxx', e.g. '(p) subplot-p'.
        '''

        if self.clean or self.title == 'none':
            return

        geo = self.ax._gplot_geo[:-1]

        if self.title is None and geo[0]*geo[1] == 1:
            return

        if self.title is None and geo[0]*geo[1] > 1:
            title = index2Letter(self.subidx)

        elif isinstance(self.title, str):

            if geo[0]*geo[1] > 1:
                # force indexing
                rep = re.compile('^\\((.*?)\\)(.*)')
                match = rep.match(self.title)
                # overwrite indexing if title starts with (a), (b) or so
                if match is not None:
                    tidx_str = '(%s)' % match.group(1)
                    tstr = match.group(2).strip()
                else:
                    tidx_str = index2Letter(self.subidx)
                    tstr = self.title
                title = '%s %s' % (tidx_str, tstr)
            else:
                title = self.title

        self.ax.set_title(title, loc='left', fontsize=self._fontsize)

        return


class Plot2QuiverCartopy(Plot2Cartopy):

    def __init__(self, u, v, method, x, y, units=None,
                 ax=None,
                 title=None, label_axes=True, axes_grid=False,
                 legend='global', legend_ori='horizontal',
                 curve=False,
                 clean=False, fontsize=12, projection='cyl', transform=None,
                 fill_color='0.8', fix_aspect=False, isdrawcoastlines=True,
                 isdrawcountries=True, isdrawcontinents=False, isdrawrivers=False,
                 isfillcontinents=False):

        Plot2Cartopy.__init__(
            self, u, method, x, y, ax=ax, units=units,
            title=title, label_axes=label_axes, axes_grid=axes_grid,
            legend=None,
            projection=projection, transform=transform,
            clean=clean, fontsize=fontsize, fill_color=fill_color,
            fix_aspect=fix_aspect, isdrawcoastlines=isdrawcoastlines,
            isdrawcountries=isdrawcountries, isdrawcontinents=isdrawcontinents,
            isdrawrivers=isdrawrivers,
            isfillcontinents=isfillcontinents)

        self.step  = self.method.step
        self.curve = curve
        self.ori_y = self.y.copy()

        self.v     = self.get_slab(v)
        self.v, _  = add_cyclic_point(self.v, self.ori_x)

        self.regrid_vars()


    def regrid_vars(self):

        # ----------------------Regrid----------------------
        if self.method.reso is not None:
            xx = self.x
            yy = self.y
            self.var, self.y, self.x = regrid_to_reso(
                self.var, yy, xx, self.method.reso, self.method.reso,
                lat_idx=-2, lon_idx=-1, method='linear', return_coords=True)

            self.v = regrid_to_reso(
                self.v, yy, xx, self.method.reso, self.method.reso, lat_idx=-2,
                lon_idx=-1, method='linear', return_coords=False)
        else:
            # ---------------------Spacing---------------------
            self.var = self.var[::self.step, ::self.step]
            self.v = self.v[::self.step, ::self.step]
            self.x = self.x[::self.step]
            self.y = self.y[::self.step]

        self.lons, self.lats = np.meshgrid(self.x, self.y)

        return



    def plot(self):

        if self.method.method == 'quiver':
            self.quiver = self._plot_quiver()
            self.qkey = self.plot_quiverkey()
        elif self.method.method == 'barbs':
            self.quiver = self._plot_barbs()
        else:
            raise Exception("Unsupported plotting method: {}".format(self.quiver))

        self.plot_axes()
        self.plot_title()

        return self.quiver


    def update_plot(self, u, v):
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

        self.var = self.get_slab(u)
        self.v = self.get_slab(v)
        self.add_cyclic_point(self.ori_x)
        self.v, _  = add_cyclic_point(self.v, self.ori_x)
        self.y = self.ori_y
        self.regrid_vars()

        self.quiver.set_UVC(self.var, self.v)

        return


    def _plot_quiver(self):
        '''Core quiver plotting function

        Returns:
            self.quiver (mappable): the quiver obj, i.e. return value quiver().
        '''

        self.ax.patch.set_color(self.fill_color)

        if self.curve:
            warnings.warn(
                '#<gplot warning>: The curved quiver functionality is experimental.')
            grains = int((len(self.x)+len(self.y)))
            quiver = modplot.velovect(self.ax, self.lons, self.lats, self.var,
                                      self.v, scale=15,
                                      grains=grains, color=self.method.color)

        # -------------------Plot vectors-------------------
        quiver = self.ax.quiver(
            self.lons, self.lats, self.var, self.v, scale=self.method.scale,
            scale_units=None, width=self.method.linewidth,
            color=self.method.color, alpha=self.method.alpha, zorder=3)

        return quiver


    def _plot_barbs(self):
        '''Core barbs plotting function

        Returns:
            self.barbs (mappable): the Barbs obj.
        '''

        if self.method.standard == 'cma':
            cma_wind_barbs.setup()
        else:
            cma_wind_barbs.restore()

        barbs = self.ax.barbs(self.lons, self.lats, self.var, self.v,
                              length=self.method.keylength,
                         sizes={'emptybarb': self.method.emptybarb,
                                'spacing': self.method.spacing,
                                'height': self.method.height},
                 barb_increments=self.method.barb_increments,
                 linewidth=self.method.linewidth,
                 transform=self._transform, zorder=3)

        return barbs


    def plot_quiverkey(self):
        '''Plot the reference quiver key

        Returns:
            quiverkey (quiver key).
        '''

        if self.method.keylength is None:
            # compute a keylength based on vector magnitudes
            # 1. use median.
            # keylength=np.median(np.sqrt(self.var.data**2+self.v.data**2))
            # 2. use 80th percentile
            slab = np.sqrt(np.array(self.var)**2 +
                           np.array(self.v)**2).flatten()
            slab = np.where(slab == np.inf, np.nan, slab)
            keylength = np.nanpercentile(slab[slab>0], 80)

            # scale to 10-100
            lg = -np.log10(keylength)+2.
            il = np.floor(lg)
            keylength = keylength*10.**il
            # round to a nice integer
            keylength = np.around((keylength/10.), 0)*10/(10.**il)
        else:
            keylength = self.method.keylength

        units = getattr(self.var, 'units', self.units)
        units = units or ''
        quiverkey = self.ax.quiverkey(
            self.quiver, X=0.77, Y=1.05, U=keylength, label='%.2f %s' %
            (keylength, units),
            labelpos='E', color='k', labelcolor='k')

        return quiverkey

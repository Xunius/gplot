'''Basic 2D plotting functions and classes.

Contains:
    * utility functions.
    * plotting method classes.
    * plotting wrapper classes, from which equivalent geographical plotting
      classes are inherited.

Memebers in this module are available under the `gplot` namespace:

    `gplot.xxx`

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2021-02-13 10:06:58.
'''

# TODO: global colorbar placement is not smart enough. *UPDATE* made some changes
#       recommended to use constrained_layout in creating the figure and
#       create all subplot axes before hand.
# TODO: add Plot2QuiverCartopy
# TODO: consider remove bmap input arg
# TODO make it possible to use barbs plot
# TODO make it possible to use colormap to decode quiver magnitude, instead of
# arrow length

# --------Import modules--------------
from __future__ import print_function
import re
import copy
import warnings
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import ticker
from matplotlib.pyplot import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colorbar as mcbar
from matplotlib import colors
from gplot.lib import modplot

__all__=[
        'rcParams',
        'restoreParams', 'mkscale', 'index2Letter', 'remappedColorMap2',
        'getColormap', 'getColorbarPad', 'pickPoint', 'getSlab', 'regridToReso',
        'getMissingMask', 'getQuantiles', 'getRange', 'plot2',
        'Isofill', 'Isoline', 'Boxfill', 'Pcolor', 'Hatch', 'Shading', 'GIS', 'Quiver',
        'Plot2D', 'Plot2Quiver'
        ]

# Default parameters
rcParams = {
    'legend': 'global',
    'title': None,
    'label_axes': True,
    'axes_grid': False,
    'fill_color': '0.8',
    'projection': 'cyl',
    'legend_ori': 'horizontal',
    'clean': False,
    'bmap': None,
    'isgeomap': True,
    'fix_aspect': False,
    'nc_interface': 'cdat',
    'geo_interface': 'basemap',
    'fontsize': 11,
    'verbose': True,
    'default_cmap': plt.cm.RdBu_r
}

# a backup copy, deepcopy produces issue in autodoc
_default_rcParams = {
    'legend': 'global',
    'title': None,
    'label_axes': True,
    'axes_grid': False,
    'fill_color': '0.8',
    'projection': 'cyl',
    'legend_ori': 'horizontal',
    'clean': False,
    'bmap': None,
    'isgeomap': True,
    'fix_aspect': False,
    'nc_interface': 'cdat',
    'geo_interface': 'basemap',
    'fontsize': 11,
    'verbose': True,
    'default_cmap': plt.cm.RdBu_r
}

#_default_rcParams = copy.deepcopy(rcParams)

# -----------------------------------------------------------------------
# -                          Utility functions                          -
# -----------------------------------------------------------------------


def restoreParams():
    '''Restore default parameters'''
    global rcParams
    rcParams.update(_default_rcParams)


def mkscale(n1, n2, nc=12, zero=1):
    '''Create nice looking levels given a min and max.

    Args:
        n1, n2 (floats): min and max levels between which to create levels.
    Keyword Args:
        nc (int): suggested number of levels. Note that the resulant levels
                  may not have the exact number of levels as required.
        zero (int): Not all implemented yet so set to 1 but values will be:
           -1: zero MUST NOT be a contour
            0: let the function decide # NOT IMPLEMENTED
            1: zero CAN be a contour  (default)
            2: zero MUST be a contour
    Returns:
        cnt (list): a list of levels between approximately <n1> and <n2>,
                    with a number of levels more or less as <nc>.

        Examples of Use:
        >>> vcs.mkscale(0,100)
        [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
        >>> vcs.mkscale(0,100,nc=5)
        [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]
        >>> vcs.mkscale(-10,100,nc=5)
        [-25.0, 0.0, 25.0, 50.0, 75.0, 100.0]
        >>> vcs.mkscale(-10,100,nc=5,zero=-1)
        [-20.0, 20.0, 60.0, 100.0]
        >>> vcs.mkscale(2,20)
        [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
        >>> vcs.mkscale(2,20,zero=2)
        [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]

        Copied from vcs/util.py
    '''
    if n1 == n2:
        return [n1]
    nc = int(nc)
    cscale = 0  # ???? May be later
    min = np.min([n1, n2])
    max = np.max([n1, n2])
    if zero > 1.:
        if min > 0.:
            min = 0.
        if max < 0.:
            max = 0.
    rg = float(max-min)  # range
    delta = rg/nc  # basic delta
    # scale delta to be >10 and <= 100
    lg = -np.log10(delta)+2.
    il = np.floor(lg)
    delta = delta*(10.**il)
    max = max*(10.**il)
    min = min*(10.**il)
    if zero > -0.5:
        if delta <= 20.:
            delta = 20
        elif delta <= 25.:
            delta = 25
        elif delta <= 40.:
            delta = 40
        elif delta <= 50.:
            delta = 50
        elif delta <= 60.:
            delta = 60
        elif delta <= 70.:
            delta = 70
        elif delta <= 80.:
            delta = 80
        elif delta <= 90.:
            delta = 90
        elif delta <= 101.:
            delta = 100
        first = np.floor(min/delta)-1.
    else:
        if delta <= 20.:
            delta = 20
        elif delta <= 25.:
            delta = 25
        elif delta <= 40.:
            delta = 40
        elif delta <= 50.:
            delta = 50
        elif delta <= 60.:
            delta = 60
        elif delta <= 70.:
            delta = 70
        elif delta <= 80.:
            delta = 80
        elif delta <= 90.:
            delta = 90
        elif delta <= 101.:
            delta = 100
        first = np.floor(min/delta)-1.5

    scvals = delta*(np.arange(2*nc)+first)
    a = 0
    for j in range(len(scvals)):
        if scvals[j] > min:
            a = j-1
            break
    b = 0
    for j in range(len(scvals)):
        if scvals[j] >= max:
            b = j+1
            break
    if cscale == 0:
        cnt = scvals[a:b]/10.**il
    else:
        # not done yet...
        raise Exception('ERROR scale not implemented in this function')
    return list(cnt)


def index2Letter(index, verbose=True):
    '''Translate an integer index to letter index

    Args:
        index (int): integer index for a subplot.
    Returns:
        letter (str): corresponding letter index for <index>.

        <index> to letter indexing is defined as following:
        ----------------------------------------------------
        <index>                     letter index
        ----------------------------------------------------
           1                            (a)
           2                            (b)
           3                            (c)
           ...                          ...
           27                           (aa)
           ...
           52                           (zz)
        ----------------------------------------------------
    '''

    index_dict = {
        1: 'a',
        2: 'b',
        3: 'c',
        4: 'd',
        5: 'e',
        6: 'f',
        7: 'g',
        8: 'h',
        9: 'i',
        10: 'j',
        11: 'k',
        12: 'l',
        13: 'm',
        14: 'n',
        15: 'o',
        16: 'p',
        17: 'q',
        18: 'r',
        19: 's',
        20: 't',
        21: 'u',
        22: 'v',
        23: 'w',
        24: 'x',
        25: 'y',
        26: 'z'
    }

    # -------------------Check inputs-------------------
    if index <= 0:
        raise Exception("<index> needs to be positive.")
    return '(%s)' % (index_dict[(index-1) % 26+1]*((index-1)//26+1))


def remappedColorMap(
        cmap, vmin, vmax, split=2, vcenter=0., name='shiftedcmap'):
    '''Re-map the colormap to split positives and negatives.

    <cmap> : The matplotlib colormap to be altered
    <vmin> : float, minimal level in data.
    <vmax> : float, maximal level in data.
    <split>: int, control behavior of negative and positive values\
            0: Do not split negatives and positives, map onto entire\
               range of [0,1];
            1: split only when vmin<0 and vmax>0, otherwise\
               map onto entire range of [0,1];
               If split is to be applied, negative values are mapped onto first half [0,0.5],
               and postives onto second half (0.5,1].
            2: force split, if vmin<0 and vmax>0, same as <split>==1;
                If vmin<0 and vmax<0, map onto 1st half [0,0.5];
                If vmin>0 and vmax>0, map onto 2nd half (0.5,1].
    NOTE: not in use any more.
    '''

    # -----------Return cmap if not splitting-----------
    if split == 0:
        return cmap
    if split == 1 and (vmin-vcenter)*(vmax-vcenter) >= 0:
        return cmap

    # ------------Resample cmap if splitting------------
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    vmin, vmax = np.sort([vmin, vmax]).astype('float')

    shift_index = np.linspace(0, 1, 256)

    # -------------------Force split-------------------
    if vmin < vcenter and vmax <= vcenter and split == 2:
        if vmax < vcenter:
            idx = np.linspace(0, 0.5, 256, endpoint=False)
        else:
            idx = np.linspace(0, 0.5, 256, endpoint=True)

    elif vmin >= vcenter and vmax > vcenter and split == 2:
        if vmin > vcenter:
            idx = np.linspace(1, 0.5, 256, endpoint=False)[::-1]
        else:
            idx = np.linspace(1, 0.5, 256, endpoint=True)[::-1]

    # --------------------Split -/+--------------------
    if (vmin-vcenter)*(vmax-vcenter) < 0:
        mididx = int(abs(vmin-vcenter)/(abs(vmax)+abs(vmin))*256)
        idx = np.hstack([np.linspace(0, 0.5, mididx, endpoint=False),
                         [0.5, ],
                         np.linspace(1, 0.5, 256-mididx-1, endpoint=False)[::-1]])

    # -------------------Map indices-------------------
    for ri, si in zip(idx, shift_index):
        r, g, b, a = cmap(ri)
        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))
    newcmap = LinearSegmentedColormap(name, cdict, N=256)
    plt.register_cmap(cmap=newcmap)

    return newcmap


def remappedColorMap2(cmap, vmin, vmax, vcenter, name='shiftedcmap'):
    '''Re-map the colormap to split positives and negatives.

    Args:
        cmap (colormap): the matplotlib colormap to be altered.
        vmin (float): minimal level in data.
        vmax (float): maximal level in data.
        vcenter (float): central level in data.
    Keyword Args:
        name (str): name for the altered colormap.
    Returns:
        newcmap (colormap): re-mapped colormap such that:
            if vmin < vmax <= vcenter:
                0   in color map corresponds to vmin
                0.5   in color map corresponds to vmax
            if vcenter <= vmin < vmax:
                0.5   in color map corresponds to vmin
                1.0   in color map corresponds to vmax
            E.g. if vcenter=0, this splits a diverging colormap to use
            only the negative/positive half the original colors.
    '''

    # ------------Resample cmap if splitting------------
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    vmin, vmax = np.sort([vmin, vmax]).astype('float')
    shift_index = np.linspace(0, 1, 256)

    # -------------------Force split-------------------
    if vmin < vcenter and vmax <= vcenter:
        if vmax < vcenter:
            idx = np.linspace(0, 0.5, 256, endpoint=False)
        else:
            idx = np.linspace(0, 0.5, 256, endpoint=True)

    elif vmin >= vcenter and vmax > vcenter:
        if vmin > vcenter:
            idx = np.linspace(1, 0.5, 256, endpoint=False)[::-1]
        else:
            idx = np.linspace(1, 0.5, 256, endpoint=True)[::-1]

    # -------------------Map indices-------------------
    for ri, si in zip(idx, shift_index):
        r, g, b, a = cmap(ri)
        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))
    newcmap = LinearSegmentedColormap(name, cdict, N=256)
    plt.register_cmap(cmap=newcmap)

    return newcmap


def getColormap(cmap):
    '''Get a colormap

    Args:
        cmap (matplotlib colormap, str or None): if colormap, return as is.
            if str, get a colormap by name: getattr(plt.cm, cmap).
            If None, use default of rcParams['default_cmap'].
    Returns:
        cmap (matplotlib colormap): matplotlib colormap.
    '''

    if cmap is None:
        cmap = rcParams['default_cmap']
    elif cmap is not None and isinstance(cmap, str):
        try:
            cmap = getattr(plt.cm, cmap)
        except:
            raise Exception("Color map name wrong.")

    return cmap


def getColorbarPad(ax, orientation, base_pad=0.0):
    '''Compute padding value for colorbar axis creation

    Args:
        ax (Axis obj): axis object used as the parent axis to create colorbar.
        orientation (str): 'horizontal' or 'vertical'.
    Keyword Args:
        base_pad (float): default pad. The resultant pad value is the computed
            space + base_pad.
    Returns:
        pad (float): the pad argument passed to make_axes_gridspec() function.
    '''

    try:
        aspect = ax.get_aspect()
        ax.set_aspect('auto')
        renderer = ax.get_figure().canvas.get_renderer()
        b1 = ax.patch.get_extents()
        b2 = ax.get_tightbbox(renderer)
        if orientation == 'horizontal':
            bbox = ax.transAxes.inverted().transform([b1.p0, b2.p0])
            pad = abs(bbox[0]-bbox[1])[1] + base_pad
        elif orientation == 'vertical':
            bbox = ax.transAxes.inverted().transform([b1.p1, b2.p1])
            pad = abs(bbox[0]-bbox[1])[0] + base_pad
        ax.set_aspect(aspect)
    except:
        pad = 0.15
    else:
        if np.isnan(pad):
            pad = 0.15

    return pad


def createDummyTextBox(ax=None, fontsize=12):
    '''Create a dummy text and return its box

    Keyword Args:
        ax (plt axis or None): given plt axis to use to create the text. If
            None, create a new.
        fontsize (int): font size to create the text.
    Returns:
        dummybox (matplotlib Bbox): bbox of the dummy text box.
    '''

    if ax is None:
        fig, ax = plt.subplots()

    dummytext = ax.text(
        0, 0, '0.0', zorder=-10, fontsize=fontsize,
        alpha=0, transform=ax.transAxes)
    dummybox = dummytext.get_window_extent(
        ax.get_figure().canvas.get_renderer())
    dummybox = dummybox.transformed(
        ax.transAxes.inverted())

    return dummybox


def pickPoint(ax, color='y'):
    '''Pick points from plot and store coordinates.

    Args:
        ax (matplotlib axis): axis from whose plot to pick points.
    Keyword Args:
        color (str or RGB tuple): Color of picked points.
    Returns:
        points (list): list of (x,y) coordinates.
    '''
    import pylab
    points = []

    while True:
        print('\n# <pickPoint>: Pick point by clicking. Enter to quit.')
        coord = pylab.ginput(n=1, timeout=False)
        if len(coord) > 0:
            coord = coord[0]
            points.append(coord)
            print('# <pickPoint>: New point:', coord)
            ax.plot(coord[0], coord[1], 'o', markersize=10, color=color)
            ax.get_figure().canvas.draw()
        else:
            break
    return np.array(points)


def getSlab(var, index1=-1, index2=-2, verbose=True):
    '''Get a slab from a variable

    Args:
        var: (ndarray): ndarray with dimension >=2.
    Keyword Args:
        index1,index2 (int): indices denoting the dimensions that define a 2d
            slab.
    Returns:
        slab (ndarray): the (1st) slab from <var>.
           E.g. <var> has dimension (12,1,241,480), getSlab(var) will
           return the 1st time point with singleton dimension squeezed.
    '''

    ndim = np.ndim(var)
    if ndim < 2:
        raise Exception('Dimension in <var> is smaller than 2.')
    if ndim == 2:
        return var

    slicer = [slice(0, 1), ]*ndim
    slicer[index1] = slice(None)
    slicer[index2] = slice(None)
    result = var[tuple(slicer)]
    try:
        result = np.squeeze(result)
    except:
        result = result(squeeze=1)
    return np.array(result)


def regridToReso(var, inlat, inlon, dlat, dlon, lat_idx=-2, lon_idx=-1,
                 method='linear', return_coords=False, verbose=True):
    '''Regrid to given resolution, using scipy

    Args:
        var (ndarray): input nd array.
        inlat (1darray): input latitude coordinates.
        inlon (1darray): input longitude coordinates.
        dlat (float): target latitudinal resolution.
        dlon (float): target longitudinal resolution.
    Keyword Args:
        lat_idx (int): index for the latitude dimension.
        lon_idx (int): index for the longitude dimension.
        method (str): interpolation method, could be 'linear' or 'nearest'.
        return_coords (bool): if True, also return new lat/lon coordinates.
    Returns:
        result (ndarray): interpolated result.
        newlat (1darray): if <return_coords> is True, the new latitude coordinates.
        newlon (1darray): if <return_coords> is True, the new longitude coordinates.
    '''

    try:
        from scipy.interpolate import RegularGridInterpolator
    except:
        raise Exception("Regridding functionality requries scipy.")

    # ------------Check inputs------------
    if not isinstance(var, np.ndarray):
        raise Exception("<var> needs to be an ndarray.")

    if dlat <= 0 or dlon <= 0:
        raise Exception('<dlat> and <dlon> need to be postive definite.')

    if method not in ['linear', 'nearest']:
        raise Exception("<method> could be 'linear' or 'nearest'.")

    shape = list(var.shape)

    if shape[lat_idx] < 2:
        raise Exception("Latitude dimension to short.")
    if shape[lon_idx] < 2:
        raise Exception("Longitude dimension to short.")

    inlat = np.array(inlat).astype('float')
    inlon = np.array(inlon).astype('float')

    # --------Create new latitude and longitudes--------
    latrange = abs(inlat[-1]-inlat[0])
    lonrange = abs(inlon[-1]-inlon[0])
    nlat = np.floor(latrange/float(dlat))+1
    nlon = np.floor(lonrange/float(dlon))+1

    if int(nlat) <= 1:
        raise Exception('Latitudinal resolution is too low.')
    if int(nlon) <= 1:
        raise Exception('Longitudinal resolution is too low.')

    newlat = np.linspace(inlat[0], inlat[-1], int(nlat))
    newlon = np.linspace(inlon[0], inlon[-1], int(nlon))

    # -------------------Squeeze var-------------------
    if method == 'linear':

        # If var has any singleton dimension, linear interpolate will create
        # all nans. Therefore, need to squeeze singleton axes, and update
        # lat_idx and lon_idx if affected.
        order = range(len(shape))
        lat_idx2 = order[lat_idx]
        lon_idx2 = order[lon_idx]
        single_dims = np.where(np.array(shape) == 1)[0]
        lat_idx2 = lat_idx2 - (single_dims < lat_idx2).sum()
        lon_idx2 = lon_idx2 - (single_dims < lon_idx2).sum()

        var2 = np.squeeze(np.array(var))
    else:
        var2 = np.array(var)

    squeeze_shape = list(var2.shape)

    # ---------Build target and original grids---------
    coords = [np.arange(x) for x in squeeze_shape]
    coords[lat_idx2] = inlat
    coords[lon_idx2] = inlon

    newcoords = [np.arange(x) for x in squeeze_shape]
    newcoords[lat_idx2] = newlat
    newcoords[lon_idx2] = newlon
    meshes = np.meshgrid(*newcoords, indexing='ij')
    target_points = np.array([cii.flatten() for cii in meshes]).T

    # -------------------Interpolate-------------------
    interpf = RegularGridInterpolator(coords, var2, bounds_error=False)
    result = interpf(target_points, method=method)

    # ---------------------Reshape---------------------
    shape[lat_idx] = len(newlat)
    shape[lon_idx] = len(newlon)
    result = result.reshape(shape)

    # TODO: regrid masks
    if return_coords:
        return result, newlat, newlon
    else:
        return result


def getMissingMask(slab):
    '''Get a bindary array denoting missing (masked or nan).

    Args:
        slab (ndarray): input array that may contain masked values or nans.
    Returns:
        mask (ndarray): bindary array with same shape as <slab> with 1s for
            missing, 0s otherwise.
    '''

    nan_mask = np.where(np.isnan(slab), 1, 0)
    if not hasattr(slab, 'mask'):
        mask_mask = np.zeros(slab.shape)
    else:
        if slab.mask.size == 1 and slab.mask == False:
            mask_mask = np.zeros(slab.shape)
        else:
            mask_mask = np.where(slab.mask, 1, 0)
    mask = np.where(mask_mask+nan_mask > 0, 1, 0)

    return mask


def getQuantiles(slab, quantiles=None, verbose=True):
    '''Find quantiles of a slab

    Args:
        slab (ndarray): input ndarray whose quantiles will be found.
    Keyword Args:
        quantiles (float or a list of floats): desired quantiles(s).
    Returns:
        results (ndarray): 1darray, left quantiles
    '''

    if quantiles is None:
        quantiles = np.array([0.001, 0.005, 0.01, 0.025, 0.05, 0.1])
    quantiles = np.atleast_1d(quantiles)
    if quantiles.ndim != 1:
        raise Exception("<quantiles> needs to be a 1D array.")

    results = np.nanquantile(slab, quantiles)
    if verbose:
        for ii, pii in enumerate(quantiles):
            print('# <getQuantiles>: %0.3f left quantile: %f.'
                  % (pii, results[ii]))
    return results


def getRange(vars, min_level=None, max_level=None, ql=None, qr=None,
             verbose=True):
    '''Get min/max value

    Args:
        vars (list): a list of ndarrays.
    Keyword Args:
        min_level (None or float): given minimum level.
        max_level (None or float): given maximum level.
        ql (None or float): given left quantile.
        qr (None or float): given right quantile.
    Returns:
        vmin (float): lowest level to take from variables.
        vmax (float): highest level to take from variables.
        data_min (float): lowest level among variables.
        data_max (float): highest level among variables.
    '''

    # -------------------Cat all vars-------------------
    for ii, vii in enumerate(vars):
        vii = vii.flatten()
        maskii = getMissingMask(vii)
        vii = np.where(maskii, np.nan, vii)
        if ii == 0:
            var_all = vii
        else:
            var_all = np.concatenate((var_all, vii), axis=0)

    # ------------------Get quantiles------------------
    if ql is not None or qr is not None:
        if ql is not None:
            left_quantile = getQuantiles(var_all, ql, verbose)[0]
        if qr is not None:
            right_quantile = getQuantiles(var_all, 1-qr, verbose)[0]

    # -------Get min/max from all vars-----------------
    data_min = np.nanmin(var_all)
    data_max = np.nanmax(var_all)

    # ----------------Set lower boundary----------------
    if min_level is not None and ql is None:
        vmin = max(data_min, min_level)
    elif min_level is None and ql is not None:
        vmin = left_quantile
    elif min_level is not None and ql is not None:
        vmin = max(data_min, min_level, left_quantile)
    else:
        vmin = data_min

    # ----------------Set upper boundary----------------
    if max_level is not None and qr is None:
        vmax = min(data_max, max_level)
    elif max_level is None and qr is not None:
        vmax = right_quantile
    elif max_level is not None and qr is not None:
        vmax = min(data_max, max_level, right_quantile)
    else:
        vmax = data_max

    if vmax < vmin:
        vmin, vmax = vmax, vmin

    return vmin, vmax, data_min, data_max

# -----------------------------------------------------------------------
# -                       Plotting method classes                       -
# -----------------------------------------------------------------------


class TwoSlopeNorm(Normalize):
    def __init__(self, vcenter, vmin=None, vmax=None):
        """
        Normalize data with a set center.

        Useful when mapping data with an unequal rates of change around a
        conceptual center, e.g., data that range from -2 to 4, with 0 as
        the midpoint.

        Parameters
        ----------
        vcenter : float
            The data value that defines ``0.5`` in the normalization.
        vmin : float, optional
            The data value that defines ``0.0`` in the normalization.
            Defaults to the min value of the dataset.
        vmax : float, optional
            The data value that defines ``1.0`` in the normalization.
            Defaults to the the max value of the dataset.

        Examples
        --------
        This maps data value -4000 to 0., 0 to 0.5, and +10000 to 1.0; data
        between is linearly interpolated::

            >>> import matplotlib.colors as mcolors
            >>> offset = mcolors.TwoSlopeNorm(vmin=-4000.,
                                              vcenter=0., vmax=10000)
            >>> data = [-4000., -2000., 0., 2500., 5000., 7500., 10000.]
            >>> offset(data)
            array([0., 0.25, 0.5, 0.625, 0.75, 0.875, 1.0])
        """

        self.vcenter = vcenter
        self.vmin = vmin
        self.vmax = vmax
        if vcenter is not None and vmax is not None and vcenter >= vmax:
            raise ValueError('vmin, vcenter, and vmax must be in '
                             'ascending order')
        if vcenter is not None and vmin is not None and vcenter <= vmin:
            raise ValueError('vmin, vcenter, and vmax must be in '
                             'ascending order')

    def autoscale_None(self, A):
        """
        Get vmin and vmax, and then clip at vcenter
        """
        super().autoscale_None(A)
        if self.vmin > self.vcenter:
            self.vmin = self.vcenter
        if self.vmax < self.vcenter:
            self.vmax = self.vcenter

    def __call__(self, value, clip=None):
        """
        Map value to the interval [0, 1]. The clip argument is unused.
        """
        result, is_scalar = self.process_value(value)
        self.autoscale_None(result)  # sets self.vmin, self.vmax if None

        if not self.vmin <= self.vcenter <= self.vmax:
            raise ValueError("vmin, vcenter, vmax must increase monotonically")
        result = np.ma.masked_array(
            np.interp(result, [self.vmin, self.vcenter, self.vmax],
                      [0, 0.5, 1.]), mask=np.ma.getmask(result))
        if is_scalar:
            result = np.atleast_1d(result)[0]
        return result


class PlotMethod(object):
    '''Base plotting method class'''
    def __init__(self, vars, split=2, min_level=None, max_level=None,
                 ql=None, qr=None, vcenter=0, cmap=None, verbose=True):
        '''Base plotting method class

        Args:
            vars (ndarray or list): if ndarray, input data to create 2d plot
                from. If list, a list of ndarrays.
        Keyword Args:
            split (int): whether to split the colormap at a given value (<vcenter>) into
                2 parts or not. Can be 1 of these 3 values:
                0: do not split.
                1: split at <vcenter> only if range of data in <vars> strides
                   <vcenter>.
                2: force split at <vcenter>.
                If split and data range strides across <vcenter>, will use
                the lower half of the colormap for values <= <vcenter>, the
                upper half of the colormap for values >= <vcenter>.
                If split and data range on 1 side of <vcenter>, will only use
                only half of the colormap range, depending on whether data
                are on which side of <vcenter>.
            min_level (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            max_level (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <min_level> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <max_level> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            verbose (bool): whether to print some info or not.
        '''

        self.split = split
        self.min_level = min_level
        self.max_level = max_level
        self.ql = ql
        self.qr = qr
        self.vcenter = vcenter
        self.cmap = cmap
        self.method = 'base'

        if split not in [0, 1, 2]:
            raise Exception("<split> not in [0,1,2].")
        if ql is not None and (ql < 0 or ql > 1):
            raise Exception("<ql> needs to be a float in [0, 1].")
        if qr is not None and (qr < 0 or qr > 1):
            raise Exception("<qr> needs to be a float in [0, 1].")
        if ql is not None and qr is not None and ql < qr:
            raise Exception("<ql> should be < <qr>.")

        if not isinstance(vars, (list, tuple)):
            vars = [vars, ]
        self.vars = vars

    def computeRange(self):
        '''Get the range of data and the range to plot'''

        # -------------------Get max/min-------------------
        self.vmin, self.vmax, self.data_min, self.data_max = getRange(
            self.vars, self.min_level, self.max_level, self.ql, self.qr)

    def computeExt(self, vmin, vmax):
        '''Determine overflow on both ends'''

        self.ext_1 = True if self.data_min < vmin else False
        self.ext_2 = True if self.data_max > vmax else False

        return

    def adjustColormap(self, vmin, vmax):
        '''Adjust colormap for split and get normalization for colormap

        Args:
            vmin,vmax (float or None): min and max value to plot.
        Returns:
            cmap (matplotlib colormap): adjusted colormap.
                If <self.split> and <vmin>,<vmax> stride across <self.vcenter>, will use
                the lower half of the colormap for values <= <vcenter>, the
                upper half of the colormap for values >= <vcenter>.
                If <split.split> and <vmin>,<vmax> on 1 side of <vcenter>, will only use
                only half of the colormap range, depending on whether data
                are on which side of <vcenter>.
            norm (TwoSlopeNorm or None): only if split the entire colormap, return
                a TwoSlopeNorm. Otherwise return None.
        '''

        cmap = self.cmap

        if self.split == 0:
            norm = None

        if self.split == 1 and (vmin-self.vcenter)*(vmax-self.vcenter) >= 0:
            norm = None

        if self.split == 1 and (vmin-self.vcenter)*(vmax-self.vcenter) < 0:
            norm = TwoSlopeNorm(self.vcenter, vmin, vmax)

        if self.split == 2:
            if vmin < self.vcenter and vmax <= self.vcenter:
                cmap = remappedColorMap2(self.cmap, vmin, vmax, self.vcenter)
                norm = None

            if vmin >= self.vcenter and vmax > self.vcenter:
                cmap = remappedColorMap2(self.cmap, vmin, vmax, self.vcenter)
                norm = None

            if (vmin-self.vcenter)*(vmax-self.vcenter) < 0:
                norm = TwoSlopeNorm(self.vcenter, vmin, vmax)

        return cmap, norm


class Isofill(PlotMethod):
    '''Plotting method for isofill/contourf plots'''
    def __init__(self, vars, num=15, zero=1, split=1, levels=None,
                 min_level=None, max_level=None, ql=None, qr=None,
                 vcenter=0, cmap=None,
                 stroke=False, stroke_color='0.3', stroke_lw=0.2,
                 stroke_linestyle='-',
                 verbose=True):
        '''Plotting method for isofill/contourf plots

        Args:
            vars (ndarray or list): if ndarray, input data to create 2d plot
                from. If list, a list of ndarrays.
        Keyword Args:
            num (int): the desired number of contour levels. NOTE that the
                resultant number may be slightly different.
            zero (int): whether 0 is allowed to be a contour level. -1 for not allowed,
                0 or 1 otherwise.
            split (int): whether to split the colormap at a given value (<vcenter>) into
                2 parts or not. Can be 1 of these 3 values:
                0: do not split.
                1: split at <vcenter> only if range of data in <vars> strides
                   <vcenter>.
                2: force split at <vcenter>.
                If split and data range strides across <vcenter>, will use
                the lower half of the colormap for values <= <vcenter>, the
                upper half of the colormap for values >= <vcenter>.
                If split and data range on 1 side of <vcenter>, will only use
                only half of the colormap range, depending on whether data
                are on which side of <vcenter>.
            levels (list, tuple or 1darray): specified contour levels. If not
                given, compute contour levels using <num>, <zero>, <min_level>,
                <max_level>, <ql>, <qr>.
            min_level (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            max_level (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <min_level> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <max_level> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            stroke (bool): whether to overlay a layer of thin contour lines on
                top of contourf.
            stroke_color (str or color tuple): color to plot the overlying
                thin contour lines.
            stroke_lw (float): line width to plot the overlying thin contour
                lines.
            stroke_linestyle (str): line style to plot the overlying thin
                contour lines.
            verbose (bool): whether to print some info or not.
        '''

        super(
            Isofill, self).__init__(
            vars, split=split, min_level=min_level, max_level=max_level, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.num = num
        self.zero = zero
        self.levels = levels
        self.stroke = stroke
        self.stroke_color = stroke_color
        self.stroke_lw = stroke_lw
        self.stroke_linestyle = stroke_linestyle
        self.method = 'isofill'

        # --------------------Get levels--------------------
        self.computeRange()

        if self.levels is None:
            self.levels = mkscale(self.vmin, self.vmax, self.num, self.zero)

        self.computeExt(np.min(self.levels), np.max(self.levels))

        # -------------------Get colormap-------------------
        self.cmap = getColormap(self.cmap)
        self.cmap, self.norm = self.adjustColormap(vmin=np.min(self.levels),
                                                   vmax=np.max(self.levels))
        # self.cmap = LinearSegmentedColormap('new_cmp2',
        # self.cmap._segmentdata,
        # N=len(self.levels)-1)

        return


class Isoline(Isofill):
    '''Plotting method for isoline/contour plots'''
    def __init__(self, vars, num=15, zero=1, split=1, levels=None,
                 min_level=None, max_level=None, ql=None, qr=None,
                 vcenter=0, cmap=None,
                 black=False, color=None, linewidth=1.0, alpha=1.0,
                 dash_negative=True, bold_lines=None,
                 label=False, label_fmt=None, label_box=False, label_box_color='w',
                 verbose=True):
        '''Plotting method for isoline/contour plots

        Args:
            vars (ndarray or list): if ndarray, input data to create 2d plot
                from. If list, a list of ndarrays.
        Keyword Args:
            num (int): the desired number of contour levels. NOTE that the
                resultant number may be slightly different.
            zero (int): whether 0 is allowed to be a contour level. -1 for not allowed,
                0 or 1 otherwise.
            split (int): whether to split the colormap at a given value (<vcenter>) into
                2 parts or not. Can be 1 of these 3 values:
                0: do not split.
                1: split at <vcenter> only if range of data in <vars> strides
                   <vcenter>.
                2: force split at <vcenter>.
                If split and data range strides across <vcenter>, will use
                the lower half of the colormap for values <= <vcenter>, the
                upper half of the colormap for values >= <vcenter>.
                If split and data range on 1 side of <vcenter>, will only use
                only half of the colormap range, depending on whether data
                are on which side of <vcenter>.
            levels (list, tuple or 1darray): specified contour levels. If not
                given, compute contour levels using <num>, <zero>, <min_level>,
                <max_level>, <ql>, <qr>.
            min_level (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            max_level (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <min_level> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <max_level> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            black (bool): use black lines instead of colored lines.
            color (str or color tuple): color to plot the contour lines.
            linewidth (float): line width to plot the contour lines.
            alpha (float): transparent level, in range of [0, 1].
            dash_negative (bool): whether to use dashed lines for negative
                contours.
            bols_lines (list if None): if a list, values to highlight using bold lines
                (line width scaled by 2.0).
            label (bool): whether to label the contour lines or not.
            label_fmt (str or dict or None): if <label> is True, format string to format
                contour levels. E.g. '%0.2f'. If None, automatically derive
                a format suitable for the contour levels.
            label_box (bool): whether to put contour labels in a bounding box
                with background color or not.
            label_box_color (str or color tuple): if <label_box> is True, the
                background color for the bounding boxes for the labels.
            verbose (bool): whether to print some info or not.
        '''

        super(
            Isoline, self).__init__(
            vars, num=num, zero=zero, split=split, levels=levels,
            min_level=min_level, max_level=max_level, ql=ql, qr=qr,
            vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.black = black
        self.color = color
        self.linewidth = linewidth
        self.alpha = alpha
        self.dash_negative = dash_negative
        self.bold_lines = bold_lines
        self.method = 'isoline'
        self.label = label
        self.label_fmt = label_fmt
        self.label_box = label_box
        self.label_box_color = label_box_color

        return


class Boxfill(PlotMethod):
    '''Plotting method for boxfill/imshow plots'''
    def __init__(self, vars, split=2, min_level=None, max_level=None,
                 ql=None, qr=None, vcenter=0, cmap=None, verbose=True):
        '''Plotting method for boxfill/imshow plots

        Args:
            vars (ndarray or list): if ndarray, input data to create 2d plot
                from. If list, a list of ndarrays.
        Keyword Args:
            split (int): whether to split the colormap at a given value (<vcenter>) into
                2 parts or not. Can be 1 of these 3 values:
                0: do not split.
                1: split at <vcenter> only if range of data in <vars> strides
                   <vcenter>.
                2: force split at <vcenter>.
                If split and data range strides across <vcenter>, will use
                the lower half of the colormap for values <= <vcenter>, the
                upper half of the colormap for values >= <vcenter>.
                If split and data range on 1 side of <vcenter>, will only use
                only half of the colormap range, depending on whether data
                are on which side of <vcenter>.
            levels (list, tuple or 1darray): specified contour levels. If not
                given, compute contour levels using <num>, <zero>, <min_level>,
                <max_level>, <ql>, <qr>.
            min_level (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            max_level (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <min_level> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <max_level> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            verbose (bool): whether to print some info or not.
        '''

        super(
            Boxfill, self).__init__(
            vars, split=split, min_level=min_level, max_level=max_level, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.method = 'boxfill'

        self.computeRange()
        self.computeExt(self.vmin, self.vmax)
        self.cmap = getColormap(self.cmap)
        self.norm = self.adjustColormap(vmin=self.vmin, vmax=self.vmax)


class Pcolor(Boxfill):
    '''Plotting method for pcolormesh plots'''
    def __init__(self, vars, split=2, min_level=None, max_level=None,
                 ql=None, qr=None, vcenter=0, cmap=None, verbose=True):
        '''Plotting method for pcolormesh plots

        Args:
            vars (ndarray or list): if ndarray, input data to create 2d plot
                from. If list, a list of ndarrays.
        Keyword Args:
            split (int): whether to split the colormap at a given value (<vcenter>) into
                2 parts or not. Can be 1 of these 3 values:
                0: do not split.
                1: split at <vcenter> only if range of data in <vars> strides
                   <vcenter>.
                2: force split at <vcenter>.
                If split and data range strides across <vcenter>, will use
                the lower half of the colormap for values <= <vcenter>, the
                upper half of the colormap for values >= <vcenter>.
                If split and data range on 1 side of <vcenter>, will only use
                only half of the colormap range, depending on whether data
                are on which side of <vcenter>.
            levels (list, tuple or 1darray): specified contour levels. If not
                given, compute contour levels using <num>, <zero>, <min_level>,
                <max_level>, <ql>, <qr>.
            min_level (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            max_level (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <min_level> if given. If both <min_level> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <max_level> if given. If both <max_level> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            verbose (bool): whether to print some info or not.
        '''

        super(
            Pcolor, self).__init__(
            vars, split=split, min_level=min_level, max_level=max_level, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.method = 'pcolor'


class Hatch(object):
    '''Plotting method for hatching plots'''
    def __init__(self, hatch='.', alpha=0.7):
        '''Plotting method for hatching plots

        Keyword Args:
            hatch (str): style of hatching. Choices:
            '.', '/', '//', '\\', '\\\\', '*', '-', '+', 'x', 'o', 'O'
            alpha (float): transparent level, in range of [0, 1].
        '''
        self.hatch = hatch
        self.alpha = alpha
        self.method = 'hatch'


class Shading(object):
    '''Plotting method for shading plots'''
    def __init__(self, color='0.5', alpha=0.5):
        '''Plotting method for shading plots

        Keyword Args:
            color (str or color tuple): color of shading.
            alpha (float): transparent level, in range of [0, 1].
        '''

        self.color = color
        self.alpha = alpha
        self.method = 'shading'

        cdict = {'red': [(0, 1, 1), ],
                 'green': [(0, 1, 1), ],
                 'blue': [(0, 1, 1), ],
                 'alpha': [(0, 0, 0), ]
                 }
        r, g, b, a = colors.ColorConverter.to_rgba(color)
        cdict['red'].append((1, r, r))
        cdict['green'].append((1, g, g))
        cdict['blue'].append((1, b, b))
        cdict['alpha'].append((1, alpha, alpha))

        c = [(r, g, b, 1), ]

        self.cmap = colors.ListedColormap(c)


class GIS(object):
    '''Plotting method for GIS plots'''
    def __init__(self, xpixels=2000, dpi=96, verbose=True):
        '''Plotting method for GIS plots

        Keyword Args:
            xpixels (int): plot size.
            dpi (int): dpi.
            verbose (bool): whats this?
        '''
        self.xpixels = xpixels
        self.dpi = dpi
        self.verbose = verbose
        self.args = {'xpixels': xpixels, 'dpi': dpi, 'verbose': verbose}
        self.method = 'gis'


class Quiver(object):
    '''Plotting method for quiver plots'''
    def __init__(self, step=1, reso=None, scale=None, keylength=None,
                 linewidth=0.0015, color='k', alpha=1.0):
        '''Plotting method for quiver plots

        Keyword Args:
            step (int): sub-sample steps in both x- and  y- axes. U and V
                data are sub-sampled using `U[::step,::step]`.
            reso (int or None): if not None, regrid input U and V data to a
                lower resolution, measured in grids.
                If both < reso > and <step> are given, use <reso>.
                Requires scipy for this functionality.
            scale (float or None): see same arg as matplotlib.pyplot.quiver().
            keylength (float or None): see same arg as matplotlib.pylot.quiver().
            linewidth (float): line width.
            color (str or color tuple): color to plot quiver arrows.
            alpha (float): transparent level in [0, 1].
        '''

        self.method = 'quiver'
        self.step = step
        self.reso = reso
        self.scale = scale
        self.keylength = keylength
        self.linewidth = linewidth
        self.color = color
        self.alpha = alpha


# -----------------------------------------------------------------------
# -                       Base 2D plotting class                        -
# -----------------------------------------------------------------------


class Plot2D(object):
    '''Base 2D plotting class

    For geographical plots, see Plot2Basemap or Plot2Cartopy,
    which handles equivalent plotting with geographical map projections.
    '''

    def __init__(self, var, method, ax=None, xarray=None, yarray=None,
                 title=None, label_axes=True, axes_grid=False, legend='global',
                 legend_ori='horizontal', clean=False, fontsize=None,
                 fill_color=None):
        '''
        Args:
            var (ndarray): input data to plot. Determines what to plot.
                Mush have dimensions >= 2.
                For data with rank>2, take the slab from the last 2 dimensions.
            method (PlotMethod): plotting method. Determines how to plot.
                Could be Isofill, Isoline, Boxfill, Quiver, Shading, Hatch, GIS.
        Keyword Args:
            ax (matplotlib axis or None): axis obj. Determines where to plot.
                If None, create a new.
            xarray (1darray or None): array to use as the x-coordinates. If None,
                use the indices of the last dimension: np.arange(slab.shape[-1]).
            yarray (1darray or None): array to use as the y-coordinates. If None,
                use the indices of the 2nd last dimension: np.arange(slab.shape[-2]).
            title (str or None): text as the figure title if <ax> is the
                single plot in the figure. If None, automatically
                get an alphabetic subtitle if <ax> is a subplot, e.g. '(a)'
                for the 1st subplot, '(d)' for the 4th one. If str and <ax>
                is a subplot, prepend <title> with the alphabetic index.
                One can force overriding the alphabetic index by giving a title
                str in the format of '(x) xxxx', e.g. '(p) subplot-p'.
            label_axes (bool or 'all' or tuple): controls axis ticks and
                ticklabels. If True, don't exert any inference other than
                changing the ticklabel fontsize, and let matplotlib put the
                ticks and ticklabels (i.e. default only left and bottom axes).
                If False, turn off all ticks and ticklabels.
                If 'all', plot ticks and ticks labels on all 4 sides.
                If (left, right, top, bottom),
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
            fill_color (str or color tuple): color to use as background color.
                If data have missings, they will be shown as this color.
                It is better to use a grey than while to better distinguish missings.
        '''

        # get kwargs
        fill_color = fill_color or rcParams['fill_color']
        title = title or rcParams['title']
        label_axes = label_axes or rcParams['label_axes']
        axes_grid = axes_grid or rcParams['axes_grid']
        fontsize = fontsize or rcParams['fontsize']
        clean = clean or rcParams['clean']
        legend = legend or rcParams['legend']
        legend_ori = legend_ori or rcParams['legend_ori']

        self.var = var
        self.method = method
        self.ax = ax or plt.subplot(111)
        self.xarray = xarray
        self.yarray = yarray

        self.title = title
        self.label_axes = label_axes
        self.axes_grid = axes_grid
        self.legend = legend
        self.legend_ori = legend_ori
        self.clean = clean
        self.fontsize = fontsize
        self.fill_color = fill_color

        self._transform = None  # to be overwriten by Plot2Cartopy

        # ---------------------Get slab---------------------
        self.var = getSlab(self.var)

        # ---------------------Get grid---------------------
        self.xarray, self.yarray, self.lons, self.lats = self.getGrid()

        # ---------------Get geo and fontsize---------------
        self.geo, self.subidx, self._fontsize = self.getGeo()

        # Store a singleton record to avoid the ax.get_geometry() result
        # get changes after creating a local colorbar:
        if not hasattr(self.ax, '_gplot_geo'):
            self.ax._gplot_geo = self.geo + (self.subidx,)

    # ---------------------Get grid---------------------

    def getGrid(self):
        '''Get x- and y- coordnates

        Returns:
            xarray (1darray): 1d array of the x-coordinates.
            yarray (1darray): 1d array of the y-coordinates.
            lons,lats (ndarray): 2d array of the x- and y- coordinates, as
                created from `lons, lats = np.meshgrid(xarray, yarray)`.
        '''

        if self.yarray is None:
            yarray = np.arange(self.var.shape[0])
        else:
            yarray = np.array(self.yarray)

        if self.xarray is None:
            xarray = np.arange(self.var.shape[1])
        else:
            xarray = np.array(self.xarray)

        if len(yarray) != self.var.shape[0]:
            raise Exception("X-axis dimention does not match")
        if len(xarray) != self.var.shape[1]:
            raise Exception("Y-axis dimention does not match")

        lons, lats = np.meshgrid(xarray, yarray)

        return xarray, yarray, lons, lats

    def getGeo(self):
        '''Get geometry layout of the axis and font size

        Returns:
            geo (nrows, ncols): subplot layout of the figure.
            subidx (int): index of the axis obj in the (nrows, ncols) layout.
                i.e. 1 for the 1st subplot.
            fontsize (int): default font size. This is determined from an
                empirical formula that scales down the default font size
                for a bigger grid layout.
        '''

        geo = self.ax.get_geometry()[:2]
        subidx = self.ax.get_geometry()[-1]
        scale = 1./max(geo)
        fontsize = 7*scale+self.fontsize  # empirical

        return geo, subidx, fontsize

    @classmethod
    def getExtend(cls, method):
        '''Get colorbar overflow on both ends

        Returns:
            extend (str): 'both', 'min', 'max' or 'neither'. Determined
                from the method obj.
        '''

        if method.ext_1 is False and method.ext_2 is False:
            extend = 'neither'
        elif method.ext_1 is True and method.ext_2 is False:
            extend = 'min'
        elif method.ext_1 is False and method.ext_2 is True:
            extend = 'max'
        else:
            extend = 'both'

        return extend

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
        self.plotAxes()
        self.cbar = self.plotColorbar()
        self.plotTitle()

        return self.cs

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

        # ------------------shading contourf------------------
        elif self.method.method == 'shading':
            cs = self._plotShading()

        return cs

    def _plotIsofill(self):
        '''Core plotting function, isofill/contourf'''

        extend = Plot2D.getExtend(self.method)

        cs = self.ax.contourf(
            self.lons, self.lats, self.var, self.method.levels,
            cmap=self.method.cmap, extend=extend, norm=self.method.norm,
            transform=self._transform)

        if self.method.stroke:
            nl = len(self.method.levels)
            css = self.ax.contour(
                self.lons, self.lats, self.var, self.method.levels,
                colors=[self.method.stroke_color, ]*nl,
                linestyles=[self.method.stroke_linestyle, ]*nl,
                linewidths=[self.method.stroke_lw, ]*nl,
                transform=self._transform
            )
            self.css = css

        return cs

    def _plotIsoline(self):
        '''Core plotting function, isoline/contour'''

        extend = Plot2D.getExtend(self.method)

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
            transform=self._transform)

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

    def plotContourLabels(self, cs):

        if self.method.label_fmt is None:
            # save the old xaxis formatter
            old_formatter = self.ax.xaxis.get_major_formatter()
            # get a new scalar formatter
            formatter = ticker.ScalarFormatter()
            # for some reason one needs to set as major and call format_ticks()
            # before this thing can do formatter(value)
            self.ax.xaxis.set_major_formatter(formatter)
            formatter.format_ticks(cs.levels)
            clabels = cs.clabel(inline=1, fmt=formatter)
            # restore old xaxis formatter
            self.ax.xaxis.set_major_formatter(old_formatter)
        else:
            clabels = cs.clabel(inline=1, fmt=self.method.label_fmt)

        if self.method.label_box:
            [txt.set_bbox(dict(facecolor=self.method.label_box_color,
                edgecolor='none', pad=0)) for txt in clabels]

        return


    def _plotBoxfill(self):
        '''Core plotting function, boxfill/imshow'''

        cs = self.ax.imshow(
            self.var, cmap=self.method.cmap, origin='lower',
            vmin=self.method.vmin, vmax=self.method.vmax,
            interpolation='nearest',
            extent=[self.xarray.min(),
                    self.xarray.max(),
                    self.yarray.min(),
                    self.yarray.max()],
            aspect='auto')

        return cs

    def _plotPcolor(self):
        '''Core plotting function, pcolormesh'''

        cs = self.ax.pcolormesh(
            self.lons, self.lats, self.var, cmap=self.method.cmap,
            vmin=self.method.vmin,
            vmax=self.method.vmax)

        return cs

    def _plotHatch(self):
        '''Core plotting function, pattern hatching'''

        # nlevel=3 necessary?
        if np.all(self.var == 0):
            nlevel = 1
        else:
            nlevel = 3
        cs = self.ax.contourf(
            self.lons[0, :],
            self.lats[:, 0],
            self.var, nlevel, colors='none',
            hatches=[None, self.method.hatch],
            alpha=0.)

        return cs

    def _plotShading(self):
        '''Core plotting function, color shading'''

        pvar = np.where(self.var == 1, 1, np.nan)
        cs = self.ax.contourf(
            self.lons,
            self.lats,
            pvar, 1, cmap=self.method.cmap,
            alpha=self.method.alpha,
            transform=self._transform)

        return cs

    def getLabelBoolForShareXY(self, geo, idx):
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

    def getLabelBool(self):
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
            parallels, meridians = self.getLabelBoolForShareXY(
                    self.ax._gplot_geo[:-1], self.subidx)

        return parallels, meridians

    def plotAxes(self):
        '''Plot axes ticks and ticklabels'''

        if self.axes_grid:
            self.ax.grid(True)

        if self.label_axes == True:
            self.ax.tick_params(axis='both', which='major',
                                labelsize=self._fontsize)

        # --------Turn off lat/lon labels if required--------
        if self.clean or not self.label_axes:
            self.ax.tick_params(left=False, labelleft=False, right=False,
                                labelright=False, top=False, labeltop=False,
                                bottom=False, labelbottom=False)
            return

        parallels, meridians = self.getLabelBool()

        # get tick labels
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

        return

    def alternateTicks(self, cbar, ticks):
        '''Create alternating ticks and ticklabels for colorbar

        Args:
            cbar (matplotlib colorbar obj): input colorbar obj to alter.
            ticks (list or array): ticks of the colorbar.
        Returns:
            cbar (matplotlib colorbar obj): the altered colorbar.

        Only works for horizontal colorbar with discrete ticks. As vertical
        colorbar doesn't tend to have overlapping tick labels issue.
        '''

        if self.legend_ori == 'vertical':
            cbar.set_ticks(ticks)
            # skip vertical colorbar as digits are less likely to overlap
            return cbar

        lbot = ticks[1:][::2]  # labels at bottom
        ltop = ticks[::2]  # labels on top

        # -------------Print bottom tick labels-------------
        '''
        # NOTE this twin axis method doesn't work for local legend.
        # Add twin axes
        cax2 = cbar.ax.twiny()
        cax2.set_frame_on(False)

        # get current positions and values of the ticks.
        # OR you can skip this part and set your own ticks instead.
        xt = cbar.ax.get_xticks()
        xtl = [i.get_text() for i in cax.get_xticklabels()]

        # set odd ticks on top (twin axe)
        cax2.set_xticks(xt[::2])
        cax2.set_xticklabels(xtl[::2], fontsize=self.fontsize)
        # set even ticks on  original axes (note the different object : cb != cax)
        cbar.set_ticks(lbot)
        #cb.set_ticklabels(xtl[::2])
        '''

        # tick all to get label text strings first
        cbar.set_ticks(ticks)
        formatter = cbar.ax.xaxis.get_major_formatter()
        ticklabels = formatter.format_ticks(ticks)

        # tick bottom
        cbar.set_ticks(lbot)

        # --------------Print top tick labels--------------
        vmin = cbar.norm.vmin
        vmax = cbar.norm.vmax

        # ---------Compute top line tick locations---------
        # need to take into account the overflow triangle
        # by default the triangle is 5% of axis length
        if cbar.extend == 'min':
            shift_l = 0.05
            scaling = 0.95
        elif cbar.extend == 'max':
            shift_l = 0.
            scaling = 0.95
        elif cbar.extend == 'both':
            shift_l = 0.05
            scaling = 0.90
        else:
            shift_l = 0.
            scaling = 1.

        if self.legend_ori == 'horizontal':
            for ii in range(len(ticklabels[::2])):
                tii = ltop[ii]
                tlii = ticklabels[::2][ii]
                xii = shift_l+scaling*(tii-vmin)/(vmax-vmin)
                # plot ticks
                cbar.ax.plot([xii, xii],
                             [1.0, 1.35],
                             'k-', linewidth=0.5,
                             clip_on=False,
                             transform=cbar.ax.transAxes)

                # plot tick labels
                cbar.ax.text(xii,
                             1.25, tlii,
                             transform=cbar.ax.transAxes, va='bottom',
                             ha='center', fontsize=self._fontsize)

        return cbar

    def plotColorbar(self):
        '''Plot colorbar

        Returns:
            cbar (matplotlib colorbar obj): colorbar obj.

        Only creates a colorbar for isofill/contourf or isoline/contour plots.
        '''

        if self.method.method in ['hatch', 'shading']:
            return

        if self.legend is None:
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
            extend = Plot2D.getExtend(self.method)
        else:
            ticks = getattr(self.method, 'levels', None)
            extend = None

        if self.legend == 'global' and self.subidx > 1:
            return

        # --------------Create a colorbar axis--------------
        if self.legend == 'local' or (
                self.legend == 'global' and self.geo[0] * self.geo[1] == 1):

            if self.method.method in ['boxfill', 'pcolor']:

                # Adjust position according to the existence of axis ticks
                pad = getColorbarPad(self.ax, self.legend_ori, base_pad=0.02)
                # NOTE: mcbar.make_axes() doesn't work well with tight_layout()

            elif self.method.method in ['isofill', 'isoline']:
                if self.legend_ori == 'horizontal':
                    # compute extra padding needed for the top side tick labels
                    dummybox = createDummyTextBox(self.ax, self._fontsize)
                    pad = getColorbarPad(
                        self.ax, self.legend_ori, base_pad=dummybox.height*1.5)
                else:
                    pad = getColorbarPad(
                        self.ax, self.legend_ori, base_pad=0.02)

            cax, kw = mcbar.make_axes_gridspec(
                self.ax, orientation=self.legend_ori, shrink=0.85, pad=pad,
                fraction=0.07, aspect=35)

        # -----Use the 1st subplot as global color bar-----
        elif self.legend == 'global' and self.subidx == 1:

            fig = self.ax.get_figure()
            subplots = list(filter(lambda x: isinstance(x, matplotlib.axes.SubplotBase), fig.axes))

            if self.legend_ori == 'horizontal':
                if len(subplots) > 1:
                    if fig.get_constrained_layout():
                        cax, kw = mcbar.make_axes(
                            subplots, orientation=self.legend_ori, shrink=0.85,
                            pad=0.01, fraction=0.07, aspect=35)
                    else:
                        dummybox = createDummyTextBox(self.ax, self._fontsize)
                        pad = dummybox.height*1.2
                        cax, kw = mcbar.make_axes(
                            subplots, orientation=self.legend_ori, shrink=0.85,
                            pad=pad, fraction=0.07, aspect=35)
                else:
                    dummybox = createDummyTextBox(self.ax, self._fontsize)
                    pad = dummybox.height*1.2
                    height = 0.02
                    fig.subplots_adjust(bottom=0.18)
                    cax = self.ax.get_figure().add_axes(
                        [0.175, 0.18-height-pad, 0.65, height])

            elif self.legend_ori == 'vertical':
                if len(subplots) > 1:
                    cax, kw = mcbar.make_axes(
                        subplots, orientation=self.legend_ori, shrink=0.85,
                        pad=0.02, fraction=0.07, aspect=35)
                else:
                    fig.subplots_adjust(right=0.90)
                    cax = self.ax.get_figure().add_axes(
                        [0.95, 0.20, 0.02, 0.6])

        # ------------------Plot colorbar------------------
        cbar = plt.colorbar(
            self.cs, cax=cax, orientation=self.legend_ori,
            ticks=ticks,
            drawedges=isdrawedges, extend=extend)

        # -------------------Re-format ticks-------------------
        if self.method.method in [
                'isofill', 'isoline'] and self.legend_ori == 'horizontal':
            cbar = self.alternateTicks(cbar, ticks)
        cbar.ax.tick_params(labelsize=self._fontsize)

        # --------------------Plot unit--------------------
        var_units = getattr(self.var, 'units', '')
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

    def plotTitle(self):
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

        geo=self.ax._gplot_geo[:-1]

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


class Plot2Quiver(Plot2D):
    '''2D vector plotting class

    For geographical vector plots, see Plot2QuiverBasemap or Plot2QuiverCartopy,
    which handles equivalent plotting with geographical map projections.
    '''

    def __init__(
            self, u, v, method, ax=None, xarray=None, yarray=None,
            title=None, label_axes=True, axes_grid=False,
            clean=False, fontsize=None, units=None, fill_color='w',
            curve=False):
        '''
        Args:
            u,v (ndarray): x- and y-component of velocity to plot.
                Mush have dimensions >= 2. For data with rank>2, take the slab
                from the last 2 dimensions.
            method (Quiver obj): quiver plotting method. Determines how to plot
                the quivers.
        Keyword Args:
            ax (matplotlib axis or None): axis obj. Determines where to plot.
                If None, create a new.
            xarray (1darray or None): array to use as the x-coordinates. If None,
                use the indices of the last dimension: np.arange(slab.shape[-1]).
            yarray (1darray or None): array to use as the y-coordinates. If None,
                use the indices of the 2nd last dimension: np.arange(slab.shape[-2]).
            title (str or None): text as the figure title if <ax> is the
                single plot in the figure. If None, automatically
                get an alphabetic subtitle if <ax> is a subplot, e.g. '(a)'
                for the 1st subplot, '(d)' for the 4th one. If str and <ax>
                is a subplot, prepend <title> with the alphabetic index.
                One can force overriding the alphabetic index by giving a title
                str in the format of '(x) xxxx', e.g. '(p) subplot-p'.
            label_axes (bool or 'all' or tuple): controls axis ticks and
                ticklabels. If True, don't exert any inference other than
                changing the ticklabel fontsize, and let matplotlib put the
                ticks and ticklabels (i.e. default only left and bottom axes).
                If False, turn off all ticks and ticklabels.
                If 'all', plot ticks and ticks labels on all 4 sides.
                If (left, right, top, bottom),
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
            units (str or None): unit of <u> and <v>. Will be plotted next to
                the reference vector.
            fill_color (str or color tuple): color to use as background color.
                If data have missings, they will be shown as this color.
            curve (bool): whether to plot quivers as curved vectors. Experimental.
        '''

        fill_color = fill_color or rcParams['fill_color']
        title = title or rcParams['title']
        label_axes = label_axes or rcParams['label_axes']
        axes_grid = axes_grid or rcParams['axes_grid']
        fontsize = fontsize or rcParams['fontsize']
        clean = clean or rcParams['clean']

        Plot2D.__init__(self, u, method, ax=ax,
                        xarray=xarray, yarray=yarray,
                        title=title,
                        label_axes=label_axes,
                        axes_grid=axes_grid, legend=None, clean=clean,
                        fontsize=fontsize,
                        fill_color=fill_color)

        self.step = self.method.step
        self.curve = curve
        self.units = units  # plot aside key
        self.v = getSlab(v)

        # ----------------------Regrid----------------------
        if self.method.reso is not None:
            xx = self.xarray
            yy = self.yarray
            self.var, self.yarray, self.xarray = regridToReso(
                self.var, yy, xx, self.method.reso, self.method.reso,
                lat_idx=-2, lon_idx=-1, method='linear', return_coords=True)
            self.v = regridToReso(
                self.v, yy, xx, self.method.reso, self.method.reso, lat_idx=-2,
                lon_idx=-1, method='linear', return_coords=False)
        else:
            # ---------------------Spacing---------------------
            self.var = self.var[::self.step, ::self.step]
            self.v = self.v[::self.step, ::self.step]
            self.xarray = self.xarray[::self.step]
            self.yarray = self.yarray[::self.step]

        # ---------------------Get grid---------------------
        self.xarray, self.yarray, self.lons, self.lats = self.getGrid()

    def plot(self):
        '''Main plotting interface

        Calls the core plotting function self._plot(), which handles the
        2D plotting using quiver plotting method.
        Then plots axes, quiverkey and title.

        Returns:
            self.quiver (mappable): the quiver obj, i.e. return value quiver().
        '''

        self.quiver = self._plot()
        self.plotAxes()
        self.ax.set_xlim(np.min(self.xarray), np.max(self.xarray))
        self.ax.set_ylim(np.min(self.yarray), np.max(self.yarray))
        self.qkey = self.plotkey()
        self.plotTitle()

        return self.quiver

    def _plot(self):
        '''Core quiver plotting function

        Returns:
            self.quiver (mappable): the quiver obj, i.e. return value quiver().
        '''

        self.ax.patch.set_color(self.fill_color)

        if self.curve:
            warnings.warn(
                '#<gplot warning>: The curved quiver functionality is experimental.')
            grains = int((len(self.xarray)+len(self.yarray)))
            quiver = modplot.velovect(self.ax, self.lons, self.lats, self.var,
                                      self.v, scale=15,
                                      grains=grains, color=self.method.color)

        # -------------------Plot vectors-------------------
        quiver = self.ax.quiver(
            self.lons, self.lats, self.var, self.v, scale=self.method.scale,
            scale_units=None, width=self.method.linewidth,
            color=self.method.color, alpha=self.method.alpha, zorder=3)

        return quiver

    def plotkey(self):
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
            keylength = np.nanpercentile(slab, 80)

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

# -----------------------------------------------------------------------
# -                    Quick plot interface function                    -
# -----------------------------------------------------------------------


def plot2(var, method, ax=None, xarray=None, yarray=None, var_v=None, **kwargs):
    '''Wrapper 2D plotting interface function

    Args:
        var (ndarray): input data to plot. Determines what to plot.
            Mush have dimensions >= 2.
            For data with rank>2, take the slab from the last 2 dimensions.
        method (PlotMethod): plotting method. Determines how to plot.
            Could be Isofill, Isoline, Boxfill, Quiver, Shading, Hatch, GIS.
    Keyword Args:
        ax (matplotlib axis or None): axis obj. Determines where to plot.
            If None, create a new.
        xarray (1darray or None): array to use as the x-coordinates. If None,
            use the indices of the last dimension: np.arange(slab.shape[-1]).
        yarray (1darray or None): array to use as the y-coordinates. If None,
            use the indices of the 2nd last dimension: np.arange(slab.shape[-2]).
        var_v (ndarray or None): if a quiver plot (method is Quiver), the
            y-component of the velocity data, and <var> is the x-component.
        nc_interface (str): netcdf data interfacing module, could be 'cdat',
            'xarray', 'iris' or 'netcdf4'.
        geo_interface (str): geographical plotting module, could be 'basemap',
            or 'cartopy'.
        isgeomap (bool): whether to use geographcial plot.
        projection (str): if use geographical plot, the map projection.
        bmap (basemap obj or None): reuse an existing basemap obj if not None.
        title (str or None): text as the figure title if <ax> is the
            single plot in the figure. If None, automatically
            get an alphabetic subtitle if <ax> is a subplot, e.g. '(a)'
            for the 1st subplot, '(d)' for the 4th one. If str and <ax>
            is a subplot, prepend <title> with the alphabetic index.
            One can force overriding the alphabetic index by giving a title
            str in the format of '(x) xxxx', e.g. '(p) subplot-p'.
        label_axes (bool or 'all' or tuple): controls axis ticks and
            ticklabels. If True, don't exert any inference other than
            changing the ticklabel fontsize, and let matplotlib put the
            ticks and ticklabels (i.e. default only left and bottom axes).
            If False, turn off all ticks and ticklabels.
            If 'all', plot ticks and ticks labels on all 4 sides.
            If (left, right, top, bottom),
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
        fix_aspect (bool): passed to the constructor of basemap: `Basemap(xxx,
            fix_aspect=fix_aspect)`.
        fill_color (str or color tuple): color to use as background color.
            If data have missings, they will be shown as this color.
            It is better to use a grey than while to better distinguish missings.
    Returns:
        plotobj (Plot2D obj).
    '''

    # get kwargs
    newkwargs = copy.deepcopy(rcParams)
    newkwargs.update(kwargs)
    nc_interface = newkwargs['nc_interface']
    geo_interface = newkwargs['geo_interface']
    fill_color = newkwargs['fill_color']
    isgeomap = newkwargs['isgeomap']
    title = newkwargs['title']
    label_axes = newkwargs['label_axes']
    axes_grid = newkwargs['axes_grid']
    projection = newkwargs['projection']
    bmap = newkwargs['bmap']
    fontsize = newkwargs['fontsize']
    clean = newkwargs['clean']
    fix_aspect = newkwargs['fix_aspect']
    legend = newkwargs['legend']
    legend_ori = newkwargs['legend_ori']

    nc_interface = nc_interface.lower()
    if nc_interface not in ['cdat', 'iris', 'xarray', 'netcdf4']:
        raise Exception(
            "Netcdf data interface not supported: %s" % nc_interface)

    geo_interface = geo_interface.lower()
    if geo_interface not in ['basemap', 'cartopy']:
        raise Exception(
            "Geographical plotting interface not supported: %s" %
            geo_interface)

    if np.ndim(var) == 1:
        raise Exception("<var> is 1D")

    if nc_interface == 'cdat':
        from gplot.lib.cdat_utils import checkGeomap
    elif nc_interface == 'netcdf4':
        from gplot.lib.netcdf4_utils import checkGeomap
    elif nc_interface == 'iris':
        raise Exception("Not implemented.")
    elif nc_interface == 'xarray':
        raise Exception("Not implemented.")

    isgeo2, var2, xx, yy = checkGeomap(var, xarray, yarray)

    # -------------------Quiver plot-------------------
    if var_v is not None and isinstance(method, Quiver):
        if geo_interface == 'basemap':
            from gplot.lib.basemap_utils import Plot2QuiverBasemap as Plot2Geo
        elif geo_interface == 'cartopy':
            from gplot.lib.cartopy_utils import Plot2QuiverCartopy as Plot2Geo

        isgeo2_v, var_v, _, _ = checkGeomap(var_v, xarray, yarray)

        if fill_color == '0.8':
            # change default to white for quiver plots
            fill_color = 'w'

        if isgeomap and isgeo2 and isgeo2_v:
            plotobj = Plot2Geo(
                var2, var_v, method, ax=ax, xarray=xx, yarray=yy,
                title=title, label_axes=label_axes, axes_grid=axes_grid,
                fill_color=fill_color, projection=projection,
                bmap=bmap, fontsize=fontsize,
                clean=clean, fix_aspect=fix_aspect)
        else:
            plotobj = Plot2Quiver(
                var, var_v, method, ax=ax, xarray=xx, yarray=yy, title=title,
                label_axes=label_axes, axes_grid=axes_grid, clean=clean,
                fontsize=fontsize, fill_color=fill_color)

    # ---------------Other types of plots---------------
    else:
        if geo_interface == 'basemap':
            from gplot.lib.basemap_utils import Plot2Basemap as Plot2Geo
        elif geo_interface == 'cartopy':
            from gplot.lib.cartopy_utils import Plot2Cartopy as Plot2Geo

        if isgeomap and isgeo2:
            if geo_interface == 'basemap':
                plotobj = Plot2Geo(
                    var2, method, ax=ax, legend=legend, xarray=xx, yarray=yy,
                    title=title, label_axes=label_axes, axes_grid=axes_grid,
                    fill_color=fill_color, projection=projection,
                    bmap=bmap, fontsize=fontsize,
                    legend_ori=legend_ori, clean=clean, fix_aspect=fix_aspect)
            elif geo_interface == 'cartopy':
                plotobj = Plot2Geo(
                    var2, method, ax=ax, legend=legend, xarray=xx, yarray=yy,
                    title=title, label_axes=label_axes, axes_grid=axes_grid,
                    fill_color=fill_color, projection=projection,
                    fontsize=fontsize,
                    legend_ori=legend_ori, clean=clean, fix_aspect=fix_aspect)
        else:
            plotobj = Plot2D(
                var, method, ax=ax, legend=legend, xarray=xx, yarray=yy,
                title=title, label_axes=label_axes, axes_grid=axes_grid,
                fontsize=fontsize, legend_ori=legend_ori, clean=clean,
                fill_color=fill_color)
    plotobj.plot()

    return plotobj

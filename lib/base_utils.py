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
# TODO make it possible to use barbs plot
# TODO add cma_barbs
# TODO add cma colormaps
# arrow length

# --------Import modules--------------
from __future__ import print_function
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colors

__all__=[
        'rcParams', 'restore_params', 'mkscale', 'index2Letter',
        'remap_colormap', 'get_colormap', 'get_colorbar_pad', 'pick_point',
        'get_slab', 'regrid_to_reso', 'get_missing_mask', 'get_quantiles',
        'get_range', 'alternate_ticks', 'Isofill', 'Isoline', 'Boxfill',
        'Pcolor', 'Hatch', 'Shading', 'GIS', 'Quiver', ]

# Default parameters
rcParams = {
    'legend'        : 'global',
    'title'         : None,
    'label_axes'    : True,
    'axes_grid'     : False,
    'fill_color'    : '0.8',
    'projection'    : 'cyl',
    'legend_ori'    : 'horizontal',
    'clean'         : False,
    'isgeomap'      : True,
    'fix_aspect'    : False,
    'nc_interface'  : 'netcdf4',
    'geo_interface' : 'cartopy',
    'fontsize'      : 8,
    'verbose'       : True,
    'default_cmap'  : plt.cm.RdBu_r
}

# a backup copy, deepcopy produces issue in autodoc
_default_rcParams = {
    'legend'        : 'global',
    'title'         : None,
    'label_axes'    : True,
    'axes_grid'     : False,
    'fill_color'    : '0.8',
    'projection'    : 'cyl',
    'legend_ori'    : 'horizontal',
    'clean'         : False,
    'isgeomap'      : True,
    'fix_aspect'    : False,
    'nc_interface'  : 'netcdf4',
    'geo_interface' : 'cartopy',
    'fontsize'      : 8,
    'verbose'       : True,
    'default_cmap'  : plt.cm.RdBu_r
}

#_default_rcParams = copy.deepcopy(rcParams)

# -----------------------------------------------------------------------
# -                          Utility functions                          -
# -----------------------------------------------------------------------


def restore_params():
    '''Restore default parameters'''
    global rcParams
    rcParams.update(_default_rcParams)


def update_kwarg(key, value):
    global rcParams
    if value is None or value == 'none':
        return rcParams.get(key, None)
    else:
        return value


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


def remap_colormap(cmap, vmin, vmax, vcenter, name='shiftedcmap'):
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


def get_colormap(cmap):
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


def get_colorbar_pad(ax, orientation, base_pad=0.0):
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


def create_dummy_textbox(ax=None, fontsize=12):
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


def pick_point(ax, color='y'):
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
        print('\n# <pick_point>: Pick point by clicking. Enter to quit.')
        coord = pylab.ginput(n=1, timeout=False)
        if len(coord) > 0:
            coord = coord[0]
            points.append(coord)
            print('# <pick_point>: New point:', coord)
            ax.plot(coord[0], coord[1], 'o', markersize=10, color=color)
            ax.get_figure().canvas.draw()
        else:
            break
    return np.array(points)


def get_slab(var, index1=-1, index2=-2, verbose=True):
    '''Get a slab from a variable

    Args:
        var: (ndarray): ndarray with dimension >=2.
    Keyword Args:
        index1,index2 (int): indices denoting the dimensions that define a 2d
            slab.
    Returns:
        slab (ndarray): the (1st) slab from <var>.
           E.g. <var> has dimension (12,1,241,480), get_slab(var) will
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
    '''
    try:
        result = np.squeeze(result)
    except:
        result = result(squeeze=1)
    return np.array(result)
    '''

    return result[0]



def regrid_to_reso(var, inlat, inlon, dlat, dlon, lat_idx=-2, lon_idx=-1,
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


def get_missing_mask(slab):
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


def get_quantiles(slab, quantiles=None, verbose=True):
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
            print('# <get_quantiles>: %0.3f left quantile: %f.'
                  % (pii, results[ii]))
    return results


def get_range(vars, vmin=None, vmax=None, ql=None, qr=None, verbose=True):
    '''Get min/max value

    Args:
        vars (list): a list of ndarrays.
    Keyword Args:
        vmin (None or float): given minimum level.
        vmax (None or float): given maximum level.
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
        maskii = get_missing_mask(vii)
        vii = np.where(maskii, np.nan, vii)
        if ii == 0:
            var_all = vii
        else:
            var_all = np.concatenate((var_all, vii), axis=0)

    # ------------------Get quantiles------------------
    if ql is not None or qr is not None:
        if ql is not None:
            left_quantile = get_quantiles(var_all, ql, verbose)[0]
        if qr is not None:
            right_quantile = get_quantiles(var_all, 1-qr, verbose)[0]

    # -------Get min/max from all vars-----------------
    data_min = np.nanmin(var_all)
    data_max = np.nanmax(var_all)

    # ----------------Set lower boundary----------------
    if vmin is not None and ql is None:
        vmin = max(data_min, vmin)
    elif vmin is None and ql is not None:
        vmin = left_quantile
    elif vmin is not None and ql is not None:
        vmin = max(data_min, vmin, left_quantile)
    else:
        vmin = data_min

    # ----------------Set upper boundary----------------
    if vmax is not None and qr is None:
        vmax = min(data_max, vmax)
    elif vmax is None and qr is not None:
        vmax = right_quantile
    elif vmax is not None and qr is not None:
        vmax = min(data_max, vmax, right_quantile)
    else:
        vmax = data_max

    if vmax < vmin:
        vmin, vmax = vmax, vmin

    return vmin, vmax, data_min, data_max


def alternate_ticks(cbar, ticks=None, fontsize=9):
    '''Create alternating ticks and ticklabels for colorbar

    Args:
        cbar (matplotlib colorbar obj): input colorbar obj to alter.
    Keyword Args:
        ticks (list or array or None): ticks of the colorbar. If None,
            get from cbar.get_ticks().
        fontsize (str): font size for tick labels.
    Returns:
        cbar (matplotlib colorbar obj): the altered colorbar.

    Only works for horizontal colorbar with discrete ticks. As vertical
    colorbar doesn't tend to have overlapping tick labels issue.
    '''

    if ticks is None:
        ticks = cbar.get_ticks()

    if cbar.orientation == 'vertical':
        cbar.set_ticks(ticks)
        # skip vertical colorbar as digits are less likely to overlap
        return cbar

    lbot = ticks[1:][::2]  # labels at bottom
    ltop = ticks[::2]  # labels on top

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

    for ii in range(len(ticklabels[::2])):
        tii = ltop[ii]
        tlii = ticklabels[::2][ii]
        xii = shift_l+scaling*(tii-vmin)/(vmax-vmin)
        # plot ticks
        cbar.ax.plot([xii, xii],
                     [1.0, 1.55],
                     'k-', linewidth=0.5,
                     clip_on=False,
                     transform=cbar.ax.transAxes)

        # plot tick labels
        cbar.ax.text(xii,
                     1.30, tlii,
                     transform=cbar.ax.transAxes, va='bottom',
                     ha='center', fontsize=fontsize)

    return cbar


def get_ax_geometry(ax):
    '''
    The get_geometry function was deprecated in Matplotlib 3.4 and will be
    removed two minor releases later. Use get_subplotspec instead.
    (get_subplotspec returns a SubplotSpec instance.)
    '''

    mpl_version = matplotlib.__version__.split('.')[:2]
    if mpl_version < ['3', '4']:
        spec = ax.get_geometry()
        geo = spec[:2]
        subidx = spec[-1]
    else:
        spec = ax.get_subplotspec().get_geometry()
        geo = spec[:2]
        subidx = spec[2] + 1

    return geo, subidx


def clean_up_artists(axis, artist_list):
    """
    try to remove the artists stored in the artist list belonging to the 'axis'.
    :param axis: clean artists belonging to these axis
    :param artist_list: list of artist to remove
    :return: nothing

    Obtained from: https://stackoverflow.com/a/42201952/2005415.
    """
    for artist in artist_list:
        try:
            # fist attempt: try to remove collection of contours for instance
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

        # second attempt, try to remove the text
        try:
            artist.remove()
        except (AttributeError, ValueError):
            pass

    return

# -----------------------------------------------------------------------
# -                       Plotting method classes                       -
# -----------------------------------------------------------------------



class PlotMethod(object):
    '''Base plotting method class'''
    def __init__(self, vars, split=2, vmin=None, vmax=None,
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
            vmin (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            vmax (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <vmin> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <vmax> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            verbose (bool): whether to print some info or not.
        '''

        self.split   = split
        self.vmin    = vmin
        self.vmax    = vmax
        self.ql      = ql
        self.qr      = qr
        self.vcenter = vcenter
        self.cmap    = cmap
        #self.method  = 'base'

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

    def compute_range(self):
        '''Get the range of data and the range to plot'''

        # -------------------Get max/min-------------------
        self.vmin, self.vmax, self.data_min, self.data_max = get_range(
            self.vars, self.vmin, self.vmax, self.ql, self.qr)

    def compute_extend(self, vmin, vmax):
        '''Determine overflow on both ends'''

        self.ext_1 = True if self.data_min < vmin else False
        self.ext_2 = True if self.data_max > vmax else False

        if self.ext_1 is False and self.ext_2 is False:
            self.extend = 'neither'
        elif self.ext_1 is True and self.ext_2 is False:
            self.extend = 'min'
        elif self.ext_1 is False and self.ext_2 is True:
            self.extend = 'max'
        else:
            self.extend = 'both'

        return

    def adjust_colormap(self, vmin, vmax):
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
        norm = None

        if self.split == 0:
            norm = None

        if self.split == 1 and (vmin-self.vcenter)*(vmax-self.vcenter) >= 0:
            norm = None

        if self.split == 1 and (vmin-self.vcenter)*(vmax-self.vcenter) < 0:
            norm = TwoSlopeNorm(self.vcenter, vmin, vmax)

        if self.split == 2:
            if vmin < self.vcenter and vmax <= self.vcenter:
                cmap = remap_colormap(self.cmap, vmin, vmax, self.vcenter)
                norm = None

            if vmin >= self.vcenter and vmax > self.vcenter:
                cmap = remap_colormap(self.cmap, vmin, vmax, self.vcenter)
                norm = None

            if (vmin-self.vcenter)*(vmax-self.vcenter) < 0:
                norm = TwoSlopeNorm(self.vcenter, vmin, vmax)

        return cmap, norm


class Isofill(PlotMethod):
    '''Plotting method for isofill/contourf plots'''

    method: str = 'isofill'
    def __init__(self, vars, num=15, zero=1, split=1, levels=None,
                 vmin=None, vmax=None, ql=None, qr=None,
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
                given, compute contour levels using <num>, <zero>, <vmin>,
                <vmax>, <ql>, <qr>.
            vmin (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            vmax (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <vmin> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <vmax> if given. If both <vmax> and <qr> are
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

        super(Isofill, self).__init__(
            vars, split=split, vmin=vmin, vmax=vmax, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.num              = num
        self.zero             = zero
        self.levels           = levels
        self.stroke           = stroke
        self.stroke_color     = stroke_color
        self.stroke_lw        = stroke_lw
        self.stroke_linestyle = stroke_linestyle

        # --------------------Get levels--------------------
        self.compute_range()

        if self.levels is None:
            self.levels = mkscale(self.vmin, self.vmax, self.num, self.zero)

        self.compute_extend(np.min(self.levels), np.max(self.levels))

        # -------------------Get colormap-------------------
        self.cmap = get_colormap(self.cmap)
        self.cmap, self.norm = self.adjust_colormap(vmin=np.min(self.levels),
                                                   vmax=np.max(self.levels))

        return


class Isoline(Isofill):
    '''Plotting method for isoline/contour plots'''
    method: str = 'isoline'

    def __init__(self, vars, num=15, zero=1, split=1, levels=None,
                 vmin=None, vmax=None, ql=None, qr=None,
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
                given, compute contour levels using <num>, <zero>, <vmin>,
                <vmax>, <ql>, <qr>.
            vmin (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            vmax (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <vmin> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <vmax> if given. If both <vmax> and <qr> are
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

        super(Isoline, self).__init__(
            vars, num=num, zero=zero, split=split, levels=levels,
            vmin=vmin, vmax=vmax, ql=ql, qr=qr,
            vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.black           = black
        self.color           = color
        self.linewidth       = linewidth
        self.alpha           = alpha
        self.dash_negative   = dash_negative
        self.bold_lines      = bold_lines
        self.label           = label
        self.label_fmt       = label_fmt
        self.label_box       = label_box
        self.label_box_color = label_box_color

        return


class Boxfill(PlotMethod):
    '''Plotting method for boxfill/imshow plots'''

    method: str = 'boxfill'
    def __init__(self, vars, split=2, vmin=None, vmax=None,
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
                given, compute contour levels using <num>, <zero>, <vmin>,
                <vmax>, <ql>, <qr>.
            vmin (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            vmax (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <vmin> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <vmax> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            verbose (bool): whether to print some info or not.
        '''

        super(Boxfill, self).__init__(
            vars, split=split, vmin=vmin, vmax=vmax, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.compute_range()
        self.compute_extend(self.vmin, self.vmax)
        self.cmap = get_colormap(self.cmap)
        self.cmap, self.norm = self.adjust_colormap(vmin=self.vmin, vmax=self.vmax)


class Pcolor(Boxfill):
    '''Plotting method for pcolormesh plots'''

    method: str = 'pcolor'
    def __init__(self, vars, split=2, vmin=None, vmax=None,
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
                given, compute contour levels using <num>, <zero>, <vmin>,
                <vmax>, <ql>, <qr>.
            vmin (float or None): specified minimum level to plot. If None,
                determine from <ql> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            vmax (float or None): specified maximum level to plot. If None,
                determine from <qr> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            ql (float or None): specified minimum left quantile to plot. If None,
                determine from <vmin> if given. If both <vmin> and <ql> are
                None, use minimum value from <vars>. If both given, take the larger.
            qr (float or None): specified maximum right quantile (e.g. 0.01 for
                the 99th percentile) to plot. If None,
                determine from <vmax> if given. If both <vmax> and <qr> are
                None, use maximum value from <vars>. If both given, take the smaller.
            vcenter (float): value at which to split the colormap. Default to 0.
            cmap (matplotlib colormap or None): colormap to use. If None, use
                the default in rcParams['default_cmap'].
            verbose (bool): whether to print some info or not.
        '''

        super(Pcolor, self).__init__(
            vars, split=split, vmin=vmin, vmax=vmax, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)



class Hatch(object):
    '''Plotting method for hatching plots'''
    method: str = 'hatch'

    def __init__(self, hatch='.', color='k', alpha=1.0):
        '''Plotting method for hatching plots

        Keyword Args:
            hatch (str): style of hatching. Choices:
            '.', '/', '//', '\\', '\\\\', '*', '-', '+', 'x', 'o', 'O'
            alpha (float): transparent level, in range of [0, 1].
        '''
        self.hatch = hatch
        self.color = color
        self.alpha = alpha


class Shading(object):
    '''Plotting method for shading plots'''
    method: str = 'shading'

    def __init__(self, color='0.5', alpha=0.5):
        '''Plotting method for shading plots

        Keyword Args:
            color (str or color tuple): color of shading.
            alpha (float): transparent level, in range of [0, 1].
        '''

        self.color = color
        self.alpha = alpha

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
    method: str = 'gis'

    def __init__(self, xpixels=2000, dpi=96, verbose=True):
        '''Plotting method for GIS plots

        Keyword Args:
            xpixels (int): plot size.
            dpi (int): dpi.
            verbose (bool): whats this?
        '''
        self.xpixels = xpixels
        self.dpi     = dpi
        self.verbose = verbose
        self.args    = {'xpixels': xpixels, 'dpi': dpi, 'verbose': verbose}


class Quiver(object):
    '''Plotting method for quiver plots'''
    method: str = 'quiver'

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

        self.step      = step
        self.reso      = reso
        self.scale     = scale
        self.keylength = keylength
        self.linewidth = linewidth
        self.color     = color
        self.alpha     = alpha

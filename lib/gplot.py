'''Basic geographical plotting functions.

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2020-12-05 10:14:28.
'''

# TODO: global colorbar placement is not smart enough
# TODO: make scipy dependency optional
# TODO: make possible to use and change rcParams
# TODO: add Plot2QuiverCarotpy
# TODO: consider remove bmap input arg

# --------Import modules--------------
from __future__ import print_function
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.pyplot import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colorbar as mcbar
from matplotlib import colors
from scipy.interpolate import RegularGridInterpolator

# Default colormap
DEFAULT_CMAP = plt.cm.PRGn
DEFAULT_CMAP = plt.cm.RdBu_r

# Default parameters
rcParams={
        'legend': 'global',
        'title': None,
        'label_axes': True,
        'axes_grid': False,
        'fill_color': '0.8',
        'projection': 'cyl',
        'legend_ori': 'horizontal',
        'clean': False,
        'isgeomap': True,
        'fix_aspect': False,
        'nc_interface': 'cdat',
        'geo_interface': 'basemap',
        'font_size': 12,
        }

# -----------------------------------------------------------------------
# -                          Utility functions                          -
# -----------------------------------------------------------------------


def mkscale(n1, n2, nc=12, zero=1):
    '''Copied from vcs/util.py

    Function: mkscale

    Description of function:
    This function return a nice scale given a min and a max

    option:
    nc # Maximum number of intervals (default=12)
    zero # Not all implemented yet so set to 1 but values will be:
           -1: zero MUST NOT be a contour
            0: let the function decide # NOT IMPLEMENTED
            1: zero CAN be a contour  (default)
            2: zero MUST be a contour
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

    <index>: integer index for a subplot.

    Return <letter>: corresponding letter index for <index>.

    <index> to letter indexing is defined as following:
    ----------------------------------------------------
    <index>                     letter index
    ----------------------------------------------------
       1                            (a)
       2                            (b)
       3                            (c)
       ...                          ...
    ----------------------------------------------------
    '''

    # ---------------Create <index> dict---------------
    index_dict = {
        1: '(a)',
        2: '(b)',
        3: '(c)',
        4: '(d)',
        5: '(e)',
        6: '(f)',
        7: '(g)',
        8: '(h)',
        9: '(i)',
        10: '(j)',
        11: '(k)',
        12: '(l)',
        13: '(m)',
        14: '(n)',
        15: '(o)',
        16: '(p)',
        17: '(q)',
        18: '(r)',
        19: '(s)',
        20: '(t)',
        21: '(u)',
        22: '(v)',
        23: '(w)',
        24: '(x)',
        25: '(y)',
        26: '(z)'
    }

    # -------------------Check inputs-------------------
    if index <= 0:
        raise Exception("<index> needs to be positive.")
    if index > 26:
        return str(index)
    else:
        return index_dict[index]


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

    if cmap is None:
        cmap = DEFAULT_CMAP
    elif cmap is not None and isinstance(cmap, str):
        cmpstr = 'cmap=plt.cm.'+cmap
        try:
            exec(cmpstr)
        except:
            raise Exception("Color map name wrong.")
    else:
        pass

    # -------------Shift colormap if needed-------------
    #cmap = remappedColorMap(cmap, vmin, vmax, split)

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


def pickPoint(ax, color='y'):
    '''Pick points from plot and store coordinates.

    <ax>: matplotlib axis obj.
    <color>: str or RGB tuple. Color of picked points.

    Return <points>: list of (x,y) coordinates.

    Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
    Update time: 2017-05-24 09:27:45.
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

    <var>: nd array with dimension >=2.
    <index1>,<index2>: str, indices denoting the dimensions from which a slab is to slice.

    Return <slab>: the (1st) slab from <var>.
                   E.g. <var> has dimension (12,1,241,480), getSlab(var) will
                   return the 1st time point with singleton dimension squeezed.

    Update time: 2015-07-14 19:23:42.
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
    '''Get a bindary denoting missing (masked or nan).

    <slab>: nd array, possibly contains masked values or nans.

    Return <mask>: nd bindary, 1s for missing, 0s otherwise.
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
    Keyword Arg:
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
    def __init__(self, vars, split=2, min_level=None, max_level=None,
                 ql=None, qr=None, vcenter=0, cmap=None, verbose=True):

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

        # -------------------Get max/min-------------------
        self.vmin, self.vmax, self.data_min, self.data_max = getRange(
            self.vars, self.min_level, self.max_level, self.ql, self.qr)

    def computeExt(self, vmin, vmax):

        self.ext_1 = True if self.data_min < vmin else False
        self.ext_2 = True if self.data_max > vmax else False

        return

    def adjustColormap(self, vmin=None, vmax=None):

        if vmin is None:
            if not hasattr(self, 'vmin'):
                self.computeRange()
            vmin = self.vmin
        if vmax is None:
            if not hasattr(self, 'vmax'):
                self.computeRange()
            vmax = self.vmax

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
    def __init__(self, vars, num=15, zero=1, split=1, levels=None,
                 min_level=None, max_level=None, ql=None, qr=None,
                 vcenter=0, cmap=None,
                 stroke=False, stroke_color='0.3', stroke_lw=0.2,
                 stroke_linestyle='-',
                 verbose=True):

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
        self.cmap = LinearSegmentedColormap('new_cmp2',
                                            self.cmap._segmentdata,
                                            N=len(self.levels)-1)

        return


class Isoline(Isofill):
    def __init__(self, vars, num=15, zero=1, split=1, levels=None,
                 min_level=None, max_level=None, ql=None, qr=None,
                 vcenter=0, cmap=None,
                 black=False, color=None, linewidth=1.0, alpha=1.0,
                 dash_negative=True, bold_lines=None, verbose=True):

        super(
            Isoline, self).__init__(
            vars, split=split, min_level=min_level, max_level=max_level, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.black = black
        self.color = color
        self.linewidth = linewidth
        self.alpha = alpha
        self.dash_negative = dash_negative
        self.bold_lines = bold_lines
        self.method = 'isoline'

        return


class Boxfill(PlotMethod):
    def __init__(self, vars, split=2, min_level=None, max_level=None,
                 ql=None, qr=None, vcenter=0, cmap=None, verbose=True):

        super(
            Boxfill, self).__init__(
            vars, split=split, min_level=min_level, max_level=max_level, ql=ql,
            qr=qr, vcenter=vcenter, cmap=cmap, verbose=verbose)

        self.method = 'boxfill'

        self.computeRange()
        self.computeExt(self.vmin, self.vmax)
        self.cmap = getColormap(self.cmap)
        self.norm = self.adjustColormap(vmin=self.vmin, vmax=self.vmax)


class Hatch(object):
    def __init__(self, hatch='.', alpha=0.7):
        # choices: '.', '/', '//', '\\', '\\\\', '*', '-', '+', 'x', 'o', 'O'
        self.hatch = hatch
        self.alpha = alpha
        self.method = 'hatch'


class Shading(object):
    def __init__(self, color='0.5', alpha=0.5):

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

        #self.cmap = colors.LinearSegmentedColormap('shading', cdict, N=2)
        self.cmap = colors.ListedColormap(c)


class GIS(object):
    def __init__(self, xpixels=2000, dpi=96, verbose=True):
        self.xpixels = xpixels
        self.dpi = dpi
        self.verbose = verbose
        self.args = {'xpixels': xpixels, 'dpi': dpi, 'verbose': verbose}
        self.method = 'gis'


class Quiver(object):
    def __init__(self, step=1, reso=None, scale=None, keylength=None,
                 linewidth=0.0015, color='k', alpha=1.0):

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

    def __init__(self, var, method, ax=None, xarray=None, yarray=None,
                 title=None, label_axes=True, axes_grid=False, legend='global',
                 legend_ori='horizontal', clean=False, fontsize=12,
                 fill_color='0.8'):

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
        # TODO: overwrite input fontsize or not?
        self.geo, self.subidx, self._fontsize = self.getGeo()

    # ---------------------Get grid---------------------

    def getGrid(self):

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

        geo = self.ax.get_geometry()[:2]
        subidx = self.ax.get_geometry()[-1]
        scale = 1./max(geo)
        fontsize = 7*scale+self.fontsize  # empirical

        return geo, subidx, fontsize

    @classmethod
    def getExtend(cls, method):

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

        self.cs = self._plot()
        self.plotAxes()
        self.cbar = self.plotColorbar()
        self.plotTitle()

        return self.cs

    def _plot(self):

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

        extend = Plot2D.getExtend(self.method)

        if self.method.color is not None:
            colors = [self.method.color]*len(self.method.levels)
        else:
            if self.method.black:
                colors = ['k']*len(self.method.levels)
            else:
                colors = None

        cs = self.ax.contour(
            self.lons, self.lats, self.var, self.method.levels,
            colors=colors,
            cmap=self.method.cmap, extend=extend,
            linewidths=self.method.linewidth,
            alpha=self.method.alpha,
            transform=self._transform)

        # -----------------Set line styles-----------------
        # for some reason it's not giving me dashed line for negatives.
        # have to set myself
        if self.method.dash_negative:
            for ii in range(len(cs.collections)):
                cii = cs.collections[ii]
                lii = cs.levels[ii]
                if lii < 0:
                    cii.set_linestyle('dashed')
                else:
                    cii.set_linestyle('solid')

        # For some reason the linewidth keyword in contour doesn't
        # work, has to set again.
        for ii in range(len(cs.collections)):
            cs.collections[ii].set_linewidth(self.method.linewidth)

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

        return cs

    def _plotBoxfill(self):

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

        cs = self.ax.pcolormesh(
            self.lons, self.lats, self.var, cmap=self.method.cmap,
            vmin=self.method.levels[0],
            vmax=self.method.levels[-1])

        return cs

    def _plotHatch(self):
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

        pvar = np.where(self.var == 1, 1, np.nan)
        cs = self.ax.contourf(
            self.lons,
            self.lats,
            pvar, 1, cmap=self.method.cmap,
            alpha=self.method.alpha,
            transform=self._transform)

        return cs

    def getLabelBool(self, geo, idx):
        '''[left, right, top, bottom]'''

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

        # if self.legend == 'local' and self.legend_ori == 'vertical' and parallels[1] == 1:
            #parallels[1] = 0

        return parallels, meridians

    def plotAxes(self):

        if self.axes_grid:
            self.ax.grid(True)

        # --------Turn off lat/lon labels if required--------
        if self.label_axes is False or self.clean:
            self.ax.xaxis.set_ticklabels([])
            self.ax.yaxis.set_ticklabels([])
            return

        if self.label_axes == 'all':
            parallels = [1, 1, 0, 0]
            meridians = [0, 0, 1, 1]
        elif isinstance(self.label_axes, (list, tuple)) and len(self.label_axes) == 2 and\
                len(self.label_axes[0]) == 4 and len(self.label_axes[1]) == 4:
            # TODO: add docstring for this
            parallels, meridians = self.label_axes
        else:
            parallels, meridians = self.getLabelBool(self.geo, self.subidx)

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
                            labeltop=labeltop, labelbottom=labelbottom)

        return

    def alternateTicks(self, cbar, ticks):

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

        # cbar.ax.set_xticklabels(ticks)  # NOTE: do not use this.
        # this will give ugly strings for floats, like 1.4999999999999 instead
        # of 1.5

        # The secondary_xaxis approach would put one additional scale label,
        # e.g. 1e-5 for the secondary x axis.
        # twinax=cbar.ax.secondary_xaxis('top')
        # twinax.set_xticks(ticks[::2])
        # twinax.tick_params(labelsize=self.fontsize)

        '''
        # NOTE: use formatter instead:
        if self.legend_ori=='horizontal':
            ticklabels = [i.get_text() for i in cbar.ax.get_xticklabels()]
        elif self.legend_ori=='vertical':
            ticklabels = [i.get_text() for i in cbar.ax.get_yticklabels()]
            ticklabels=formatter.format_ticks(ticks)
        '''

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

        if self.method.method in ['hatch', 'shading']:
            return

        if self.legend is None:
            return

        if self.method.method in ['isofill', 'isoline']:
            isdrawedges = True
        else:
            isdrawedges = False

        if self.method.method in ['boxfill', 'pcolor']:
            extend = Plot2D.getExtend(self.method)

        # TODO: optimization needed here!

        # ---------------Draw local colorbar---------------
        if self.legend == 'local' or (
                self.legend == 'global' and self.geo[0] * self.geo[1] == 1):

            if self.method.method in ['boxfill', 'pcolor']:

                # Adjust position according to the existence of axis ticks
                pad = getColorbarPad(self.ax, self.legend_ori)

                # --------------Create a colorbar axis--------------
                cax, kw = mcbar.make_axes_gridspec(
                    self.ax, orientation=self.legend_ori, shrink=0.85, pad=pad,
                    fraction=0.07, aspect=35)
                cbar = plt.colorbar(
                    self.cs, cax=cax, orientation=self.legend_ori,
                    drawedges=isdrawedges, extend=extend)

                ticks = cbar.get_ticks()
            elif self.method.method in ['isofill', 'isoline']:
                # compute extra padding needed for the top side tick labels
                if self.legend_ori == 'horizontal':
                    dummytext = self.ax.text(
                        0, 0, '0.0', zorder=-10, fontsize=self._fontsize,
                        alpha=0, transform=self.ax.transAxes)
                    dummybox = dummytext.get_window_extent(
                        self.ax.get_figure().canvas.get_renderer())
                    dummybox = dummybox.transformed(
                        self.ax.transAxes.inverted())

                    # Adjust position according to the existence of axis ticks
                    pad = getColorbarPad(
                        self.ax, self.legend_ori, base_pad=dummybox.height*1.25)
                else:

                    pad = getColorbarPad(self.ax, self.legend_ori)

                ticks = getattr(self.method, 'levels', None)
                # NOTE: mcbar.make_axes() doesn't work well with tight_layout()
                cax, kw = mcbar.make_axes_gridspec(
                    self.ax, orientation=self.legend_ori, shrink=0.85, pad=pad,
                    fraction=0.07, aspect=35)
                cbar = plt.colorbar(
                    self.cs, cax=cax, orientation=self.legend_ori, ticks=ticks,
                    drawedges=isdrawedges)

                cbar = self.alternateTicks(cbar, ticks)

            # -------------------Re-format ticks-------------------
            cbar.ax.tick_params(labelsize=self._fontsize)
            if all([ll == int(ll) for ll in ticks]):
                ticks = [int(ll) for ll in ticks]

        # -----Use the 1st subplot as global color bar-----
        elif self.legend == 'global' and self.subidx == 1:

            fig = self.ax.get_figure()

            if self.legend_ori == 'horizontal':
                dummytext = self.ax.text(
                    0, 0, '0.0', zorder=-10, fontsize=self._fontsize, alpha=0,
                    transform=self.ax.transAxes)
                dummybox = dummytext.get_window_extent(
                    self.ax.get_figure().canvas.get_renderer())
                dummybox = dummybox.transformed(fig.transFigure.inverted())
                pad = dummybox.height*2.6
                height = 0.02
                fig.subplots_adjust(bottom=0.18)
                cax = self.ax.get_figure().add_axes(
                    [0.15, 0.18-height-pad, 0.65, height])

            else:
                fig.subplots_adjust(right=0.90)
                cax = self.ax.get_figure().add_axes([0.92, 0.20, 0.02, 0.6])

            if self.method.method in ['boxfill', 'pcolor']:
                cbar = plt.colorbar(
                    self.cs, cax=cax, orientation=self.legend_ori, ticks=None,
                    drawedges=isdrawedges, extend=extend, aspect=35)
                ticks = cbar.get_ticks()
            else:
                ticks = getattr(self.method, 'levels', None)
                cbar = plt.colorbar(
                    self.cs, cax=cax, orientation=self.legend_ori, ticks=ticks,
                    drawedges=isdrawedges, aspect=35)

                cbar = self.alternateTicks(cbar, ticks)

            # -----------------Re-format ticks-----------------
            cbar.ax.tick_params(labelsize=self._fontsize)

            if all([ll == int(ll) for ll in ticks]):
                ticks = [int(ll) for ll in ticks]

        elif self.legend == 'global' and self.subidx > 1:
            return

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

        if self.clean or self.title == 'none':
            return

        if self.title is None and self.geo[0]*self.geo[1] > 1:
            title = index2Letter(self.subidx)

        elif isinstance(self.title, str):

            if self.geo[0]*self.geo[1] > 1:
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
    '''General purpose 2D vector plots.

    For geo vector plots, see Plot2QuiverBasemap, which handles geo-map plotting
    and map projections.
    '''

    # TODO make it possible to use barbs plot
    # TODO make it possible to use colormap to decode magnitude, instead of
    # arrow length

    def __init__(
            self, u, v, method, ax=None, xarray=None, yarray=None,
            title=None, label_axes=True, axes_grid=False,
            clean=False, fontsize=12, units=None, fill_color='w'):

        Plot2D.__init__(self, u, method, ax=ax,
                        xarray=xarray, yarray=yarray,
                        title=title,
                        label_axes=label_axes,
                        axes_grid=axes_grid, legend=None, clean=clean,
                        fontsize=fontsize,
                        fill_color=fill_color)

        self.step = self.method.step
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
        self.quiver = self._plot()
        self.plotAxes()
        self.qkey = self.plotkey()
        self.plotTitle()

        return self.quiver

    def _plot(self):

        self.ax.patch.set_color(self.fill_color)

        # -------------------Plot vectors-------------------
        quiver = self.ax.quiver(
            self.lons, self.lats, self.var, self.v, scale=self.method.scale,
            scale_units=None, width=self.method.linewidth,
            color=self.method.color, alpha=self.method.alpha, zorder=3)

        return quiver

    def plotkey(self):

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


def plot2(var, method, ax=None, legend='global',
          xarray=None, yarray=None,
          var_v=None,
          title=None, label_axes=True, axes_grid=False, fill_color='0.8',
          projection='cyl', legend_ori='horizontal', clean=False,
          isgeomap=True,
          fix_aspect=False,
          nc_interface='cdat',
          geo_interface='basemap',
          bmap=None,
          fontsize=12,
          verbose=True):

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
                label_axes=label_axes, axes_grid=axes_grid, clean=clean, fontsize=fontsize,
                fill_color=fill_color)

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
                title=title, label_axes=label_axes, axes_grid=axes_grid, fontsize=fontsize,
                legend_ori=legend_ori, clean=clean, fill_color=fill_color)
    plotobj.plot()

    return plotobj

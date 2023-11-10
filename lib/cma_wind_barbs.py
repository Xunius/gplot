'''设置使用中国气象风羽规范

默认matplotlib风羽等级：
    1. 短杆：5
    2. 长杆：10
    3. 填充三角旗：50

修改后风羽等级：
    1. 短杆：2
    2. 长杆：4
    3. 空心三角旗：20
    4. 填充三角旗：50

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2023-09-16 22:09:53.
'''

import numpy as np
from numpy import ma
from matplotlib import cbook
from matplotlib.quiver import Barbs, _check_consistent_shapes
from matplotlib.patches import CirclePolygon
import matplotlib.transforms as transforms

ori_find_tails = Barbs._find_tails
ori_set_UVC = Barbs.set_UVC
ori_make_barbs = Barbs._make_barbs

def _find_tails(self, mag, rounding=True, half=2, full=4, flag=20, fullflag=50):
    """
    Find how many of each of the tail pieces is necessary.

    Parameters
    ----------
    mag : `~numpy.ndarray`
        Vector magnitudes; must be non-negative (and an actual ndarray).
    rounding : bool, default: True
        Whether to round or to truncate to the nearest half-barb.
    half, full, flag, fullflag : float, defaults: 2, 4, 20, 50
        Increments for a half-barb, a barb, a hollow flag and a full (filled) flag.

    Returns
    -------
    n_fullflags, n_flags, n_barbs : int array
        For each entry in *mag*, the number of filled flags, hollow flags and barbs.
    half_flag : bool array
        For each entry in *mag*, whether a half-barb is needed.
    empty_flag : bool array
        For each entry in *mag*, whether nothing is drawn.
    """
    # If rounding, round to the nearest multiple of half, the smallest
    # increment
    if rounding:
        mag = half * np.around(mag / half)

    ### CHANGE {{{ compute number of filled flags
    n_fullflags, mag = divmod(mag, fullflag)
    ### CHANGE }}}

    n_flags, mag = divmod(mag, flag)
    n_barb, mag = divmod(mag, full)
    half_flag = mag >= half

    ### CHANGE {{{ compute number of empty flags
    empty_flag = ~(half_flag | (n_flags > 0) | (n_barb > 0) | (n_fullflags > 0))
    ### CHANGE }}}

    ### CHANGE {{{ add n_fullflags return
    return n_fullflags.astype('int'), n_flags.astype(int), n_barb.astype(int), half_flag, empty_flag
    ### CHANGE }}}

def set_UVC(self, U, V, C=None):
    # We need to ensure we have a copy, not a reference to an array that
    # might change before draw().
    self.u = ma.masked_invalid(U, copy=True).ravel()
    self.v = ma.masked_invalid(V, copy=True).ravel()

    # Flip needs to have the same number of entries as everything else.
    # Use broadcast_to to avoid a bloated array of identical values.
    # (can't rely on actual broadcasting)
    if len(self.flip) == 1:
        flip = np.broadcast_to(self.flip, self.u.shape)
    else:
        flip = self.flip

    if C is not None:
        c = ma.masked_invalid(C, copy=True).ravel()
        x, y, u, v, c, flip = cbook.delete_masked_points(
            self.x.ravel(), self.y.ravel(), self.u, self.v, c,
            flip.ravel())
        _check_consistent_shapes(x, y, u, v, c, flip)
    else:
        x, y, u, v, flip = cbook.delete_masked_points(
            self.x.ravel(), self.y.ravel(), self.u, self.v, flip.ravel())
        _check_consistent_shapes(x, y, u, v, flip)

    magnitude = np.hypot(u, v)

    ### CHANGE {{{ compute numbers of fullflags, hollow flags
    fullflags, flags, barbs, halves, empty = self._find_tails(
        magnitude, self.rounding, **self.barb_increments)

    # Get the vertices for each of the barbs

    plot_barbs = self._make_barbs(u, v, fullflags, flags, barbs, halves, empty,
                                  self._length, self._pivot, self.sizes,
                                  self.fill_empty, flip)
    ### CHANGE }}}

    self.set_verts(plot_barbs)

    ### CHANGE {{{ force facecolor to be 'none'
    # get edge and face colors
    barbcolor = self.get_edgecolor()
    # force facecolor to be none
    self.set_facecolor('none')
    # restore edge color
    self.set_edgecolor(barbcolor)
    ### CHANGE }}}

    # Set the color array
    if C is not None:
        self.set_array(c)

    # Update the offsets in case the masked data changed
    xy = np.column_stack((x, y))
    self._offsets = xy
    self.stale = True

def _make_barbs(self, u, v, nfullflags, nflags, nbarbs, half_barb, empty_flag,
                length, pivot, sizes, fill_empty, flip):
    """
    Create the wind barbs.

    Parameters
    ----------
    u, v
        Components of the vector in the x and y directions, respectively.

    nfullflags, nflags, nbarbs, half_barb, empty_flag
        Respectively, the number of filled flags, hollow flags, number of barbs,
        flag for half a barb, and flag for empty barb, ostensibly obtained from
        :meth:`_find_tails`.

    length
        The length of the barb staff in points.

    pivot : {"tip", "middle"} or number
        The point on the barb around which the entire barb should be
        rotated.  If a number, the start of the barb is shifted by that
        many points from the origin.

    sizes : dict
        Coefficients specifying the ratio of a given feature to the length
        of the barb. These features include:

        - *spacing*: space between features (flags, full/half barbs).
        - *height*: distance from shaft of top of a flag or full barb.
        - *width*: width of a flag, twice the width of a full barb.
        - *emptybarb*: radius of the circle used for low magnitudes.

    fill_empty : bool
        Whether the circle representing an empty barb should be filled or
        not (this changes the drawing of the polygon).

    flip : list of bool
        Whether the features should be flipped to the other side of the
        barb (useful for winds in the southern hemisphere).

    Returns
    -------
    list of arrays of vertices
        Polygon vertices for each of the wind barbs.  These polygons have
        been rotated to properly align with the vector direction.
    """

    # These control the spacing and size of barb elements relative to the
    # length of the shaft
    spacing = length * sizes.get('spacing', 0.125)
    full_height = length * sizes.get('height', 0.4)
    full_width = length * sizes.get('width', 0.25)
    empty_rad = length * sizes.get('emptybarb', 0.15)

    # Controls y point where to pivot the barb.
    pivot_points = dict(tip=0.0, middle=-length / 2.)

    endx = 0.0
    try:
        endy = float(pivot)
    except ValueError:
        endy = pivot_points[pivot.lower()]

    # Get the appropriate angle for the vector components.  The offset is
    # due to the way the barb is initially drawn, going down the y-axis.
    # This makes sense in a meteorological mode of thinking since there 0
    # degrees corresponds to north (the y-axis traditionally)
    angles = -(ma.arctan2(v, u) + np.pi / 2)

    # Used for low magnitude.  We just get the vertices, so if we make it
    # out here, it can be reused.  The center set here should put the
    # center of the circle at the location(offset), rather than at the
    # same point as the barb pivot; this seems more sensible.
    circ = CirclePolygon((0, 0), radius=empty_rad).get_verts()
    if fill_empty:
        empty_barb = circ
    else:
        # If we don't want the empty one filled, we make a degenerate
        # polygon that wraps back over itself
        empty_barb = np.concatenate((circ, circ[::-1]))

    barb_list = []

    for index, angle in np.ndenumerate(angles):
        # If the vector magnitude is too weak to draw anything, plot an
        # empty circle instead
        if empty_flag[index]:
            # We can skip the transform since the circle has no preferred
            # orientation
            barb_list.append(empty_barb)

            continue

        poly_verts = [(endx, endy)]
        offset = length

        # Handle if this barb should be flipped
        barb_height = -full_height if flip[index] else full_height

        # Add vertices for each fullflag
        for i in range(nfullflags[index]):
            # The spacing that works for the barbs is a little to much for
            # the flags, but this only occurs when we have more than 1
            # flag.
            if offset != length:
                offset += spacing / 2.

            '''
            poly_verts.extend(
                [[endx, endy + offset],
                 [endx + barb_height, endy - full_width / 2 + offset],
                 [endx, endy - full_width + offset]])
            '''

            # CHANGE {{{ fill the full flags with multiple strokes
            poly_verts.extend(
                    [[endx, endy + offset],
                     [endx + full_height/4, endy - full_width / 8 + offset],
                     [endx, endy - full_width / 8 + offset],
                     [endx + full_height/4, endy - full_width / 8 + offset],
                     [endx + full_height/2, endy - full_width / 4 + offset],
                     [endx, endy - full_width / 4 + offset],
                     [endx + full_height/2, endy - full_width / 4 + offset],
                     [endx + 3*full_height/4, endy - 3*full_width / 8 + offset],
                     [endx, endy - 3*full_width / 8 + offset],
                     [endx + 3*full_height/4, endy - 3*full_width / 8 + offset],
                     [endx + full_height, endy - full_width / 2 + offset],
                     [endx,endy-full_width/2+offset],
                     [endx + full_height, endy - full_width / 2 + offset],
                     [endx + 3*full_height/4, endy - 5*full_width / 8 + offset],
                     [endx, endy - 5*full_width / 8 + offset],
                     [endx + 3*full_height/4, endy - 5*full_width / 8 + offset],
                     [endx + full_height/2, endy - 3*full_width / 4 + offset],
                     [endx, endy - 3*full_width / 4 + offset],
                     [endx + full_height/2, endy - 3*full_width / 4 + offset],
                     [endx + full_height/4, endy - 7*full_width / 8 + offset],
                     [endx, endy - 7*full_width / 8 + offset],
                     [endx + full_height/4, endy - 7*full_width / 8 + offset],
                     [endx, endy - full_width + offset]])

            # CHANGE }}}

            offset -= full_width + spacing

        # Add vertices for each flag
        for i in range(nflags[index]):
            # The spacing that works for the barbs is a little to much for
            # the flags, but this only occurs when we have more than 1
            # flag.
            if offset != length:
                offset += spacing / 2.
            poly_verts.extend(
                [[endx, endy + offset],
                 [endx + barb_height, endy - full_width / 2 + offset],
                 [endx, endy - full_width + offset]])

            offset -= full_width + spacing

        # Add vertices for each barb.  These really are lines, but works
        # great adding 3 vertices that basically pull the polygon out and
        # back down the line
        for i in range(nbarbs[index]):
            poly_verts.extend(
                [(endx, endy + offset),
                 (endx + barb_height, endy + offset + full_width / 2),
                 (endx, endy + offset)])

            offset -= spacing

        # Add the vertices for half a barb, if needed
        if half_barb[index]:
            # If the half barb is the first on the staff, traditionally it
            # is offset from the end to make it easy to distinguish from a
            # barb with a full one
            if offset == length:
                poly_verts.append((endx, endy + offset))
                offset -= 1.5 * spacing
            poly_verts.extend(
                [(endx, endy + offset),
                 (endx + barb_height / 2, endy + offset + full_width / 4),
                 (endx, endy + offset)])

        # Rotate the barb according the angle. Making the barb first and
        # then rotating it made the math for drawing the barb really easy.
        # Also, the transform framework makes doing the rotation simple.
        poly_verts = transforms.Affine2D().rotate(-angle).transform(poly_verts)

        barb_list.append(poly_verts)

    return barb_list

def setup():
    '''设置使用中国气象风羽规范

    默认matplotlib风羽等级：
        1. 短杆：5
        2. 长杆：10
        3. 填充三角旗：50

    修改后风羽等级：
        1. 短杆：2
        2. 长杆：4
        3. 空心三角旗：20
        4. 填充三角旗：50
    '''

    Barbs.set_UVC = set_UVC
    Barbs._find_tails = _find_tails
    Barbs._make_barbs = _make_barbs

    return


def restore():
    '''Restore to matplotlib's defaults'''

    Barbs.set_UVC = ori_set_UVC
    Barbs._find_tails = ori_find_tails
    Barbs._make_barbs = ori_make_barbs

    return


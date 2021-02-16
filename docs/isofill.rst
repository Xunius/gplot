Create isofill/contourf plots
=============================

.. contents:: Table of Contents
  :local:

The ``Isofill`` class
##############################

To create a isofill/contourf plot, one creates an :py:class:`base_utils.Isofill`
object as the plotting method, and passes it to the :py:class:`base_utils.Plot2D`
constructor or the :py:func:`base_utils.plot2` function.


Define the contour levels
##############################

One key element of a good isofill/contourf plot is a set of appropriately
chosen contour levels. There are basically 2 ways to define the contour levels
in :py:class:`base_utils.Isofill`:


1. Automatically derive from input data, and a given number of levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your data may come with various orders of magnitudes, and sometimes it can be
a bit tricky (and annoying) to manually craft the contour levels for each and
every plot you create, particularly when you just want to have a quick read of
the data. The 1st approach comes as a handy choice for such cases.

To automatically derive the contour levels, these input arguments to the
constructor of :py:class:`base_utils.Isofill` are relevant:

* ``vars``: input data array(s).

  The 1st and only mandatory input argument is ``vars``, which is the input
  ``ndarray`` to plot, or a list of ``ndarray``. This is used to determine the
  value range of the input data. Missing values (masked or ``nan``) are not
  taken into account.

  The list input form is useful when one wants to use the same set of contour
  levels to plot multiple pieces of data.

* ``num``: the **desired** number of contour levels.

  Note that in order to derive nice-looking numbers in the contour levels, the
  resultant number may be sightly different.

  What is meant by "nice-looking" is that the contour level values won't be some
  floating point numbers with 5+ decimal places, like what one would get using

  ::

      >>> np.linspace(0, 30, 12)
      array([ 0.        ,  2.72727273,  5.45454545,  8.18181818, 10.90909091,
             13.63636364, 16.36363636, 19.09090909, 21.81818182, 24.54545455,
             27.27272727, 30.        ])

  Instead, :py:class:`base_utils.Isofill` would suggest something like this:

  ::

      [0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0]


* ``zero``: whether ``0`` is allowed to be one contour level.

  ``zero = 0`` exerts no inference on the inclusion of ``0``.

  ``zero = -1`` prevents the number ``0`` from being included in the contour levels,
  instead, there would be a 0-crossing contour interval, e.g. ``-2, 2``,
  that represent the 0-level with a range.

  This is very helpful in plots with a divergent colormap, e.g.
  ``plt.cm.RdBu``.  Your plot will have a white contour interval, rather than
  just various shades of blues and reds.  The white area represents a kind of
  buffer zone in which the difference is not far from 0, and the plot will
  almost always end up being cleaner and more informative.

* ``min_level``, ``max_level``, ``ql``, ``qr``: determines the lower and
  upper bounds of the data range to plot.

  ``min_level`` and ``max_level`` are used to specify the *absolute* bounds. If
  ``None`` (the default), these are taken from the minimum and maximum values
  from ``vars``.

  ``ql`` and ``qr`` are used to specify by relative bounds: ``ql`` for the left
  quantile and ``qr`` for the right quantile. E.g. ``ql = 0.01`` takes the ``0.01``
  left quantile as the lower bound, and ``qr = 0.05`` takes the 0.95 quantile
  as the upper bound. These are useful for preventing some outliers from inflating
  the colorbar.

  If both ``ql`` and ``min_level`` are given, whichever gives a greater absolute
  value is chosen as the lower bound. Similarly for ``qr`` and ``max_level``.

  If the lower/upper bound doesn't cover the entire data range, an **extension**
  is on the relevant side is activate:

  ::

        self.ext_1 = True if self.data_min < vmin else False
        self.ext_2 = True if self.data_max > vmax else False

  These will be visually represented as an **overflow** on the colorbar.




2. Manually specify the contour levels.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Manual contour levels are simply specified by the `levels` optional argument:

::

  iso = Isofill(var, 10, levels=np.arange(-10, 12, 2))


This will override effects from all the arguments listed in the above section.


Split colorbar colors
##############################

Overlay with stroke
##############################

Overlay with stroke
##############################

Create quiver plots
===================

.. contents:: Table of Contents
  :local:

The ``Quiver`` class
##############################

To create a 2D quiver plot, one creates a :py:class:`base_utils.Quiver`
object as the plotting method, and passes it to the :py:class:`base_utils.Plot2Quiver`
constructor or the :py:func:`base_utils.plot2` function.

The ``__init__()`` of :py:class:`base_utils.Quiver` takes these input arguments:

* ``step``
* ``reso``
* ``scale``
* ``keylength``
* ``linewidth``
* ``color``
* ``alpha``

``linewidth``, ``color`` and ``alpha`` should be self-explanatory. Others are explained
in further details below.

Control the quiver density
###########################

When the input data have too fine a resolution, the quiver plot may end up being
too dense and not quite readable (see :numref:`Fig.%sa <figure8>` below for an
example). This can be solved by either

1. sub-sampling the data with a step: ``u = u[::step, ::step]; v = v[::step, ::step]``, or
2. regridding the data to a lower resolution ``reso``.

Method 1 is controlled by the ``step`` input argument (see :numref:`Fig.%sb
<figure8>` below for an example), and the latter method the ``reso`` argument
(see :numref:`Fig.%sc,d <figure8>`). If both are given, the
latter one takes precedence.

.. note::
   regridding requires *scipy* as an optional dependency.


.. _figure8:

.. figure:: quiver_comparison1.png
   :width: 780px
   :align: center
   :figclass: align-center

   Density control of a quiver plot.
   (a) default quiver density ``q = Quiver()``.
   (b) reduced density by sub-sampling: ``q = Quiver(step=8)``.
   (c) reduced density by regridding: ``q = Quiver(reso=4)``.
   (d) reduced density by regridding: ``q = Quiver(reso=8)``.


Control the quiver lengths
###########################

The lengths of the quiver arrows are controlled by the ``scale`` argument.  A
larger scale value creates shorter arrows.  When left as the default ``None``,
it will try to derive a suitable scale level for the given inputs.

The length of the reference quiver arrow is controlled by the ``keylength``
argument. Given a set ``scale``, a larger ``keylength`` makes the **reference**
quiver arrow longer.  Similar as ``scale``, ``keylength`` is default to
``None``, and the plotting function will try to derive a suitable value
automatically for you.

:numref:`Fig.%s <figure9>` below shows some examples of controlling the lengths.

.. _figure9:

.. figure:: quiver_comparison2.png
   :width: 780px
   :align: center
   :figclass: align-center

   Length control of a quiver plot.
   (a) automatic scale ``q = Quiver(step=8, scale=None)``.
   (b) specify scale=200: ``q = Quiver(step=8, scale=200)``.
   (c) specify scale=500: ``q = Quiver(step=8, scale=500)``.
   (d) specify scale=500, keylength=20: ``q = Quiver(step=8, scale=500, keylength=20)``.



The mappable object
##############################

The *mappable object* of a quiver plot is stored as an attribute of the
:py:class:`base_utils.Plot2Quiver` (or
:py:class:`basemap_utils.Plot2QuiverBasemap`) object:

::

    >>> q = gplot.Quiver()
    >>> pobj = Plot2QuiverBasemap(u, v, q, xarray=lons, yarray=lats, ax=ax, projection='cyl')
    >>> pobj.plot()
    >>> pobj.quiver
    <matplotlib.quiver.Quiver object at 0x7f2e03aed750>


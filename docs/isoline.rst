Create isoline/contour plots
============================

.. contents:: Table of Contents
  :local:

The ``Isoline`` class
##############################

To create a isoline/contour plot, one creates a :py:class:`base_utils.Isoline`
object as the plotting method, and passes it to the :py:class:`base_utils.Plot2D`
constructor or the :py:func:`base_utils.plot2` function.

In many aspects, the :py:class:`base_utils.Isoline` class is similar as
:py:class:`base_utils.Isofill` (it is in fact derived from the latter).
They share these arguments in their ``__init__()`` method:

* ``vars``
* ``num``
* ``zero``
* ``split``
* ``levels``
* ``min_level``
* ``max_level``
* ``ql``
* ``qr``
* ``vcenter``
* ``cmap``

More explanations of these arguments are given in :doc:`isofill`.

There are a few arguments unique to ``Isoline``, and are introduced in below
sections.


Line width and color controls
##############################

Line width is controlled by the ``line_width`` input argument, which is default
to ``1.0``.
See :numref:`Fig.%sb <figure4>` for an example of changing the line width to a
greater value.

Line color, by default, is determined by the colormap (``cmap``).
Alternatively, one can use only the black color by specifying ``black = True``.
Or, use a different color for all contour lines ``color = 'blue'``.
For single colored isoline plots, the colorbar will not be plotted.
See :numref:`Fig.%sb,c,d <figure4>` for examples of monochromatic isoline plots.

.. _figure4:

.. figure:: isoline_comparisons.png
   :width: 600px
   :align: center
   :figclass: align-center

   Isoline plot examples. Complete script can be found in :py:func:`tests.basemap_tests.test_basemap_isolines`
   (a) default isoline plot: colored contours, ``linewidth=1``.
   (b) isoline plot with ``linewidth=2.0, color='b'``.
   (c) isoline plot with ``black=True, dash_negative=True``.
   (d) isoline plot with ``black=True, dash_negative=True, bold_lines=[0,], label=True, label_box=True``.


Use dashed line for negatives
##############################

It is also common to use dashed lines for negative contours and solid lines
for positive values, with optionally a 0-level contour as bold. These can
be achieved using:

::

    isoline = gplot.Isoline(var, 10, zero=1, black=True, dash_negative=True,
                            bold_lines=[0,])

See :numref:`Fig.%sc,d <figure4>` for examples.

.. note::

   It is possible to asign multiple levels as bold, by specifying them in a list
   to ``bold_lines``.


Label the contour lines
##############################

For plots with monochromatic contour lines, one needs to provide a different mechanism
for the reading of contour levels, such as labelling out the contours. This can
be achieved by passing in the ``label = True`` argument.

The format of the labels can be controlled by ``label_fmt``.
An optional bounding box can be added by ``label_box = True``, and one can
change the box background color by altering ``label_box_color``.
See :numref:`Fig.%sd <figure4>` for an example.







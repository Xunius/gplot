Managing subplots
=================

.. contents:: Table of Contents
  :local:

Recommended way of creating subplots
####################################

In academic works, people usually compose a single figure with multiple
subplots, sometimes to facilitate comparisons, but mostly to make the most of
the valuable real estates of a graph.

There are more than one ways of creating subplots in ``matplotlib``.
For usage with ``gplot``, the recommended way of creating subplots is:

::

    figure, axes = plt.subplots(nrows=2, ncols=2, constrained_layout=True)

The returned ``axes`` is a 2D array, holding the axes for a 2x2 grid layout.
To iterate through the axes, one can use:

::

    for ii, axii in enumerate(axes.flat):
        rowii, colii = np.unravel_index(ii, (nrows, ncols))
        ...


.. note::
   the ``constrained_layout=True`` argument is recommended. This will
   adjust the spacings of the subplots to avoid overlaps between subplots, and
   wasted spaces as well. **Do not** use ``figure.tight_layout()`` afterwards,
   as it tends to mess up the placement of a shared, global colorbar.

.. note::
   the placement of a globally shared colorbar is currently not as robust
   as a local colorbar. One may find the global colorbar tick labels
   overlaping with those in the bottom row x-axis, if the ``constrained_layout``
   is not set to ``True``.


Automatically label the subplots with alphabetic indices
##########################################################

The ``title`` input argument to the :py:class:`base_utils.Plot2D` constructor
or the :py:func:`base_utils.plot2` function is used to label the subplots. It
is defaulted to ``None``. The ``clean`` argument also has some effects. They
function a bit differently in different scenarios:


* ``title = None``:

    * If figure has only 1 subplot: no title is drawn.
    * If figure has more than 1 subplots, an alphabetic index is used as the
      subplot title, e.g. ``(a)`` for the 1st subplot, ``(b)`` for the 2nd, and
      so on. The order is row-major. After using up all the 26 letters, it will
      cycle through them again but with 2 letters at a time, e.g. ``(aa)`` for
      the 27th subplots. This rarely happens in practice.

* ``title = some_text``:

    * If figure has only 1 subplot: use ``some_text`` as the title.
    * If figure has more than 1 subplots, an alphabetic index is prepended
      to form the subplot title: ``(a) some_text``.
      An example of this can be seen :ref:`here <subplottitleexample>`.

* ``title = (x) some_text``:

    Where ``x`` is an arbitrary string. Use ``(x) some_text`` as the title. This
    can be used to override the automatic row-major ordering of the subplot
    indices. For instance, you want to label it as ``(k)`` when
    the subplot is at a position of ``(h)``.

* ``title = 'none'`` or ``clean = True``: no title is drawn in any circumstances.

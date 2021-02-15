.. Gplot documentation master file, created by
   sphinx-quickstart on Sun Feb 14 20:12:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Gplot's documentation!
=================================

.. contents:: Table of Contents
  :local:


Introduction
############

*Gplot* is a thin wrapper of `matplotlib`, `basemap` and `cartopy` for
quick and easy creations of geographical plots.


Installation
############

Install from conda
^^^^^^^^^^^^^^^^^^

``gplot`` can be installed in an existing conda environment:
::

    conda install -c guangzhi gplot

will install ``gplot`` and its dependencies for Python 3.


Dependencies
############

* Mandatory:

        * OS: Linux or MacOS. Windows is not tested.
        * Python: >= 3.
        * numpy
        * matplotlib: developed in 3.2.2. **NOTE** that versions later than 3.2.2 are incompatible with basemap.

* Optional:

        * scipy: optional, developed in 1.2.1. For 2D interpolation.

        * For plot the geography: basemap or cartopy.

                * basemap: developed in 1.2.0.
                * cartopy: optional, developed in 0.16.0, not fully supported yet.

        * For netCDF file reading: netCDF4 or CDAT or xarray or iris.

                * netCDF4: included as dependencies, developed in 1.5.5.1.
                * cdms module of CDAT: developed in 3.1.5.
                * xarray: not implemented yet.
                * iris: not implemented yet.

Quick start
###########

After installation of `gplot` and `basemap`, create a
isofill/contourf plot of the global sea level pressure field (included in the
installation) using the following snippet:
::

    import matplotlib as plt
    import gplot
    from gplot.lib import netcdf4_utils

    var = netcdf4_utils.readData('msl')
    lats = netcdf4_utils.readData('latitude')
    lons = netcdf4_utils.readData('longitude')

    figure = plt.figure(figsize=(12, 10), dpi=100)
    ax = figure.add_subplot(111)
    iso = gplot.Isofill(var)
    gplot.plot2(var, iso, ax, xarray=lons, yarray=lats,
                title='Default basemap', projection='cyl',
                nc_interface='netcdf4')
    figure.show()

The output is given below:

.. figure:: default_contourf.png
   :width: 600px
   :align: center
   :figclass: align-center

   Default contourf plot of global surface pressure field (in Pa), from ERA-I.


Documentation
###########################


.. toctree::
   :maxdepth: 2
   :caption: Contents:

    Basic workflow <basic>
    Isofill/Contourf plots <isofill>
    Isoline/Contour plots <isoline>
    Boxfill/imshow plots <boxfill>
    Colorbar <colorbar>
    Quiver plots <quiver>
    Subplot layouts <subplots>
    Misc <misc>


gplot module contents
#####################

.. toctree::
   :maxdepth: 1



Github and Contact
##################

The code of this package is hosted at https://github.com/Xunius/gplot.

For any queries, please contact xugzhi1987@gmail.com.

Contributing and getting help
#############################

We welcome contributions from the community. Please create a fork of the
project on GitHub and use a pull request to propose your changes. We strongly encourage creating
an issue before starting to work on major changes, to discuss these changes first.

For help using the package, please post issues on the project GitHub page.



License
#######

:ref:`license`




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

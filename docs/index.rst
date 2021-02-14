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

*Gplot* is a thin wrapper of `matplotlib`, `basemap` and `cartopy` for creation of quick and easy geographical plots.


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

* Mandentory:

        * OS: Linux or MacOS. Windows is not tested.
        * Python: >= 3.
        * numpy
        * matplotlib: developed in 3.2.2. **NOTE** that versions later than 3.2.2 are imcompatible with basemap.

* Optional:

        * scipy: optional, developed in 1.2.1. For 2D interpolation.

        * For plot the geography: basemap or cartopy.

                * basemap: developed in 1.2.0.
                * cartopy: optional, developed in 0.16.0, not fully supported yet.

        * For netCDF file reading: netCDF4 or CDAT or xarray or iris.

                * netCDF4: developed in 1.5.5.1.
                * cdms module of CDAT: developed in 3.1.5.
                * xarray: not implemented yet.
                * iris: not implemented yet.

Quick start
###########


More Detailed Documentation
###########################


.. toctree::
   :maxdepth: 2
   :caption: Contents:

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

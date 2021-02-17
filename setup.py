#!/usr/bin/python

# Gplot

from setuptools import find_packages, setup

setup(name='gplot',
        version='0.3a',
        description='Gplot is a thin wrapper of `matplotlib`, `basemap` and `cartopy` for the creation of quick and easy geographical plots.',
        author='Guangzhi XU',
        author_email='xugzhi1987@gmail.com',
        url='https://github.com/Xunius/gplot',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Atmospheric Science'
            ],
        install_requires=[
            "numpy",
            "scipy",
            "netcdf4",
            "matplotlib<=3.2.2",
        ],
        packages=find_packages(include=['lib', 'lib.*']),
        package_data={'tests': ['*']},
        license='GPL-3.0-or-later'
        )


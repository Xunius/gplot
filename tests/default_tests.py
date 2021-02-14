'''Tests for default matplotlib plots

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2021-01-25 14:54:04.
'''
from __future__ import print_function
from __future__ import absolute_import

#--------Import modules-------------------------
import numpy as np
import matplotlib.pyplot as plt
from gplot.lib import gplot
from gplot.lib import cdat_utils

SAVE=False



def test_plot2d_default():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='default Plot2D')
    figure.show()

    return

def test_plot2d_isofill_overflow():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1, num=10, zero=1, split=1, min_level=11000, qr=0.01)
    gplot.plot2(var1, iso, ax, title='Isofill with overflows')
    figure.show()

    return

def test_plot2d_isofill_split():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1, num=10, zero=1, split=2)
    gplot.plot2(var1, iso, ax, title='Isofill with force split')
    figure.show()

    return

def test_plot2d_boxfill():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    box=gplot.Boxfill(var1)
    gplot.plot2(var1, box, ax, title='default Boxfill')
    figure.show()

    return

def test_plot2d_axes_grid():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Plot2D axes_grid=True', axes_grid=True)
    figure.show()

    return

def test_plot2d_label_axes_True():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Plot2D label_axes=True', label_axes=True)
    figure.show()

    return

def test_plot2d_label_axes_False():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Plot2D label_axes=False', label_axes=False)
    figure.show()

    return

def test_plot2d_label_axes_all():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Plot2D label_axes="all"', label_axes='all')
    figure.show()

    return

def test_plot2d_label_axes_specified():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Plot2D label_axes=specified',
            label_axes=(0, 1, 1, 0))
    figure.show()

    return

def test_plot2d_vertical_legend():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='Plot2D vertical_legend', legend_ori='vertical')
    figure.show()

    return

def test_plot2d_subplots():

    figure=plt.figure(figsize=(12,10),dpi=100)
    plot_vars1=[var1[ii] for ii in range(3)]
    plot_vars2=[var2[ii] for ii in range(3)]
    iso1=gplot.Isofill(plot_vars1, ql=0.005, qr=0.001)
    iso2=gplot.Isofill(plot_vars2, ql=0.05, qr=0.05)
    titles1=['var1-%d' %ii for ii in range(3)]
    titles2=['var2-%d' %ii for ii in range(3)]

    for ii, vii in enumerate(plot_vars1):
        ax=figure.add_subplot(3,2,2*ii+1)
        gplot.plot2(vii, iso1, ax, title=titles1[ii], legend='local')

    for ii, vii in enumerate(plot_vars2):
        ax=figure.add_subplot(3,2,2*ii+2)
        gplot.plot2(vii, iso2, ax, title=titles2[ii], legend='local')

    figure.show()

    return

def test_plot2d_subplots_global_legend():

    figure=plt.figure(figsize=(12,10),dpi=100)
    plot_vars=[var1[ii] for ii in range(4)]
    iso1=gplot.Isofill(plot_vars, ql=0.005, qr=0.001)
    titles=['var1-%d' %ii for ii in range(4)]

    for ii, vii in enumerate(plot_vars):
        ax=figure.add_subplot(2,2,ii+1)
        gplot.plot2(vii, iso1, ax, title=titles[ii], legend='global')

    figure.show()

    return

def test_plot2d_quiver():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver()
    pquiver=gplot.Plot2Quiver(u, v, q, ax=ax, title='default quiver')
    pquiver.plot()

    figure.show()

    return

def test_plot2d_quiver2():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver()
    gplot.plot2(u, q, var_v=v, ax=ax, title='default quiver')
    figure.show()

    return

def test_plot2d_quiver3():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(step=10)
    pquiver=gplot.Plot2Quiver(u, v, q, ax=ax, title='curved quiver', curve=True)
    pquiver.plot()

    figure.show()

    return

def test_plot2d_quiver_step():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(step=5)
    pquiver=gplot.Plot2Quiver(u, v, q, ax=ax, title='quiver step=5')
    pquiver.plot()

    figure.show()

    return

def test_plot2d_quiver_step2():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(step=5)
    gplot.plot2(u, q, var_v=v, ax=ax, title='quiver step=5')

    figure.show()

    return

def test_plot2d_quiver_reso():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(reso=10)
    pquiver=gplot.Plot2Quiver(u, v, q, ax=ax, title='quiver reso=10')
    pquiver.plot()

    figure.show()

    return

def test_plot2d_quiver_scale():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(step=5, scale=500)
    pquiver=gplot.Plot2Quiver(u, v, q, ax=ax, title='quiver step=5, scale=500')
    pquiver.plot()

    figure.show()

    return

def test_plot2d_quiver_scale_keylength():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    q=gplot.Quiver(step=5, scale=500, keylength=20)
    pquiver=gplot.Plot2Quiver(u, v, q, ax=ax, title='quiver step=5, scale=500, keylength=20')
    pquiver.plot()

    figure.show()

    return

def test_plot2d_quiver_overlay():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='default Plot2D')

    q=gplot.Quiver(step=6, scale=500)
    pquiver=gplot.Plot2Quiver(u, v, q, ax=ax, title='quiver overlay')
    pquiver.plot()
    figure.show()

    return

def test_plot2d_quiver_overlay2():

    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)
    iso=gplot.Isofill(var1)
    gplot.plot2(var1, iso, ax, title='default Plot2D')

    q=gplot.Quiver(step=6, scale=500)
    gplot.plot2(u, q, var_v=v, ax=ax, title='quiver overlay')
    figure.show()

    return

if __name__=='__main__':

    var1=cdat_utils.readData('msl')
    var2=cdat_utils.readData('sst')
    u=cdat_utils.readData('u')
    v=cdat_utils.readData('v')

    # remove metadata
    var1=np.array(var1)
    var2=np.where(var2.mask, np.nan, var2)
    u=np.array(u)
    v=np.array(v)

    #----------------------Tests----------------------
    '''
    test_plot2d_default()
    test_plot2d_isofill_overflow()
    test_plot2d_isofill_split()
    test_plot2d_boxfill()
    test_plot2d_axes_grid()
    test_plot2d_vertical_legend()
    test_plot2d_subplots()
    test_plot2d_subplots_global_legend()

    test_plot2d_label_axes_True()
    test_plot2d_label_axes_False()
    test_plot2d_label_axes_all()
    test_plot2d_label_axes_specified()
    test_plot2d_quiver()
    test_plot2d_quiver2()
    test_plot2d_quiver3()
    test_plot2d_quiver_step()
    test_plot2d_quiver_step2()
    test_plot2d_quiver_reso()
    test_plot2d_quiver_scale()
    test_plot2d_quiver_scale_keylength()
    '''
    test_plot2d_quiver_overlay()
    test_plot2d_quiver_overlay2()

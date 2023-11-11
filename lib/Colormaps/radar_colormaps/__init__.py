'''多普勒天气雷达观测产品色标规范色标实现

参考文件：
  《多普勒天气雷达观测产品色标规范》(https://www.doc88.com/p-20699043245476.html)

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2023-10-27 08:32:17.
'''

__all__ = ['REFL_CMAP', 'CR_CMAP', 'V_CMAP', 'ET_CMAP', 'VIL_CMAP', 'PRE_TOTAL_CMAP', 'SW_CMAP']


import os
from ..colormap import ColorMap, Level, create_cmap_from_csv

SUB_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'images', 'radar_colormaps')


# collect all defined colormaps
RADAR_COLORMAPS = {}


#----------------------代码形式定义----------------------



#--------------------csv文件形式定义--------------------
REFL_CMAP = create_cmap_from_csv(os.path.join(SUB_DIR, 'refl.csv'), RADAR_COLORMAPS)

CR_CMAP = create_cmap_from_csv(os.path.join(SUB_DIR, 'cr.csv'), RADAR_COLORMAPS)

V_CMAP    = create_cmap_from_csv(os.path.join(SUB_DIR, 'v.csv'), RADAR_COLORMAPS)

ET_CMAP   = create_cmap_from_csv(os.path.join(SUB_DIR, 'et.csv'), RADAR_COLORMAPS)

VIL_CMAP  = create_cmap_from_csv(os.path.join(SUB_DIR, 'vil.csv'), RADAR_COLORMAPS)

PRE_TOTAL_CMAP  = create_cmap_from_csv(os.path.join(SUB_DIR, 'pre_total.csv'), RADAR_COLORMAPS)

SW_CMAP  = create_cmap_from_csv(os.path.join(SUB_DIR, 'sw.csv'), RADAR_COLORMAPS)



#-------------Main---------------------------------
if __name__=='__main__':

    os.makedirs(IMG_DIR, exist_ok=True)

    for kk, vv in RADAR_COLORMAPS.items():
        print(f'plot {kk}')
        ax = vv.plot_demo()
        fig = ax.get_figure()

        #----------------- Save plot------------
        plot_save_name = '{}_demo.png'.format(vv.description)
        plot_save_name = os.path.join(IMG_DIR, plot_save_name)
        print('\n# <cma_colors>: Save figure to', plot_save_name)
        fig.savefig(plot_save_name, dpi=100, bbox_inches='tight')




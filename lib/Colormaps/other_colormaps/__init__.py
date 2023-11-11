'''其它色标

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2023-10-27 10:32:05.
'''

__all__ = ['RAIN_CMAP' ]


import os
from ..colormap import ColorMap, Level, create_cmap_from_csv

SUB_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'images', 'other_colormaps')


# collect all defined colormaps
OTHER_COLORMAPS = {}


#----------------------代码形式定义----------------------



#--------------------csv文件形式定义--------------------
RAIN_1H_CMAP = create_cmap_from_csv(os.path.join(SUB_DIR, 'rain_1h.csv'), OTHER_COLORMAPS)




#-------------Main---------------------------------
if __name__=='__main__':

    os.makedirs(IMG_DIR, exist_ok=True)

    for kk, vv in OTHER_COLORMAPS.items():
        print(f'plot {kk}')
        ax = vv.plot_demo()
        fig = ax.get_figure()

        #----------------- Save plot------------
        plot_save_name = '{}_demo.png'.format(vv.description)
        plot_save_name = os.path.join(IMG_DIR, plot_save_name)
        print('\n# <cma_colors>: Save figure to', plot_save_name)
        fig.savefig(plot_save_name, dpi=100, bbox_inches='tight')




'''中国气象局《气象预报服务产品色标标准》色标实现

参考文件：
 《中国气象局气象预报服务产品色标标准》（征求意见稿, 2009-11.23）

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2023-10-24 09:32:09.
'''

__all__ = ['TEMP_CMAP',            'DTEMP_CMAP',           'TEMP_ANO_CMAP',
           'PRE_LEVEL_CMAP',       'PRE_TOTAL_CMAP',       'SNOW_LEVEL_CMAP',
           'PRE_ANO_CMAP',         'RH_CMAP',              'ALARM_LEVEL_CMAP',
           'DRAUGHT_LEVEL_CMAP',   'FLOOD_LEVEL_CMAP',     'FOG_CMAP',
           'SANDSTORM_LEVEL_CMAP', 'SNOW_DEPTH_CMAP',      'WIND_LEVEL_CMAP',
           'RAIN_1H_CMAP',         'RAIN_3H_CMAP',         'TEMP_RT_CMAP',
           'WS10_CMAP',            'SLP_CMAP',             'WS10_TYPHOONE_CMAP',
           'RH850_CMAP',           'SST_CMAP',             'VIS_CMAP',
           ]

import os
from ..colormap import ColorMap, Level, create_cmap_from_csv

SUB_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'images', 'cma_colormaps')


# collect all defined colormaps
CMA_COLORMAPS = {}


#----------------------代码形式定义----------------------

# 气温分布图配色表
TEMP_CMAP = ColorMap(name='temp',
                     unit=r'$^{\circ}C$',
                     level_colors=[
                         Level(None , -30  , (2   , 12  , 100)) ,
                         Level(-30  , -28  , (7   , 30  , 120)) ,
                         Level(-28  , -26  , (17  , 49  , 139)) ,
                         Level(-26  , -24  , (27  , 68  , 159)) ,
                         Level(-24  , -22  , (38  , 87  , 179)) ,
                         Level(-22  , -20  , (48  , 106 , 199)) ,
                         Level(-20  , -18  , (59  , 126 , 219)) ,
                         Level(-18  , -16  , (78  , 138 , 221)) ,
                         Level(-16  , -14  , (97  , 150 , 224)) ,
                         Level(-14  , -12  , (116 , 163 , 226)) ,
                         Level(-12  , -10  , (135 , 175 , 229)) ,
                         Level(-10  , -8   , (155 , 188 , 232)) ,
                         Level(-8   , -6   , (154 , 196 , 220)) ,
                         Level(-6   , -4   , (153 , 205 , 208)) ,
                         Level(-4   , -2   , (152 , 214 , 196)) ,
                         Level(-2   , 0    , (151 , 232 , 173)) ,
                         Level(0    , 2    , (215 , 222 , 126)) ,
                         Level(2    , 4    , (234 , 219 , 112)) ,
                         Level(4    , 6    , (244 , 217 , 99))  ,
                         Level(6    , 8    , (250 , 204 , 79))  ,
                         Level(8    , 10   , (247 , 180 , 45))  ,
                         Level(10   , 12   , (242 , 155 , 0))   ,
                         Level(12   , 14   , (241 , 147 , 3))   ,
                         Level(14   , 16   , (240 , 132 , 10))  ,
                         Level(16   , 18   , (239 , 117 , 17))  ,
                         Level(18   , 20   , (238 , 102 , 24))  ,
                         Level(20   , 22   , (238 , 88  , 31))  ,
                         Level(22   , 24   , (231 , 75  , 26))  ,
                         Level(24   , 26   , (224 , 63  , 22))  ,
                         Level(26   , 28   , (217 , 51  , 18))  ,
                         Level(28   , 30   , (208 , 36  , 14))  ,
                         Level(30   , 32   , (194 , 0   , 3))   ,
                         Level(32   , 34   , (181 , 1   , 9))   ,
                         Level(34   , 35   , (169 , 2   , 16))  ,
                         Level(35   , 37   , (138 , 5   , 25))  ,
                         Level(37   , 40   , (111 , 0   , 21))  ,
                         Level(40   , None , (80  , 0   , 15))  ,
                         ],
                     description='气温分布图配色表')


# 变温分布图配色表
DTEMP_CMAP = ColorMap(name='dtemp',
                     unit=r'$^{\circ}C$',
                     level_colors=[
                         Level(None , -16  , (2   , 12  , 100)) ,
                         Level(-16  , -14  , (17  , 49  , 139)) ,
                         Level(-14  , -12  , (38  , 87  , 179)) ,
                         Level(-12  , -10  , (59  , 126 , 219)) ,
                         Level(-10  , -8   , (97  , 150 , 224)) ,
                         Level(-8   , -6   , (135 , 175 , 229)) ,
                         Level(-6   , -4   , (154 , 196 , 220)) ,
                         Level(-4   , -2   , (152 , 214 , 196)) ,
                         Level(-2   , -0   , (151 , 232 , 173)) ,
                         Level(0    , 2    , (215 , 222 , 126)) ,
                         Level(2    , 4    , (244 , 217 , 99))  ,
                         Level(4    , 6    , (247 , 180 , 45))  ,
                         Level(6    , 8    , (241 , 147 , 3))   ,
                         Level(8    , 10   , (239 , 117 , 17))  ,
                         Level(10   , 12   , (231 , 75  , 26))  ,
                         Level(12   , 14   , (208 , 36  , 14))  ,
                         Level(14   , 16   , (169 , 2   , 16))  ,
                         Level(16   , None , (111 , 0   , 21))  ,
                         ],
                     description='变温分布图配色表')


#气温距平分布图配色表
TEMP_ANO_CMAP = ColorMap(name='temp_ano',
                     unit=r'$^{\circ}C$',
                     level_colors=[
                         Level(None , -8   , (2   , 12  , 100)) ,
                         Level(-8   , -7   , (17  , 49  , 139)) ,
                         Level(-7   , -6   , (38  , 87  , 179)) ,
                         Level(-6   , -5   , (59  , 126 , 219)) ,
                         Level(-5   , -4   , (97  , 150 , 224)) ,
                         Level(-4   , -3   , (135 , 175 , 229)) ,
                         Level(-3   , -2   , (154 , 196 , 220)) ,
                         Level(-2   , -1   , (152 , 214 , 196)) ,
                         Level(-1   , 0    , (151 , 232 , 173)) ,
                         Level(0    , 1    , (215 , 222 , 126)) ,
                         Level(1    , 2    , (244 , 217 , 99))  ,
                         Level(2    , 3    , (247 , 180 , 45))  ,
                         Level(3    , 4    , (241 , 147 , 3))   ,
                         Level(4    , 5    , (239 , 117 , 17))  ,
                         Level(5    , 6    , (231 , 75  , 26))  ,
                         Level(6    , 7    , (208 , 36  , 14))  ,
                         Level(7    , 8    , (169 , 2   , 16))  ,
                         Level(8    , None , (111 , 0   , 21))  ,
                         ],
                     description='气温距平分布图配色表')


# 降雨量等级分布图配色表
PRE_LEVEL_CMAP = ColorMap(name='pre_level',
                     unit='',
                     level_colors=[
                         Level(0.1 , 1.5  , (165 , 243 , 141) , '小雨')     ,
                         Level(1.5 , 7    , (61  , 185 , 63)  , '中雨')     ,
                         Level(7   , 15   , (99  , 184 , 249) , '大雨')     ,
                         Level(15  , 40   , (0   , 0   , 254) , '暴雨')     ,
                         Level(40  , 50   , (243 , 5   , 238) , '大暴雨')   ,
                         Level(50  , 100 , (129 , 0   , 64)  , '特大暴雨') ,
                         Level(100  , None , (129 , 0   , 64)  , '特大暴雨') ,
                         ],
                     description='降雨量等级分布图配色表')


# 累计降雨量分布图配色表
PRE_TOTAL_CMAP = ColorMap(name='pre_total',
                     unit='mm',
                     level_colors=[
                         Level(0.1  , 9.9  , (165 , 243 , 141)) ,
                         Level(10   , 24.9 , (153 , 210 , 202)) ,
                         Level(25   , 49.9 , (155 , 188 , 232)) ,
                         Level(50   , 99.9 , (107 , 157 , 225)) ,
                         Level(100  , 200  , (59  , 126 , 219)) ,
                         Level(200  , 250  , (43  , 92  , 194)) ,
                         Level(250  , 300  , (28  , 59  , 169)) ,
                         Level(300  , 400  , (17  , 44  , 144)) ,
                         Level(400  , 600  , (7   , 30  , 120)) ,
                         Level(600  , 800  , (70  , 25  , 129)) ,
                         Level(800  , 1000 , (134 , 21  , 138)) ,
                         Level(1000 , 2000 , (200 , 17  , 169)) ,
                         Level(2000 , None , (129 , 0   , 64))  ,
                         ],
                     description='累计降雨量分布图配色表')


# 降雪量等级分布图配色表
SNOW_LEVEL_CMAP = ColorMap(name='snow_level',
                     unit='',
                     level_colors=[
                         Level(1 , 1 , (153 , 210 , 202) , '小雪') ,
                         Level(2 , 2 , (155 , 188 , 232) , '中雪') ,
                         Level(3 , 3 , (107 , 157 , 225) , '大雪') ,
                         Level(4 , 4 , (59  , 126 , 219) , '暴雪') ,
                         ],
                     description='降雪量等级分布图配色表')



# 降水量距平百分率分布图配色表
PRE_ANO_CMAP = ColorMap(name='pre_ano',
                     unit='%',
                     level_colors=[
                         Level(-100 , -75  , (177 , 9   , 9))   ,
                         Level(-75  , -50  , (221 , 83  , 30))  ,
                         Level(-50  , -25  , (236 , 152 , 0))   ,
                         Level(-25  , 0    , (254 , 217 , 99))  ,
                         Level(0    , 25   , (151 , 232 , 173)) ,
                         Level(25   , 50   , (154 , 196 , 220)) ,
                         Level(50   , 100  , (116 , 163 , 226)) ,
                         Level(100  , 150  , (59  , 126 , 219)) ,
                         Level(150  , 200  , (27  , 68  , 159)) ,
                         Level(200  , None , (2   , 12  , 100)) ,
                         ],
                     description='降水量距平百分率分布图配色表')


# 相对湿度分布图配色表
RH_CMAP = ColorMap(name='rh',
                     unit='%',
                     level_colors=[
                         Level(0  , 10  , (151 , 232 , 173)) ,
                         Level(10 , 20  , (153 , 210 , 202)) ,
                         Level(20 , 30  , (155 , 188 , 232)) ,
                         Level(30 , 40  , (107 , 157 , 225)) ,
                         Level(40 , 50  , (59  , 126 , 219)) ,
                         Level(50 , 60  , (43  , 92  , 194)) ,
                         Level(60 , 70  , (28  , 59  , 169)) ,
                         Level(70 , 80  , (17  , 44  , 144)) ,
                         Level(80 , 90  , (7   , 30  , 120)) ,
                         Level(90 , 100 , (0   , 15  , 80))  ,
                         ],
                     description='相对湿度分布图配色表')


#--------------------csv文件形式定义--------------------
TEMP_CMAP            = create_cmap_from_csv(os.path.join(SUB_DIR, 'temp.csv'), CMA_COLORMAPS)
DTEMP_CMAP           = create_cmap_from_csv(os.path.join(SUB_DIR, 'dtemp.csv'), CMA_COLORMAPS)
TEMP_ANO_CMAP        = create_cmap_from_csv(os.path.join(SUB_DIR, 'temp_ano.csv'), CMA_COLORMAPS)
PRE_LEVEL_CMAP       = create_cmap_from_csv(os.path.join(SUB_DIR, 'pre_level.csv'), CMA_COLORMAPS)
PRE_TOTAL_CMAP       = create_cmap_from_csv(os.path.join(SUB_DIR, 'pre_total.csv'), CMA_COLORMAPS)
SNOW_LEVEL_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'snow_level.csv'), CMA_COLORMAPS)
PRE_ANO_CMAP         = create_cmap_from_csv(os.path.join(SUB_DIR, 'pre_ano.csv'), CMA_COLORMAPS)
RH_CMAP              = create_cmap_from_csv(os.path.join(SUB_DIR, 'rh.csv'), CMA_COLORMAPS)
ALARM_LEVEL_CMAP     = create_cmap_from_csv(os.path.join(SUB_DIR, 'alarm_level.csv'), CMA_COLORMAPS)
DRAUGHT_LEVEL_CMAP   = create_cmap_from_csv(os.path.join(SUB_DIR, 'draught_level.csv'), CMA_COLORMAPS)
FLOOD_LEVEL_CMAP     = create_cmap_from_csv(os.path.join(SUB_DIR, 'flood_level.csv'), CMA_COLORMAPS)
FOG_CMAP             = create_cmap_from_csv(os.path.join(SUB_DIR, 'fog.csv'), CMA_COLORMAPS)
SANDSTORM_LEVEL_CMAP = create_cmap_from_csv(os.path.join(SUB_DIR, 'sandstorm_level.csv'), CMA_COLORMAPS)
SNOW_DEPTH_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'snow_depth.csv'), CMA_COLORMAPS)
WIND_LEVEL_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'wind_level.csv'), CMA_COLORMAPS)

RAIN_1H_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'rain_1h.csv'), CMA_COLORMAPS)
RAIN_3H_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'rain_3h.csv'), CMA_COLORMAPS)
TEMP_RT_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'temp_rt.csv'), CMA_COLORMAPS)
WS10_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'ws10.csv'), CMA_COLORMAPS)
SLP_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'slp.csv'), CMA_COLORMAPS)

WS10_TYPHOONE_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'ws10_typhoon.csv'), CMA_COLORMAPS)

RH850_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'rh850.csv'), CMA_COLORMAPS)
SST_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'sst.csv'), CMA_COLORMAPS)
VIS_CMAP      = create_cmap_from_csv(os.path.join(SUB_DIR, 'vis.csv'), CMA_COLORMAPS)


#-------------Main---------------------------------
if __name__=='__main__':

    os.makedirs(IMG_DIR, exist_ok=True)

    for kk, vv in CMA_COLORMAPS.items():
        print(f'plot {kk}')
        ax = vv.plot_demo()
        fig = ax.get_figure()

        #----------------- Save plot------------
        plot_save_name = '{}_demo.png'.format(vv.description)
        plot_save_name = os.path.join(IMG_DIR, plot_save_name)
        print('\n# <cma_colors>: Save figure to', plot_save_name)
        fig.savefig(plot_save_name, dpi=100, bbox_inches='tight')




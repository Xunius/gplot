# 自定义matplotlib气象色标实现


## 中国气象局《气象预报服务产品色标标准》色标实现

### 参考文件

《中国气象局气象预报服务产品色标标准》（征求意见稿, 2009-11-23）。
见`docs/气象色标标准.pdf`。


### 包含色标


| 色标描述                                              | 变量名                                 | 定义文件位置                                      | 示例图位置               |
| ---------------------------------                     | -------------------------------------- | -------------------------------------             | ------------------------ |
| 预报（警报）等级分布图配色表                          | `CMA_COLORMAPS.ALARM_LEVEL_CMAP`       | `colormap_defs/cma_colormaps/alarm_level.csv`     | `images/cma_colormaps/`  |
| 气象干旱等级分布图配色表                              | `CMA_COLORMAPS.DRAUGHT_LEVEL_CMAP`     | `colormap_defs/cma_colormaps/draught_level.csv`   | ~                        |
| 变温分布图配色表                                      | `CMA_COLORMAPS.DTEMP_CMAP`             | `colormap_defs/cma_colormaps/dtemp.csv`           | ~                        |
| 洪涝等级分布图配色表                                  | `CMA_COLORMAPS.FLOOD_LEVEL_CMAP`       | `colormap_defs/cma_colormaps/flood_level.csv`     | ~                        |
| 雾区分布图配色表                                      | `CMA_COLORMAPS.FOG_CMAP`               | `colormap_defs/cma_colormaps/fog.csv`             | ~                        |
| 降水量距平百分率分布图配色表                          | `CMA_COLORMAPS.PRE_ANO_CMAP`           | `colormap_defs/cma_colormaps/pre_ano.csv`         | ~                        |
| 降雨量等级分布图配色表                                | `CMA_COLORMAPS.PRE_LEVEL_CMAP`         | `colormap_defs/cma_colormaps/pre_level.csv`       | ~                        |
| 累计降雨量分布图配色表                                | `CMA_COLORMAPS.PRE_TOTAL_CMAP`         | `colormap_defs/cma_colormaps/pre_total.csv`       | ~                        |
| 相对湿度分布图配色表                                  | `CMA_COLORMAPS.RH_CMAP`                | `colormap_defs/cma_colormaps/rh.csv`              | ~                        |
| 沙尘天气等级分布图配色表                              | `CMA_COLORMAPS.SANDSTORM_LEVEL_CMAP`   | `colormap_defs/cma_colormaps/sandstorm_level.csv` | ~                        |
| 积雪分布图配色表                                      | `CMA_COLORMAPS.SNOW_DEPTH_CMAP`        | `colormap_defs/cma_colormaps/snow_depth.csv`      | ~                        |
| 降雪量等级分布图配色表                                | `CMA_COLORMAPS.SNOW_LEVEL_CMAP`        | `colormap_defs/cma_colormaps/snow_level.csv`      | ~                        |
| 气温距平分布图配色表                                  | `CMA_COLORMAPS.TEMP_ANO_CMAP`          | `colormap_defs/cma_colormaps/temp_ano.csv`        | ~                        |
| 气温分布图配色表                                      | `CMA_COLORMAPS.TEMP_CMAP`              | `colormap_defs/cma_colormaps/temp.csv`            | ~                        |
| 风力等级（6级以上）分布图配色表                       | `CMA_COLORMAPS.WIND_LEVEL_CMAP`        | `colormap_defs/cma_colormaps/wind_level.csv`      | ~                        |
| 1h累积降水量实况色标(采自国家气象信息中心)            | `CMA_COLORMAPS.RAIN_1H_CMAP`           | `colormap_defs/cma_colormaps/rain_1h.csv`         | ~                        |
| 3h累积降水量实况色标(采自国家气象信息中心)            | `CMA_COLORMAPS.RAIN_3H_CMAP`           | `colormap_defs/cma_colormaps/rain_3h.csv`         | ~                        |
| 气温实况色标(采自国家气象信息中心)                    | `CMA_COLORMAPS.TEMP_RT_CMAP`           | `colormap_defs/cma_colormaps/temp_rt.csv`         | ~                        |
| 10m风速色标(6.25km 1h 采自国家气象信息中心)           | `CMA_COLORMAPS.WS10_CMAP`              | `colormap_defs/cma_colormaps/ws10.csv`            | ~                        |
| 海平面气压色标(台风动力诊断 采自国家气象信息中心)     | `CMA_COLORMAPS.SLP_CMAP`               | `colormap_defs/cma_colormaps/slp.csv`             | ~                        |
| 10m风速色标(台风动力诊断 采自国家气象信息中心)        | `CMA_COLORMAPS.WS_TYPHOON_CMAP`        | `colormap_defs/cma_colormaps/ws10_typhoon.csv`    | ~                        |
| 850hPa相对湿度色标(台风湿度诊断 采自国家气象信息中心) | `CMA_COLORMAPS.RH850_CMAP`             | `colormap_defs/cma_colormaps/rh850.csv`           | ~                        |
| 海表温度色标(采自国家气象信息中心)                    | `CMA_COLORMAPS.SST_CMAP`               | `colormap_defs/cma_colormaps/sst.csv`             | ~                        |
| 最低能见度色标(采自国家气象信息中心)                  | `CMA_COLORMAPS.VIS_CMAP`               | `colormap_defs/cma_colormaps/vis.csv`             | ~                        |


### 色标样例


![气温分布图配色表](images/cma_colormaps/气温分布图配色表_demo.png)


![降雨量等级分布图配色表](images/cma_colormaps/降雨量等级分布图配色表_demo.png)


![风力等级（6级以上）分布图配色表](images/cma_colormaps/风力等级（6级以上）分布图配色表_demo.png)


### 使用方法

E.g.

```python

from Colormaps.CMA_COLORMAPS import TEMP_CMAP

# prepare your data ...
XX, YY = ...
data = ...

# plot data
fig, ax = plt.subplots()
ax.pcolormesh(XX, YY, data,
              cmap=TEMP_CMAP.cmap,
              norm=TEMP_CMAP.norm,
              extend=TEMP_CMAP.extend)

# plot colorbar
cbar = TEMP_CMAP.plot_colorbar(ax, orientation='horizontal', spacing='uniform')
fig.show()
```

+ `orientation`: `'vertical'` (default) or `'horizontal'`
+ `spacing`: `'uniform'` (default) or `'proportional'`


### 运行示例代码


```python

python cma_colormaps/__init__.py
```



## 《多普勒天气雷达观测产品色标规范》色标实现

### 参考文件

  《多普勒天气雷达观测产品色标规范》(https://www.doc88.com/p-20699043245476.html)



### 包含色标


| 色标描述         | 变量名                           | 定义文件位置                                  | 示例图位置                |
| ---------------- | ------------------------------   | ----------------------------                  | ------------------------  |
| 反射率色标       | `RADAR_COLORMAPS.REFL_CMAP`      | `colormap_defs/radar_colormaps/refl.csv`      | `images/radar_colormaps/` |
| 组合反射率色标   | `RADAR_COLORMAPS.CR_CMAP`        | `colormap_defs/radar_colormaps/cr.csv`        | ~                         |
| 多普勒速度色标   | `RADAR_COLORMAPS.V_CMAP`         | `colormap_defs/radar_colormaps/v.csv`         | ~                         |
| 回波顶高色标     | `RADAR_COLORMAPS.ET_CMAP`        | `colormap_defs/radar_colormaps/et.csv`        | ~                         |
| 液态含水量色标   | `RADAR_COLORMAPS.VIL_CMAP`       | `colormap_defs/radar_colormaps/vil.csv`       | ~                         |
| 降水累积量色标   | `RADAR_COLORMAPS.PRE_TOTAL_CMAP` | `colormap_defs/radar_colormaps/pre_total.csv` | ~                         |
| 谱宽色标         | `RADAR_COLORMAPS.SW_CMAP`        | `colormap_defs/radar_colormaps/sw.csv`        | ~                         |


### 色标样例


![反射率色标](images/radar_colormaps/反射率色标_demo.png)

![组合反射率色标](images/radar_colormaps/组合反射率色标_demo.png)

![回波顶高色标](images/radar_colormaps/回波顶高色标_demo.png)

![液态含水量色标](images/radar_colormaps/液态含水量色标_demo.png)




## 其它色标



### 包含色标


| 色标描述               | 变量名                         | 定义文件位置                                | 示例图位置                |
| ----------------       | ------------------------------ | ----------------------------                | ------------------------  |
| 1h降水量色标(武杰提供) | `OTHER_COLORMAPS.RAIN_1H_CMAP` | `colormap_defs/other_colormaps/rain_1h.csv` | `images/other_colormaps/` |



### 色标样例


![降水累积量色标(武杰提供)](images/other_colormaps/1h降水量色标_demo.png)


## 贡献代码

### 添加新色标系列


新色标系列建议在本库根目录下新建文件夹，例如

`Colormaps/colormap_defs/my_colormaps`。

之后，在 `my_colormaps` 内以`csv`文件格式新增色标。如新建`my_colormaps/pre_total.csv` , 其中：


```
description=累计降雨量分布图配色表
unit=mm
vmin , vmax , r   , g   , b   , label
0.1  , 9.9  , 165 , 243 , 141 ,
10   , 24.9 , 153 , 210 , 202 ,
25   , 49.9 , 155 , 188 , 232 ,
50   , 99.9 , 107 , 157 , 225 ,
100  , 200  , 59  , 126 , 219 ,
200  , 250  , 43  , 92  , 194 ,
250  , 300  , 28  , 59  , 169 ,
300  , 400  , 17  , 44  , 144 ,
400  , 600  , 7   , 30  , 120 ,
600  , 800  , 70  , 25  , 129 ,
800  , 1000 , 134 , 21  , 138 ,
1000 , 2000 , 200 , 17  , 169 ,
2000 , None , 129 , 0   , 64  ,
```

更多示例见 `colormap_defs/cma_colormaps`, `colormap_defs/radar_colormaps`。

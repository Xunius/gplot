'''自定义matplotlib色标实现

Author: guangzhi XU (xugzhi1987@gmail.com; guangzhi.xu@outlook.com)
Update time: 2023-10-24 09:31:38.
'''




# -------- Import modules -------------------------
import os
from typing import Tuple, List, Union, Optional
from collections import namedtuple
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import matplotlib as mpl


# data to store a single level, with these fields:
# vmin, vmax: min/max value of the level, e.g. -30, -20
# if any of vmin and vmax is None, and the Level is the 1st one in the entire
# colormap, it means an underflow level. E.g. vmin=None, vmax=-30 means a level
# that corresponds to values <= -30.

# if any of vmin and vmax is None, and the Level is the last one in the entire
# colormap, it means an overflow level. E.g. vmin=40, vmax=None means a level
# that corresponds to values >= 40.

# rgb_tuple: (r, g, b) values, within range [0, 255].

# label: optional string label. E.g. '暴雨', '8级'.
Level = namedtuple('Level', ['vmin', 'vmax', 'rgb_tuple', 'label'], defaults=[''])




@dataclass
class ColorMap(object):
    """Colormap class

    name (str): name of colormap, e.g. 'pre'.
    unit (str): unit of colormap bin edges/centers, e.g. 'mm'.
    level_colors (list): list of Level tuples, defining the levels and colors.
    description (str): text description of the colormap.
    """

    name         : str  = ''
    unit         : str  = ''
    level_colors : list = field(default_factory = list)
    description  : str  = ''


    def __post_init__(self):

        if len(self.level_colors) == 0:
            res = self.init_default_levels()
        elif len(self.level_colors) == 1:
            res = self.init_single_level()
        else:
            res = self.init_from_levels()

        self._bin_edges, self._bin_centers, self._cmap, self._norm, self._extend,\
            self._labels = res

        # colorbar ticks
        if all([x == '' for x in self.labels]):
            # if no labels, use boundary numbers as ticks
            self._ticks = self.bin_edges
            self._tick_labels = None
            self.spacing = 'proportional'
        else:
            # if labels provided, set ticks at level centers, and use uniform
            # spacing
            self._ticks = self.bin_centers
            self._tick_labels = self.labels
            self.spacing = 'uniform'

    @property
    def bin_edges(self):
        return self._bin_edges

    @property
    def bin_centers(self):
        return self._bin_centers

    @property
    def cmap(self):
        return self._cmap

    @property
    def norm(self):
        return self._norm

    @property
    def extend(self):
        return self._extend

    @property
    def labels(self):
        return self._labels

    @property
    def ticks(self):
        return self._ticks

    @property
    def tick_labels(self):
        return self._tick_labels


    @staticmethod
    def norm_rgb(rgb_tuple: Tuple) -> Tuple:
        '''Normalize RGB values to [0, 1] range'''
        return tuple(map(lambda x: x/255, rgb_tuple))


    @staticmethod
    def get_bin_centers(bin_edges: Union[List, NDArray]) -> NDArray:
        '''Get bin center values from bin edges'''

        bin_edges = np.array(bin_edges)
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

        return bin_centers


    def init_default_levels(self):
        '''Init a default linear colormap'''

        bin_edges   = np.linspace(-1, 1, 256)
        bin_centers = self.get_bin_centers(bin_edges)
        cmap        = plt.cm.RdBu_r
        norm        = mpl.colors.Normalize()
        extend      = 'neither'
        labels      = ['']

        return bin_edges, bin_centers, cmap, norm, extend, labels


    def init_single_level(self):
        '''Init a single level colormap'''

        name        = self.name or 'my_cmap'
        vmin        = self.level_colors[0].vmin
        vmax        = self.level_colors[0].vmax
        bin_edges   = np.array([vmin, vmax])
        bin_centers = self.get_bin_centers(bin_edges)
        rgb         = self.norm_rgb(self.level_colors[0].rgb_tuple)
        cmap        = mpl.colors.ListedColormap([rgb,], name=name, N=1)
        norm        = mpl.colors.Normalize()
        extend      = 'neither'
        labels      = self.level_colors[0].label

        return bin_edges, bin_centers, cmap, norm, extend, labels


    def init_from_levels(self):
        '''Init from a list of Level objs'''

        # left most level
        first_level = self.level_colors[0]
        vmin, vmax, color, label = first_level
        if vmin is None or vmax is None:
            extend_left = True
        else:
            extend_left = False

        # right most level
        last_level = self.level_colors[-1]
        vmin, vmax, color, label = last_level
        if vmin is None or vmax is None:
            extend_right = True
        else:
            extend_right = False

        if extend_left and extend_right:
            extend = 'both'
        elif extend_left and not extend_right:
            extend = 'min'
        elif not extend_left and extend_right:
            extend = 'max'
        elif not extend_left and not extend_right:
            extend = 'neither'

        # levels in the middle
        mid_levels = self.level_colors[int(extend_left):len(self.level_colors)-\
                int(extend_right)]

        if all([x.vmin == x.vmax for x in mid_levels]):
            # if vmin == vmax for all levels
            bin_centers = [x.vmin for x in mid_levels]
            bin_edges = [bin_centers[0]*2 - bin_centers[1]] +\
                    bin_centers +\
                    [bin_centers[-1]*2 - bin_centers[-2]]
            bin_edges = self.get_bin_centers(bin_edges)
        else:
            # if vmin != vmax for all levels
            bin_edges = [mid_levels[0].vmin,] + [x.vmax for x in mid_levels]
            bin_centers = self.get_bin_centers(bin_edges)

        colors = [self.norm_rgb(x.rgb_tuple) for x in mid_levels]
        labels = [x.label for x in mid_levels]
        n_levels = len(mid_levels)

        assert len(bin_edges) - len(colors) == 1, 'length wrong'
        assert len(bin_centers) == len(colors), 'length wrong'

        # create cmap obj
        name = self.name or 'my_cmap'
        cmap = mpl.colors.ListedColormap(colors, name=name, N=len(colors))

        # set overflow
        if extend_left:
            cmap.set_under(self.norm_rgb(first_level.rgb_tuple))

        if extend_right:
            cmap.set_over(self.norm_rgb(last_level.rgb_tuple))

        cmap.colorbar_extend = extend

        # create norm
        norm = mpl.colors.BoundaryNorm(bin_edges, n_levels)


        return bin_edges, bin_centers, cmap, norm, extend, labels


    def plot_demo(self, ax=None):
        '''Plot colorbar showing the colormap'''

        if ax is None:
            fig, ax = plt.subplots(figsize=(3, 6), dpi=100)

        vmin = np.min(self.bin_edges)
        vmax = np.max(self.bin_edges)

        # values
        yy = np.r_[np.array(vmin-1), self.bin_centers, self.bin_edges, np.array(vmax+1)]
        yy.sort()
        # make 3 columns array
        xx = np.arange(3)
        XX, YY = np.meshgrid(xx, yy)

        ax.pcolormesh(XX, YY, YY, cmap=self.cmap, norm=self.norm)
        ax.set_xticklabels([])
        ax.set_yticks(yy)

        # plot colorbar
        #cbar = fig.colorbar(cs, ax=ax, shrink=1.0, fraction=0.2,
        '''
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=self.norm,
                                                  cmap=self.cmap),
                            ax=ax,
                            ticks=self.ticks,
                            spacing=self.spacing,
                            extend=self.extend, label=self.unit)

        if self.tick_labels is not None:
            cbar.set_ticklabels(self.tick_labels)
        '''
        self.plot_colorbar(ax)

        ax.set_title(self.description)

        fig.show()

        return ax


    def plot_colorbar(self, ax, cax=None, orientation='vertical', spacing='uniform'):

        fig = ax.get_figure()
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=self.norm, cmap=self.cmap),
                            ax=ax,
                            cax=cax,
                            ticks=self.ticks,
                            spacing=spacing,
                            extend=self.extend,
                            orientation=orientation,
                            label=self.unit)

        if self.tick_labels is not None:
            cbar.set_ticklabels(self.tick_labels)

        return cbar


    def read_from_csv(self, file_path: str):
        '''Read level and color definitions from a csv file

        Args:
            file_path (str): absolute file path to the csv file.

        Format of the csv file:

        description=<description text>
        unit=<unit string of vmin, vmax values>
        vmin , vmax , r   , g   , b  , label
        <x>  , <y>  , <r> , <g> , <b>, <optional label str>

        E.g.

        description=积雪分布图配色表
        unit=cm
        vmin , vmax , r   , g   , b   , label
        0    , 5    , 151 , 232 , 173 ,
        5    , 10   , 155 , 188 , 232 ,
        10   , 15   , 59  , 126 , 219 ,
        15   , 20   , 28  , 59  , 169 ,
        20   , 25   , 7   , 30  , 120 ,
        25   , 50   , 134 , 21  , 138 ,
        50   , None , 200 , 17  , 169 ,
        '''

        self.level_colors = []

        with open(file_path, 'r') as fin:
            # header line 1
            line = fin.readline().strip()
            self.description = line.split('=')[1]

            # header line 2
            line = fin.readline().strip()
            self.unit = line.split('=')[1]

            if self.unit[:2] == "r'" and self.unit[-1] == "'":
                self.unit = self.unit[2:-1]

            self.unit = self.unit.strip("'")

            # skip header line
            fin.readline()

            while True:
                line = fin.readline().strip()
                if len(line) == 0:
                    break

                vmin, vmax, r, g, b, label = line.split(',')

                vmin = vmin.strip(' ')
                if vmin == 'None':
                    vmin = None
                else:
                    vmin = float(vmin)

                vmax = vmax.strip(' ')
                if vmax == 'None':
                    vmax = None
                else:
                    vmax = float(vmax)

                r = int(r.strip(' '))
                g = int(g.strip(' '))
                b = int(b.strip(' '))
                label = label.strip(' ')
                ll = Level(vmin, vmax, (r, g, b), label)
                self.level_colors.append(ll)

        name = os.path.basename(file_path)
        name = os.path.splitext(name)[0]
        self.name = name
        self.__post_init__()

        return self


def create_cmap_from_csv(file_path: str, collector_dict: Optional[dict]) -> ColorMap:
    '''Helper function to create a colormap obj from csv file'''

    cmap = ColorMap()
    cmap.read_from_csv(file_path)

    if collector_dict is not None:
        collector_dict[cmap.name] = cmap

    return cmap




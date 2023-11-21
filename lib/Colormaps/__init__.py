'''Load colormap defs into namespace of Colormaps

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2023-11-21 10:04:55.
'''

from .colormap import load_colormaps, DEF_FOLDER, ColorMap, ColorMapGroup, create_cmap_from_csv

# load colormaps into this module's namespace
names = load_colormaps(DEF_FOLDER)

for name, obj in names:
    try:

        exec(f'{name} = obj')
    except:
        print(f'Failed to add name {name} to module namespace.')

#cm = __import__(__name__)
# remove these from namespace
del names
del name
del obj
del DEF_FOLDER


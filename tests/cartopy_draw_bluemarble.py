import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig1 = plt.figure(figsize=(30, 5))
ax = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_title('stock_img (shaded relief)', fontsize = 20)
ax.stock_img()

ax.add_feature(cfeature.BORDERS.with_scale('50m'), linewidth=1, edgecolor='r')
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=1, edgecolor='r')
fig1.show()


fig2 = plt.figure(figsize=(20, 5))
ax = fig2.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_title('bluemarble', fontsize = 20)
img = plt.imread('../docs/bluemarble.png')
img_extent = (-180, 180, -90, 90)
ax.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree())

ax.add_feature(cfeature.BORDERS.with_scale('50m'), linewidth=1, edgecolor='r')
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=1, edgecolor='r')
fig2.show()


fig3 = plt.figure(figsize=(20, 5))
ax = fig3.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_title('etopo', fontsize = 20)
img = plt.imread('../docs/etopo.png')
img_extent = (-180, 180, -90, 90)
ax.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree())

ax.add_feature(cfeature.BORDERS.with_scale('50m'), linewidth=1, edgecolor='r')
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=1, edgecolor='r')
fig3.show()


fig4 = plt.figure(figsize=(20, 5))
ax = fig4.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.background_img(name='ne_shaded', resolution='low')
#ax.coastlines(resolution='110m')
fig4.show()



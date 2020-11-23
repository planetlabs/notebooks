import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

"""
The NDVI values will range from -1 to 1. You want to use a diverging color scheme to visualize the data,
and you want to center the colorbar at a defined midpoint. The class below allows you to normalize the colorbar.
"""
class MidpointNormalize(colors.Normalize):
    """
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)
    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    Credit: Joe Kington, http://chris35wills.github.io/matplotlib_diverging_colorbar/
    Credit: https://stackoverflow.com/a/48598564
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)
    
    def __call__(self, value, clip=None):    
        # Note that I'm ignoring clipping and other edge cases here.
        result, is_scalar = self.process_value(value)
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.array(np.interp(value, x, y), mask=result.mask, copy=False)


def show_ndvi(ndvi, figsize=(20, 10)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)

    # diverging color scheme chosen from https://matplotlib.org/users/colormaps.html
    cmap = plt.cm.RdYlGn 

    mmin = np.nanmin(ndvi)
    mmax = np.nanmax(ndvi)
    mid = 0

    cax = ax.imshow(ndvi, cmap=cmap, clim=(mmin, mmax),
                    norm=MidpointNormalize(midpoint=mid,vmin=mmin, vmax=mmax))

    ax.axis('off')
    ax.set_title('Normalized Difference Vegetation Index', fontsize=18, fontweight='bold')

    cbar = fig.colorbar(cax, orientation='horizontal', shrink=0.5)

    plt.show()
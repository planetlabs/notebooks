import matplotlib.pyplot as plt
import numpy as np


def plot_image(masked_bands, do_scale=True, title=None, figsize=(10, 10)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)
    show(ax, masked_bands, do_scale=do_scale)
    if title:
        ax.set_title(title)
    ax.set_axis_off()


def show(axis, bands, do_scale=True, alpha=True):
    """Show bands as image with option of converting mask to alpha.

    Alters axis in place.
    """
    assert len(bands) in [1, 3]

    try:
        mask = bands[0].mask
        assert mask.shape == bands[0].shape
    except AttributeError:
        # no mask
        mask = None
    except AssertionError:
        # mask not the same shape as band
        mask = None

    bands = [b for b in bands.copy()]  # turn into list
    bands = _scale_bands(bands, percentile=True)

    if alpha and len(bands) == 3 and mask is not None:
        bands.append(_mask_to_alpha(mask))

    if len(bands) >= 3:
        dbands = np.dstack(bands)
    else:
        dbands = bands[0]

    return axis.imshow(dbands)


def _mask_bands(bands, mask):
    return [np.ma.array(b, mask) for b in bands]


def _scale_bands(bands, percentile=True):
    def _percentile(bands, percentile):
        all_pixels = np.concatenate([b.compressed() for b in bands])
        return np.percentile(all_pixels, percentile)

    if percentile:
        old_min = _percentile(bands, 2)
        old_max = _percentile(bands, 98)
    else:
        old_min = 0
        old_max = 2 ** 12 - 1

    new_min = 0
    new_max = 1

    def _linear_scale(ndarray, old_min, old_max, new_min, new_max):
        # https://en.wikipedia.org/wiki/Normalization_(image_processing)
        return (ndarray - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

    scaled = [np.clip(_linear_scale(b.astype(np.float),
                                    old_min, old_max,
                                    new_min, new_max),
                      new_min, new_max)
              for b in bands]

    filled = [b.filled(fill_value=0) for b in scaled]
    return filled


def _mask_to_alpha(mask):
    alpha = np.zeros_like(np.atleast_3d(mask))
    alpha[~mask] = 1
    return alpha

import matplotlib.colors as colors
import matplotlib.patches as mpatches

def plot_classified_band(class_band, class_labels=None, cmap='rainbow',
                         title='Class Labels', figdim=10):
    fig = plt.figure(figsize=(figdim, figdim))
    ax = fig.add_subplot(1, 1, 1)
    imshow_class_band(ax, class_band, class_labels, cmap=cmap)
    ax.set_title(title)
    ax.set_axis_off()

def imshow_class_band(ax, class_band, class_labels=None, cmap='rainbow'):
    """Show classified band with colormap normalization and color legend. Alters ax in place.
    
    possible cmaps ref: https://matplotlib.org/examples/color/colormaps_reference.html
    """
    class_norm = _ClassNormalize(class_band)
    im = ax.imshow(class_band, cmap=cmap, norm=class_norm)

    try:
        # add class label legend
        # https://stackoverflow.com/questions/25482876
        # /how-to-add-legend-to-imshow-in-matplotlib
        color_mapping = class_norm.mapping
        colors = [im.cmap(color_mapping[k]) for k in class_labels.keys()]
        labels = class_labels.values()

        # https://matplotlib.org/users/legend_guide.html
        # tag: #creating-artists-specifically-for-adding-to-the-legend-aka-proxy-artists
        patches = [mpatches.Patch(color=c, label=l) for c,l in zip(colors, labels)]

        ax.legend(handles=patches, bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.)
    except AttributeError:
        # class_labels not specified
        pass

# https://matplotlib.org/users/colormapnorms.html#custom-normalization-two-linear-ranges
class _ClassNormalize(colors.Normalize):
    """Matplotlib colormap normalizer for a classified band.
    
    Inspired by https://matplotlib.org/users/colormapnorms.html#custom-normalization-two-linear-ranges
    """
    def __init__(self, arry):
        # get unique unmasked values
        values = [v for v in np.unique(arry)
                  if not isinstance(v, np.ma.core.MaskedConstant)]

        # map unique values to points in the range 0-1
        color_ticks = np.array(range(len(values)), dtype=np.float) / (len(values) - 1)
        self._mapping = dict((v, ct) for v, ct in zip(values, color_ticks))
        
        # Initialize base Normalize instance
        vmin = 0
        vmax = 1
        clip = False
        colors.Normalize.__init__(self, vmin, vmax, clip)
    
    def __call__(self, arry, clip=None):
        '''Create classified representation of arry for display.'''
        # round array back to ints for logical comparison
        arry = np.around(arry)
        new_arry = arry.copy()
        for k, v in self._mapping.items():
            new_arry[arry==k] = v
        return new_arry
    
    @property
    def mapping(self):
        '''property required for colors.Normalize classes
        
        We update the _mapping property in __init__ and __call__ and just
        return that property here.
        '''
        return self._mapping

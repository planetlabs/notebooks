import matplotlib.pyplot as plt
import numpy as np


def plot_image(masked_bands, title=None, figsize=(10, 10)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)
    show(ax, masked_bands)
    if title:
        ax.set_title(title)
    ax.set_axis_off()


def show(axis, bands, alpha=True):
    """Show bands as image with option of converting mask to alpha.

    Alters axis in place.
    """
    assert len(bands) in [1, 3]

    mask = None
    try:
        mask = bands[0].mask
    except AttributeError:
        # no mask
        pass

    bands = [b for b in bands.copy()]  # turn into list
    bands = _scale_bands(bands)

    if alpha and len(bands) == 3 and mask is not None:
        bands.append(_mask_to_alpha(mask))

    if len(bands) >= 3:
        dbands = np.dstack(bands)
    else:
        dbands = bands[0]

    return axis.imshow(dbands)


def _mask_bands(bands, mask):
    return [np.ma.array(b, mask) for b in bands]


def _scale_bands(bands):
    def _percentile(bands, percentile):
        all_pixels = np.concatenate([b.compressed() for b in bands])
        return np.percentile(all_pixels, percentile)

    old_min = _percentile(bands, 2)
    old_max = _percentile(bands, 98)
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

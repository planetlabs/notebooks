# This script takes the image clips in the AOI and creates matrices 
# for each spectral band, where the channels of the matrices represent
# different time stamps

import glob
import os
import numpy as np
import rasterio

def load_image4(filename):
    """ Return a 4D (r, g, b, nir) numpy array with the data in the specifed TIFF filename. """
    path = os.path.abspath(os.path.join('./',filename))
    if os.path.exists(path):
        with rasterio.open(path) as src:
            b, g, r, re, nir = src.read()
            #return np.dstack([r, g, b, nir])
            return np.dstack([b, g, r, re, nir])

def load_labels(labels_fname):
    """ Returns a 2D numpy array with data labels for each crop type. """
    path = os.path.abspath(os.path.join('./', labels_fname))
    if os.path.exists(path):
        with rasterio.open(path) as src:
            labels = src.read()
            return labels

def get_img_fnames(imgs_dir):
    imgs = []
    for filename in glob.glob(imgs_dir):
        imgs.append(filename)
    print(imgs)
    return imgs

def divide_imgs(img_files, labels):
    b_time = []
    g_time = []
    r_time = []
    re_time = []
    nir_time = []

    labels = np.squeeze(labels)
    print(labels.shape)

    b_time.append(labels)
    g_time.append(labels)
    r_time.append(labels)
    re_time.append(labels)
    nir_time.append(labels)

    for idx in range(len(img_files)):
        cur_img = img_files[idx]
        print(cur_img[:,:,0].shape)
        b_time.append(cur_img[:,:,0])
        g_time.append(cur_img[:,:,1])
        r_time.append(cur_img[:,:,2])
        re_time.append(cur_img[:,:,3])
        nir_time.append(cur_img[:,:,4])

    b_time = np.dstack(b_time)
    g_time = np.dstack(g_time)
    r_time = np.dstack(r_time)
    re_time = np.dstack(re_time)
    nir_time = np.dstack(nir_time)
    return b_time, g_time, r_time, re_time, nir_time

def main():
    imgs_dir = 'DATA_kings_05_imgs/clip/*.tif'
    labels_fname = 'CDL_files/CDL_Kings_2016_06031/CDL_2016_06031_clip_05.tif'
    
    imgs = get_img_fnames(imgs_dir)
    img_files = [load_image4(fname) for fname in imgs]
    labels = load_labels(labels_fname)
    print('------')
    print(labels.shape)
    print('------')
    
    b_time, g_time, r_time, re_time, nir_time = divide_imgs(img_files, labels)

    np.save('b_time.npy', b_time, allow_pickle=True)
    np.save('g_time.npy', g_time, allow_pickle=True)
    np.save('r_time.npy', r_time, allow_pickle=True)
    np.save('re_time.npy', re_time, allow_pickle=True)
    np.save('nir_time.npy', nir_time, allow_pickle=True)

if __name__ == '__main__':
    main()

# In this script, a dataset is constructed from saved 
# temporal signatures of each spectral band image

import numpy as np
import matplotlib.pyplot as plt
import pdb

def sort_crops(b_time):
    # Prints out the top 20 crops. The user must decide which crops to use. The crops corresponding to the
    # 'sorted_crops' values can be found in the CDL database, for example here:
    # https://www.nass.usda.gov/Research_and_Science/Cropland/metadata/metadata_ca16.htm
    # where the values correspond to the 'Attribute Code' in the link.
    vals = np.histogram(b_time[:,:,0].ravel(), bins=256, range=(0,255))
    sorted_crops = np.argsort(vals[0])
    amt = np.sort(vals[0])
    amt = amt[-20:]
    amt = amt[::-1]
    sorted_crops = sorted_crops[-20:]
    sorted_crops = sorted_crops[::-1]
    print( '---- SORTED CROPS ---- ')
    print(sorted_crops)
    print(' ---- AMT OF EACH ----- ')
    print(amt)
    return sorted_crops

def get_masks(b_time, sorted_crops):
    # Build up the 'final_mask_xl' variable with the selected crop indices from 'sorted_crops'.
    masks = []
    for idx in range(sorted_crops.shape[0]):
        cur_mask = b_time[:,:,0] == sorted_crops[idx]
        masks.append(cur_mask)
    
    # Final mask is all pixels of the selected classes
    final_mask_xl = masks[0] + masks[1] + masks[2] + masks[3] + masks[4] + masks[5] + masks[6] + masks[7]+ masks[8]

    # You can visualize and save the masks
    #plt.figure()
    #plt.imshow(masks[5])
    #plt.savefig('corn.png')
    return masks, final_mask_xl

def concat_features(b_time, g_time, r_time, re_time, nir_time, masks):
    # For each selected crop, concatenate the spectral features from each mask index together. 
    # You will likely need to change the mask indices to suit the mask indices that you have chosen from 'sorted_crops'
    crop0 = np.concatenate([b_time[masks[0]], g_time[masks[0]][:,1:], r_time[masks[0]][:,1:], re_time[masks[0]][:,1:], nir_time[masks[0]][:,1:]], axis=1) # wintwheat/corn
    crop1 = np.concatenate([b_time[masks[1]], g_time[masks[1]][:,1:], r_time[masks[1]][:,1:], re_time[masks[1]][:,1:], nir_time[masks[1]][:,1:]], axis=1) # alfalfa
    crop2 = np.concatenate([b_time[masks[2]], g_time[masks[2]][:,1:], r_time[masks[2]][:,1:], re_time[masks[2]][:,1:], nir_time[masks[2]][:,1:]], axis=1) # almonds
    crop3 = np.concatenate([b_time[masks[3]], g_time[masks[3]][:,1:], r_time[masks[3]][:,1:], re_time[masks[3]][:,1:], nir_time[masks[3]][:,1:]], axis=1) # pistachios
    crop4 = np.concatenate([b_time[masks[4]], g_time[masks[4]][:,1:], r_time[masks[4]][:,1:], re_time[masks[4]][:,1:], nir_time[masks[4]][:,1:]], axis=1) # idle
    crop5 = np.concatenate([b_time[masks[5]], g_time[masks[5]][:,1:], r_time[masks[5]][:,1:], re_time[masks[5]][:,1:], nir_time[masks[5]][:,1:]], axis=1) # corn
    crop6 =np.concatenate([b_time[masks[6]], g_time[masks[6]][:,1:], r_time[masks[6]][:,1:], re_time[masks[6]][:,1:], nir_time[masks[6]][:,1:]], axis=1) # walnuts
    crop7 = np.concatenate([b_time[masks[7]], g_time[masks[7]][:,1:], r_time[masks[7]][:,1:], re_time[masks[7]][:,1:], nir_time[masks[7]][:,1:]], axis=1) # cotton
    crop8 = np.concatenate([b_time[masks[8]], g_time[masks[8]][:,1:], r_time[masks[8]][:,1:], re_time[masks[8]][:,1:], nir_time[masks[8]][:,1:]], axis=1) # winter wheat
    crops = [crop0, crop1, crop2, crop3, crop4, crop5, crop6, crop7, crop8]
    return crops

def get_labels(labels):
    # The current labels are the values of the 'Attribute Codes' for each crop. You want to change them so that they are integer values, starting from zero.
    # Be careful to not overwrite and Attribute Codes if they need to be saved first. For example, the second label below (for attribute code == 1), was 
    # changed to 5 before the following line changed the Attribute odes of 36 to be == 1.
    labels[labels == 225] = 0
    labels[labels == 1] = 5
    labels[labels == 36] = 1
    labels[labels == 2] = 7
    labels[labels == 75] = 2
    labels[labels == 204] = 3
    labels[labels == 61] = 4
    labels[labels == 76] = 6
    labels[labels == 24] = 8

    labels_scalars = labels
    one_hot = np.zeros((labels.shape[0],9))
    one_hot[np.arange(labels.shape[0]),labels] = 1
    return one_hot, labels_scalars

def split_dataset(crops_sub, train_split, val_split, test_split):
    # Shuffles and splits the dataset into train, validation, test sets
    np.random.shuffle(crops_sub)
    rows = crops_sub.shape[0]
    
    labels = crops_sub[:,0]
    labels, labels_sc = get_labels(labels)

    data = crops_sub[:,1:]

    train_data = data[0:int(rows*train_split), :]
    val_data = data[int(rows*train_split):int(rows*train_split+rows*val_split),:]
    test_data = data[int(-rows*val_split):,:]

    #train_labels = labels[0:int(rows*train_split), :] # one hot
    train_labels_sc = labels_sc[0:int(rows*train_split)]

    #val_labels = labels[int(rows*train_split):int(rows*train_split+rows*val_split),:] # one hot
    val_labels_sc = labels_sc[int(rows*train_split):int(rows*train_split+rows*val_split)]
    
    #test_labels = labels[int(-rows*val_split):,:] # one hot
    test_labels_sc = labels_sc[int(-rows*val_split):]

    return train_data, val_data, test_data, train_labels_sc, val_labels_sc, test_labels_sc

def crop_dataset(crops):
    crops_sub = []
    for crop in crops:
        np.random.shuffle(crop)
        crop = crop[0:100000]
        crops_sub.append(crop)

    crops_sub = np.concatenate(crops_sub, axis=0)
    return crops_sub

def make_full():
    # This is for creating a dataset of the whole image for a visual classification result
    b_time = np.load('../../data/DATA_kings_04_imgs/b_time.npy')
    g_time = np.load('../../data/DATA_kings_04_imgs/g_time.npy')
    r_time = np.load('../../data/DATA_kings_04_imgs/r_time.npy')
    re_time = np.load('../../data/DATA_kings_04_imgs/re_time.npy')
    nir_time = np.load('../../data/DATA_kings_04_imgs/nir_time.npy')

    b_sub = b_time[:, :, 1:]
    g_sub = g_time[:, :, 1:]
    r_sub = r_time[:, :, 1:]
    re_sub = re_time[:, :, 1:]
    nir_sub = nir_time[:, :, 1:]

    data_sub = np.concatenate((b_sub, g_sub, r_sub, re_sub, nir_sub), axis=2)
    labels = b_time[:, :, 0]
    labels = np.reshape(labels, (labels.shape[0]*labels.shape[1], 1))

    # FOR KINGS 05
    #labels_new = np.ones(labels.shape)*4
    #labels_new[labels == 225] = 0
    #labels_new[labels == 1] = 5
    #labels_new[labels == 36] = 1
    #labels_new[labels == 2] = 7
    #labels_new[labels == 75] = 2
    #labels_new[labels == 204] = 3
    #labels_new[labels == 61] = 4  # idle
    #labels_new[labels == 76] = 6
    #labels_new[labels == 24] = 8

    # FOR KINGS 04
    labels_new = np.ones(labels.shape)*5 # make all pixels idle, and then override with other crop classes
    labels_new[labels == 2] = 0
    labels_new[labels == 33] = 1
    labels_new[labels == 54] = 2
    labels_new[labels == 24] = 3  
    labels_new[labels == 22] = 4
    labels_new[labels == 61] = 5

    data_sub = np.reshape(data_sub, (data_sub.shape[0]*data_sub.shape[1], data_sub.shape[2]))

    np.save('ALL_data.npy', data_sub, allow_pickle=True)
    np.save('ALL_lbls.npy', labels_new, allow_pickle=True)

def main():
    b_time = np.load('DATA_kings_04_imgs/b_time.npy')
    g_time = np.load('DATA_kings_04_imgs/g_time.npy')
    r_time = np.load('DATA_kings_04_imgs/r_time.npy')
    re_time = np.load('DATA_kings_04_imgs/re_time.npy')
    nir_time = np.load('DATA_kings_04_imgs/nir_time.npy')

    sorted_crops = sort_crops(b_time)
    masks, final_mask = get_masks(b_time, sorted_crops)

    crops = concat_features(b_time, g_time, r_time, re_time, nir_time, masks)
    crops_sub = crop_dataset(crops)

    train_data, val_data, test_data, train_labels_sc, val_labels_sc, test_labels_sc  = split_dataset(crops_sub, 0.9, 0.05, 0.05)
    np.save('train_data.npy', train_data, allow_pickle=True)
    np.save('train_lbl_sc.npy', train_labels_sc, allow_pickle=True)
    
    np.save('val_data.npy', val_data, allow_pickle=True)
    np.save('val_lbl_sc.npy', val_labels_sc, allow_pickle=True)
    
    np.save('test_data.npy', test_data, allow_pickle=True)
    np.save('test_lbl_sc.npy', test_labels_sc, allow_pickle=True)

if __name__ == '__main__':
    #make_full()
    main()

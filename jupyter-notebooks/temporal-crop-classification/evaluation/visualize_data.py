# Visualize the datasets by plotting average irradiance values of each spectral band over the growing season

import numpy as np
import matplotlib.pyplot as plt
import pdb

def sort_crops(b_time):
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
    masks = []
    for idx in range(sorted_crops.shape[0]):
        cur_mask = b_time[:,:,0] == sorted_crops[idx]
        masks.append(cur_mask)
    #final_mask_xl = masks[0] + masks[1] + masks[2] + masks[3] + masks[4] + masks[5] + masks[6] + masks[7]+ masks[8]
    final_mask_xl = masks[0] + masks[1] + masks[2] + masks[3] + masks[5] + masks[8] 
    return masks, final_mask_xl

#def concat_features(b_time, g_time, r_time, re_time, nir_time, masks):
#    wintwheat_corn_0 = np.concatenate([b_time[masks[0]], g_time[masks[0]][:,1:], r_time[masks[0]][:,1:], re_time[masks[0]][:,1:], nir_time[masks[0]][:,1:]], axis=1)
#    print(wintwheat_corn_0.shape)
#    alfalfa_1 = np.concatenate([b_time[masks[1]], g_time[masks[1]][:,1:], r_time[masks[1]][:,1:], re_time[masks[1]][:,1:], nir_time[masks[1]][:,1:]], axis=1)
#    print(alfalfa_1.shape)
#    almonds_2 = np.concatenate([b_time[masks[2]], g_time[masks[2]][:,1:], r_time[masks[2]][:,1:], re_time[masks[2]][:,1:], nir_time[masks[2]][:,1:]], axis=1)
#    pistachios_3 = np.concatenate([b_time[masks[3]], g_time[masks[3]][:,1:], r_time[masks[3]][:,1:], re_time[masks[3]][:,1:], nir_time[masks[3]][:,1:]], axis=1)
#    idle_4 = np.concatenate([b_time[masks[4]], g_time[masks[4]][:,1:], r_time[masks[4]][:,1:], re_time[masks[4]][:,1:], nir_time[masks[4]][:,1:]], axis=1)
#    corn_5 = np.concatenate([b_time[masks[5]], g_time[masks[5]][:,1:], r_time[masks[5]][:,1:], re_time[masks[5]][:,1:], nir_time[masks[5]][:,1:]], axis=1)
#    walnuts_6 =np.concatenate([b_time[masks[6]], g_time[masks[6]][:,1:], r_time[masks[6]][:,1:], re_time[masks[6]][:,1:], nir_time[masks[6]][:,1:]], axis=1)
#    cotton_7 = np.concatenate([b_time[masks[7]], g_time[masks[7]][:,1:], r_time[masks[7]][:,1:], re_time[masks[7]][:,1:], nir_time[masks[7]][:,1:]], axis=1)
#    wintwheat_8 = np.concatenate([b_time[masks[8]], g_time[masks[8]][:,1:], r_time[masks[8]][:,1:], re_time[masks[8]][:,1:], nir_time[masks[8]][:,1:]], axis=1)
#    crops = [wintwheat_corn_0, alfalfa_1, almonds_2, pistachios_3, idle_4, corn_5, walnuts_6, cotton_7, wintwheat_8]
#    return crops

def concat_features(b_time, g_time, r_time, re_time, nir_time, masks):
    crop0 = np.concatenate([b_time[masks[0]], g_time[masks[0]][:,1:], r_time[masks[0]][:,1:], re_time[masks[0]][:,1:], nir_time[masks[0]][:,1:]], axis=1)
    print(crop0.shape)
    crop1 = np.concatenate([b_time[masks[1]], g_time[masks[1]][:,1:], r_time[masks[1]][:,1:], re_time[masks[1]][:,1:], nir_time[masks[1]][:,1:]], axis=1)
    print(crop1.shape)
    crop2 = np.concatenate([b_time[masks[2]], g_time[masks[2]][:,1:], r_time[masks[2]][:,1:], re_time[masks[2]][:,1:], nir_time[masks[2]][:,1:]], axis=1)
    crop3 = np.concatenate([b_time[masks[5]], g_time[masks[5]][:,1:], r_time[masks[5]][:,1:], re_time[masks[5]][:,1:], nir_time[masks[5]][:,1:]], axis=1)
    crop4 = np.concatenate([b_time[masks[8]], g_time[masks[8]][:,1:], r_time[masks[8]][:,1:], re_time[masks[8]][:,1:], nir_time[masks[8]][:,1:]], axis=1)
    crop5 = np.concatenate([b_time[masks[3]], g_time[masks[3]][:,1:], r_time[masks[3]][:,1:], re_time[masks[3]][:,1:], nir_time[masks[3]][:,1:]], axis=1)
    crops = [crop0, crop1, crop2, crop3, crop4, crop5]
    return crops

def one_hot_labels(labels):
    #labels[labels == 225] = 0
    #labels[labels == 1] = 5
    #labels[labels == 36] = 1
    #labels[labels == 2] = 7
    #labels[labels == 75] = 2
    #labels[labels == 204] = 3
    #labels[labels == 61] = 4
    #labels[labels == 76] = 6
    #labels[labels == 24] = 8

    labels[labels == 2] = 0
    labels[labels == 33] = 1
    labels[labels == 54] = 2
    labels[labels == 24] = 3
    labels[labels == 22] = 4
    labels[labels == 61] = 5

    print(labels)
    labels_scalars = labels
    one_hot = np.zeros((labels.shape[0],9))
    one_hot[np.arange(labels.shape[0]),labels] = 1
    return one_hot, labels_scalars

def crop_dataset(crops):
    cur_iter = 0
    for crop in crops:
        np.random.shuffle(crop)
        #crop = crop[0:100000]
        crop = crop[0:10000]
        fname = 'crop_' + str(cur_iter) + '.npy'
        print(crop.shape)
        np.save(fname, crop, allow_pickle=True)
        cur_iter += 1

def main_04():
    b_time = np.load('../data/DATA_kings_04_imgs/b_time.npy')
    g_time = np.load('../data/DATA_kings_04_imgs/g_time.npy')
    r_time = np.load('../data/DATA_kings_04_imgs/r_time.npy')
    re_time = np.load('../data/DATA_kings_04_imgs/re_time.npy')
    nir_time = np.load('../data/DATA_kings_04_imgs/nir_time.npy')

    sorted_crops = sort_crops(b_time)
    masks, final_mask = get_masks(b_time, sorted_crops)

    crops = concat_features(b_time, g_time, r_time, re_time, nir_time, masks)
    crops_sub = crop_dataset(crops)

def main_05():
    b_time = np.load('../data/DATA_kings_05_imgs/b_time.npy')
    g_time = np.load('../data/DATA_kings_05_imgs/g_time.npy')
    r_time = np.load('../data/DATA_kings_05_imgs/r_time.npy')
    re_time = np.load('../data/DATA_kings_05_imgs/re_time.npy')
    nir_time = np.load('../data/DATA_kings_05_imgs/nir_time.npy')

    sorted_crops = sort_crops(b_time)
    masks, final_mask = get_masks(b_time, sorted_crops)

    crops = concat_features(b_time, g_time, r_time, re_time, nir_time, masks)
    crops_sub = crop_dataset(crops)

def main_visualize():
    crop0 = np.load('crop_0.npy')
    crop1 = np.load('crop_1.npy')
    crop2 = np.load('crop_2.npy')
    crop3 = np.load('crop_3.npy')
    crop4 = np.load('crop_4.npy')
    crop5 = np.load('crop_5.npy')
    #crop6 = np.load('crop_6.npy')
    #crop7 = np.load('crop_7.npy')
    #crop8 = np.load('crop_8.npy')
    
    mean0 = np.mean(crop0, axis=0)
    mean1 = np.mean(crop1, axis=0)
    mean2 = np.mean(crop2, axis=0)
    mean3 = np.mean(crop3, axis=0)
    mean4 = np.mean(crop4, axis=0)
    mean5 = np.mean(crop5, axis=0)
    #mean6 = np.mean(crop6, axis=0)
    #mean7 = np.mean(crop7, axis=0)
    #mean8 = np.mean(crop8, axis=0)

    plt.figure()
    plt.plot(mean0[1:])
    plt.plot(mean1[1:])
    plt.plot(mean2[1:])
    plt.plot(mean3[1:])
    plt.plot(mean4[1:])
    plt.plot(mean5[1:])
    #plt.plot(mean6[1:])
    #plt.plot(mean7[1:])
    #plt.plot(mean8[1:])
    cur_axes = plt.gca()
    cur_axes.axes.get_xaxis().set_ticks([])
    plt.ylabel('Sensor Irradiance Values')
    #plt.title('Average Spectral Irradiance Values for Each Crop in Scene #2')
    plt.title('Average Spectral Irradiance Values for Each Crop in Scene #1')
    #plt.legend(['wintwht/corn', 'alfalfa', 'almonds', 'pistachios', 'idle', 'corn', 'walnuts', 'cotton', 'wintwht']) 
    plt.legend(['cotton', 'safflower', 'tomatoes', 'idle', 'wintwht', 'durumwheat']) 
        
    plt.show()

if __name__ == '__main__':
    #main_04()
    main_visualize()

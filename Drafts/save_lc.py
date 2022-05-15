import lightkurve as lk
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
from astropy.io import fits
import numpy as np
import torch
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

targetlist_path = 'to be defined' #This is the download for all confirmed planets
targets = pd.read_csv(targetlist_path, comment='#')
ids = targets['TICID']
download_path = 'to be defined'
name = 'planet.'
last = '.pt'
planet_tic = 'tic ' + str(ids)
counter = 0 #pls change it according to how much tensors you have already downloaded

for s in ids[1:10]:
    tic = 'tic ' + str(s)
    print(tic)
    search_result = lk.search_lightcurve(tic)
    if len(search_result) == 0:
        print("No result for the star")
    else:
        counter += 1
        print('Downloading')
        try:
            if(os.path.isdir('to be defined')==True):
                shutil.rmtree('to be defined')
            os.mkdir('R:\TTT') 
            lc_collection = search_result.download_all(download_dir='to be defined')# Add your own file address to the download_dir to reduce the possibility of buffer errors in Python
        except:
            print('download failed')
        print('Processing')
        lc = lc_collection.stitch().flatten(window_length=901).remove_outliers()
        period = np.linspace(1, 20, 10000)
        bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500);
        planet_b_period = bls.period_at_max_power
        planet_b_t0 = bls.transit_time_at_max_power
        planet_b_dur = bls.duration_at_max_power
        ax = lc.fold(period=planet_b_period*2, epoch_time=planet_b_t0+planet_b_period*0.5)
        print('Saving')
        c = lc.to_pandas()
        my_array = np.array(c)
        my_tensor = torch.tensor(my_array)
        path = download_path + name + str(counter) + last
        print(path)
        torch.save(my_tensor, path)

import lightkurve as lk
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
from astropy.io import fits
import numpy as np

# download_path = 'X:\Research - Exo\download\\'

#The target list CSV file
targets = pd.read_csv(r'X:\Research\data download\all_targets_S046_v1.csv', comment='#')
ids = targets['TICID']


def plot_curve(TIC):
    '''Plot all curves for the inputed TIC id'''
    print('Searching...')
    try:
        search_result = lk.search_lightcurve(TIC)
    except:
        print('Ended plotting, since unable to search curve for: ',TIC)
        return
    try:
        if(os.path.isdir('X:\Research\data download\\'+TIC+' plots')==True):
            print('Deleting old folder')
            shutil.rmtree('X:\Research\data download\\'+TIC+' plots')
        print('Creating file path...')
        os.mkdir('X:\Research\data download\\'+TIC+' plots')
    except:
        print('Ended plotting, since failed to create file directory')
        return
    print('Downloading...')
    for search_result in search_result:
        try:
            downloaded_curve = search_result.download(download_dir='X:\Research\data download\\'+TIC+' plots')
            downloaded_curve.plot()
        except:
                print('Failed to download and plot the curve')

def plot_batch(count,end):
    '''Plot a bunch of targets from the target list csv file(Starting target id number, ending target id number)'''
    for this_id in ids[count:end]:
        print('Ready to plot for ', f'TIC {this_id}')
        try:
            plot_curve(f'TIC {this_id}')
        except:
            print('Unsupported file type or buffer problem if indicated')
            print()
            continue

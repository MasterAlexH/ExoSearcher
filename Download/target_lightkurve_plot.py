import lightkurve as lk
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
from astropy.io import fits
import numpy as np
import torch

#Documentations below specific functions

download_path = 'X:\Research - Exo\download\\'
targetlist_path = r'X:\Research\data download\all_targets_S046_v1.csv'
targets = pd.read_csv(targetlist_path, comment='#')
ids = targets['TICID']

def plot_curve(TIC):
    '''Plot all available light curves for the inputed TIC id'''
    print('Searching...')
    try:
        search_result = lk.search_lightcurve(TIC)
    except:
        print('Unable to search curve for: ',TIC)
        return
    try:
        if(os.path.isdir(download_path+TIC+' plots')==True):
            print('Deleting old folder')
            shutil.rmtree(download_path+TIC+' plots')
        print('Creating file path...')
        os.mkdir(download_path+TIC+' plots')
    except:
        print('Failed to create file directory')
        return
    print('Downloading...')
    for search_result in search_result:
        try:
            downloaded_curve = search_result.download(download_dir=download_path+TIC+' plots')
            downloaded_curve.plot()
        except:
                print('Failed to plot the curve')

def plot_batch(start,end):
    '''Plots all light kurves from the number<start> target of the target list, to the number<end>'''
    for this_id in ids[start:end]:
        print('Ready to plot for ', f'TIC {this_id}')
        try:
            plot_curve(f'TIC {this_id}')
        except:
            print('Did not work')
            print()
            continue

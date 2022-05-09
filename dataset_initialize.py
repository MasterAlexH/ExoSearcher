import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from torch.utils.data import DataLoader,Dataset
from skimage import io,transform
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
import numpy as np
import lightkurve as lk

class Tessdataset(Dataset): 
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir   
        self.transform = transform
        self.lightcurve = os.listdir(self.root_dir)
    
    def __len__(self):#返回整个数据集的大小
        return len(self.lightcurve)
    
    def __getitem__(self,index):
        lightcurve_index = self.lightcurve[index]
        lc_path = os.path.join(self.root_dir, lightcurve_index)
        lc = torch.load(lc_path)
        label = lc_path.split('\\')[-1].split('.')[0]
        sample = {'image':lc,'label':label}
        
        if self.transform:
            sample = self.transform(sample)
        return sample
      
#This is for testing and examination of tensor size
      '''if __name__=='__main__':
    data = Tessdataset('R:\Dataset',transform=None)
    dataloader = DataLoader(data,batch_size=1,shuffle=True)
    for i_batch,batch_data in enumerate(dataloader):
        print(i_batch)
        print(batch_data['image'].size())
        print(batch_data['label'])'''

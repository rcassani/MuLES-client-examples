# -*- coding: utf-8 -*-
"""
MuLES client example: auto_start_mules
This example shows how to:
- Start a MuLES instance from Python 
- Connect to MuLES instance
- Stream data for 10 s
- Close a MuLES instance from Python  

The scrip is divided as follows
1. Start MuLES instance
2. Connection with MuLES
3. Get 10 s of data
4. Close connection and close MuLES instance

 Instructions:
 MuLES and the Client are expected to be in the same computer

 1 Run this script

"""

import mules              # The signal acquisition toolbox we'll use (MuLES)
import numpy as np        # Module that simplifies computations on matrices 
import matplotlib.pyplot as plt # Module used for plotting
import time
import subprocess

if __name__ == "__main__":
    
    plt.close('all')  
    
    # 1. Start MuLES instance
    mules_exe_path = '"C:\Program Files (x86)\MuSAE_Lab\MuLES\mules.exe"'
    
    # Data from a given device DEVICEXX
    # subprocess.Popen(mules_exe_path + ' -- "DEVICE06" PORT=30001 LOG=F TCP=T &')
    
    # Data from a CSV file
    data_file = '"C:\Program Files (x86)\MuSAE_Lab\MuLES\eeg_files\log20141210_195303.csv"'
    subprocess.Popen(mules_exe_path + ' -- ' +  data_file + ' PORT=30001 LOG=F TCP=T &')

    # Allow MuLES to start    
    time.sleep(5)  
    
    # 2. Connection with MuLES
    mules_client = mules.MulesClient('127.0.0.1', 30001) # connects with MuLES at 127.0.0.1 : 30001
    device_name = mules_client.getdevicename()           # get device name
    channel_names = mules_client.getnames()              # get channel names
    fs = 1.0 * mules_client.getfs()                      # get sampling frequency

    # 3. Request 10 seconds of EEG data
    mules_client.tone(600,250)
    eeg_data = mules_client.getdata(10)
    mules_client.tone(900,250)
    channel = 4;
    time_vector =  np.arange(0,eeg_data.shape[0]) / fs
    h, ax = plt.subplots()
    h.canvas.set_window_title('EEG data from: ' + device_name + '. Electrode: ' + channel_names[channel-1]   )
    ax.plot(time_vector, eeg_data[:,channel-1])

    # 4. Close connection and close MuLES instance
    mules_client.kill()


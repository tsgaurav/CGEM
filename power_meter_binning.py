import visa
import time
import matplotlib.pyplot as plt
import numpy as np
import h5py

start_time = time.strftime("%y%m%d%H%M")

data_dir = './DRAO_data/'
freq_bins = 10
time_ind = 2000
band = 1600.0 #in MHz
start_freq = 900.0  #in MHz

resourceString1 = 'TCPIP::10.0.1.160::INSTR'  # Standard LAN connection (also called VXI-11)

rm = visa.ResourceManager('@py')
scope = rm.open_resource( resourceString1 )
scope.write_termination = '\n'

 # Clear instrument io buffers and status

scope.write('*RST;*CLS')
scope.write('CALC:PMET:CPOW:BAND '+str(band) + ' MHz')


f = h5py.File(data_dir+start_time+'.hdf5', "a")
set1 = f.create_dataset("timestamp", shape=(time_ind, 10 ), dtype='<f8')
set2 = f.create_dataset("power", shape=(time_ind, 10))
set3 = f.create_dataset("settings", shape=(1, ), data="BW="+str(band)+"MHz  Freq="+str(start_freq)+'MHz')
set4 = f.create_dataset("freq", shape=(10, ))

for i in range(freq_bins):
    set4[i] = start_freq + 0.5*band/freq_bins + i * band/freq_bins 


for count in range(time_ind):
    print("Loop "+str(count+1)+"/"+str(time_ind))
    for i in range(10):
        freq = start_freq + 0.5*band/freq_bins + i*band/freq_bins
        scope.write('PMET:FREQ '+ str(freq) + ' MHz')
        time.sleep(0.2)
        set2[count, i] = float(scope.query("FETC1:PMET?"))
        set1[count, i] = time.time()
        time.sleep(0.1)


f.close()

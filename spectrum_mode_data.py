import visa
import time
import matplotlib.pyplot as plt
import numpy as np
import h5py

start_time = time.strftime("%y%m%d%H%M")

data_dir="./DRAO_data/"
start_freq = float(900.0)                  #in MHz
stop_freq = float(1611.0)                  #in MHz
sweep_count = '10'
sweep_time = '0.1s'
time_ind = 60*3

resourceString1 = 'TCPIP::10.0.1.160::INSTR'  # Standard LAN connection (also called VXI-11)

rm = visa.ResourceManager('@py')
scope = rm.open_resource( resourceString1 )
scope.write_termination = '\n'

 # Clear instrument io buffers and status

#scope.write('*RST;*CLS')
scope.write('FREQ:STAR '+ str(start_freq) +'MHz')
scope.write('FREQ:STOP ' + str(stop_freq) + 'MHz')
time.sleep(0.5)
scope.write('*OPC')

stored = scope.query('*OPC?')

#scope.write('DISP:TRAC:Y:RLEV 0dBm')
scope.write('INIT:CONT OFF')
scope.write('DISP:WIND:TRAC:MODE AVER')

scope.write('SWE:COUN 5')
scope.write('SWE:TIME 0.05s')

scope.write('INIT')

while scope.query('*OPC?') != stored:
    time.sleep(0.1)

cal_trace = scope.query('TRAC:DATA? TRACE1')

cal_list = np.fromstring(cal_trace, sep=',')

f = h5py.File(data_dir+start_time+'.hdf5', "a")                                      
set1 = f.create_dataset("timestamp", shape=(time_ind,), dtype='<f8')
set2 = f.create_dataset("power", shape=(time_ind, len(cal_list)), dtype='f')
set3 = f.create_dataset("settings", shape=(1, ), data=sweep_count+" x "+sweep_time)
scope.write('SWE:COUN '+ sweep_count)
scope.write('SWE:TIME '+ sweep_time)

for count in range(time_ind):

    print("Loop "+str(count+1)+"/"+str(time_ind))
    
    scope.write('INIT')
    while scope.query('*OPC?') != stored:
        time.sleep(0.1)

    my_list = scope.query('TRAC:DATA? TRACE1')
    set1[count] = time.time()
    set2[count] = np.fromstring(my_list, sep=',')
    
    

x_step = (stop_freq-start_freq)/(len(cal_list)-1)
x_ax = []

for i in range(len(cal_list)):
    x_ax.append(start_freq+x_step*i)

set3 = f.create_dataset("freq", shape=(len(x_ax), ), data=np.asarray(x_ax))
f.close()



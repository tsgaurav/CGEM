# CGEM
This repository contains scripts for acquiring data from the R&amp;S Spectrum Analyzer, along with solar transit data acquired from the scripts
# Initial Setup
The module `pyvisa` is required to run the scripts and can be installed using pip :

`sudo pip install pyvisa`

Ensure that the the Spectrum Analyzer is on the same subnet as the machine running the scripts and the scripts have the IP address of the analyzer entered in them
# Script Description

* `spectrum_mode_data.py` requires the analyzer to be in Spectrum mode. This script instructs the analyzer to perform a number of sweeps, time averages them, and stores the spectrum along with a timestamp. The frequency range, sweep time and number of sweeps can be set in the script. The data is stored in an HDF5 file using the date in YYMMDDHHMM format as the name. 

* `power_meter_binning.py` requires the analyzer to be in Power Meter mode. The user has to set the frequency range and the number of bins to divide the range into. The script then collects the power from each frequency interval and stores it with a timestamp. Note that a minimum rest time of 300ms is required for the Analyzer before the script can switch bins. 

# Data Files

* `1807131408.hdf5` and `1807131614.hdf5` contain a full solar transit over different frequency ranges in spectrum mode
* `1807201558.hdf5` contains half a solar transit in spectrum mode, with the sun fully on axis at time=0
* `1807231140.hdf5` contains a full solar transit in power meter mode, over the full output range of the amplifier on CGEM

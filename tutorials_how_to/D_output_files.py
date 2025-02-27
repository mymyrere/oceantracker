#!/usr/bin/env python
# coding: utf-8

# # Output files
# 
# [This note-book is in oceantracker/tutorials_how_to/]
# 
# After running OceanTacker, output files are in the files are the folder given by parameters ./"root_output_dir"/"output_file_base"
# 
# The main files are:
# 
#    *   **users_params_*.json**, a copy of the parameters as supplied by the user, useful in debugging or re-running.
# 
#    *  **_runInfo.json** holds 
#       
#          * file names of case  files
# 
#          * information on computer used
#          
#          * code version, including git commit ID to enable rerunning with exactly the same version
#     
#    * **_caseInfo.json** files, have all the output files for each parallel case run (only 1 case in examples give so far), plus information about the run and data useful in plotting. Eg. 
# 
#       * full set of working parameters with defaults used
# 
#       * timings of parts of code
# 
#       * output_files, the names of all output files generated by the run separated by type.
# 
#       * information about the hindcast, eg start date, end date, time step, ...
#       
#       * basic information from each class used in the computational pipeline
# 
#    * **_caseLog_log.txt** has a copy of what appeared on the screen during the run 
# 
#    * **_tracks.nc** holds the particle tracks in a netcdf file, see below for code example on reading the tracks
# 
#    * **_grid_outline.json** are the boundaries of hydrodynamic model's domain and islands, useful in plotting
# 
#    * **_grid.nc** a netcdf of the hydo-model's grid and other information, useful in plotting and analysis
#    * **_events.nc** a netcdf output from events classes, which only writes output when events occur, eg. a particle entering or exiting given polygons.
#    
#    
# Time variables in these file are in seconds since 1970-01-01
#   
# Below list the files after running the minimal example. 
#     

# In[1]:


# show a list of output files after running  minimal_example
import glob
for f in glob.glob('output/minimal_example/*'):
    print(f) 



# ## Reading particle tracks
# 
# The below shows how to read the netcdf particle track output file into a python dictionary. The track file has a record of each of the particle properties, plus other useful information. The netcdf tracks file has a compact format, the below code reads this file into rectangular numpy  [ time, particle] arrays. Key variables are
# :
# 
# * tracks['x']- the particle locations as a rectangular array of position vectors. With dimensions [ time, particle, vector component]. So that the 2D location is 
# 
#     ``x, y = tracks['x'][:,:,0], tracks['x'][:,:,1]``
# 
# and for a 3D model the vertical position is z= tracks['x'][:,:,2]
# 
# * tracks['time'] - array of time in seconds since 1970-1-1
# 
# * tracks['date'] - array of dates as numpy datetime64[s]
# 
# * tracks['status'] - the numerical codes of particle status, eg moving, dead etc as [ time, particle] array. The values of these status codes are also in the dictionary, eg tracks['status_stranded_by_tide'] = 3. 
# 
# * tracks['age'] - time series of each particles age, ie time since release in seconds. 
# 
# * tracks['IDrelease_group'] and tracks['IDpulse'] - id's of which release group particles where released from and which pulse within that group. These are  based indices and arrays of size particle, the total number of particles released during the run.
# 
# The index within the "particle" dimension, is the individual particleID, ordered from first to last release across the entire model run.
# 
# Note: For very large track files reading may fail, eg where variables exceed the 2-4Gb numpy array limit in Windows. To avoid this rerun using the tracks_writer setting "time_steps_per_per_file" to split the track file into files with given number of time steps.   Key variables in the dictionary are:
#  
# 
# The below also shows how read the hydrodynamic grid. 

# In[2]:


# example of reading tracks file

# read netcdf into dictionary
from oceantracker.post_processing.read_output_files import read_ncdf_output_files

tracks =read_ncdf_output_files.read_particle_tracks_file('output/minimal_example\minimal_example_tracks_compact.nc')
print('Track data', tracks.keys())

# read the hydro-dynamic grid file, useful in plotting
grid =read_ncdf_output_files.read_grid_file('output/minimal_example\minimal_example_grid.nc')
print('Grid data',grid.keys())


# ## Load data method
# 
# Load data method, reads the netcdf, grid, and other  information needed to plot into a dictionary. This is the  recommended method for reading track output.  It uses the case_info file to locate all these files associated with the case run.

# In[3]:


# load netcdf with grid and other useful info for plotting
from oceantracker.post_processing.read_output_files import load_output_files

tracks_plot =load_output_files.load_track_data('output/minimal_example\minimal_example_caseInfo.json')

print('tracks_plot data', tracks_plot.keys())


# 

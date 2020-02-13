# %% Imports
import numpy as np
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile
from pynwb.ecephys import ElectricalSeries, SpikeEventSeries
from pynwb import NWBHDF5IO
from scipy.io import loadmat

# %% Create File & electrodes


# %%
electrode_table_region = nwbfile.create_electrode_table_region([0, 2], 'the first and third electrodes')

rate = 10.0
np.random.seed(1234)
data_len = 1000
ephys_data = np.random.rand(data_len * 2).reshape((data_len, 2))
ephys_timestamps = np.arange(data_len) / rate

ephys_ts = ElectricalSeries('test_ephys_data',
                            ephys_data,
                            electrode_table_region,
                            timestamps=ephys_timestamps,
                            # Alternatively, could specify starting_time and rate as follows
                            # starting_time=ephys_timestamps[0],
                            # rate=rate,
                            resolution=0.001,
                            comments="This data was randomly generated with numpy, using 1234 as the seed",
                            description="Random numbers generated with numpy.random.rand")
nwbfile.add_acquisition(ephys_ts)

nwbfile.add_unit(id=1, electrodes=[0], spike_times=None)
nwbfile.add_unit(id=2, electrodes=[0])

# %% Read
io = NWBHDF5IO('ecephys_example.nwb', 'r')
nwbfile = io.read()
ephys_ts = nwbfile.acquisition['test_ephys_data']
elec2 = ephys_ts.electrodes[1]

# %% Importing a CMBHOME Object
dat = loadmat('C:/Users/wchapman/Downloads/example.mat')  # Data from CMBHOME.Session.Export

root = NWBFile('my first synthetic recording',
               'EXAMPLE_ID',
               datetime.now(tzlocal()),
               experimenter='Dr. Bilbo Baggins',
               lab='Bag End Laboratory',
               institution='University of Middle Earth at the Shire',
               experiment_description='I went on an adventure with thirteen dwarves to reclaim vast treasures.',
               session_id='LONELYMTN')

# %% Create Electrode groups
# Pretend we have two tetrode groups (eg: rsc + hpc) for demonstration
device1 = root.create_device(name='headplate1')

electrode_group1 = root.create_electrode_group('rsc_1',
                                              description='',
                                              location='retrosplenial',
                                              device=device1)

for idx in np.arange(0, 6):
    root.add_electrode(id=idx,
                       x=0., y=0., z=0.,
                       imp=0.,
                       location='retrosplenial',
                       filtering='none',
                       group=electrode_group1)

# moving to second tetrode group
device2 = root.create_device(name='headplate2')

electrode_group2 = root.create_electrode_group('rsc_2',
                                              description='',
                                              location='retrosplenial',
                                              device=device2)

for idx in np.arange(7, 14):
    root.add_electrode(id=idx,
                       x=0., y=0., z=0.,
                       imp=0.,
                       location='retrosplenial',
                       filtering='none',
                       group=electrode_group2)

# %% Add LFP

# %% Add Behavioral Variables

# %% Add Spike Times
for trode in range(0, root.electrodes.__len__()):
    for cluster in range(0, dat['spk_ts'][trode].__len__()):
        root.add_unit(id=cluster, electrodes=[trode], spike_times=dat['spk_ts'][trode][cluster].flatten())

# %% Save it
with NWBHDF5IO('ecephys_example.nwb', 'w') as io:
    io.write(root)

# %%
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
import beepy.Analyses
import beepy.Lfp
import beepy.Unit
import beepy.Session

# %% Import data
dat = loadmat('C:/Users/wchapman/Downloads/track_exported.mat')
# Data from CMBHOME.Session.Export

# begin LFP
lfp = dict()
for channel in range(dat['lfp_ts'].shape[0]):
    lfp_ts = dat['lfp_ts'][channel, :].flatten()
    if not all(lfp_ts == 0):
        lfp_sig = dat['lfp_signal'][channel, :].flatten()
        lfp_fs = 1/(lfp_ts[2] - lfp_ts[1])
        L = beepy.Lfp.Lfp(lfp_fs, lfp_ts, lfp_sig)
        lfp[channel] = L

# begin units
units = dict()
for trode in range(dat['spk_ts'].shape[0]):
    for clust in range(dat['spk_ts'].shape[1]):
        if np.prod(dat['spk_ts'][trode][clust].shape):
            spikes = dat['spk_ts'][trode][clust].flatten()
            units[trode, clust] = beepy.Unit.Unit(spikes)

# Create behavioral data
ts = dat['beh_ts'].flatten()
x = dat['beh_x'].flatten()
y = dat['beh_y'].flatten()
hd = dat['beh_hd'].flatten()
fs = 1/(ts[2] - ts[1])

root = beepy.Session.Session(fs, ts, x, y, lfp=lfp, units=units)
root.active_lfp = 13
root.active_unit = (0, 0)
root.align()
root.lfp.add_band(name='theta')
root.unit

# %%
# root.align()
# root.active_unit = (1, 0)
# #root.active_lfp = 0
#
# root.epoch = [-np.inf, np.inf]
# rm, occ, spks = beepy.Analyses.fields.ratemap(root, kernel_size=1)
#
# plt.clf()
# plt.imshow(rm, interpolation='bilinear')
# plt.show()

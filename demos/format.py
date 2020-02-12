# %%
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
import beepy
import beepy.Lfp

# %% Import data
dat = loadmat('C:/Users/wchapman/Downloads/example.mat')  # Data from CMBHOME.Session.Export

beh = {
    'ts': dat['beh_ts'].flatten(),
    'x': dat['beh_x'].flatten(),
    'y': dat['beh_y'].flatten(),
    'hd': dat['beh_hd'].flatten(),
}


# %%
ts = dat['lfp_ts'][13, :].flatten()
sig = dat['lfp_signal'][13, :].flatten()
fs = 1/(ts[2] - ts[1])
Lfp = beepy.Lfp.Lfp(fs, ts, sig)

# %%
units = dict()
for trode in range(dat['spk_ts'].shape[0]):
    for clust in range(dat['spk_ts'].shape[1]):
        if np.prod(dat['spk_ts'][trode][clust].shape):
            units[trode, clust] = {
                'ts': dat['spk_ts'][trode][clust].flatten(),
            }


# %%


# %%
root = beepy.Session.Session(beh, None, units)
root.align()
root.active_unit = (1, 0)
#root.active_lfp = 0

root.epoch = [-np.inf, np.inf]
rm, occ, spks = beepy.Analyses.fields.ratemap(root, kernel_size=1)

plt.clf()
plt.imshow(rm, interpolation='bilinear')
plt.show()

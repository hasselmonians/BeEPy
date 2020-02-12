# %%
from copy import deepcopy as dc
import numpy as np
from collections import namedtuple
from scipy.signal import hilbert, butter, filtfilt

class Lfp:
    def __init__(self, fs, ts, signal, name=None):
        self.name = name
        self.__raw = {'signal': dc(signal), 'ts': dc(ts)}
        self.__processed = dict()
        self.__epoched = dict()
        self.fs = fs
        self.data = None  # Todo: currently this allows the user to overwrite

        self.update()

    def align(self, ts_beh):
        self.__raw['ind_beh'] = np.digitize(self.__raw['ts'], ts_beh)

    def update(self):
        format = namedtuple('data', list(self.__epoched.keys()), defaults=[None] * self.__epoched.keys().__len__())
        self.data = format._make(self.__epoched.values())

    def add_custom(self, var, name):
        assert self.__raw['ts'].__len__() == var.__len__(), \
            "Var must be same length as original time sequence: %d" %(self.__raw['ts'].__len__())
        pass

    def add_band(self, band=None, name=None):
        """
        Filters LFP within a band and appends corresponding signal, phase, and amplitude to
        :param
            band:
                Two element list indicating the bands to filter to filter down to
            name: Name of the band

            If name is defined as one of a predefined, and band is None, then uses predefined frequencies
        """

        if (band is None) and (name is not None):
            if band == 'theta':
                pass
            if band == 'delta':
                pass
            if band == 'alpha':
                pass
            if band == 'gamma':
                pass

        b, a = butter(3, band[0], band[1], fs=self.fs)
        sig = filtfilt(b, a, self.__raw['signal'])
        amp = np.abs(sig)
        phs = np.imag(sig)

        pass


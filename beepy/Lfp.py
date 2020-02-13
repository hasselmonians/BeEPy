# %%
from copy import deepcopy as dc
import numpy as np
from collections import namedtuple
from scipy.signal import hilbert, butter, filtfilt


class Lfp:
    def __init__(self, fs, ts, signal, name=None):
        self.name = name
        self.fs = fs

        self.__raw = {'signal': dc(signal), 'ts': dc(ts)}
        self.__data = None
        self.__epoch = (-np.inf, np.inf)

    def align(self, ts_beh):
        self.__raw['ind_beh'] = np.digitize(self.__raw['ts'], ts_beh)
        self__epoch = self.epoch

    @property
    def epoch(self):
        return self.__epoch

    @epoch.setter
    def epoch(self, epoch=None):
        if epoch is None:
            epoch = [(-np.inf, np.inf)]
        if type(epoch[0]) != list:
            epoch = [epoch]

        self.__data = {}
        for k in self.__raw:
            self.__data[k] = self.__data[k] = [[]] * epoch.__len__()

        for e in np.arange(epoch.__len__()):
            inds = (self.__raw['ts'] > epoch[e][0]) & (self.__raw['ts'] < epoch[e][1])
            for k in self.__raw:
                self.__data[k][e] = self.__raw[k][inds]

    @property
    def data(self):
        return dc(self.__data)

    def add_custom(self, var, name):
        if not(self.__raw['ts'].__len__() == var.__len__()):
            print("Var must be same length as original time sequence: %d" % (self.__raw['ts'].__len__()))
        else:
            self.__raw[name] = var

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
            if name == 'theta':
                band = [6, 10]
            if name == 'delta':
                band = [2, 4]
            if name == 'alpha':
                pass
            if name == 'gamma':
                pass

        b, a = butter(3, band, fs=self.fs, btype='bandpass')
        sig = filtfilt(b, a, self.__raw['signal'])
        ana = hilbert(sig)
        amp = np.abs(ana)
        phs = np.angle(ana)
        freq = self.fs * np.concatenate((np.nan*np.ones(1), np.diff(np.unwrap(phs)))) / (2*np.pi)
        bads = np.logical_or(freq < 0.5 * band[0], freq > 1.5 * band[1])
        freq[bads] = np.nan

        self.__raw[name] = sig
        self.__raw[name+'_amp'] = amp
        self.__raw[name+'_phs'] = phs
        self.__raw[name+'_freq'] = freq

        self.epoch = self.epoch

    def __repr__(self):
        s = "BeEpy.Lfp with: \n"
        s += "  N raw = %d \n" % (self.__raw['ts'].__len__())
        #s += "\n"
        #s += "  N epoched = %d" % (self.__data['ts'].__len__())
        s += "And fields: \n"
        for k in self.__raw.keys():
            s += k
            s += "; "

        return s

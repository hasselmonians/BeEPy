from collections import namedtuple
import numpy as np
from copy import deepcopy as dc


class Unit:
    def __init__(self, ts):
        self.__raw = {'ts': ts}
        self.__epoched = None
        self.epoch = [-np.inf, np.inf]

    def align(self, beh, lfp=None):
        self.__raw['ind_beh'] = np.digitize(self.__raw['ts'], beh['ts'])
        self.__raw['ind_lfp'] = np.digitize(self.__raw['ts'], lfp['ts'])

        for k in beh.keys():
            if k not in ['ts', 'ind']:
                self.__raw[k] = beh[k][self.__raw['ind_beh']]

        for k in lfp.keys():
            if k not in ['ts', 'ind', 'ind_beh']:
                self.__raw[k] = lfp[k][self.__raw['ind_lfp']]

        self.epoch = self.epoch

    @property
    def epoch(self):
        return None

    @epoch.setter
    def epoch(self, epoch=None):
        if epoch is None:
            epoch = [[-np.inf, np.inf]]
        if type(epoch[0]) != list:
            epoch = [epoch]

        self.__data = {}
        for k in self.__raw:
            self.__data[k] = [[]] * epoch.__len__()

        for e in np.arange(epoch.__len__()):
            inds = (self.__raw['ts'] > epoch[e][0]) & (self.__raw['ts'] < epoch[e][1])
            for k in self.__raw:
                self.__data[k][e] = self.__raw[k][inds]

    @property
    def data(self):
        return dc(self.__data)

    def __repr__(self):
        s = "BeEpy.Unit with: \n" \
            "  %d spikes \n" \
            "  %d in this epoch" % (self.__raw['ts'].__len__(), self.__raw['ts'].__len__())
        # TODO: Multiple epochs
        return s

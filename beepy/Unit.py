from collections import namedtuple
import numpy as np
from copy import deepcopy as dc


class Unit:
    def __init__(self, ts):
        self.__raw = {'ts': ts}
        self.__epoched = None
        self.epoch = [-np.inf, np.inf]

    def align(self):
        pass

    @property
    def epoch(self):
        return None

    @epoch.setter
    def epoch(self, epoch=(-np.inf, np.inf)):
        inds = (self.__raw['ts'] > epoch[0]) & (self.__raw['ts'] < epoch[1])
        data = namedtuple('data', list(self.__raw.keys()), defaults=[None] * self.__raw.keys().__len__())
        self.__data = data._make(self.__raw.values())

        for k in self.__data:
            k = k[inds]

    @property
    def data(self):
        return dc(self.__data)

    def __repr__(self):
        s = "BeEpy.Unit with: \n" \
            "  %d spikes \n" \
            "  %d in this epoch" % (self.__raw['ts'].__len__(), self.__raw['ts'].__len__())
        # TODO: Multiple epochs
        return s
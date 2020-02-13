from copy import deepcopy as dc
import numpy as np
from collections import namedtuple
import beepy
import beepy.Lfp
import beepy.Unit


class Session:
    def __init__(self, fs, ts, x, y, hd=None, vel=None, lfp=None, units=None):
        self.__fs = fs
        self.__raw = {'ts': dc(ts), 'x': dc(x), 'y': dc(y), 'i': np.cumsum(np.ones_like(x)) - 1}
        if hd is not None:
            self.add_custom(hd, 'hd')
        if vel is not None:
            self.add_custom(vel, 'vel')

        self.__active_lfp = None
        self.__active_unit = None

        self.__lfp = lfp
        self.__units = units

        self.epoch = [-np.inf, np.inf]

    @property
    def data(self):
        return dc(self.__data)

    def add_custom(self, var, name):
        assert self.__raw['ts'].__len__() == var.__len__(), \
            "Var must be same length as original time sequence: %d" % (self.__raw['ts'].__len__())
        self.__raw[name] = dc(var)

    def align(self):
        ts_beh = self.__raw['ts']

        for lfp in self.__lfp.values():
            lfp.align(ts_beh)

        for clu in self.__units.values():
            if self.__lfp is not None:
                k = list(self.__lfp.keys())[0]
                clu.align(self.__raw, self.__lfp[k]._Lfp__raw)
            else:
                clu.align(self.__raw)


    @property
    def epoch(self):
        return self.__epoch

    @epoch.setter
    def epoch(self, value):
        self.__spk_aligner(epoch=value)

    @property
    def unit(self):
        if self.__active_unit is None:
            return None
        else:
            return self.__units[self.__active_unit]

    @property
    def lfp(self):
        if self.__lfp is None:
            print("No LFP data loaded")
            return None
        elif self.active_lfp is None:
            print("Must set active_lfp")
            return None
        else:
            return self.__lfp[self.active_lfp]

    @lfp.setter
    def lfp(self, value):
        if type(value) == beepy.Lfp.Lfp:
            self.__lfp = value
            self.__lfp.epoch = self.epoch
            self.__lfp.align(self.__raw['ts'])
        elif type(value) == dict:
            for channel in value.values():
                channel.epoch = self.epoch
                channel.align(self.__raw['ts'])
            self.__lfp = value
        else:
            print("Input must be singleton or dict of beepy.LFP.lfp objects")

    @property
    def active_unit(self):
        return self.__active_unit

    @active_unit.setter
    def active_unit(self, value):
        if value in self.__units.keys():
            self.__spk_aligner(unit=value)
        elif value is None:
            self.__spk_aligner(unit=value)
        else:
            print('Note a valid unit key')

    @property
    def active_lfp(self):
        return self.__active_lfp

    @active_lfp.setter
    def active_lfp(self, value):
        if value in self.__lfp.keys():
            self.__spk_aligner(lfp=value)
        elif value is None:
            self.__spk_aligner(lfp=value)
        else:
            print("Not a valid lfp name")

    def __spk_aligner(self, epoch=None, unit=None, lfp=None):
        if epoch is None:
            epoch = self.epoch
        if unit is None:
            unit = self.active_unit
        if lfp is None:
            lfp = self.active_lfp

        if type(epoch[0]) != list:
            epoch = [epoch]

        self.__data = {}
        for k in self.__raw:
            self.__data[k] = [[]] * epoch.__len__()

        for e in np.arange(epoch.__len__()):
            inds = (self.__raw['ts'] > epoch[e][0]) & (self.__raw['ts'] < epoch[e][1])
            for k in self.__raw:
                self.__data[k][e] = self.__raw[k][inds]

        if lfp is not None:
            self.__lfp[lfp].epoch = epoch

        if unit is not None:
            self.__units[unit].align(self.__raw, self.__lfp[self.active_lfp]._Lfp__raw)
            self.__units[unit].epoch = epoch

        self.__epoch = epoch
        self.__active_lfp = lfp
        self.__active_unit = unit

    def __repr__(self):
        s = "BeEpy.Session with: \n"
        s += "  N raw = %d \n" % (self.__raw['ts'].__len__())
        # s += "\n"
        # s += "  N epoched = %d" % (self.__data['ts'].__len__())
        s += "And fields: \n"
        for k in self.__raw.keys():
            s += k
            s += '; '

        return s

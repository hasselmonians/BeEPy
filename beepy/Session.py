from copy import deepcopy as dc
import numpy as np


class Session:
    def __init__(self, ts, beh, lfp, units):
        self.__raw = {'ts': ts}

        self._raw_beh = dc(beh)
        self._raw_units = dc(units)
        self._raw_lfp = dc(lfp)

        self.__epoched_beh = None
        self.__epoched_lfp = None
        self.__epoched_unit = None

        self.__epoch = [-np.inf, np.inf]
        self.__active_lfp = None
        self.__active_unit = None

    def align(self):
        ts_beh = self._raw_beh['ts']

        if self._raw_lfp is not None:
            for lfp in self._raw_lfp.values():
                lfp['ind_beh'] = np.digitize(lfp['ts'], ts_beh)

        for clu in self._raw_units.values():
            clu['ind_beh'] = np.digitize(clu['ts'], ts_beh)

            if self._raw_lfp is not None:
                clu['ind_lfp'] = np.digitize(clu['ts'], self._raw_lfp[0]['ts'])

    @property
    def epoch(self):
        return self.__epoch

    @epoch.setter
    def epoch(self, value):
        self.__spk_aligner(epoch=value)

    @property
    def beh(self):
        return self.__epoched_beh

    @property
    def spike(self):
        return self.__epoched_unit

    @property
    def lfp(self):
        return self.__epoched_lfp

    @property
    def active_unit(self):
        return self.__active_unit

    @active_unit.setter
    def active_unit(self, value):
        self.__spk_aligner(unit=value)

    @property
    def active_lfp(self):
        return self.__active_lfp

    @active_lfp.setter
    def active_lfp(self, value):
        self.__spk_aligner(lfp=value)

    def __spk_aligner(self, epoch=None, unit=None, lfp=None):
        if epoch is None:
            epoch = self.epoch
        if unit is None:
            unit = self.active_unit
        if lfp is None:
            lfp = self.active_lfp

        inds_beh = (self._raw_beh['ts'] > epoch[0]) & (self._raw_beh['ts'] < epoch[1])
        self.__epoched_beh = {}
        for k in self._raw_beh.keys():
            self.__epoched_beh[k] = self._raw_beh[k][inds_beh]

        self.__epoched_lfp = {}
        if lfp is not None:
            inds_lfp = (self._raw_lfp[lfp]['ts'] > epoch[0]) & (self._raw_lfp[lfp]['ts'] < epoch[1])
            for k in self._raw_lfp[lfp].keys():
                self.__epoched_lfp = self._raw_lfp[lfp][k][inds_lfp]
            self.__active_lfp = lfp

        self.__epoched_unit = {}
        if unit is not None:
            inds_units = (self._raw_units[unit]['ts'] > epoch[0]) & (self._raw_units[unit]['ts'] < epoch[1])
            i_ub = self._raw_units[unit]['ind_beh'][inds_units]
            self.__epoched_unit['ts'] = self._raw_units[unit]['ts'][inds_units]
            for k in self._raw_beh.keys():
                self.__epoched_unit[k] = self._raw_beh[k][i_ub]

            if lfp is not None:
                self.__epoched_unit['lfp'] = {}
                i_ul = self._raw_units[unit]['ind_lfp'][inds_units]
                for k in self._raw_lfp[lfp].keys():
                    self.__epoched_unit['lfp'][k] = self._raw_lfp[lfp][k][i_ul]

            self.__active_unit = unit

        self.__epoch = epoch

    def __str__(self):
        return "TODO: print(root)"
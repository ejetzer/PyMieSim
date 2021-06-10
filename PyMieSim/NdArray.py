#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy
import matplotlib.pyplot as plt
from itertools import product
import pprint
pp = pprint.PrettyPrinter(indent=4)

from PyMieSim.Config     import *
from PyMieSim.ErrorMsg   import *
from PyMieSim.utils      import FormatStr, FormatString, ToList, Table
from PyMieSim.Plots      import ExperimentPlot



class Table:
    def __init__(self, lst0, lst1):
        assert len(set(lst0)) == len(lst0), 'Invalid input'
        assert len(set(lst1)) == len(lst1),  'Invalid input'
        self.lst0 = lst0
        self.lst1 = [element.lower() for element in lst1]


    @FormatStr
    def __getitem__(self, Val):
        assert Val in self.lst0 + self.lst1,  'Invalid input'
        if isinstance(Val, str):
            idx = self.lst1.index(Val)
            return self.lst0[idx]
        else:
            return self.lst1[Val]

    @FormatStr
    def label(self, Val):
        assert Val in self.lst0 + self.lst1,  'Invalid input'
        if isinstance(Val, str):
            dic = Arg2Dict[Val]

        else:
            Val = self.lst1[Val]
            dic = Arg2Dict[Val]

        return dic['label']


    @FormatStr
    def format(self, Val):
        assert Val in self.lst0 + self.lst1,  'Invalid input'
        if isinstance(Val, str):
            dic = Arg2Dict[Val]

        else:
            Val = self.lst1[Val]
            dic = Arg2Dict[Val]

        return dic['format']


class PMSArray(object):

    def __init__(self, array, conf):
        self.data = array
        self.conf = conf

        Torder = []
        Korder = []
        for order, key in self.conf['X'].items():
            Torder.append(order)
            Korder.append(key['name'])

        self.Table = Table(Torder, Korder )


    @FormatStr
    def Cost(self, arg = 'max'):
        """Method return cost function evaluated as defined in the ___ section
        of the documentation.

        Parameters
        ----------
        arg : :class:`str`
            String representing the cost function.

        Returns
        -------
        :class:`float`
            The evaluated cost.

        """

        arg = arg.lower().split('+', 2)

        if len(arg) == 1:
            if   'max'  in arg : return np.max(self)
            elif 'min'  in arg : return np.min(self)
            elif 'mean' in arg : return np.mean(self)

        if len(arg) == 2:
            if   arg[0] == 'rsd'          : func = self.rsd
            elif arg[0] == 'monotonic'    : func = self.Monotonic

            if   arg[1] == 'ri'           : return np.mean( func(self.data, axis = 4) )
            elif arg[1] == 'diameter'     : return np.mean( func(self.data, axis = 3) )
            elif arg[1] == 'polarization' : return np.mean( func(self.data, axis = 2) )
            elif arg[1] == 'wavelength'   : return np.mean( func(self.data, axis = 1) )
            elif arg[1] == 'detector'     : return np.mean( func(self.data, axis = 0) )

        raise ValueError(f"Invalid metric input. \nList of metrics: {MetricList}")


    @FormatStr
    def Monotonic(self, axis):
        """Method compute and the monotonic value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the monotonic metric value of axis.

        """

        arr  = np.gradient(self.data,
                           axis = self.Table[axis]).std( axis = self.Table[axis])

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, conf=conf)


    @FormatStr
    def Mean(self, axis):
        """Method compute and the mean value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the mean value of axis.

        """

        arr  = np.mean(self.data, axis=self.Table[axis] )

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, conf=conf)


    @FormatStr
    def Std(self, axis):
        """Method compute and the std value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the std value of axis.

        """

        arr  = np.std(self.data, axis=self.Table[axis] )

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, conf=conf)


    @FormatStr
    def Rsd(self, axis):
        """Method compute and the rsd value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the rsd value of axis.

        """

        arr  = np.std(self.data, axis=self.Table[axis] ) \
              /np.mean(self.data, axis=self.Table[axis] )

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, conf=conf)


    def UpdateConf(self, axis):
        """Method update the configuration variable (config) in order to
        ouput a new :class:`PMSArray` instance.
        A new instance is created each time a reduction operation is applied,
        such as :func:`Mean`, :func:`Std`, :func:`Rsd`, :func:`Monotonic` .

        Parameters
        ----------
        axis : str
            Key vale of the self dict for which we apply a reduction opration.

        Returns
        -------
        type
            New instance of :class:`PMSArray` .

        """

        newConf = self.conf.copy()

        n = 0
        new = {}
        for order, val in self.conf['X'].items():
            if val['name'] == axis: continue
            new[n] = val
            n += 1

        newConf['X'] = new

        return newConf


    @ExperimentPlot
    @FormatStr
    def Plot(self, y, x,  Scale='linear', figure=None, ax=None, *args, **kwargs):
        """Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Parameters
        ----------
        x : str
            Key of the self dict which represent the abscissa.
        Scale : str
            Options allow to switch between log and linear scale ['log', 'linear'].

        """
        y = ToList(y)

        assert set(y).issubset(set(self.conf['Got'])), ErrorExperimentPlot

        DimSlicer, xval = self.GetSlicer(x)

        for iddx in DimSlicer:
            for key, val in self.conf['Y'].items():

                idx = (*iddx, val['order'])

                label, common  = self.GetLegend(x, idx, val)

                ax.plot(xval, self.data[idx], label=label, *args, **kwargs)

        plt.gcf().text(0.12, 0.9, common, fontsize = 8,
                       bbox      = dict(facecolor='none',
                       edgecolor = 'black',
                       boxstyle  = 'round'))


    def GetSlicer(self, x):

        shape       = list(self.data.shape)

        Xidx        = self.Table[x]

        shape[Xidx] = None

        xval        = self.conf['X'][Xidx]['dimension']

        DimSlicer   = [range(s) if s is not None else [slice(None)] for s in shape[:-1]]

        return product(*DimSlicer), xval


    def GetLegend(self, axis, idx, ydict):
        """Method generate and return the legend text for the specific plot.

        Parameters
        ----------
        axis : :class:`str`
            Axis which is used for x-axis of the specific plot
        idx : :class:`tuple`
            Dimension indices of the specific plot

        Returns
        -------
        :class:`str`
            Text for the legend

        """

        if ydict['type'] == "coupling":
            label = f"{str(ydict['name']): >7} | "

        else:
            label = f"{ydict['legend']: >7} | "

        common = ''

        for order, xdict in self.conf['X'].items():

            format = self.Table.format(order)
            name   = self.Table[order]

            if axis != name:
                val = xdict['dimension'][idx[order]]

                if name == 'material' : val = val.__str__()

                string = f"{name}: {val:{format}} | "

                if xdict['size'] != 1: label += string

                else: common += string

        return label, common


    def __getitem__(self, key):
        index = self.conf['Y'][key]['order']
        return self.data[..., index].squeeze()


    def __str__(self):

        name = [str(val['name']) for val in self.conf['Y'].values()]

        text =  f'PyMieArray \nVariable: {name.__str__()}\n' + '='*120 + '\n'

        text += f"{'Parameter':13s}\n" + '-'*120 + '\n'

        for order, key in self.conf['X'].items():
            label  = self.Table.label(order)
            format = self.Table.format(order)
            dim    = order
            size   = key['size']

            text += f"""{label:30s}\
            | dimension = {name}\
            | size      = {size}\
            \n"""

        text += '='*120 + '\n'

        return text



class Opt5DArray(np.ndarray):
    def __new__(cls, *args, **kwargs):
        this = np.array(*args, **kwargs, copy=False)
        this = np.asarray(this).view(cls)

        return this


    def __array_finalize__(self, obj):
        pass


    def __init__(self, arr, Name=''):
        self.Name         = Name

        self.dim = { 'detector'     : True,
                     'wavelength'   : True,
                     'polarization' : True,
                     'diameter'     : True,
                     'index'        : True}

    @FormatStr
    def DefineCostFunc(self, arg):
        arg = arg.lower().split('+', 2)

        if len(arg) == 1:
            if   'max'  in arg : self.CostFunc = np.max
            elif 'min'  in arg : self.CostFunc = np.min
            elif 'mean' in arg : self.CostFunc = np.mean

        if len(arg) == 2:
            if   arg[0] == 'rsd'       : func = self.rsd
            elif arg[0] == 'monotonic' : func = self.Monotonic
            elif arg[0] == 'max'       : func = np.max
            elif arg[0] == 'min'       : func = np.min
            elif arg[0] == 'mean'      : func = np.mean


            if   arg[1] == 'all'          : self.CostFunc = np.mean( func(self) )
            elif arg[1] == 'ri'           : self.CostFunc = np.mean( func(self, axis = 4) )
            elif arg[1] == 'diameter'     : self.CostFunc = np.mean( func(self, axis = 3) )
            elif arg[1] == 'polarization' : self.CostFunc = np.mean( func(self, axis = 2) )
            elif arg[1] == 'wavelength'   : self.CostFunc = np.mean( func(self, axis = 1) )
            elif arg[1] == 'detector'     : self.CostFunc = np.mean( func(self, axis = 0) )

            raise ValueError(f"Invalid metric input. \nList of metrics: {MetricList}")



    def Cost(self):

        return self.CostFunc(self)

    def Monotonic(self, axis):

        Grad = np.gradient(self, axis = axis)

        STD = Grad.std( axis = axis)

        return STD[0]


    def rsd(self, array, axis):
        return np.std(array, axis)/np.mean(array, axis)


    def RIMonotonic(self):

        Grad = np.gradient(self, axis = 0)

        STD = Grad.std( axis = 0)

        return STD[0]

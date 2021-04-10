import numpy as np
import copy
from collections import OrderedDict
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from itertools import product


MetricList = ["max",
              "min",
              "mean",
              "rsd+ri",
              "rsd+diameter",
              "rsd+polarization"
              "rsd+wavelength"
              "rsd+detector",
              "monotonic+ri",
              "monotonic+diameter",
              "monotonic+polarization",
              "monotonic+wavelength",
              "monotonic+detector"]

DetectorParamList = ['NA',
                     'PhiOffset',
                     'ThetaOffset',
                     'Filter']

SourceParamList = ['E0',
                   'Polarization',
                   'Wavelength']

ParameterList = DetectorParamList + SourceParamList

class Optimizer:
    def __init__(self,
                 Setup,
                 Metric,
                 Parameter,
                 X0,
                 WhichDetector,
                 MinVal,
                 MaxVal,
                 Optimum,
                 FirstStride,
                 MaxIter=50,
                 Tol=1e-10):

        assert Metric.lower() in MetricList, f"Metric {Metric} not in the MetricList \n{MetricList}"
        assert all(len(x)==len(Parameter) for x in [X0, MinVal, MaxVal ]  ), f'Lenght of parameters, X0, MinVal, MaxVal not equal'

        self.Setup           = Setup
        self.Metric          = Metric
        self.Parameters      = Parameter
        self.X0              = X0
        self.WhichDetector   = WhichDetector
        self.MinVal          = MinVal
        self.MaxVal          = MaxVal
        self.FirstStride     = FirstStride
        self.MaxIter         = MaxIter
        self.Tol             = Tol

        if Optimum.lower()   == 'maximum':
            self.sign = -1
        elif Optimum.lower() == 'minimum':
            self.sign = 1


        self.Result = self.Run()



    def ComputePenalty(self, Parameters, x, MaxVal, MinVal, factor=100):
        Penalty = 0
        for n in range(len(Parameters)):
            if MinVal[n] and x[0]< MinVal[n]:
                Penalty += np.abs( x[0]*factor );
                x[0]     = self.MinVal[n]

            if MinVal[n] and x[0]> MaxVal[n]:
                Penalty += np.abs( x[0]*factor );
                x[0]     = self.MaxVal[n]

        return Penalty


    def UpdateConfiguration(self, Parameters, x, WhichDetector):

        for n in range(len(Parameters)):
            if Parameters[n] in DetectorParamList:
                setattr(self.Setup.DetectorSet[WhichDetector], Parameters[0], x[0])

            elif Parameters[n] in SourceParamList:
                setattr(self.Setup.SourceSet.Source, Parameters[0], x[0])


    def Run(self):

        def EvalFunc(x):
            Penalty = self.ComputePenalty(self.Parameters, x, self.MaxVal, self.MinVal, factor=100)

            self.UpdateConfiguration(self.Parameters, x, self.WhichDetector)

            Cost = self.Setup.Coupling(AsType='Optimizer').Cost(self.Metric)

            return self.sign * np.abs(Cost) + Penalty

        Minimizer = Caller(EvalFunc, ParameterName = self.Parameters)

        return minimize(fun      = Minimizer.optimize,
                        x0       = self.X0,
                        method   = 'COBYLA',
                        tol      = self.Tol,
                        options  = {'maxiter': self.MaxIter, 'rhobeg':self.FirstStride})



class Caller:
    def __init__(self, function, ParameterName: list):
        self.ParameterName = ParameterName
        self.f = function # actual objective function
        self.num_calls = 0 # how many times f has been called
        self.callback_count = 0 # number of times callback has been called, also measures iteration count
        self.list_calls_inp = [] # input of all calls
        self.list_calls_res = [] # result of all calls
        self.decreasing_list_calls_inp = [] # input of calls that resulted in decrease
        self.decreasing_list_calls_res = [] # result of calls that resulted in decrease
        self.list_callback_inp = [] # only appends inputs on callback, as such they correspond to the iterations
        self.list_callback_res = [] # only appends results on callback, as such they correspond to the iterations

    def optimize(self, x):
        """Executes the actual simulation and returns the result, while
        updating the lists too. Pass to optimizer without arguments or
        parentheses."""
        result = self.f(x) # the actual evaluation of the function
        if not self.num_calls: # first call is stored in all lists
            self.decreasing_list_calls_inp.append(x)
            self.decreasing_list_calls_res.append(result)
            self.list_callback_inp.append(x)
            self.list_callback_res.append(result)
        elif result < self.decreasing_list_calls_res[-1]:
            self.decreasing_list_calls_inp.append(x)
            self.decreasing_list_calls_res.append(result)
        self.list_calls_inp.append(x)
        self.list_calls_res.append(result)
        self.num_calls += 1


        if len(self.ParameterName) == 1:

            text = """ \
            Call Number : {0} \
            \t {1}: {2:.5e} \
            \t Cost+Penalty: {3:.10e} \
            """.format(self.num_calls,
                       self.ParameterName[0],
                       x[0],
                       result)

        if len(self.ParameterName) == 2:
            text = """ \
            Call Number : {0} \
            \t {1}: {2:.5e} \
            \t {3}: {4:.5e} \
            \t Cost+Penalty: {5:.10e} \
            """.format(self.num_calls,
                       self.ParameterName[0],
                       x[0],
                       self.ParameterName[1],
                       x[1],
                       result)

        print(text)
        return result




class PMSArray(object):

    def __init__(self, array, Name, conf):
        self.data = array
        self.Name = Name

        self.conf = conf


    def Cost(self, arg = 'max'):

        arg = arg.lower().split('+', 2)

        if len(arg) == 1:
            if   'max' in arg:  return np.max(self)
            elif 'min' in arg:  return np.min(self)
            elif 'mean' in arg: return np.mean(self)

        if len(arg) == 2:
            if   arg[0] == 'rsd':        func = self.rsd
            elif arg[0] == 'monotonic':  func = self.Monotonic

            if   arg[1] == 'ri':           return np.mean( func(self, axis = 4) )
            elif arg[1] == 'diameter':     return np.mean( func(self, axis = 3) )
            elif arg[1] == 'polarization': return np.mean( func(self, axis = 2) )
            elif arg[1] == 'wavelength':   return np.mean( func(self, axis = 1) )
            elif arg[1] == 'detector':     return np.mean( func(self, axis = 0) )

        raise ValueError(f"Invalid metric input. \nList of metrics: {MetricList}")



    def Monotonic(self, axis):

        axis = axis.lower()

        arr = np.gradient(self.data,
                          axis = self.conf['order'][axis]).std( axis = self.conf['order'][axis])

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, Name=self.Name, conf=conf)


    def Mean(self, axis):

        axis = axis.lower()

        arr = np.mean(self.data, axis=self.conf['order'][axis] )

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, Name=self.Name, conf=conf)


    def Std(self, axis):

        axis = axis.lower()

        arr = np.std(self.data, axis=self.conf['order'][axis] )

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, Name=self.Name, conf=conf)


    def Rsd(self, axis):

        axis = axis.lower()

        arr = np.std(self.data, axis=self.conf['order'][axis] ) \
             /np.mean(self.data, axis=self.conf['order'][axis] )

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, Name=self.Name, conf=conf)


    def UpdateConf(self, axis):

        newConf = copy.deepcopy(self.conf)

        newConf['order'].pop(axis)
        newConf['dimension'].pop(axis)

        for n, key in enumerate(newConf['order'].keys()):
            newConf['order'][key] = n

        return newConf

    def Plot(self, y, x):
        x = x.lower()
        shape = list(self.data.shape)
        for key, order in self.conf['order'].items():
            if x == key:
                shape[order] = None
                xlabel = key
                xval   = self.conf['dimension'][key]


        for idx in product(*[range(s) if s is not None else [slice(None)] for s in shape]):
            plt.plot(xval,
                     self.data[idx],
                     label = self.GetLabel(x, idx))

        plt.xlabel(xlabel)
        plt.grid()
        plt.legend(fontsize=8)
        plt.show()


    def GetLabel(self, x, idx):
        label = ''

        for key in self.conf['order']:

            if x != key:
                index = idx[self.conf['order'][key]]
                val = self.conf['dimension'][key][index]
                label += f"{key[:3]}.:{val} | "

        return label


    def __getitem__(self, key):
        return self.data[key]


    def __setitem__(self, key, value):
        self.data[key] = value


    def __str__(self):
        text = f'Variable: {self.Name}\n' + '='*90 + '\n'
        text += f"{'Parameter':13s}\n" + '-'*90 + '\n'
        for key, val in self.conf['order'].items():
            text += f"""{key:13s}\
                        | dimension = {val:2d}\
                        | size = {len(self.conf['dimension'][key]):2d}\
                         \n"""

        text += '='*90 + '\n'
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

        self.dim = { 'detector'      : True,
                      'wavelength'   : True,
                      'polarization' : True,
                      'diameter'     : True,
                      'index'        : True}




    def Cost(self, arg = 'max'):

        arg = arg.lower().split('+', 2)

        if len(arg) == 1:
            if   'max' in arg:  return np.max(self)
            elif 'min' in arg:  return np.min(self)
            elif 'mean' in arg: return np.mean(self)

        if len(arg) == 2:
            if   arg[0] == 'rsd':        func = self.rsd
            elif arg[0] == 'monotonic':  func = self.Monotonic

            if   arg[1] == 'ri':           return np.mean( func(self, axis = 4) )
            elif arg[1] == 'diameter':     return np.mean( func(self, axis = 3) )
            elif arg[1] == 'polarization': return np.mean( func(self, axis = 2) )
            elif arg[1] == 'wavelength':   return np.mean( func(self, axis = 1) )
            elif arg[1] == 'detector':     return np.mean( func(self, axis = 0) )

        raise ValueError(f"Invalid metric input. \nList of metrics: {MetricList}")


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

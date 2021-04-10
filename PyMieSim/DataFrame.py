import pandas as pd
import matplotlib.pyplot as plt

def show(func):
    def inner(*args, **kwargs):
        try: return func(*args, **kwargs)

        finally: plt.show()

    return inner



class ExperimentDF(pd.DataFrame):

    def __init__(self, *args, **kwargs):
        pd.DataFrame.__init__(self, *args, **kwargs)
        self.ax = None

    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')

    @show
    def Plot(self, y='Coupling', x = 'Diameter', **kwargs):


        if   x == 'Diameter':
            index  = [0,1,2,4];
            title  = 'Det/Wav/Pol/RI';
            xlabel = r'Scatterer diameter [m]'

        elif x == 'Wavelength':
            index = [0,2,3,4];
            title = 'Det/Dia/Pol/RI';
            xlabel = r'Source wavelength [m]' ;

        fig = self.unstack(level=index).plot(y       = y,
                                              grid    = True,
                                              figsize = (8,4),
                                              xlabel  = xlabel,
                                              ylabel  = r'Coupling [Watt]',
                                              **kwargs)

        fig.legend(prop={'size': 8}, title=title,loc=2)

        return fig



class EfficiencesDF(pd.DataFrame):

    def __init__(self, *args, **kwargs):
        pd.DataFrame.__init__(self, *args, **kwargs)
        self.ax = None


    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')

    @show
    def Plot(self, y='Qsca', x = 'Diameter', **kwargs):

        if   x == 'Diameter':
            index  = [0,1,3];
            title  = 'Pol/Wav/RI'
            xlabel = r'Scatterer diameter [m]'

        elif x == 'Wavelength':
            index = [0,1,2];
            title = 'Pol/Dia/RI'
            xlabel = r'Source wavelength [m]' ;

        Name = 'Efficiency'

        fig = self.unstack(level=index).plot(y       = y,
                                              grid    = True,
                                              figsize = (8,4),
                                              xlabel  = xlabel,
                                              ylabel  = f'{Name}',
                                              **kwargs)

        fig.legend(prop={'size': 8}, title=title,loc=2)

        return fig


class ExperimentalDataFrame(pd.DataFrame):

    def __init__(self, **kwargs):
        pd.DataFrame.__init__(self, **kwargs)
        self.ax = None

    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')

    @show
    def Plot(self, y='Coupling', **kwargs):

        fig = self.unstack(level=[-3,-1]).plot(y       = y,
                                              grid    = True,
                                              figsize = (8,4),
                                              xlabel  = r'Scatterer diameter [m]',
                                              ylabel  = r'Coupling [Watt]',
                                              **kwargs)

        fig.legend(prop={'size': 8}, title='Detec. , Refrac. index',loc=2)

        return fig



class S1S2DataFrame(pd.DataFrame):

    def __init__(self,**kwargs):
        pd.DataFrame.__init__(self,**kwargs)
        self.ax = None

    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')

    @show
    def Plot(self, **kwargs):

        fig = self.unstack(level=[0,1]).plot(y       = 'S1',
                                            grid    = True,
                                            figsize = (8,4),
                                            xlabel  = r'$\phi$ angle [degree]',
                                            ylabel  = r'$|S1|$',
                                            **kwargs)

        fig1 = self.unstack(level=[0,1]).plot(y       = 'S2',
                                             grid    = True,
                                             figsize = (8,4),
                                             xlabel  = r'$\phi$ angle [degree]',
                                             ylabel  = r'$|S2|$',
                                             **kwargs)

        fig.legend(prop={'size': 8})

        fig1.legend(prop={'size': 8})

        return(fig, fig1)



class QscaDataFrame(pd.DataFrame):

    def __init__(self,**kwargs):
        pd.DataFrame.__init__(self,**kwargs)
        self.ax = None

    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')

    @show
    def Plot(self, **kwargs):

        fig = self.unstack(level=[1]).plot(y       = 'Qsca',
                                          grid    = True,
                                          figsize = (8,4),
                                          xlabel  = r'Scatterer diameter [m]',
                                          ylabel  = r'Q$_{Scat}$ [Watt.m$^{-2}$]',
                                          **kwargs)

        fig.legend(prop={'size': 8}, title='Refrac. index', loc=4)

        return fig

















# -

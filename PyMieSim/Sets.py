import numpy as np
import pandas as pd
from typing import Tuple, Union

from PyMieSim.utils import LoadLibraries
from PyMieSim.Physics import Source
from PyMieSim.Optimizer import OptArray
from PyMieSim.Detector import LPmode, Photodiode
from PyMieSim.DataFrame import ExperimentalDataFrame, S1S2DataFrame, QscaDataFrame
from PyMieSim.Scattering import Scatterer, WMSample

GetS1S2, GetEfficiencies = LoadLibraries(['S1S2', 'Efficiencies'])


class ScattererSet(object):
    """Small class which represents the set of scatterer considered for analysis.

    Parameters
    ----------
    DiameterList : list
        List of diameters to be considered for the single scatterers.
    RIList : list
        List of refractive index to be considered for the single scatterers.
    Source : Source
        Source <class> representing the illumination impinging the scatterers.

    Attributes
    ----------
    DiameterList
    RIList
    Source

    """

    def __init__(self,
                 DiameterList:    list,
                 RIList:          list,
                 Source:          Source,
                 IndexMedium:     float   = 1.0
                 ):

        if not isinstance(RIList, (list, np.ndarray)): RIList = [RIList]

        if not isinstance(DiameterList, (list, np.ndarray)): DiameterList = [DiameterList]

        self.DiameterList, self.RIList = DiameterList, RIList

        self.nMedium = IndexMedium

        self.Source = Source


    def Qsca(self):
        """Methode generate a Pandas Dataframe of scattering efficiencies
        (Qsca) vs. scatterer diameter vs. scatterer refractive index.

        Returns
        -------
        pandas.DataFrame
            Dataframe containing Qsca vs. Diameter vs. Index.

        """

        MI = pd.MultiIndex.from_product([self.DiameterList, self.RIList], names=['Diameter', 'RI'])

        df = QscaDataFrame(index = MI, columns = ['Qsca'])

        for nr, RI in enumerate(self.RIList):

            for nd, Diameter in enumerate(self.DiameterList):
                SizeParam =  2 * np.pi * Diameter/self.Source.Wavelength

                Qsca, Qext, Qabs = GetEfficiencies(RI, SizeParam);

                df.loc[(Diameter, RI),'Qsca'] = np.abs(Qsca)

        return df


    def S1S2(self, num=201):
        """Methode generate a Pandas Dataframe of S1 and S2 parameter as a
        of the scattering angle, this for the differents scatterer diameter
        and refractive index.

        Returns
        -------
        pandas.DataFrame
            Dataframe containing S1 and S2 vs. phi angle vs Diameter vs. Index.

        """
        Angle = np.linspace(0,2*np.pi,num)

        MI = pd.MultiIndex.from_product([self.DiameterList, self.RIList, Angle],
                                        names=['Diameter', 'RI', 'Angle'])

        df = S1S2DataFrame(index = MI, columns = ['S1', 'S2'])

        for nr, RI in enumerate(self.RIList):

            for nd, Diameter in enumerate(self.DiameterList):
                SizeParam =  2 * np.pi * Diameter/self.Source.Wavelength

                S1, S2 = GetS1S2(m          = RI,
                                 diameter   = Diameter,
                                 wavelength = self.Source.Wavelength,
                                 nMedium    = self.nMedium,
                                 phi        = np.linspace(0,2*np.pi,num))

                df.loc[(Diameter, RI),'S1'] = np.abs(S1S2[0])

                df.loc[(Diameter, RI),'S2'] = np.abs(S1S2[1])

        return df




class ExperimentalSet(object):
    """Small class which represents experimental setup for analysis.
    THe setup is comprised of ScattrererSet and a tuple of Detectors.

    Parameters
    ----------
    ScattererSet : <ScattererSet>
        Instance containing information about the scatterer to analyse in the experiment.
    Detectors : tuple
        Tuple containing all the detectors instance to analyses the scattering signal.

    Attributes
    ----------
    Detectors
    ScattererSet
    _Coupling

    """

    def __init__(self,
                 ScattererSet: ScattererSet = None,
                 Detectors:    tuple        = None):


        if isinstance(Detectors, (Photodiode, LPmode)): Detectors = (Detectors,)

        assert isinstance(Detectors, tuple), 'Detectors arguement must be a tuple'

        self.Detectors = Detectors

        self.ScattererSet = ScattererSet

        self._Coupling = None


    @property
    def Coupling(self):
        """Property method which return a n by m by l OptArray array, n being the
        number of detectors, m is the point evaluated for the refractive index,
        l is the nomber of point evaluted for the scatterers diameters.

        Returns
        -------
        OptArray
            Raw array of detectors coupling.

        """
        temp = np.empty( [len(self.Detectors), len(self.ScattererSet.RIList), len(self.ScattererSet.DiameterList) ] )

        for nDetector, Detector in enumerate(self.Detectors):

            for nIndex, RI in enumerate(self.ScattererSet.RIList):
                for nDiameter, Diameter in enumerate(self.ScattererSet.DiameterList):

                    Scat = Scatterer(Diameter  = Diameter,
                                     Index     = RI,
                                     Source    = self.ScattererSet.Source)

                    Coupling = Detector.Coupling(Scatterer = Scat)

                    temp[nDetector, nIndex, nDiameter] = Coupling

        return OptArray(temp)


    @property
    def DataFrame(self):
        """Property method which return pandas.DataFrame of the scattering-
        detector coupling for the different diameter and refracive index
        evaluated.

        Returns
        -------
        pandas.DataFrame
            DataFrame of detectors coupling.

        """
        MI = pd.MultiIndex.from_product([range(len(self.Detectors)), self.ScattererSet.DiameterList, self.ScattererSet.RIList],
                                        names=['Detectors','Diameter','RI',])


        df = ExperimentalDataFrame(index = MI, columns = ['Coupling'])

        df.attrs['Detectors'] = self.Detectors

        for nr, RI in enumerate( self.ScattererSet.RIList ):

            for nd, Diameter in enumerate(self.ScattererSet.DiameterList):

                for nDetector, Detector in enumerate(self.Detectors):

                    Scat = Scatterer(Diameter    = Diameter,
                                     Index       = RI,
                                     Source      = self.ScattererSet.Source)

                    Coupling = Detector.Coupling(Scatterer = Scat)

                    df.at[(nDetector, Diameter, RI),'Coupling'] = Coupling

        df.Coupling = df.Coupling.astype(float)

        df['Mean'] = df.groupby(['Detectors','Diameter']).Coupling.transform('mean')

        df['STD'] = df.groupby(['Detectors','Diameter']).Coupling.transform('std')

        return df




class SampleSet(object):

    def __init__(self,
                 gList:           list,
                 LcList:          list,
                 D:               float,
                 Nc:              float,
                 Detector:        Union[LPmode, Photodiode],
                 Source:          Source,
                 Mode:            str = 'Centered',
                 Npts:            int = 201,
                 ):

        self.gList, self.LcList = gList, LcList

        self.D = D; self.Nc = Nc

        self.Source = Source

        self.Detector, self.Source, self.Mode = Detector, Source, Mode

        self.Coupling = np.empty( [len(self.LcList), len(self.gList)] )

        maxPhi, minPhi = np.max(Detector.Meshes.Phi.Degree), np.min(Detector.Meshes.Phi.Degree)

        self.PhiVector = np.linspace(-np.pi/2, np.pi/2,201)

        self.PhiVectorDetector = np.linspace(minPhi, maxPhi, 101)


    @property
    def DataFrame(self, Filter: list = ['None'] ):

        if not isinstance(Filter, list): Filter = [Filter]

        MI = pd.MultiIndex.from_product([Filter, self.gList, self.LcList], names=['Filter','g','lc',])

        df = DataFrame(index = MI, columns = ['Coupling'])

        df.attrs['Filter'] = Filter

        for ng, g in enumerate( self.gList ):

            for nlc, lc in enumerate(self.LcList):

                Scat = Sample(g           = g,
                              lc          = lc,
                              D           = self.D,
                              Nc          = self.Nc,
                              Source      = LightSource,
                              Meshes      = self.Detector.Meshes)

                for Polar in df.attrs['Filter']:
                    self.Detector.Filter = Polar

                    Coupling = self.Detector.Coupling(Scatterer = Scat, Mode = self.Mode)

                    df.at[(Polar, g, lc),'Coupling'] = Coupling


        df.Coupling = df.Coupling.astype(float)

        df.DetectorNane = self.Detector._name

        return df


    @property
    def Coupling(self, Filter='None'):

        temp = np.empty( [ len(self.gList), len(self.LcList) ] )


        for ng, g in enumerate( self.gList ):

            for nlc, lc in enumerate(self.LcList):

                Samp = Sample(g           = g,
                              lc          = lc,
                              D           = self.D,
                              Nc          = self.Nc,
                              Source      = self.Source,
                              Meshes      = self.Detector.Meshes)

                Coupling = self.Detector.Coupling(Scatterer = Samp, Mode = self.Mode)

                temp[ng, nlc] = Coupling

        return OptArray(temp)






# -

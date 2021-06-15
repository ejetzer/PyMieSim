#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mayavi
import matplotlib._pylab_helpers
from mayavi     import mlab
from unittest   import TestCase
from numpy      import linspace, pi
from pyface.api import GUI
import matplotlib.pyplot as plt
import numpy             as np

from PyMieSim.Scatterer          import Sphere, Cylinder, WMSample
from PyMieSim.Source             import PlaneWave, GaussianBeam
from PyMieSim.GLMT.python.Sphere import SPF
from PyMieSim.Detector           import LPmode, Photodiode, _Photodiode
from PyMieSim.Experiment         import ScatSet, Setup, SourceSet, SampleSet, DetectorSet
from PyMieSim.Mesh               import FibonacciMesh
from PyMieSim.Plots              import *
from unittest.mock               import patch
from PyMieSim.Representations    import S1S2


LightSource = PlaneWave(Wavelength = 450e-9, Polarization = 0)
Scat        = Sphere(Diameter = 300e-9, Index = 1.4, Source = LightSource)
Samp        = WMSample(g = 0.8, lc = 1e-5, D = 2.5, Nc = 1e4, Source = LightSource)
Detector    = LPmode(Mode = (0, 1,'h'), Sampling = 11, NA = 0.2)
Detector1   = Photodiode(Sampling = 11, NA = 0.2)
phi         = linspace(-pi/2, pi/2,4)
theta       = linspace(-pi, pi,4)


scatKwargs   = { 'Diameter' : 200e-9,
                 'Index'    : [4],
                 'nMedium'  : [1] }

sourceKwargs = { 'Wavelength'   : np.linspace(400e-9, 1000e-9, 10),
                 'Polarization' : [0]}


def CloseMatplotlib():
    """Close matplotlib scene."""
    figures=[manager.canvas.figure
         for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
    if len(figures) >= 1:
        plt.close('all')


def CloseMlab():
    """Close mayavi scene."""
    engine = mlab.get_engine()
    scene = engine.current_scene
    if scene is not None:
        mlab.close()

def Close():
    """Close all scene."""
    CloseMatplotlib()

    CloseMlab()



PLOTTIME = 600

class DetectorTestCase(unittest.TestCase):

    def test00(self):
        global Detector0
        Detector0 = Photodiode(Sampling     = 11,
                               NA           = 0.2,
                               GammaOffset  = 0,
                               PhiOffset    = 0,
                               CouplingMode = 'Centered')

        print('Photodiode initialisation passed')


    def test01(self):
        from PyMieSim.Detector import LPmode
        global LPmode
        LPmode = LPmode(Mode         = (0,1),
                        Sampling     = 11,
                        NA           = 0.2,
                        GammaOffset  = 0,
                        PhiOffset    = 0,
                        CouplingMode = 'Centered')

        print('LPmode initialisation passed')


    def test02(self):
        from PyMieSim.Detector import IntegratingSphere
        global IntegratingSphere
        IntegratingSphere = IntegratingSphere()

        print('IntegratingSphere initialisation passed')


    def test03(self):
        GUI.invoke_after(PLOTTIME, Close)
        Detector0.Plot()
        print('Photodiode Plotting passed')


    def test04(self):
        GUI.invoke_after(PLOTTIME, Close)
        LPmode.Plot()
        print('LPmode Plotting passed')


    def test05(self):
        GUI.invoke_after(PLOTTIME, Close)
        IntegratingSphere.Plot()
        print('IntegratingSphere Plotting passed')


class ScattererTestCase(unittest.TestCase):

    def test00(self):
        from PyMieSim.Scatterer import Sphere
        global sScat
        sScat = Sphere(Diameter = 300e-9,
                       Index    = 1.4,
                       Source   = LightSource)

        print('Sphere initialisation passed')


    def test01(self):
        from PyMieSim.Scatterer import Cylinder
        global cScat
        cScat = Cylinder(Diameter = 300e-9,
                         Index    = 1.4,
                         Source   = LightSource)

        print('Cylinder initialisation passed')


    def test02(self):
        sScat.S1S2(Num=10)
        print('Spherical Scatterer <S1S2> compute passed')


    def test03(self):
        sScat.Stokes(Num=10)
        print('Spherical Scatterer <Stokes> compute passed')


    def test04(self):
        sScat.FarField(Num=10)
        print('Spherical Scatterer <FarFields> compute passed')


    def test05(self):
        sScat.SPF(Num=10)
        print('Spherical Scatterer <SPF> compute passed')


    def test06(self):
        Detector0.Coupling(Scatterer = sScat)
        print('<Photodiode> coupling passed')

    def test07(self):
        LPmode.Coupling(Scatterer = sScat)
        print('<LPmode> coupling passed')


    def test08(self):
        IntegratingSphere.Coupling(Scatterer = sScat)
        print('<IntegratingSphere> coupling passed')


    def test09(self):
        GUI.invoke_after(PLOTTIME, Close)
        sScat.S1S2(10).Plot()
        print('<S1S2> Plot passed')


    def test10(self):
        #GUI.invoke_after(PLOTTIME, Close)
        #sScat.Stokes(10).Plot()
        print('<Stokes> Plot passed')


    def test11(self):
        #GUI.invoke_after(PLOTTIME, Close)
        #GUI.invoke_after(2*PLOTTIME, Close)
        #sScat.FarField(10).Plot()
        print('<FarField> Plot passed')


    def test12(self):
        #GUI.invoke_after(PLOTTIME, Close)
        #sScat.SPF(10).Plot()
        print('<SPF> Plot passed')


    def test13(self):
        Detector0.Footprint(Scatterer=sScat, Num=10)
        print('Photodiode footprint compute passed')


    def test14(self):
        LPmode.Footprint(Scatterer=sScat, Num=10)
        print('LPmode footprint compute passed')




class ExperiementTestCase(unittest.TestCase):
    def test00(self):
        global sScatSet
        sScatSet = ScatSet(Scatterer = Sphere,  kwargs = scatKwargs )

        print('<ScattererSet> initialisation passed')


    def test01(self):
        global sourceSet
        sourceSet  = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

        print('<SourceSet> initialisation passed')


    def test02(self):
        global ExpSet

        detecKwargs = { 'NA'            : [0.03],
                       'Sampling'       : 300,
                       'GammaOffset'    : 0,
                       'PhiOffset'      : 0,
                       'CouplingMode'   : 'Centered'}

        DetecSet   = DetectorSet(Detector = Photodiode, kwargs = detecKwargs)

        ExpSet = Setup(ScattererSet = sScatSet,
                       SourceSet    = sourceSet,
                       DetectorSet  = DetecSet)

        print('<Setup> initialisation passed')


    def test03(self):
        global pymieArrayEff
        pymieArrayEff = ExpSet.Get('Qsca')
        print('Experiment Efficiencies computing passed')


    def test04(self):
        global pymieArrayCoupling
        pymieArrayCoupling = ExpSet.Get('Coupling')
        print('Experiment Coupling computing passed')


    def test05(self):
        GUI.invoke_after(PLOTTIME, Close)
        pymieArrayEff.Plot(y='Qsca', x='diameter')
        print('PyMieSim Array Efficiencies plotting passed')


    def test06(self):
        GUI.invoke_after(PLOTTIME, Close)
        pymieArrayCoupling.Plot(y='Coupling', x='diameter')
        print('PyMieSim Array Coupling plotting passed')


    def test07(self):
        ExpSet.Get('Qsca')
        print("<Experiment> 'pymiesim' output passed")


    def test08(self):
        ExpSet.Get('Coupling')
        print("<Experiment> 'dataframe' output passed")


    def test09(self):
        ExpSet.Get('Coupling')
        print("<Experiment> 'optimizer' output passed")


class GLMTTestCase(unittest.TestCase):


    def test00(self):
        global Gbeam
        Gbeam = GaussianBeam(Wavelength   = 1.3e-6,
                             NA           = 0.6,
                             Polarization = 0,
                             Offset       = [0e-6,0e-6,0e-6])

        print('GaussianBeam beam initialisation passed')


    def test01(self):
        Gbeam.GetBSC(MaxOrder=3, save=False, Sampling=100)
        print('GaussianBeam beam BSC compute passed')


    def test02(self):
        global PWbeam
        PWbeam = PlaneWave(Wavelength = 0.632e-6, Polarization = 0)
        print('PlaneWave beam initialisation passed')


    def test03(self):
        PWbeam.GetBSC(MaxOrder=3, save=False)
        print('GaussianBeam beam BSC compute passed')


class QuantitativeTestCase(unittest.TestCase):

    def test00(self):
        Mesh = FibonacciMesh(MaxAngle    = pi,
                             Sampling    = 1000,
                             PhiOffset   = 0,
                             GammaOffset = 0)

        val0 = Scat.CrossSection(Mesh)
        val1 = Scat.Qsca * Scat.Area
        Rerror = np.abs(val0-val1)/val0
        assert Rerror < 1e-2
        print('Validation QSca - CrossSection passed')


    def test01(self):
        Detector1 = _Photodiode(Sampling = 500, NA = 2.0)
        val0      = Scat.EnergyFlow(Detector1.Mesh)
        val1      = Detector1.Coupling(Scat)
        error     = np.abs(val0-val1)/val0
        assert error < 1e-2
        print('Validation EnergyFlow - coupling passed')


    def test02(self):
        Source = PlaneWave(Wavelength = 1e-6)
        Csca = Sphere(Diameter = 1e-6, Index = 1.5, Source = Source).Csca
        assert np.isclose( Csca, 2.7349e-12, 0.001 )
        print('Validation scattering cross-section -> Scott Prahl')


    def test03(self):
        Source = PlaneWave(Wavelength = 1e-6)
        g = Sphere(Diameter = 1e-6, Index = 1.5, Source = Source).g
        assert np.isclose( g, 0.72924, 0.001 )
        print('Validation g = <cos> -> Scott Prahl')


    def test04(self):
        Source = PlaneWave(Wavelength = 1e-6)
        Cext = Sphere(Diameter = 1e-6, Index = 1.5 + 1j, Source = Source).Cext
        assert np.isclose( Cext, 2.1422e-12, 0.001 )
        print('Validation extinction sross-section -> Scott Prahl')



def suite():
    suite = unittest.TestSuite()
    suite.addTest(DetectorTestCase('test00'))
    suite.addTest(DetectorTestCase('test01'))
    suite.addTest(DetectorTestCase('test02'))
    suite.addTest(DetectorTestCase('test03'))
    suite.addTest(DetectorTestCase('test04'))
    suite.addTest(DetectorTestCase('test05'))

    suite.addTest(ScattererTestCase('test00'))
    suite.addTest(ScattererTestCase('test01'))
    suite.addTest(ScattererTestCase('test02'))
    suite.addTest(ScattererTestCase('test03'))
    suite.addTest(ScattererTestCase('test04'))
    suite.addTest(ScattererTestCase('test05'))
    suite.addTest(ScattererTestCase('test06'))
    suite.addTest(ScattererTestCase('test07'))
    suite.addTest(ScattererTestCase('test08'))
    suite.addTest(ScattererTestCase('test09'))
    suite.addTest(ScattererTestCase('test10'))
    suite.addTest(ScattererTestCase('test11'))
    suite.addTest(ScattererTestCase('test12'))
    suite.addTest(ScattererTestCase('test13'))
    suite.addTest(ScattererTestCase('test14'))

    suite.addTest(ExperiementTestCase('test00'))
    suite.addTest(ExperiementTestCase('test01'))
    suite.addTest(ExperiementTestCase('test02'))
    suite.addTest(ExperiementTestCase('test03'))
    suite.addTest(ExperiementTestCase('test04'))
    suite.addTest(ExperiementTestCase('test05'))
    suite.addTest(ExperiementTestCase('test06'))
    suite.addTest(ExperiementTestCase('test07'))
    suite.addTest(ExperiementTestCase('test08'))
    suite.addTest(ExperiementTestCase('test09'))

    suite.addTest(GLMTTestCase('test00'))
    suite.addTest(GLMTTestCase('test01'))
    suite.addTest(GLMTTestCase('test02'))
    suite.addTest(GLMTTestCase('test03'))

    suite.addTest(QuantitativeTestCase('test00'))
    suite.addTest(QuantitativeTestCase('test01'))
    suite.addTest(QuantitativeTestCase('test02'))
    suite.addTest(QuantitativeTestCase('test03'))
    suite.addTest(QuantitativeTestCase('test04'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

















# -

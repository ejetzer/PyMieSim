def run(Plot, Save):
    return
    import numpy as np
    from PyMieSim            import Material
    from PyMieSim.Scatterer  import Sphere
    from PyMieSim.Detector   import Photodiode, LPmode
    from PyMieSim.Source     import PlaneWave
    from PyMieSim.Experiment import ScatSet, SourceSet, Setup, DetectorSet

    DiameterList   = np.linspace(100e-9, 1000e-9, 200)

    Detector0 = Photodiode(NA                 = 0.1,
                         Sampling          = 300,
                         GammaOffset       = 20,
                         PhiOffset         = 0,
                         CouplingMode      = 'Centered')

    scatKwargs   = { 'Diameter'    : np.linspace(400e-9, 2000e-9, 200),
                     'Material'    : Material('BK7'),
                     'nMedium'     : [1] }

    sourceKwargs = { 'Wavelength'   : 1e-6,
                     'Polarization' : [0]}

    Detector0 = Photodiode(NA                = 2.0,
                           Sampling          = 300,
                           GammaOffset       = 0,
                           PhiOffset         = 0,
                           CouplingMode      = 'Centered')

    detecSet   = DetectorSet([Detector0])

    scatSet    = ScatSet(Scatterer = Sphere,  kwargs = scatKwargs )

    sourceSet  = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

    Experiment = Setup(ScattererSet = scatSet,
                       SourceSet    = sourceSet,
                       DetectorSet  = detecSet)

    # Metric can be "max"
    #               "min"
    #               "mean"
    #               "std+RI"
    #               "std+Diameter"
    #               "std+Polarization"
    #               "std+Wavelength"
    #               "std+Detector"
    #               "monotonic+RI"
    #               "monotonic+Diameter"
    #               "monotonic+Polarization"
    #               "monotonic+Wavelength"
    #               "monotonic+Detector"

    Opt = Experiment.Optimize(Setup           = Experiment,
                     Metric          = 'mean',
                     Parameter       = ['PhiOffset'],
                     Optimum         = 'Maximum',
                     MinVal          = [1e-5],
                     MaxVal          = [180],
                     WhichDetector   = 0,
                     X0              = [0.6],
                     MaxIter         = 350,
                     Tol             = 1e-4,
                     FirstStride     = 30)

    print(Opt.Result)

    df = Experiment.Coupling(AsType='dataframe')

    if Plot:
        df.Plot(y='Coupling', x='Diameter') # can be "Couplimg"  or  "STD"


if __name__ == '__main__':
    run(Plot=True, Save=False)

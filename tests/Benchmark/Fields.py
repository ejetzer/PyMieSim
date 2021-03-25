import matplotlib.pyplot as plt
import numpy as np
import timeit

from PyMieSim.Plots import PlotField
from PyMieSim.LMT.python.Sphere import Fields as PyField

from PyMieSim.LMT.Scatterer import SPHERE as SPHERELMT
from PyMieSim.GLMT.Scatterer import SPHERE as SPHEREGLMT


def Speed(setup):
    BenchPython = """PyField(*args0)"""

    GLMTLMTBenchPyBind = """A.sFields(Phi=Phi, Theta=Theta, R=1. );"""

    LMTClass = """A.sFields(Phi=Phi, Theta=Theta, R=1. ); """

    Bench = timeit.timeit(setup = setup,stmt = BenchPython, number = 1)
    print('\nLMT PYTHON BENCHMARK: ', Bench)

    Bench = timeit.timeit(setup = setup,stmt = LMTClass, number = 1)
    print('\n\n'+'='*50 + '\n\n LMT C++ class BENCHMARK', Bench)

    Bench = timeit.timeit(setup = setup,stmt = GLMTLMTBenchPyBind, number = 1)
    print('\n\n'+'='*50 + '\n\n GLMT C++ BENCHMARK', Bench)


def Correctness():
    Phi = np.linspace(-np.pi/2,np.pi/2,100);
    Theta = np.linspace(-np.pi,np.pi,100)

    THETA, PHI = np.meshgrid(Theta, Phi)

    args0 = (1.4, 10e-6, 1e-6, 1, Phi-np.pi/2, Theta-np.pi/2, 0,1,1)
    args1 = (1.4, 10e-6, 1e-6, 1, Phi, Theta, 0,1,1)
    args3 = (1.4, 10e-6, 1e-6, 1., 0, 1)

    PyParallel, PyPerpendicular = PyField(*args0);

    CppParallel, CppPerpendicular = SPHERELMT(*args3).SFields(Phi=Phi, Theta=Theta, R=1. );

    PlotField(Theta, Phi, CppParallel, CppPerpendicular)

    PlotField(Theta, Phi, PyParallel, PyPerpendicular)

    plt.show()



setup = """
import numpy as np
from PyMieSim.LMT.python.Sphere import Fields as PyField

from PyMieSim.Source import PlaneWave
from PyMieSim.LMT.Scatterer import SPHERELMT
from PyMieSim.GLMT.Scatterer import SPHEREGLMT

beam = PlaneWave(Wavelength=1e-6)
BSC = beam.GetBSC(MaxOrder=10)
Phi = np.linspace(-np.pi/2,np.pi/2,800); Theta = np.linspace(-np.pi,np.pi,800)

args0 = (1.4, 1e-6, 1e-6, 1, Phi, Theta, 0,1,1)
args1 = (1.4, 1e-6, 1e-6, 1, Phi, Theta, 0,1,1, beam._BSC_, beam.MaxOrder)
args2 = (1.4, 1e-6, 1e-6, 1., 0, 1)
A=SPHERELMT(*args2);
B=SPHEREGLMT(*args1);
"""

if __name__=='__main__':
    Speed(setup)
    Correctness()











    # -

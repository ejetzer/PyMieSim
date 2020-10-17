import matplotlib.pyplot as plt
import numpy as np

from miecoupling.src.classes.Fiber import fiber
from miecoupling.src.classes.Modes import mode
from miecoupling.src.classes.Scattering import Scatterer

from miecoupling.src.functions.couplings import PointFieldCoupling, MeanFieldCoupling



npts=101

Fiber = fiber(4.2e-6,
              1.4456,
              20.5e-6,
              1.4444)

Mode = mode(fiber=Fiber,
            LPmode=(1, 1),
            wavelength=400e-9,
            npts=npts,
            )

Mode.magnificate(magnification=2.)

#Mode.PlotFields()

Scat = Scatterer(diameter=500e-9,
                 wavelength=400e-9,
                 index=1.4,
                 npts=200,
                 ThetaBound=[-20,20],
                 PhiBound=[-20,20])



Scat.GenField(PolarizationAngle=0)

#Scat.PlotFields()

Scat.Field.PlotStokes(RectangleTheta=[-5,5], RectanglePhi=[-5,5])














# -

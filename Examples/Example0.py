
"""
_________________________________________________________
Scattering Parallel Field coupling with en-face LP01 mode
_________________________________________________________
"""

from miecoupling.src.classes.Fiber import fiber
from miecoupling.src.classes.Modes import mode
from miecoupling.src.classes.Scattering import Scatterer
from miecoupling.src.functions.couplings import PointFieldCoupling, MeanFieldCoupling



npts=201

Fiber = fiber(core_radius = 4.2e-6,
              core_index  = 1.4456,
              clad_radius = 20.5e-6,
              clad_index  = 1.4444)

LP01 = mode(fiber      = Fiber,
            LPmode     = (1, 1),
            wavelength = 400e-9,
            npts       = npts,
            )

Mode.PlotFields()

Scat = Scatterer(diameter    = 100e-9,
                 wavelength  = 400e-9,
                 index       = 1.4,
                 npts        = 200,
                 ThetaBound  = [-180,180],
                 ThetaOffset = 0,
                 PhiBound    = [-180,180],
                 PhiOffset   = 10)



Scat.PlotFields()

Scat.Field.PlotStokes(RectangleTheta=[-5,5], RectanglePhi=[-5,5])














# -

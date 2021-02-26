from PyMieSim.Source import GaussianBeam
import matplotlib.pyplot as plt
import numpy as np

beam = GaussianBeam(Wavelength=0.632e-6,
                    NA           = 0.8,
                    Polarization = 0)



angle, val = beam.Anm(20,15)

plt.plot(np.rad2deg(angle), val.real,'k')
plt.plot(np.rad2deg(angle), val.imag,'r--')
plt.grid()
plt.show()

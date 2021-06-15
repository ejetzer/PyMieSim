import numpy             as np
import matplotlib.pyplot as plt
from mayavi              import mlab

from PyMieSim.Plots       import StructuredAmplitude, StokesPlot, StructuredAbs
from PyMieSim.utils       import Direct2spherical, AngleUnit2DirectUnit
from PyMieSim.units       import Area
from PyMieSim.Directories import *


class Stokes(dict): # https://en.wikipedia.org/wiki/Stokes_parameters
    """Dict subclass representing scattering Far-field in the Stokes
    representation.
    | The stokes parameters are:
    |     I : Intensity of the fields
    |     Q : linear polarization parallel to incident polarization
    |     U : linear polarization 45 degree to incident polarization
    |     V : Circular polarization

    .. math:
        I &= \\big| E_x \big|^2 + \\big| E_y \\big|^2

        Q &= \\big| E_x \big|^2 - \\big| E_y \\big|^2

        U &= 2 \\mathcal{Re} \\big\{ E_x E_y^* \\big\}

        V &= 2 \\mathcal{Im} \\big\{ E_x E_y^* \\big\}

    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the Stokes parameters in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the Stokes parameters.

    Returns
    -------
    :class:`dict`
        Representation of Stokes parameters.

    """

    def __init__(self, Parent, Num=100, Distance=1.):


        self.Parent       = Parent

        Phi, Theta = np.linspace(-np.pi/2, np.pi/2, Num), np.linspace(-np.pi, np.pi, Num)

        self['Phi'], self['Theta'] = np.meshgrid(Phi, Theta)

        EPhi, ETheta = Parent.Bind.sFields(Phi = Phi, Theta=Theta, R=1.)

        self['I'] = np.abs(EPhi)**2 + np.abs(ETheta)**2

        self['Q'] = np.abs(EPhi)**2 - np.abs(ETheta)**2

        self['U'] = +2 * np.real(EPhi*ETheta.conjugate())

        self['V'] = -2 * np.imag(EPhi*ETheta.conjugate())


    def _Plot(self):
        Name = 'Scattering phase function'

        StokesPlot(I            = self['I'],
                   Q            = self['Q'],
                   U            = self['U'],
                   V            = self['V'],
                   Phi          = self['Phi'],
                   Theta        = self['Theta'],
                   Name         = 'Stokes Parameter',
                   Polarization = self.Parent.Source.Polarization.Radian)


    def Plot(self):
        self._Plot()

        mlab.show()


    def SaveFig(self, Directory):
        dir = os.path.join(ZeroPath, Directory) + '.png'

        print(f'Saving figure in {dir}...')

        self._Plot()

        mlab.savefig(dir)

        mlab.close(all=True)


    def __repr__(self):
        return f"""
        Object:          Dictionary
        Keys:            S1, S2, S3,, S4, Theta, Phi
        Structured data: Yes
        Method:          <Plot>
        Shape:           {self['S1'].shape}"""


class SPF(dict):
    """Dict subclass representing scattering phase function of SPF in short.
    The SPF is defined as:
    .. math::
        \\text{SPF} = E_{\\parallel}(\\phi,\\theta)^2 + E_{\\perp}(\\phi,\\theta)^2

    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the SPF in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the SPF.

    Returns
    -------
    :class:`dict`
        Representation of SPF.

    """

    def __init__(self, Parent, Num=100, Distance=1.):

        self.Parent = Parent

        Phi, Theta = np.linspace(-np.pi/2, np.pi/2, Num), np.linspace(-np.pi, np.pi, Num)

        self['Phi'], self['Theta'] = np.meshgrid(Phi, Theta)

        self['EPhi'], self['ETheta'] = Parent.Bind.sFields(Phi = Phi, Theta=Theta, R=1.)

        self['SPF'] = np.sqrt( self['EPhi'].__abs__()**2 + self['ETheta'].__abs__()**2 )


    def _Plot(self):

        StructuredAbs(Scalar       = self['SPF'],
                      Phi          = self['Phi'],
                      Theta        = self['Theta'],
                      Name         = 'Scattering phase function',
                      Polarization = self.Parent.Source.Polarization.Radian)



    def Plot(self):
        self._Plot()

        mlab.show()


    def SaveFig(self, Directory):
        dir = os.path.join(ZeroPath, Directory) + '.png'

        print(f'Saving figure in {dir}...')

        self._Plot()

        mlab.savefig(dir)

        mlab.close(all=True)


    def __repr__(self):
        return f"""
        Object:          Dictionary
        Keys:            SPF, EPhi, ETheta, Theta, Phi
        Structured data: Yes
        Method:          <Plot>
        Shape:           {self['Phi'].shape}"""



class S1S2(dict):
    """Dict subclass representing S1 and S2 function.
    S1 and S2 are defined as:

    .. math::
        S_1=\\sum\\limits_{n=1}^{n_{max}} \\frac{2n+1}{n(n+1)}(a_n \\pi_n+b_n \\tau_n)

        S_2=\\sum\\limits_{n=1}^{n_{max}}\\frac{2n+1}{n(n+1)}(a_n \\tau_n+b_n \\pi_n)


    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the S1 and S2 in spherical coord.

    Returns
    -------
    :class:`dict`
        Representation of S1 S2.

    """
    def __init__(self, Parent, Num):

        self.Parent = Parent

        self['Phi'] = np.linspace(0, 2*np.pi, Num)

        Phi = np.linspace(-np.pi,np.pi,Num);

        self['S1'], self['S2'] = Parent.Bind.S1S2(Phi = Phi)


    def _Plot(self):

        S1 = np.abs(self['S1'])
        S2 = np.abs(self['S2'])

        fig, axes = plt.subplots(nrows      = 1,
                                 ncols      = 2,
                                 figsize    = (7,4),
                                 subplot_kw = {'projection':'polar'})

        axes[0].set_title('S1 function'); axes[1].set_title('S2 function')

        axes[0].plot(self['Phi'], S1,  color = 'k')

        axes[0].fill_between(x     = self['Phi'],
                             y2    = 0,
                             y1    = S1,
                             color = 'C0',
                             alpha = 0.4)


        axes[1].plot(self['Phi'], S2, color = 'k')

        axes[1].fill_between(x     = self['Phi'],
                             y2    = 0,
                             y1    = S2,
                             color = 'C1',
                             alpha = 0.4)


    def Plot(self):
        self._Plot()

        plt.show()


    def SaveFig(self, Directory):
        dir = os.path.join(ZeroPath, Directory) + '.png'

        print(f'Saving figure in {dir}...')

        self._Plot()

        plt.savefig(dir)

        plt.close()


    def __repr__(self):
        return f"""
        Object:          Dictionary
        Keys:            S1, S2, Phi
        Structured data: Yes
        Method:          <Plot>
        Shape:           {self['Phi'].shape}"""




class ScalarFarField(dict):
    """Dict subclass representing scattering Far-field in a spherical
    coordinate representation.
    The Far-fields are defined as:

    .. math::
        \\text{Fields} = E_{||}(\\phi,\\theta)^2, E_{\\perp}(\\phi,\\theta)^2


    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the far-fields in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the far-fields.

    Returns
    -------
    :class:`dict`
        Representation of far-fields.

    """
    def __init__(self, Num = 200, Parent = None, Distance=1.):

        self.Parent = Parent

        Phi, Theta = np.linspace(-np.pi/2, np.pi/2, Num), np.linspace(-np.pi, np.pi, Num)

        self['Phi'], self['Theta'] = np.meshgrid(Phi, Theta)

        self['EPhi'], self['ETheta'] = Parent.Bind.sFields(Phi = Phi, Theta=Theta, R=1.)

        self['Distance'] = Distance

        self['SPF'] = np.sqrt( self['EPhi'].__abs__()**2 + self['ETheta'].__abs__()**2 )


    def _Plot(self):
        StructuredAmplitude(Scalar       = self['EPhi'],
                            Phi          = self['Phi'],
                            Theta        = self['Theta'],
                            Name         = u'E_φ',
                            Polarization = self.Parent.Source.Polarization.Radian)

        StructuredAmplitude(Scalar       = self['ETheta'],
                            Phi          = self['Phi'],
                            Theta        = self['Theta'],
                            Name         = u'E_θ',
                            Polarization = self.Parent.Source.Polarization.Radian)


    def Plot(self):
        self._Plot()

        mlab.show()


    def SaveFig(self, Directory):
        dir = os.path.join(ZeroPath, Directory) + '.png'

        print(f'Saving figure in {dir}...')

        self._Plot()

        mlab.savefig(dir)

        mlab.close(all=True)


    def __repr__(self):

        return f"""
        Object:          Dictionary
        Keys:            EPhi, ETheta, Theta, Phi, Distance
        Structured data: Yes
        Method:          <Plot>
        Shape:           {self['Theta'].shape}"""





class Footprint(dict):
    """Dict subclass representing footprint of the scatterer.
    The footprint usually depend on the scatterer and the detector.
    For more information see references in the
    `documentation <https://pymiesim.readthedocs.io/en/latest>`_
    The footprint is defined as:

    .. math::
        \\text{Footprint} = \\big| \\mathscr{F}^{-1} \\big\\{ \\tilde{ \\psi }\
        (\\xi, \\nu), \\tilde{ \\phi}_{l,m}(\\xi, \\nu)  \\big\\} \
        (\\delta_x, \\delta_y) \\big|^2


    Parameters
    ----------
    Scatterer : :class:`Scatterer`
        The scatterer.
    Detector : :class:`Detector`
        The detector.
    Num : :class:`int`
        Number of point to evaluate the footprint in cartesian coord.

    Returns
    -------
    :class:`dict`
        Representation of footprint.

    """
    def __init__(self, Scatterer, Detector, Num=100):

        x, y = np.mgrid[-50: 50: complex(Num), -50: 50: complex(Num)]

        MaxAngle = np.abs( np.pi/2 - Detector.Mesh.Phi.Radian.min() )

        Phi, Theta = Direct2spherical(X=x, Y=y, MaxAngle=MaxAngle)

        Direct = AngleUnit2DirectUnit(Phi, Scatterer.Source.k)

        FarFieldPara, FarFieldPerp = Scatterer.uS1S2(Phi.flatten(), Theta.flatten())

        Perp =  \
        Detector.FarField(Num=Num, Structured=True) * FarFieldPerp.reshape(Theta.shape)

        Para = \
        Detector.FarField(Num=Num, Structured=True) * FarFieldPara.reshape(Theta.shape)

        n = 5

        FourierPara = np.fft.ifft2(Para, s=[512*n, 512*n])

        FourierPara = np.fft.fftshift(FourierPara).__abs__()**2

        FourierPerp = np.fft.ifft2(Perp,  s=[512*n, 512*n])

        FourierPerp = np.fft.fftshift(FourierPerp).__abs__()**2

        Direct = np.linspace(np.min(Direct), np.max(Direct), FourierPerp.shape[0])

        self['Map'] = FourierPara + FourierPerp

        self['DirectX'] = Direct; self['DirectY'] = Direct



    def Plot(self):

        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.contourf(self['DirectX']*1e6, self['DirectY']*1e6, self['Map'], cmap='gray')

        ax.set_xlabel(r'Offset distance in X-axis [$\mu$m]')

        ax.set_ylabel(r'Offset distance in Y-axis [$\mu$m]')

        ax.set_title('Scatterer Footprint')

        plt.show()



    def __repr__(self):
        return f"""
        Object:          Dictionary
        Keys:            Map, DirectX, DirectY
        Structured data: Yes
        Method:          <Plot>
        Shape:           {self['Phi'].shape}"""





class ScatProperties(dict):
    """Dict subclass representing the basic properties of the scattere
    | Those properties are:
    |    Efficiencies:
    |        Qsca
    |        Qext
    |        Qabs
    |        Qback
    |        Qratio
    |        Qpr
    |    Cross-sections:
    |        Csca
    |        Cext
    |        Cabs
    |        Cback
    |        Cratio
    |        Cpr
    |    Others:
    |        area
    |        index
    |        g

    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.

    Returns
    -------
    :class:`dict`
        Scatterer properties.

    """
    def __init__(self, Parent):

        self.Parent       = Parent

        data = Parent.Bind.Efficiencies

        self['efficiencies'] = { 'Qsca'    : data[0],
                                 'Qext'    : data[1],
                                 'Qabs'    : data[2],
                                 'Qback'   : data[3],
                                 'Qratio'  : data[4],
                                 'Qpr'     : data[6]}

        self['cross-sections'] = { 'Csca'  : Area( data[0] * Parent.Area),
                                   'Cext'  : Area( data[1] * Parent.Area),
                                   'Cabs'  : Area( data[2] * Parent.Area),
                                   'Cback' : Area( data[3] * Parent.Area),
                                   'Cratio': Area( data[4] * Parent.Area),
                                   'Cpr'   : Area( data[6] * Parent.Area) }


        self['others'] = {'area'           : Parent.Area,
                          'index'          : Parent.Index }

        if Parent._Concentration is not None:

            self['others'].update( {
                                      'Concentration'  : Parent.Concentration,
                                      u'\u03bc sca'    : Parent.MuSca,
                                      u'\u03bc ext'    : Parent.MuExt,
                                      u'\u03bc abs'    : Parent.MuAbs,
                                      'g'              : data[6] } )

    def Plot(self):
        print('There is not plotting method for the properties representation. Try print')

    def __repr__(self):
        text= f"""
        Object:          Dictionary
        Keys:            Efficiencies, cross-sections, others
        Structured data: Yes
        Method:          <Plot>
        Shape:           {[7,1]}
        """
        text += "=" * 40 + '\n' + "-" * 70 + '\n'

        for n, (key, val) in enumerate( self['efficiencies'].items() ):
            if n == 0:
                text+= f"Efficiencies   | {key:15s}  | {val} \n" + "-" * 70 + '\n'
            else:
                text+= f"               | {key:15s}  | {val} \n" + "-" * 70 + '\n'


        for n, (key, val) in enumerate( self['cross-sections'].items() ):
            if n == 0:
                text+= f"cross-sections | {key:15s}  | {val} \n" + "-" * 70 + '\n'
            else:
                text+= f"               | {key:15s}  | {val} \n" + "-" * 70 + '\n'


        for n, (key, val) in enumerate( self['others'].items() ):
            if n == 0:
                text+= f"others         | {key:15s}  | {val} \n" + "-" * 70 + '\n'
            else:
                text+= f"               | {key:15s}  | {val} \n" + "-" * 70 + '\n'

        return text

# -

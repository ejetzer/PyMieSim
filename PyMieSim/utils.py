import itertools
import numpy           as np
from scipy.interpolate import griddata
from scipy             import ndimage
import re

import PyMieSim
from PyMieSim.Physics import Angle



def Norm(Scalar):
    return np.sqrt(np.sum(np.abs(Scalar)**2))


def Normalize(Scalar):
    return Scalar / Norm(Scalar)


def InterpFull(Meshes, Scalar, Shape):

    Phi, Theta = np.mgrid[-np.pi/2:np.pi/2:complex(Shape[0]),
                          -np.pi:np.pi:complex(Shape[1])]

    Scalar = interp_at(Meshes.Phi.Radian,
                       Meshes.Theta.Radian,
                       Scalar.astype(np.complex).flatten(),
                       Phi.flatten(),
                       Theta.flatten(),
                       algorithm='linear',
                       extrapolate=True)

    return Scalar.reshape(Shape), Phi, Theta


def RescaleComplex(Input, Scale):
    InputReal = ndimage.interpolation.zoom(input=Input.real, zoom=(Scale), order = 2)
    InputImag = ndimage.interpolation.zoom(input=Input.imag, zoom=(Scale), order = 2)
    return InputReal + 1j * InputImag


def RotateComplex(Input, Rotation):
    InputReal =  ndimage.rotate(Input.real, Rotation, reshape=False)
    InputImag =  ndimage.rotate(Input.imag, Rotation, reshape=False)
    return InputReal + 1j * InputImag


def interp_at(x, y, v, xp, yp, algorithm='cubic', extrapolate=False):
    """
    Interpolate data onto the specified points.

    Parameters:

    * x, y : 1D arrays
        Arrays with the x and y coordinates of the data points.
    * v : 1D array
        Array with the scalar value assigned to the data points.
    * xp, yp : 1D arrays
        Points where the data values will be interpolated
    * algorithm : string
        Interpolation algorithm. Either ``'cubic'``, ``'nearest'``,
        ``'linear'`` (see scipy.interpolate.griddata)
    * extrapolate : True or False
        If True, will extrapolate values outside of the convex hull of the data
        points.

    Returns:

    * v : 1D array
        1D array with the interpolated v values.

    """
    if algorithm not in ['cubic', 'linear', 'nearest']:
        raise ValueError("Invalid interpolation algorithm: " + str(algorithm))

    grid = griddata((x, y), v, (xp, yp), method=algorithm).ravel()

    if extrapolate and algorithm != 'nearest' and np.any(np.isnan(grid)):
        grid = extrapolate_nans(xp, yp, grid)
    return grid


def extrapolate_nans(x, y, v):
    """
    Extrapolate the NaNs or masked values in a grid INPLACE using nearest
    value.

    .. warning:: Replaces the NaN or masked values of the original array!

    Parameters:

    * x, y : 1D arrays
        Arrays with the x and y coordinates of the data points.
    * v : 1D array
        Array with the scalar value assigned to the data points.

    Returns:

    * v : 1D array
        The array with NaNs or masked values extrapolated.

    """
    if np.ma.is_masked(v):
        nans = v.mask
    else:
        nans = np.isnan(v)
    notnans = np.logical_not(nans)
    v[nans] = griddata((x[notnans], y[notnans]),
                        v[notnans],
                        (x[nans], y[nans]),
                        method='nearest').ravel()
    return v


def Angle2Direct(AngleVec: np.ndarray, k: float,) -> np.ndarray:

    RadSpace = np.deg2rad(AngleVec)

    FourierSpace = np.sin(RadSpace) * k / (2 * np.pi)

    fourier_unit = (FourierSpace[1] - FourierSpace[0]).__abs__()

    DirectSpace = np.fft.fftshift( np.fft.fftfreq( AngleVec.shape[0], d = fourier_unit ) )

    return DirectSpace



def Direct2Angle(DirectVec: np.ndarray, k: float) -> np.ndarray:

    direct_unit = (DirectVec[1] - DirectVec[0]).__abs__()

    FourierSpace = np.fft.fftshift( np.fft.fftfreq( DirectVec.shape[0], d = direct_unit ) )

    AngleVec = np.arcsin(2 * np.pi * FourierSpace / k) # conversion spatial frequency to angular space

    if np.isnan(AngleVec).any():
        raise Exception("Magnification too large.")

    return AngleVec * 180 / np.pi


def NA2Angle(NA: float) -> np.ndarray:
    if NA <=1.0: return Angle( np.arcsin(NA), unit='Radian')
    if NA >= 1.0: return Angle( np.arcsin(NA-1) + np.pi/2, unit='Radian')


def Direct2spherical(X, Y, MaxAngle):
    Z = 50 / np.tan(MaxAngle)

    _, Phi, Theta = Cart2Sp(X, Y, X*0+Z)

    return Phi, Theta

def Direct2Angle(X, Y, MaxAngle):
    MaxZ = np.max(X) / np.cos(MaxAngle)



def AngleUnit2DirectUnit(Angle, k):
    FourierSpace = np.sin(Angle) * k / (2 * np.pi)

    fourier_unit = (FourierSpace[1] - FourierSpace[0]).__abs__()

    DirectSpace = np.fft.fftshift( np.fft.fftfreq( Angle.shape[0], d = fourier_unit ) )

    return DirectSpace


def Cart2Sp(x,y,z):
    r = np.sqrt(x**2+y**2+z**2)
    theta = np.arcsin(z/r)
    phi = np.arctan2(y, x)
    return r, phi, theta


def Sp2Cart(r, phi, theta):
    x = r*np.cos(phi)*np.cos(theta)
    y = r*np.cos(phi)*np.sin(theta)
    z = r*np.sin(phi)
    return x,y,z


def mx_rot_x(gamma):
    """Returns rotational matrix for right-handed rotation
    around X axis.

    Args:
        gamma (scalar): Rotation angle around X in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.matrix([
        [1, 0, 0],
        [0, np.cos(gamma), -np.sin(gamma)],
        [0, np.sin(gamma), np.cos(gamma)]
    ])

def mx_rot_y(theta):
    """Returns rotational matrix for right-handed rotation
    around Y axis.

    Args:
        theta (scalar): Rotation angle around Y in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.matrix([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])



def mx_rot_z(phi):
    """Returns rotational matrix for right-handed rotation
    around Z axis.

    Args:
        phi (scalar): Rotation angle around Z in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.matrix([
        [np.cos(phi), -np.sin(phi), 0],
        [np.sin(phi), np.cos(phi), 0],
        [0, 0, 1]
    ])


def mx_apply(T, x, y, z):
    """Applies rotation to data using rotational matrix.

    Args:
        T (numpy.matrix): Rotational matrix.
        x (scalar or array_like): X-component of data.
        y (scalar or array_like): Y-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (x, y, z) of data in cartesian coordinates.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    scalar_input = False
    if x.ndim == 0 and y.ndim == 0 and z.ndim == 0:
        x = x[None]
        y = y[None]
        z = z[None]
        scalar_input = True
    x_ = T[0, 0]*x+T[0, 1]*y+T[0, 2]*z
    y_ = T[1, 0]*x+T[1, 1]*y+T[1, 2]*z
    z_ = T[2, 0]*x+T[2, 1]*y+T[2, 2]*z
    if scalar_input:
        return (x_.squeeze(), y_.squeeze(), z_.squeeze())
    return (x_, y_, z_)


def IO(text):
    txt = '\n' + '-' * 100 + '\n'
    txt += text
    txt += '\n' + '-' * 100
    return txt


def NearestIndex(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx



UlistLike = (list, np.ndarray, tuple)

def ToList(*args):
    out = []
    for arg in args:
        if not isinstance(arg, UlistLike): out.append( [arg] )
        else: out.append(arg)

    if len(out) == 1: return out[0]
    return out


def GeneratorFromDict(dictionnary):
    order = {a: n for n, a in enumerate(dictionnary.keys())}

    Generator = itertools.product( *( a for a in dictionnary.values() ) )


    for arguments in Generator:
        for n, key in enumerate( dictionnary.keys() ):
            order[key] = arguments[n]

        yield order


def _GeneratorFromDict(dictionnary):
    order = {a: n for n, a in enumerate(dictionnary.keys())}
    return itertools.product( *( a for a in dictionnary.values() ) ), order


def MergeDict(dict0, dict1):
    for key in dict1.keys():
        if key in dict0.keys() and key != 'name':
            dict0[key][dict1['name']] = dict1[key]


def FormatStr(function):
    def wrapped(*args, **kwargs):
        args = (re.sub(r"\s+", "", arg.lower() ) if isinstance(arg, str) else arg for arg in args)

        kwargs = {k: re.sub(r"\s+", "", v.lower() ) if isinstance(v, str) else v for k, v in kwargs.items()}

        return function(*args, **kwargs)
    return wrapped


def FormatString(string):
    return re.sub(r"\s+", "", string.lower() )



class Table:
    def __init__(self, lst0, lst1):
        assert len(set(lst0)) == len(lst0), 'Invalid input'
        assert len(set(lst1)) == len(lst1),  'Invalid input'
        self.lst0 = lst0
        self.lst1 = [element.lower() for element in lst1]


    @FormatStr
    def __getitem__(self, Val):
        assert Val in self.lst0 + self.lst1,  'Invalid input'
        if isinstance(Val, str):
            idx = self.lst1.index(Val)
            return self.lst0[idx]
        else:
            return self.lst1[Val]
# -

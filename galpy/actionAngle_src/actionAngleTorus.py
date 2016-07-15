###############################################################################
#      class: actionAngleTorus
#
#             Use McMillan, Binney, and Dehnen's Torus code to calculate (x,v)
#             given actions and angles
#
#
###############################################################################
import warnings
import numpy
from galpy.potential import MWPotential
from galpy.util import galpyWarning
import galpy.actionAngle_src.actionAngleTorus_c as actionAngleTorus_c
from galpy.actionAngle_src.actionAngleTorus_c import _ext_loaded as ext_loaded
from galpy.potential_src.Potential import _check_c
_autofit_errvals= {}
_autofit_errvals[-1]= 'something wrong with input, usually bad starting values for the parameters'
_autofit_errvals[-2]= 'Fit failed the goal by a factor <= 2'
_autofit_errvals[-3]= 'Fit failed the goal by more than 2'
_autofit_errvals[-4]= 'Fit aborted: serious problems occured'
class actionAngleTorus(object):
    """Action-angle formalism using the Torus machinery"""
    def __init__(self,*args,**kwargs):
        """
        NAME:
           __init__
        PURPOSE:
           initialize an actionAngleTorus object
        INPUT:
           pot= potential or list of potentials (3D)

           tol= default tolerance to use when fitting tori (|dJ|/J)

        OUTPUT:

           instance

        HISTORY:
           2015-08-07 - Written - Bovy (UofT)
        """
        if not 'pot' in kwargs: #pragma: no cover
            raise IOError("Must specify pot= for actionAngleTorus")
        self._pot= kwargs['pot']
        if self._pot == MWPotential:
            warnings.warn("Use of MWPotential as a Milky-Way-like potential is deprecated; galpy.potential.MWPotential2014, a potential fit to a large variety of dynamical constraints (see Bovy 2015), is the preferred Milky-Way-like potential in galpy",
                          galpyWarning)
        if ext_loaded:
            self._c= _check_c(self._pot)
            if not self._c:
                raise RuntimeError('The given potential is not fully implemented in C; using the actionAngleTorus code is not supported in pure Python')
        else:# pragma: no cover
            raise RuntimeError('actionAngleTorus instances cannot be used, because the actionAngleTorus_c extension failed to load')
        self._tol= kwargs.get('tol',0.003)
        return None
    
    def __call__(self,jr,jphi,jz,angler,anglephi,anglez,**kwargs):
        """
        NAME:
           __call__
        PURPOSE:
           evaluate the phase-space coordinates (x,v) for a number of angles on a single torus
        INPUT:
           jr - radial action (scalar)
           jphi - azimuthal action (scalar)
           jz - vertical action (scalar)
           angler - radial angle (array [N])
           anglephi - azimuthal angle (array [N])
           anglez - vertical angle (array [N])
           tol= (object-wide value) goal for |dJ|/|J| along the torus
        OUTPUT:
           [R,vR,vT,z,vz,phi]
        HISTORY:
           2015-08-07 - Written - Bovy (UofT)
        """
        out= actionAngleTorus_c.actionAngleTorus_xvFreqs_c(\
            self._pot,
            jr,jphi,jz,
            angler,anglephi,anglez,
            tol=kwargs.get('tol',self._tol))
        if out[9] != 0:
            warnings.warn("actionAngleTorus' AutoFit exited with non-zero return status %i: %s" % (out[9],_autofit_errvals[out[9]]),
                          galpyWarning)
        return numpy.array(out[:6]).T

    def xvFreqs(self,jr,jphi,jz,angler,anglephi,anglez,**kwargs):
        """
        NAME:
           xvFreqs
        PURPOSE:
           evaluate the phase-space coordinates (x,v) for a number of angles on a single torus as well as the frequencies
        INPUT:
           jr - radial action (scalar)
           jphi - azimuthal action (scalar)
           jz - vertical action (scalar)
           angler - radial angle (array [N])
           anglephi - azimuthal angle (array [N])
           anglez - vertical angle (array [N])
           tol= (object-wide value) goal for |dJ|/|J| along the torus
        OUTPUT:
           ([R,vR,vT,z,vz,phi],OmegaR,Omegaphi,Omegaz,AutoFit error message)
        HISTORY:
           2015-08-07 - Written - Bovy (UofT)
        """
        out= actionAngleTorus_c.actionAngleTorus_xvFreqs_c(\
            self._pot,
            jr,jphi,jz,
            angler,anglephi,anglez,
            tol=kwargs.get('tol',self._tol))
        if out[9] != 0:
            warnings.warn("actionAngleTorus' AutoFit exited with non-zero return status %i: %s" % (out[9],_autofit_errvals[out[9]]),
                          galpyWarning)
        return (numpy.array(out[:6]).T,out[6],out[7],out[8],out[9])

    def Freqs(self,jr,jphi,jz,**kwargs):
        """
        NAME:
           Freqs
        PURPOSE:
           return the frequencies corresponding to a torus
        INPUT:
           jr - radial action (scalar)
           jphi - azimuthal action (scalar)
           jz - vertical action (scalar)
           tol= (object-wide value) goal for |dJ|/|J| along the torus
        OUTPUT:
           (OmegaR,Omegaphi,Omegaz)
        HISTORY:
           2015-08-07 - Written - Bovy (UofT)
        """
        out= actionAngleTorus_c.actionAngleTorus_Freqs_c(\
            self._pot,
            jr,jphi,jz,
            tol=kwargs.get('tol',self._tol))
        if out[3] != 0:
            warnings.warn("actionAngleTorus' AutoFit exited with non-zero return status %i: %s" % (out[3],_autofit_errvals[out[3]]),
                          galpyWarning)
        return out

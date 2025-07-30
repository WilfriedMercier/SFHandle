#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
.. codeauthor:: Wilfried Mercier - LAM <wilfried.mercier@lam.fr>

Main part of the module that defines a SFH object to be manipulated.
'''

import numpy             as     np
from   numpy.typing      import NDArray, ArrayLike
from   scipy.interpolate import interp1d

import custom_types      as     ctypes

class SFH:
    r'''
    .. codeauthor:: Wilfried Mercier - LAM <wilfried.mercier@lam.fr>

    Class representing a SFH.

    :param lb_time: time steps in look-back time for the SFH
    :type lb_time: numpy.ndarray
    :param sfh: amplitude of the SFH (Msun/yr) at each time step
    :type lb_timsfh: numpy.ndarray
    :param err: error on the amplitude of the SFH (Msun/yr) at each time step
    :type err: numpy.ndarray
    '''

    def __init__(
        self, 
        lb_time : ArrayLike,
        sfh     : ArrayLike,
        err     : ArrayLike
    ) -> None:

        # Default values for the SFH
        self.lb_time = np.array(lb_time)
        self.sfh     = np.array(sfh)
        self.err     = np.array(err)

        # Interpolated values. They are set to an array when interpolate_sfh is called.
        self._interp_lb_time : NDArray | None = None
        self._interp_sfh     : NDArray | None = None
        self._interp_err     : NDArray | None = None

        return
    
    ##########################
    #       Properties       #
    ##########################
    
    @property
    def interp_lb_time(self) -> NDArray | None: 
        r'''High-resolution time array used for SFH interpolation.'''
        
        return self._interp_lb_time
    
    @property
    def interp_sfh(self) -> NDArray | None: 
        r'''Interpolated SFH to high-resolution time array.'''
        
        return self._interp_sfh

    @property
    def interp_err(self) -> NDArray | None: 
        r'''Interpolated error on the SFH amplitude to high-resolution time array.'''
        
        return self._interp_err

    @property
    def integral(self) -> ctypes.Numpy_float: 
        r'''Integral of the SFH in Msun'''
        
        # Duration of each bin in Myr
        tstep = (self.lb_time[::-1][:-1] - self.lb_time[::-1][1:])
        
        return np.nansum(self.sfh[::-1][:-1] * tstep) * 1e6

    #################################
    #            Methods            #
    #################################

    def interpolate_sfh(self, 
        lb_time      : ArrayLike,
        kind         : ctypes.Interp_kind = 'next',
        bounds_error : bool               = False,
        fill_value   : float              = 0.0,
        **kwargs
    ) -> tuple[NDArray, NDArray]:
        r'''
        Interpolate the SFH and its uncertainty on a new look-back time grid.
        
        .. important:

            By default ``kind`` is equal to ``"next"``. This is the correct interpolation type for non-parametric SFHs. Change this parameter only if you know what you are doing.

        :param lb_time: high-resolution look-back time array
        :type lb_time: numpy.ndarray or similar
        :param kind: type of interpolation
        :type kind: :py:class:`custom_types.Interp_kind`
        :param bool bounds_error: whether to throw an error if extrapolating or not
        :param float fill_value: value to use when extrapolating

        :returns: interpolated SFH and interpolated error on SFH amplitude
        :rtype: (numpy.ndarray, numpy.ndarray)
        '''

        # Store the high-resolution range of look-back time
        self._interp_lb_time = np.array(lb_time)

        # Interpolate SFH
        self._interp_sfh = self._interpolate(
            lb_time, self.lb_time, self.sfh,
            kind         = kind, 
            bounds_error = bounds_error, 
            fill_value   = fill_value,
            **kwargs
        )

        # Interpolate the error on the SFH
        self._interp_err = self._interpolate(
            lb_time, self.lb_time, self.err,
            kind         = kind, 
            bounds_error = bounds_error, 
            fill_value   = fill_value,
            **kwargs
        )

        return self.interp_sfh, self.interp_err # pyright: ignore[reportReturnType]

    @classmethod
    def _interpolate(cls,
        new_x        : ArrayLike,
        old_x        : ArrayLike,
        old_y        : ArrayLike,
        **kwargs
    ) -> NDArray:
        r'''
        Class method implementing a useful 1D interpolation using scipy.
        
        .. note:

            Interpolation is done on a function of the kind :math:`y = f(x)`

        :param new_x: new array used for interpolation
        :type new_x: numpy.ndarray or similar
        :param old_x: old x array defining the function
        :type old_x: numpy.ndarray or similar
        :param old_y: old y array defining the function
        :type old_x: numpy.ndarray or similar

        Keyword arguments
        -----------------
        :param kwargs: additional keywords that are passabled to :python:`scipy.interpolate.interp1d`

        :returns: interpolated function on `new_x`
        :rtype: numpy.ndarray
        '''

        return interp1d(old_x, old_y, **kwargs)(new_x)
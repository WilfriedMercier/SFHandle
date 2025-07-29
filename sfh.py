#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
.. codeauthor:: Wilfried Mercier - LAM <wilfried.mercier@lam.fr>

Main part of the module that defines a SFH object to be manipulated.
'''

import numpy             as     np
from   numpy.typing      import NDArray, ArrayLike
from   scipy.interpolate import interp1d

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
    
    @property
    def interp_lb_time(self): return self._interp_lb_time
    
    @property
    def interp_sfh(self): return self._interp_sfh

    @property
    def interp_err(self): return self._interp_err

    def interpolate_sfh(self, 
        lb_time      : ArrayLike,
        kind         : str   = 'next',
        bounds_error : bool  = False,
        fill_value   : float = 0.0,
        **kwargs
    ) -> tuple[NDArray, NDArray]:

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

        return interp1d(old_x, old_y, **kwargs)(new_x)
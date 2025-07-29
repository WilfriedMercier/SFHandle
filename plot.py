#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
.. codeauthor:: Wilfried Mercier - LAM <wilfried.mercier@lam.fr>

Plotting utilities for SFHs.
'''

import matplotlib.pyplot as     plt
from   matplotlib.axes   import Axes

# Local imports
from   sfh               import SFH

def plot_sfh(sfh : SFH) -> None:

    plt.figure(figsize=(10, 5))

    # Interpolated SFH
    plt.step(
        sfh.interp_lb_time,  # pyright: ignore[reportArgumentType]
        sfh.interp_sfh,  # pyright: ignore[reportArgumentType]
        color = 'firebrick', 
        ls    = '--'
    )

    plt.scatter(
        sfh.interp_lb_time,  # pyright: ignore[reportArgumentType]
        sfh.interp_sfh,   # pyright: ignore[reportArgumentType]
        c      = 'firebrick', 
        marker = 'x'
    )

    plt.fill_between(
        sfh.interp_lb_time, # pyright: ignore[reportArgumentType]
        sfh.interp_sfh - sfh.interp_err, # type: ignore
        sfh.interp_sfh + sfh.interp_err, # type: ignore
        edgecolor = 'firebrick', 
        facecolor = 'none',
        hatch     = '/',
        alpha     = 0.3,
        step      = 'pre'
    )

    # Original SFH
    plt.step(sfh.lb_time, sfh.sfh, color='k', where='pre')
    plt.scatter(sfh.lb_time, sfh.sfh, c='k', marker='o')
    
    plt.fill_between(
        sfh.lb_time,
        sfh.sfh - sfh.err,
        sfh.sfh + sfh.err,
        color = 'k',
        alpha = 0.3,
        step  = 'pre'
    )

    plt.xscale('log')
    plt.yscale('log')

    plt.ylabel(r'SFH [M$_{\odot}$ yr$^{-1}$]')
    plt.xlabel(r'Lookback time [Myr]')

    plt.show()

    return
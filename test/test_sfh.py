#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
.. codeauthor:: Wilfried Mercier - LAM <wilfried.mercier@lam.fr>

Test suite for the sfh.py module.
'''
import os
import sys
import astropy.table as     tab
import numpy         as     np
from   numpy.typing  import NDArray, ArrayLike

sys.path.append(os.path.abspath('.'))

import sfh
import utilities

class Test_SFH:
    r'''
    .. codeauthor:: Wilfried Mercier - LAM <wilfried.mercier@lam.fr>

    Test suite for the SFH class.
    '''

    def load_test_data(self) -> tab.Table:
        r'''Load a test data set.'''

        return tab.Table.read('test/test.csv')

    def load_sample(self) -> tuple[NDArray, NDArray, NDArray]:
        r'''Load a single entry in the test data set.'''

        data = self.load_test_data()
        return utilities.cigale_sfh(data[0]) # pyright: ignore[reportArgumentType]
        
    ###########################################
    #            Tests for methods            #
    ###########################################

    def test_constructor(self) -> None:
        r'''Test the creation of sfh data.'''

        res = self.load_sample()
        
        sfh.SFH(res[0], res[2], res[2])

        assert True

    def test__interpolate(self) -> None:
        r'''Test the interpolation of a step function.'''

        mysfh = sfh.SFH([], [], [])
        
        res   = mysfh._interpolate(
            [0, 0.5, 1],
            [0, 1],
            [0, 1],
            kind = 'next'
        )

        assert np.all(res == [0, 1, 1])

    def test_interpolate_sfh(self) -> None:
        r'''
        Test the interpolation of a simple SFH using the default parameters.
        '''

        mysfh = sfh.SFH([0, 1], [1, 2], [2, 3])
        res   = mysfh.interpolate_sfh([0, 0.5, 1, 1.5])

        assert (np.all(res[0] == [1, 2, 2, 0]) 
                and
                np.all(res[1] == [2, 3, 3, 0])
               )

    def test_interpolate_sfh_with_nan(self) -> None:
        r'''
        Test the interpolation of a simple SFH asking to extrapolate to NaN.
        '''

        mysfh = sfh.SFH([0, 1], [1, 2], [2, 3])
        res   = mysfh.interpolate_sfh(
            [0, 0.5, 1, 1.5],
            fill_value = np.nan
        )

        assert np.all(np.isnan([res[0][-1], res[1][-1]]))
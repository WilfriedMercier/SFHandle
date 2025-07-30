from   typing import Literal
import numpy  as     np

Interp_kind = Literal['linear', 
                      'nearest',
                      'nearest-up', 
                      'zero', 
                      'slinear', 
                      'quadratic', 
                      'cubic', 
                      'previous', 
                      'next'
                     ]

Numpy_float = np.float16 | np.float32 | np.float64 | np.float128
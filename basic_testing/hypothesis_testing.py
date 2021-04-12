from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays
import numpy as np

x = [0]

@given(arrays(dtype=float,
              shape=st.integers(min_value=10, max_value=100),
       elements=st.floats(allow_nan=False, allow_infinity=False)))
def test_arrays(arr):
    
    x[0] = arr
 
    assert np.all(arr.astype(int) % 10 == 0)

import numpy as np
import cupy as cp


squared_diff = cp.ElementwiseKernel(
   'float32 x, float32 y',
   'float32 z',
   'z = (x - y) * (x - y)',
   'squared_diff')

x = cp.arange(10, dtype=np.float32).reshape(2, 5)
y = cp.arange(5, dtype=np.float32)

print(x)
print(y)
print(squared_diff(x, y))

#[[0. 1. 2. 3. 4.]
# [5. 6. 7. 8. 9.]]
#[0. 1. 2. 3. 4.]
#[[ 0.  0.  0.  0.  0.]
# [25. 25. 25. 25. 25.]]

squared_diff_generic = cp.ElementwiseKernel(
    'T x, T y',
    'T z',
    'z = (x - y) * (x - y)',
    'squared_diff_generic')

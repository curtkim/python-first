import math
import cupy as cp
import numpy as np

l2norm_kernel = cp.ReductionKernel(
    'T x',  # input params
    'T y',  # output params
    'x * x',  # map
    'a + b',  # reduce
    'y = sqrt(a)',  # post-reduction map
    '0',  # identity value
    'l2norm'  # kernel name
)
x = cp.arange(5, dtype=np.float32).reshape(1, 5)

print(x)
print(l2norm_kernel(x, axis=1))
print( math.sqrt(0*0 + 1*1 + 2*2 + 3*3 + 4*4))
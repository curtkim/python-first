# nvprof --print-gpu-trace python examples/stream/cublas.py
import cupy

# without stream
x = cupy.array([1, 2, 3])
y = cupy.array([[1], [2], [3]])
expected = cupy.matmul(x, y)
cupy.cuda.Device().synchronize()

# with stream
stream = cupy.cuda.stream.Stream()
with stream:
    z = cupy.matmul(x, y)
stream.synchronize()
cupy.testing.assert_array_equal(z, expected)

# use stream
stream = cupy.cuda.stream.Stream()
stream.use()
z = cupy.matmul(x, y)
stream.synchronize()
cupy.testing.assert_array_equal(z, expected)

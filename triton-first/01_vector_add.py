import torch
import triton.language as tl
import triton


@triton.jit
def _add(
    X,  # *Pointer* to first input vector
    Y,  # *Pointer* to second input vector
    Z,  # *Pointer* to output vector
    N,  # Size of the vector
    **meta  # Optional meta-parameters for the kernel
):
    pid = tl.program_id(0)
    # Create an offset for the blocks of pointers to be
    # processed by this program instance
    offsets = pid * meta['BLOCK'] + tl.arange(0, meta['BLOCK'])
    # Create a mask to guard memory operations against
    # out-of-bounds accesses
    mask = offsets < N
    # Load x
    x = tl.load(X + offsets, mask=mask)
    y = tl.load(Y + offsets, mask=mask)
    # Write back x + y
    z = x + y
    tl.store(Z + offsets, z)


def add(x, y):
    z = torch.empty_like(x)
    N = z.shape[0]
    # The SPMD launch grid denotes the number of kernel instances that run in parallel.
    # It is analogous to CUDA launch grids. It can be either Tuple[int], or Callable(metaparameters) -> Tuple[int]
    grid = lambda meta: (triton.cdiv(N, meta['BLOCK']), )
    # NOTE:
    #  - each torch.tensor object is implicitly converted into a pointer to its first element.
    #  - `triton.jit`'ed functions can be index with a launch grid to obtain a callable GPU kernel
    #  - don't forget to pass meta-parameters as keywords arguments
    _add[grid](x, y, z, N, BLOCK=1024)
    # We return a handle to z but, since `torch.cuda.synchronize()` hasn't been called, the kernel is still
    # running asynchronously at this point.
    return z


torch.manual_seed(0)
size = 98432
x = torch.rand(size, device='cuda')
y = torch.rand(size, device='cuda')
za = x + y
zb = add(x, y)
print(za)
print(zb)
print(f'The maximum difference between torch and triton is ' f'{torch.max(torch.abs(za - zb))}')

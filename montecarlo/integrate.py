import math
import random

def gaussian(x: float) -> float:
    return math.exp(-x*x)

def monteCarloIntegrator(a: float, b:float, n:int) -> float:
    s = 0.0
    for i in range(n):
        ui = random.random()
        xi = a + (b-a)*ui
        s += gaussian(xi)

    return (b-a) / n * s

n = 1_000_000
print(monteCarloIntegrator(-20, 20, n))


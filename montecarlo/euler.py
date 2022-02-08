import random
import math

experiments = 1_000_000
acc = 0

for i in range(0, experiments):
    sum = 0.0
    num2success = 0

    while sum <= 1:
        n = random.random()
        sum += n
        num2success += 1

    acc += num2success


expected = acc / experiments
print(expected)
print(math.e)

def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a+b

for i, num in enumerate(fib()):
    print(num, i)
    if i >= 10:
        break
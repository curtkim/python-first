import concurrent.futures
import math
import threading
import time

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    print(threading.get_ident())

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    start = time.perf_counter()
    for number in PRIMES:
        print('[%s] %d is prime: %s' % (threading.get_ident(), number, is_prime(number)))
    end = time.perf_counter() - start
    print(f"---> (took {end:0.2f} seconds).")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        start = time.perf_counter()
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('[%s] %d is prime: %s' % (threading.get_ident(), number, prime))
        end = time.perf_counter() - start
        print(f"---> (took {end:0.2f} seconds).")

    '''
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('[%s] %d is prime: %s' % (threading.get_ident(), number, prime))
    end = time.perf_counter() - start
    print(f"---> (took {end:0.2f} seconds).")
    '''

if __name__ == '__main__':
    main()
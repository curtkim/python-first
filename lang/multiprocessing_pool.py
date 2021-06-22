import multiprocessing


def square(x):
    return x * x


def add(a, b):
    return a + b


if __name__ == '__main__':
    # Pool 객체 초기화
    pool = multiprocessing.Pool()
    # pool = multiporcessing.Pool(processes=4)

    # starmap
    outputs_startmap = pool.starmap(add, [(1, 2), (3, 4)])
    print(outputs_startmap)


    # Pool.map
    inputs = [0, 1, 2, 3, 4]
    outputs = pool.map(square, inputs)
    print(outputs)

    # Pool.map_async
    outputs_async = pool.map_async(square, inputs)
    outputs = outputs_async.get()
    print(outputs)

    # Pool.apply_async
    results_async = [pool.apply_async(square, [i]) for i in range(10)]
    results = [r.get() for r in results_async]
    print(results)
import time
import random
import ray


ray.init(num_cpus = 4)

@ray.remote
def do_some_work(x):
    time.sleep(random.uniform(0,4))
    return x

def process_results(results):
    sum = 0
    for x in results:
        time.sleep(1)
        sum += x
    return sum

start = time.time()
data_list = ray.get([do_some_work.remote(x) for x in range(4)])
sum = process_results(data_list)
print(f"duration = {time.time() - start}, result = {sum}")


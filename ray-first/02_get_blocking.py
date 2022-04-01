import time
import ray

ray.init(num_cpus = 4)

@ray.remote
def do_some_work(x):
    time.sleep(1)
    return x


start = time.time()
results = [ray.get(do_some_work.remote(x)) for x in range(4)]
print(f"duration = {time.time() - start}, results = {results}")


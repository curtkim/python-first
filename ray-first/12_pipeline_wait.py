import time
import random
import ray


ray.init(num_cpus = 4)

@ray.remote
def do_some_work(x):
    time.sleep(random.uniform(0,4))
    return x

def process_incremental(sum, result):
    time.sleep(1)
    return sum + result


start = time.time()
result_ids = [do_some_work.remote(x) for x in range(4)]
sum = 0

while len(result_ids):
    done_id, result_ids = ray.wait(result_ids)
    sum = process_incremental(sum, ray.get(done_id[0]))

print(f"duration = {time.time() - start}, result = {sum}")


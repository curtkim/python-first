import time

def do_some_work(x):
    time.sleep(1)
    return x

start = time.time()
results = [do_some_work(x) for x in range(4)]
print(f"duration = {time.time() - start}, results = {results}")


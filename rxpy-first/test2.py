import multiprocessing
import random
import time
from threading import current_thread

from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops
import rx


optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

lidar1 = rx.interval(1)
lidar2 = rx.interval(1)
lidar3 = rx.interval(1)

gps = rx.interval(0.1)


lidar1.pipe(
    ops.with_latest_from(lidar2, lidar3, gps.pipe(ops.buffer(lidar1))),
    #ops.observe_on(pool_scheduler)
).subscribe(
    on_next=lambda v: print("PROCESS 3: {0} {1}".format(current_thread().name, v)),
    on_error=lambda e: print(e),
)

input('press enter to exit\n')

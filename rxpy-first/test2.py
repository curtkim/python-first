import multiprocessing
import random
import time
from threading import current_thread

from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops
import rx

class FrameData:

    def __init__(self, l1, l2, l3, gps_list):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.gps_all = gps_list
        self.gps = gps_list[-1]
        self.lidar_all = None


optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

lidar1 = rx.interval(1)
lidar2 = rx.interval(1)
lidar3 = rx.interval(1)

gps = rx.interval(0.1)

def decision(v):
    [guide, lidar_all, gps_list, lidar_localized_pos, obstacles] = v
    way_points = []
    return (guide, lidar_all, way_points)

def control(v):
    [guide, lidar_all, way_points] = v
    acc = 0.0
    handle = 0.0
    return (acc, handle, guide, lidar_all, way_points)

def compose_lidar(v):
    [l1, l2, l3, l1_pair, gps_list] = v
    return (l1, l2, l3)

def doit(v):
    [l1, l2, l3, l1_pair, gps_list] = v
    print("PROCESS 3: {0} {1} {2} {3} {4} {5}".format(current_thread().name, l1, l2, l3, l1_pair, gps_list))

lidar1.pipe(
    ops.with_latest_from(lidar2, lidar3, lidar1.pipe(ops.pairwise()), gps.pipe(ops.buffer(lidar1))),
    #ops.map()
    #ops.observe_on(pool_scheduler)
).subscribe(doit)

input('press enter to exit\n')

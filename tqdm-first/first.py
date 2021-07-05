from tqdm import tqdm
from time import sleep

#              진행 < 남은   초당 iteration수
# ... 100/100 [00:10<00:00,  9.96it/s]
for i in tqdm(range(100)):
    sleep(0.1)



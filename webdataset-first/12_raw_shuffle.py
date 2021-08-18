import webdataset as wds

my_iter = wds.shuffle(iter([1, 2, 3, 4, 5]))

for item in my_iter:
    print(item)

from shapely.geometry.polygon import LinearRing
ring = LinearRing([(0, 0, 0), (1, 1, 0), (1, 0 ,0)])
print(ring.length)

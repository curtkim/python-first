a = list('abcdefgh')
print('Middle two:', a[3:5])
print('All but ends:', a[1:7])
assert a[:5] == a[0:5]
assert a[5:] == a[5:len(a)]

b = a[:]
assert b==a and b is not a


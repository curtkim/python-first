import clifford as cf

layout, blades = cf.Cl(2)
e1 = blades['e1']
e2 = blades['e2']
e12 = blades['e12']

print(e1 * e2)
print(e1 | e2)
print(e1 ^ e2)

# Reflection
a = e1+e2
n = e1
print(-n * a * n.inv())   # reflect 'a' in hyperplane normal to 'n'


# Rotation
from math import e, pi
R = e**(pi / 4 * e12)       # rotation by pi/2
print(R)

print(R * e1 * ~R)          # rotate e1 by pi/2 in the e12 plnae


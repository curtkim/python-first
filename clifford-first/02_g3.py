import math
import clifford as cf


layout, blades = cf.Cl(3)

e1 = blades['e1']
e2 = blades['e2']

locals().update(blades)

print(e3)
print(e123)

print(e1^e2^e3)

A = 1 + 2*e1 + 3*e12 + 4*e123
print(A)

# Reversion
print(~A)

# Grade Projection
print(A(0))
print(A(1))
print(A(2))

# Magnitude
print(abs(A)**2)

# Inverse
print(A.inv() * A)

print(A.inv())

# Dual
a= 1*e1 + 2*e2 + 3*e3
print(a.dual())


# Pretty, Ugly
cf.ugly()
print(A.inv())

cf.pretty(precision=2)
print(A.inv())


# Reflections
c = e1 + e2 + e3
n = e1
print('reflection', n*c*n)

# Rotations
R = math.e**(-math.pi / 4 * e12)
print("rotate e1 by pi/2 in the e12-plane", R*e1*~R)


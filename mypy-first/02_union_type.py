from typing import Union


Number = Union[float, int]

def union_add(x: Number, y: Number) -> Number:
   return x + y


x1: int = 5
y1: int = 2
print(union_add(x1, y1))
# 7

x2: float = 3.14
y2: float = 3.14
print(union_add(x2, y2))
# 6.28

x3: str = "2"
y3: str = "1"
print(union_add(x3, y3))


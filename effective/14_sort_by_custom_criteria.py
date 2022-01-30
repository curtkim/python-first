class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool {self.name!r}, {self.weight}'

tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25)
]

print('Unsorted', tools)
tools.sort(key=lambda x: x.name)
print('sorted', tools)


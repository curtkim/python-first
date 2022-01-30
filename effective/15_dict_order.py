baby_names = {
    'cat': 'kitten',
    'dog': 'puppy',
}

print(baby_names)


def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

my_func(goose='gosling', kangaroo='joey')


class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'

a = MyClass()
for k, v in a.__dict__.items():
    print(f'{k} = {v}')


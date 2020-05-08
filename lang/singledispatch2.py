from functools import singledispatch
from dataclasses import dataclass


@dataclass
class Cat:
    genus: str
    species: str


@dataclass
class Dog:
    genus: str
    species: str


@singledispatch
def process(obj=None):
    raise NotImplementedError("Implement process for bucket")


@process.register(Cat)
def sub_process(obj):
    # processing cat
    return "Cat data has been processed successfully!"


@process.register(Dog)
def sub_process(obj):
    # processing dog
    return "Dog data has been processed successfully!"


if __name__ == "__main__":
    cat_obj = Cat(genus="Felis", species="catus")
    dog_obj = Dog(genus="Canis", species="familiaris")

    print(process(cat_obj))
    print(process(dog_obj))
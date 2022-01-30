car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)

oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

oldest, *others, youngest = car_ages_descending
print(oldest, others, youngest)

car_inventory = {
    'donwtown': ('Silver Shadow', 'Pinto', 'DMC'),
    'Airport': ('Skiline', 'Viper', 'Nova'),
}

((loc1, (best1, *rest1)), 
 (loc2, (best2, *rest2))) = car_inventory.items()

print(f'{loc1} is {best1}, {rest1}')
print(f'{loc2} is {best2}, {rest2}')


short_list = [1,2]
first, second, *rest = short_list
print(first, second, rest)
assert rest == []


# iterator
first, second = iter(range(1,3))
print(f'{first} and {second}')


# generator
def generate_csv():
    yield ('Data', 'Make', 'Model', 'Year', 'Price')
    yield (1, 2, 3, 4, 5)

it = generate_csv()
header, *rows = it
print('CSV header', header)
print('Row count: ', len(rows))


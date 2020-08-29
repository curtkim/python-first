# 1) *argv
def test_var_args(f_arg, *argv):
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv:", arg)

print(1)
test_var_args('yasoob', 'python', 'eggs', 'test')

# 2) **kwargs
def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} = {1}".format(key, value))

print(2)
greet_me(name="yasoob", age=10)


# 3) with args
def test_args_kwargs(arg1, arg2, arg3):
    print("arg1:", arg1)
    print("arg2:", arg2)
    print("arg3:", arg3)

print(3)
args = ("two", 3, 5)
test_args_kwargs(*args)

# 4) with **kwargs
print(4)
kwargs = {"arg3": 3, "arg2": "two", "arg1": 5}
test_args_kwargs(**kwargs)
def coro():
    hello = yield "Hello"
    print(f"{hello} in coro")
    yield hello

c = coro()
print(next(c))
print(c.send("World"))
from rx import of, operators as op

source = of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

composed = source.pipe(
    op.map(lambda s: len(s)),
    op.filter(lambda i: i >= 5)
)
composed.subscribe(lambda value: print("Received {0}".format(value)))
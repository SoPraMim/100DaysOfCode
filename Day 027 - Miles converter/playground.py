def add(**args):
    print(type(args))
    total = 0
    for n in args:
        total += n
    return total

print(add(test=1, test2=2))
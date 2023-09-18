def addNumbers(tal1, tal2, *args):
    return tal1 + tal2 + sum(args)

#print(addNumbers(1))
print(addNumbers(1, 2))
print(addNumbers(1, 2, 3))
print(addNumbers(1, 2, 3, 4))
print(addNumbers(1, 2, 3, 4, 5))
print(addNumbers(1, 2, 3, 4, 5, 6))
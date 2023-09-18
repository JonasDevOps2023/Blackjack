def minimum(numbers):
    smallest = numbers[0]
    for number in numbers:
        if number < smallest:
            smallest = number
    return smallest

def minsta(nummer):
    return min(nummer)

numbers = [5, 2, 7, 4, 9]
print(minimum(numbers))
print(minsta(numbers))
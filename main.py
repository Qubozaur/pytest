def func(x):
    return x + 1


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def is_even(n):
    return n % 2 == 0


def greet(name):
    if not name:
        raise ValueError("name cannot be empty")
    return f"Hello, {name}!"


def reverse_string(s):
    return s[::-1]


def max_of_three(a, b, c):
    return max(a, b, c)


def sum_list(numbers):
    if not numbers:
        return 0
    return sum(numbers)


def find_in_list(items, target):
    if target not in items:
        raise LookupError(f"{target} not found")
    return items.index(target)

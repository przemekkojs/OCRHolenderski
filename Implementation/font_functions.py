def fibonacci(n:int) -> int:
    n += 5
    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a - 2

def linear(n:int) -> int:
    n += 3
    return 2 * n
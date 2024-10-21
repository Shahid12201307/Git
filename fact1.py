def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Example Usage
print(factorial_iterative(5))  # Output: 120

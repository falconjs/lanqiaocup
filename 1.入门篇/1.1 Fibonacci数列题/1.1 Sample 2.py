# Example 1

n = int(input())

Fib = [1 for i in range(n + 1)]

k = 3

while k <= n:
    Fib[k] = (Fib[k - 1] + Fib[k - 2]) % 10007  # Wrong

    k += 1

print(Fib[n])

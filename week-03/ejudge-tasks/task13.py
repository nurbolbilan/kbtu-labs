nums = list(map(int, input().split()))

primes = list(filter(lambda x: x > 1 and all(x % i != 0 for i in range(2, x)), nums))

if not primes:
    print("No primes")
else:
    print(*primes)
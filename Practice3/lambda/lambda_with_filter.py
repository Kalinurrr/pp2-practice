numbers = [1,2,3,4,5,6,7,8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

numbers = [3,5,-3,2,-7,-12,34,-5]
positive = list(filter(lambda x : x > 0, numbers))
print(positive)

arr = [3,4,1,5,6,3,7,8,4,9]
divbythree =list(filter(lambda x : x % 3 == 0, arr))
print(divbythree)

ns = list(map(int, input().split()))
primes = list(filter(lambda x : x >=2 and all(x % i != 0 for i in range(2,x)), ns))
print(primes)
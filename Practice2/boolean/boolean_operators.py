x = 5
print(x > 0 and x < 10)

x = 5
print(x < 5 or x > 10)

x = 5
print(not(x > 3 and x < 10))


x = ["apple", "banana"]
y = ["apple", "banana"]
z = x
print(x is z)
print(x is y)
print(x == y)

x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)
print(x is y)
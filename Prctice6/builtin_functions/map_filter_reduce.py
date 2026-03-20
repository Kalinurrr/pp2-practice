from functools import reduce

numbers = [1,2,3,4,5,6]
#map()
squared = list(map(lambda x: x*x,numbers))
print("Squared using map:", squared)

#filter()
even_ones = list(filter(lambda x: x%2 == 0,numbers))
print("Evens using filter:", even_ones)

#reduce()
total = reduce(lambda x, y: x+y,numbers)
print("Sum using reduce:", total)

# Other useful built-in functions
print("Length:", len(numbers))
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Sum:", sum(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))



fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)



for i in range(1, 6):
    if i == 3:
        continue
    print(i)


for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)


text = "Hello World"

for char in text:
    if char == " ":
        continue
    print(char)



numbers = [4, -2, 7, -5, 10]

for num in numbers:
    if num < 0:
        continue
    print(num)

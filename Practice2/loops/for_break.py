fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  


fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

for i in range(1, 10):
    if i == 5:
        break
    print(i)


numbers = [2, 4, 6, 8, 10]

for num in numbers:
    if num == 8:
        break
    print(num)



for i in range(100):
    word = input("Type something (exit to stop): ")
    if word == "exit":
        break
    print(word)

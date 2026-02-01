i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1


i = 1
while i <= 10:
    if i == 5:
        break
    print(i)
    i += 1

while True:
    word = input("Type something (stop to end): ")
    if word == "stop":
        break
    print(word)

numbers = [2, 4, 6, 8, 10]
i = 0
while i < len(numbers):
    if numbers[i] == 8:
        break
    print(numbers[i])
    i += 1


i = 0
while True:
    if i == 3:
        break
    print("Loop running")
    i += 1

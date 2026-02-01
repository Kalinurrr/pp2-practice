print(10 > 9)
print(10 == 9)
print(10 < 9)

# Boolean variables
is_student = True
is_teacher = False

print(is_student)   # True
print(is_teacher)   # False


x = "Hello"
y = 15
print(bool(x))
print(bool(y))

bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])


bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")
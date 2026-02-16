class Person:
  def __init__(self, name):
    self.name = name
  def greet(self):
    print("Hello, my name is " + self.name)
p1 = Person("Emil")
p1.greet()


class Calculator:
  def add(self, a, b):
    return a + b
  def multiply(self, a, b):
    return a * b
calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))

class Rectangle:
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def area(self):
    return self.width * self.height
  
r1 = Rectangle(5, 3)

print(r1.area())
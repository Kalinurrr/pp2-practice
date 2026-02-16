class Student:
    school = "KBTU"   # class variable

s1 = Student()
s2 = Student()

print(s1.school)
print(s2.school)


class Car:
    wheels = 4

c1 = Car()
c2 = Car()

Car.wheels = 6

print(c1.wheels)
print(c2.wheels)



class Dog:
    species = "Animal"   # class variable

    def __init__(self, name):
        self.name = name  # instance variable

d1 = Dog("Bob")
d2 = Dog("Max")

print(d1.species, d1.name)
print(d2.species, d2.name)



class Phone:
    brand = "Apple"

p1 = Phone()
p2 = Phone()

p1.brand = "Samsung"

print(p1.brand)
print(p2.brand)

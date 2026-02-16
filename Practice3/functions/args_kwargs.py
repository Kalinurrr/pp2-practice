def my_function(*kids):
    print("The youngest child is", kids[2])
my_function("Emil", "Tobias", "Linus")

#def my_function(*args): args-is tuple
    #print(type(args))

def my_function(*args):
    print("Type:", type(args))
    print("First:", args[0])
    print("Second:", args[1])
    print("All:", args)
my_function("Emil", "Tobias", "Linus")

def my_func(greeting, *names):
    for name in names:
        print(greeting, name)
my_func("Hello", "Kalinur","Aman","Aidyn")


def sum_is(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total
print(sum_is(1,2,3))
print(sum_is(10,20,30,40))
print(sum_is(5))


def find_max(*numbers):
    if len(numbers) == 0:
        return None
    max = numbers[0]
    for num in numbers:
        if num > max: max = num
    return max
print(find_max(3,7,2,9,1))


def find_min(*numbers):
    if len(numbers) == 0:
        return None
    min = numbers[0]
    for num in numbers:
        if num < min: min = num
    return min
print(find_min(3,6,5,8,1))




def my_function(**kid):
    print("His last name is " + kid["lname"])
my_function(fname="Tobias", lname="Refsnes")

def my_function(**kid):
    print("His first name is " + kid["fname"])
my_function(fname="Tobias", lname="Refsnes")


def my_function(**myvar):
    print("Type:", type(myvar))
    print("Name:", myvar["name"])
    print("Age:", myvar["age"])
    print("All data:", myvar)
my_function(name="Tobias", age=30, city="Bergen")

def my_function(username, **details):
    print("Username:", username)
    print("Additional details:")
    for key, value in details.items():
        print(" ", key + ":", value)
my_function("emil123", age=25, city="Oslo", hobby="coding")

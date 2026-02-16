x = lambda a : a + 10
print(x(5))

x = lambda a, b : a *b
print(x(5,6))

x = lambda a,b,c : a + b +c
print(x(5,6,2))

x = lambda a : a * a
print(x(4))

def myfunc(n):
    return lambda a : a * n
mydoubler = myfunc(2) #n
print(mydoubler(11)) #a

def myfunc(n):
    return lambda a : a * n
mytripler = myfunc(3)
print(mytripler(11))


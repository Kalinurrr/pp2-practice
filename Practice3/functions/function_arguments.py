def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus")


def my_function(name):   # name is PARA
    print("Hello", name)
my_function("Emil")      # "Emil" is ARG

#numberofarg
def my_function(fname, lname):
    print(fname + " " + lname)
my_function("Emil", "Refsnes")






def my_function(name = "friend"):
  print("Hello", name)
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

def my_function(country = "Norway"):
  print("I am from", country)
my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")
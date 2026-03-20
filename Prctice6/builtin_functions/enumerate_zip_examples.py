names = ["Ali", "Dana", "Mira"]
scores = [85, 90, 78]

# enumerate()
print("Using enurmate:")
for index, name in enumerate(names, start=1):
    print(index,name)

# zip()
print("Using zip:")
for name, score in zip(names, scores):
    print(f"{name} -> {score}")

#Type checking
value = "123"
print("Type of value:", type(value))
print("Is value a string?", isinstance(value, str))

# Type conversions
number_int = int(value)
number_float = float(value)
text_value = str(456)
letters_list = list("hello")
numbers_tuple = tuple([1, 2, 3])

print("\nConverted to int:", number_int)
print("Converted to float:", number_float)
print("Converted to str:", text_value)
print("Converted to list:", letters_list)
print("Converted to tuple:", numbers_tuple)
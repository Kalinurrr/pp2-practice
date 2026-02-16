numbers = [1,2,3,4,5]
doubled = list(map(lambda x : x *2, numbers ))
print(doubled)

arr = list(map(int, input().split()))
tripled = list(map(lambda x : x * 3, arr))
print(tripled)

data = ["10", "20", "30"]
nums = list(map(lambda x: int(x), data))
print(nums)

names = input().split()

upper_names = list(map(lambda x: x.upper(), names))
print(upper_names)
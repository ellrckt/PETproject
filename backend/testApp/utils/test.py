# def repeat(n):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             print('BEFORE')
#             func(*args,**kwargs)
#             print("AFTER")
#             print(n)
#         return wrapper
#     return decorator

# @repeat(3)
# def prib(name: str):
#     print(f"HI {name}")

# prib("danik")


# a = [1,2,3]
# i = iter(a)
# print(next(i))
# print(next(i))
# print(next(i))
# print(next(i))

# class Counter:

#     current: int
#     def __init__(self,current):
#         self.current = current

#     def __iter__(self):
#         return self

#     def __next__(self):
#         self.current += 1
#         return self.current

# c = Counter(0)
# a = iter(c)

# print(next(a))
# print(next(a))
# print(next(a))
# print(next(a))


# def gen():
#     yield 1

# a = gen()

# print(next(a))
# print(next(a))


a = {i: i for i in range(5) if i % 2 == 0}
print(a)

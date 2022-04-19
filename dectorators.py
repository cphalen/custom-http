# this small example clarifies Python wrappers which we will use
# in the custom HTTP server

# wrappers take in a function and perform some pre-processing or
# post-processing, in this case we turn the function result into a string
def stringify(f) -> str:
    def inner(*args):
        return str(f(*args))
    return inner

def return_10():
    return 10

@stringify
def return_10_string():
    return 10

@stringify
def add_one(v: int) -> int:
    return v + 1

def append(postfix: str) -> str: #  params passed to decorator
    def decorator(f): # actual function
        def wrapper(*args): # params passed to function
            return f(*args) + postfix
        return wrapper
    return decorator

@append("world!")
def return_hello_world(v: str):
    return "hello "

print(return_hello_world("hello ")) # prints "hello world!"
print(return_10(), type(return_10())) # prints 10 <int>
print(return_10_string(), type(return_10_string())) # prints 10 <str>
print(add_one(10), type(add_one(10))) # prints 11 <str>
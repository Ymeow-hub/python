from functools import wraps

def mock(value):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return value
        return wrapper
    return decorator

@mock(value='☆*:.｡.o(≧▽≦)o.｡.:*☆')
def f1(x, y, z):
    return x + y + z

@mock(value='сори, не судьба')
def f2(z, y):
    return z * y

print(f1(1, 2, 3)) 
print(f2(9, 1))  

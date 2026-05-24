def my_wraps(func):
    def decorator(wrapper):
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper
    return decorator

def trace(f):
    @my_wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        print(f'{f.__name__}, arguments: {args}, kwargs: {kwargs}, res: {res}')
        return res
    return wrapper

@trace
def say_hi():
    print('hi')

print(say_hi.__name__)
print(say_hi.__doc__)
print(say_hi.__module__)
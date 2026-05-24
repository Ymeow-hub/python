from warnings import warn
from functools import wraps

def deprecated(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        warn("Dont use me i am outdated!!!", UserWarning)
        return func(*args,**kwargs)
    return wrapper
@deprecated
def f(i) :
    return i

print(f(3))
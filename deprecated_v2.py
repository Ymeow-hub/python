from warnings import warn
from functools import wraps

def deprecated(message):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            warn(message, UserWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapped
    return decorator

@deprecated('Ne nado menya ispolzovat pliz')
def f(i):
    return i

print(f(1))
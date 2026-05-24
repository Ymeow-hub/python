from functools import singledispatch

@singledispatch
def func(x):
    print('im not implemented!!')

@func.register
def _(x: int):
    print(x, 'int')

@func.register
def _(x: str):
    print(x, 'string')

func(1)
func('meowmeow')
func([])
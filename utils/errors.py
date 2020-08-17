from typing import NoReturn


def raise_type(argument_name: str, expected_type: type, real_type: type) -> NoReturn:
    # NOTE maybe change to
    # TypeError: int() argument must be a string, a bytes-like object or a number, not 'list'
    raise TypeError(f'expected {argument_name} to be {expected_type}, got {real_type} instead')

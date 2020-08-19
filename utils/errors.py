from typing import NoReturn


def raise_type(argument_name: str, expected_type: type, real_type: type) -> NoReturn:
    # TODO accept multiple expected types
    raise TypeError(f'expected {argument_name} to be {expected_type}, got {real_type} instead')

from typing import NoReturn, Tuple, Union


def raise_type(argument_name: str, expected_type: Union[type, Tuple[type, ...]], real_type: type) -> NoReturn:
    raise TypeError(f'expected {argument_name} to be {expected_type}, got {real_type} instead')

from configparser import ConfigParser
from tests.func.Libraries.helper.decorators import checkargs


@checkargs
def get_ini_as_dict(path: str, section: str) -> dict:
    config: ConfigParser = ConfigParser()
    config.read(path)
    user_input = config.items(section)

    return dict(user_input)


@checkargs
def combine_dict_values(key_dict: dict, val_dict: dict) -> dict:
    """Combines values of two dict's equal keys into new dictionary.

    The passed dictionaries are compared to one another.
    If both contain an equal key, a new key value pair is created using
    the associated value of the :param:key_dict as key and the associated
    value of the :param:val_dict as value.
    This new key-value pair is added to the returned dictionary.

    Therefor, the maximum length of the returned dict cannot exceed the
    length of the shortest passed in dictionary. If no match is found,
    the returned dictionary will be empty.

    :param dict key_dict: values of matching keys are used as keys for
    resulting dictionary
    :param dict val_dict: values of matching keys are used as values for
    resulting dictionary
    """

    result = {}

    for key, value in key_dict.items():
        if key in val_dict:
            result[value] = val_dict[key]

    return result


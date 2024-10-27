from gendiff.parser import read
from gendiff.format.stylish import get_stylish
from gendiff.format.plain import get_plain
from gendiff.format.json import get_json


FORMAT = {
    'stylish': get_stylish,
    'plain': get_plain,
    'json': get_json,
}


def generate_diff(file_1, file_2, format='stylish'):
    first_dict = read(file_1)
    second_dict = read(file_2)
    diff = build_diff(first_dict, second_dict)

    return FORMAT[format](diff)


def build_diff(data_1, data_2):
    combine = sorted(data_1.keys() | data_2.keys())
    return [get_node(key, data_1, data_2) for key in combine]


def get_node(key, data_1, data_2):
    val_1 = data_1.get(key)
    val_2 = data_2.get(key)

    match (key in data_1, key in data_2, val_1, val_2):
        case (True, False, _, _):
            return dict_diff('removed', key, val_1)
        case (False, True, _, _):
            return dict_diff('added', key, val_2)
        case (True, False, val_1, _) if is_dict(val_1):
            return dict_diff('nested', key, build_diff(val_1))
        case (False, True, _, val_2) if is_dict(val_2):
            return dict_diff('nested', key, build_diff(val_2))
        case (True, True, val_1, val_2):
            if val_1 == val_2:
                return dict_diff('unchanged', key, val_1)
            elif is_dict(val_1) and is_dict(val_2):
                return dict_diff(
                    'nested', key, build_diff(val_1, val_2)
                )
            return dict_diff('updated', key, val_1, val_2)


def is_dict(val):
    return isinstance(val, dict)


def dict_diff(type_, key, val_1, val_2=None):
    diff_dict = {
        'type': type_,
        'key': key,
    }
    if type_ == 'nested':
        diff_dict['children'] = val_1
    else:
        diff_dict['val_1'] = val_1

    if type_ == 'updated':
        diff_dict['val_2'] = val_2

    return diff_dict

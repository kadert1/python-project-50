import itertools


SYMBOLS = {
    'unchanged': '  ',
    'removed': '- ',
    'changed': '+ ',
    'added': '+ ',
    'nested': '  '
}


def format_dict(dict_, depth):
    indent = " "
    formatted_lines = []
    for key, value in dict_.items():
        current_indent = indent * (depth * 2 + 2)
        formatted_lines.append(
            f"{current_indent}{key}: "
            f"{format_val(value, depth + 2)}"
        )
        closer_indent = indent * ((depth - 1) * 2)
    result = itertools.chain("{", formatted_lines, [closer_indent + "}"])
    return '\n'.join(result)


def format_val(val, depth=0):
    if isinstance(val, bool):
        if val:
            return 'true'
        else:
            return 'false'
    elif isinstance(val, dict):
        return format_dict(val, depth)
    else:
        if val is None:
            return 'null'
        else:
            return val


def get_stylish(diffs, replace=' ', spaces=2):

    def inner(current, depth):
        deep_indent = replace * (depth * spaces)
        lines = []
        for diff in current:
            key = diff.get('key')
            val_1 = diff.get('val_1')
            val_2 = diff.get('val_2')
            status = SYMBOLS.get(diff['type'])
            match diff['type']:
                case 'unchanged' | 'removed' | 'added':
                    lines.append(
                        f"{deep_indent}{status}{key}: "
                        f"{format_val(val_1, depth + spaces)}"
                    )
                case 'updated':
                    lines.append(
                        f"{deep_indent}{SYMBOLS['removed']}{key}: "
                        f"{format_val(val_1, depth + spaces)}"
                    )
                    lines.append(
                        f"{deep_indent}{SYMBOLS['added']}{key}: "
                        f"{format_val(val_2, depth + spaces)}"
                    )
                case 'nested':
                    lines.append(
                        f"{deep_indent}{status}{key}: "
                        f"{inner(diff['children'], depth + spaces)}"
                    )
                case _:
                    raise ValueError(f"Unknown type: {diff['type']}")
        closer_indent = replace * ((depth - 1) * spaces)
        result = itertools.chain("{", lines, [closer_indent + "}"])
        return '\n'.join(result)

    return inner(diffs, 1)

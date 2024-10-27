def format_val(val):
    if isinstance(val, bool):
        if val:
            return 'true'
        else:
            return 'false'
    elif isinstance(val, dict):
        return '[complex value]'
    elif val is None:
        return 'null'
    else:
        if isinstance(val, str):
            return f"'{val}'"
        else:
            return val


def get_plain(diffs, path=''):
    lines = []
    for diff in diffs:
        key = diff.get('key')
        val_1 = format_val(diff.get('val_1'))
        val_2 = format_val(diff.get('val_2'))
        current = ""
        if path:
            current = f"{path}.{key}"
        else:
            current = key
        match diff['type']:
            case 'unchanged': continue
            case 'added':
                lines.append(
                    f"Property '{current}' was added with value: {val_1}"
                )
            case 'removed':
                lines.append(
                    f"Property '{current}' was removed"
                )
            case 'updated':
                lines.append(
                    f"Property '{current}' was updated. "
                    f"From {val_1} to {val_2}"
                )
            case 'nested':
                lines.append(
                    get_plain(diff['children'], current)
                )
            case _:
                raise ValueError(f"Unknown type: {diff['type']}")
    return '\n'.join(lines)

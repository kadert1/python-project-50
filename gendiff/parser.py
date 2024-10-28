import yaml
import json
from pathlib import Path


def extension(file_path):
    return Path(file_path).suffix


def read(file_path, encoding='utf-8'):
    extens = extension(file_path)
    with open(file_path, 'r', encoding=encoding) as file:
        data = file.read()
    return parse_(data, extens)


def parse_(data, file_extens):
    parsers = {
        '.json': lambda data: json.loads(data),
        '.yml': lambda data: yaml.load(data, Loader=yaml.FullLoader),
        '.yaml': lambda data: yaml.load(data, Loader=yaml.FullLoader),
    }
    if file_extens in parsers:
        return parsers[file_extens](data)
    raise ValueError(f'Unsupported file extension - {file_extens}')

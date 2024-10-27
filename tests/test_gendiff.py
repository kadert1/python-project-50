import pytest
from gendiff import generate_diff
from pathlib import Path


def fixture_path(file_name):
    return Path(__file__).parent / 'fixtures' / file_name


def read_file(file_path):
    with open(file_path, encoding='utf8') as file:
        return file.read()


@pytest.mark.parametrize("file_name_1, file_name_2, format, expected", [
    ('file_3.json', 'file_4.json', 'plain', 'plain_result.txt'),
    ('file_1.yaml', 'file_2.yaml', 'plain', 'plain_result.txt'),
    ('file_3.json', 'file_4.json', 'json', 'json_result.txt'),
    ('file_1.yaml', 'file_2.yaml', 'json', 'json_result.txt'),
    ('file_1.json', 'file_2.json', 'stylish', 'usually_result.txt'),
    ('file_3.yaml', 'file_4.yaml', 'stylish', 'usually_result.txt'),
    ('file_3.json', 'file_4.json', 'stylish', 'stylish_result.txt'),
    ('file_1.yaml', 'file_2.yaml', 'stylish', 'stylish_result.txt')
])
def test_gendiff(file_name_1, file_name_2, format, expected):
    file_1 = fixture_path(file_name_1)
    file_2 = fixture_path(file_name_2)
    result = read_file(fixture_path(expected))
    assert generate_diff(file_1, file_2, format) == result

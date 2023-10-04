# reader.py

import csv
from collections.abc import Iterable
from typing import List, Union


def read_csv_as_dicts(
    filename: str, types: List[type], headers: Union[List[str], None] = None
) -> List[dict]:
    """
    Read CSV data into a list of dictionaries with optional type conversion
    """
    file = open(filename)
    return csv_as_dicts(file, types, headers)


def read_csv_as_instances(
    filename: str, cls: type, headers: Union[List[str], None] = None
) -> List[type]:
    """
    Read CSV data into a list of instances
    """
    file = open(filename)
    return csv_as_instances(file, cls, headers)


def csv_as_dicts(
    lines: Iterable[str], types: List[type], headers: Union[List[str], None] = None
) -> List[dict]:
    """
    Convert CSV data into a list of dictionaries with optional type conversion
    """
    return convert_csv(
        lines,
        lambda headers, row: {
            name: func(val) for name, func, val in zip(headers, types, row)
        },
        headers,
    )


def csv_as_instances(
    lines: Iterable[str], cls: type, headers: Union[List[str], None] = None
) -> List[type]:
    """
    Convert CSV data into a list of instances
    """
    return convert_csv(lines, lambda headers, row: cls.from_row(row), headers)


def convert_csv(lines, func, headers=None):
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    return list(map(lambda row: func(headers, row), rows))


def parse_line(line):
    try:
        name, val = line.split("=", 2)
        return (name, val)
    except ValueError:
        return None

import collections.abc
import csv
from sys import intern


def read_csv_as_dicts(filename, coltypes):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            records.append(
                {name: func(val) for name, func, val in zip(headers, coltypes, row)}
            )
    return records


def read_csv_as_instances(filename, cls):
    """
    Read a CSV file into a list of instances
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        _headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records


def read_csv_as_columns(filename, types):
    data = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        data = [list() for _ in range(len(headings))]
        for row in rows:
            for i, (func, val) in enumerate(zip(types, row)):
                if func == str:
                    func = intern
                data[i].append(func(val))
    return DataCollection(headings, data)


class DataCollection(collections.abc.Sequence):
    def __init__(self, headings, data):
        self.headings = headings
        self.data = data

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.data[0])

    def __getitem__(self, index):
        if isinstance(index, int):
            record = []
            for i in range(len(self.headings)):
                record.append(self.data[i][index])
            return dict(zip(self.headings, record))
        elif isinstance(index, slice):
            slice_output = []
            for idx in range(*index.indices(len(self.data[0]))):
                record = []
                for i in range(len(self.headings)):
                    record.append(self.data[i][idx])
                slice_output.append(dict(zip(self.headings, record)))
            return slice_output

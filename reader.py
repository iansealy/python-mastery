import collections.abc
import csv
from abc import ABC, abstractmethod
from sys import intern


class CSVParser(ABC):
    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return {name: func(val) for name, func, val in zip(headers, self.types, row)}


class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


def read_csv_as_dicts(filename, coltypes):
    parser = DictCSVParser(coltypes)
    return parser.parse(filename)


def read_csv_as_instances(filename, cls):
    """
    Read a CSV file into a list of instances
    """
    parser = InstanceCSVParser(cls)
    return parser.parse(filename)


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

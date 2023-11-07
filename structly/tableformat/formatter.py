from abc import ABC, abstractmethod


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


from .formats.csv import CSVTableFormatter
from .formats.html import HTMLTableFormatter
from .formats.text import TextTableFormatter


def create_formatter(format, column_formats=None, upper_headers=False):
    if format == "txt" or format == "text":
        cls = TextTableFormatter
    elif format == "csv":
        cls = CSVTableFormatter
    elif format == "html":
        cls = HTMLTableFormatter

    if column_formats:

        class cls(ColumnFormatMixin, cls):
            formats = column_formats

    if upper_headers:

        class cls(UpperHeadersMixin, cls):
            pass

    return cls()


def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)

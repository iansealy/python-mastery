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


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(" ".join("%10s" % h for h in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, rowdata):
        print(" ".join("%10s" % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join(str(d) for d in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr>", " ".join("<th>" + h + "</th>" for h in headers), "</tr>")

    def row(self, rowdata):
        print("<tr>", " ".join("<td>" + str(d) + "</td>" for d in rowdata), "</tr>")


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

from ..formatter import TableFormatter


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr>", " ".join("<th>" + h + "</th>" for h in headers), "</tr>")

    def row(self, rowdata):
        print("<tr>", " ".join("<td>" + str(d) + "</td>" for d in rowdata), "</tr>")

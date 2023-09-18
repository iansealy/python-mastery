# readrides.py

import collections.abc
import csv


def read_rides_as_tuples(filename):
    """
    Read the bus ride data as a list of tuples
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        _headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_dicts(filename):
    """
    Read the bus ride data as a list of dictionaries
    """
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        _headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                "route": route,
                "date": date,
                "daytype": daytype,
                "rides": rides,
            }
            records.append(record)
    return records


def read_rides_as_objects(filename):
    """
    Read the bus ride data as a list of objects
    """

    class Row:
        def __init__(self, route, date, daytype, rides):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides

    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        _headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_namedtuples(filename):
    """
    Read the bus ride data as a list of named tuples
    """
    from collections import namedtuple

    Row = namedtuple("Row", ["route", "date", "daytype", "rides"])

    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        _headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_objects_with_slots(filename):
    """
    Read the bus ride data as a list of objects with slots
    """

    class Row:
        __slots__ = ["route", "date", "daytype", "rides"]

        def __init__(self, route, date, daytype, rides):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides

    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        _headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_columns(filename):
    """
    Read the bus ride data into 4 lists, representing columns
    """
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        _headings = next(rows)  # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


class RideData(collections.abc.Sequence):
    def __init__(self):
        # Each value is a list with all of the values (a column)
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        if isinstance(index, int):
            return {
                "route": self.routes[index],
                "date": self.dates[index],
                "daytype": self.daytypes[index],
                "rides": self.numrides[index],
            }
        elif isinstance(index, slice):
            slice_output = []
            for idx in range(*index.indices(len(self.routes))):
                slice_output.append(
                    {
                        "route": self.routes[idx],
                        "date": self.dates[idx],
                        "daytype": self.daytypes[idx],
                        "rides": self.numrides[idx],
                    }
                )
            return slice_output

    def append(self, d):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append(d["rides"])


if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    rows = read_rides_as_tuples("Data/ctabus.csv")
    print("Memory Use: Current %d, Peak %d (tuple)" % tracemalloc.get_traced_memory())
    tracemalloc.stop()

    tracemalloc.start()
    rows = read_rides_as_tuples("Data/ctabus.csv")
    print("Memory Use: Current %d, Peak %d (dict)" % tracemalloc.get_traced_memory())
    tracemalloc.stop()

    tracemalloc.start()
    rows = read_rides_as_objects("Data/ctabus.csv")
    print("Memory Use: Current %d, Peak %d (object)" % tracemalloc.get_traced_memory())
    tracemalloc.stop()

    tracemalloc.start()
    rows = read_rides_as_namedtuples("Data/ctabus.csv")
    print(
        "Memory Use: Current %d, Peak %d (named tuple)"
        % tracemalloc.get_traced_memory()
    )
    tracemalloc.stop()

    tracemalloc.start()
    rows = read_rides_as_objects_with_slots("Data/ctabus.csv")
    print(
        "Memory Use: Current %d, Peak %d (object with slots)"
        % tracemalloc.get_traced_memory()
    )
    tracemalloc.stop()

    tracemalloc.start()
    rows = read_rides_as_columns("Data/ctabus.csv")
    print("Memory Use: Current %d, Peak %d (columns)" % tracemalloc.get_traced_memory())
    tracemalloc.stop()

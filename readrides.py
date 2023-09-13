# readrides.py

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
    records = []
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

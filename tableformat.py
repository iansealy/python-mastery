def print_table(portfolio, fields):
    print(" ".join(f"{f:>10}" for f in fields))
    print(("-" * 10 + " ") * len(fields))
    for s in portfolio:
        attrs = (getattr(s, name) for name in fields)
        print(" ".join(f"{attr:>10}" for attr in attrs))

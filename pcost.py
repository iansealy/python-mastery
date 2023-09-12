# pcost.py

import sys


def portfolio_cost(file):
    cost = 0.0

    with open(file, "r") as f:
        for line in f:
            name, shares, price = line.split()
            try:
                cost += int(shares) * float(price)
            except ValueError as e:
                print("Couldn't parse: %s\nReason: %s" % (repr(line), e))

    return cost


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python pcost.py file")
    print(portfolio_cost(sys.argv[1]))

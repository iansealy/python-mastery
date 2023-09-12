# pcost.py

import sys


def pcost(file):
    cost = 0.0

    with open(file, "r") as f:
        for line in f:
            name, shares, price = line.split()
            cost += int(shares) * float(price)

    print(cost)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python pcost.py file")
    pcost(sys.argv[1])

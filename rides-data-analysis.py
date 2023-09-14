from collections import Counter

import readrides

rides = readrides.read_rides_as_objects_with_slots("Data/ctabus.csv")

routes = {ride.route for ride in rides}
print("1: ", len(routes))

print(
    "2: ",
    sum(
        ride.rides for ride in rides if ride.route == "21" and ride.date == "02/02/2011"
    ),
)

total = Counter()
for ride in rides:
    total[ride.route] += ride.rides
print("3:")
for route in sorted(total):
    print(route, total[route])

increase = Counter()
for ride in rides:
    if ride.date.endswith("/2001"):
        increase[ride.route] -= ride.rides
    if ride.date.endswith("/2011"):
        increase[ride.route] += ride.rides
print("4: ", ",".join([route for route, _count in increase.most_common(5)]))

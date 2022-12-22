import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "[{},{}]".format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __add__(self, o):
        return Vector(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vector(self.x - o.x, self.y - o.y)

    def add(self, other):
        return self + other

    def add_x(self, x_val: int):
        return self.add(Vector(x_val, 0))

    def add_y(self, y_val: int):
        return self.add(Vector(0, y_val))

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Grid:
    def __init__(self, start_x, stop_x, start_y, stop_y, initialize_with='.'):
        self.size_x = stop_x - start_x + 1
        self.size_y = stop_y - start_y + 1
        self.start_x = start_x
        self.stop_x = stop_x
        self.start_y = start_y
        self.stop_y = stop_y
        self.grid = []

        self.offset = Vector(start_x, start_y)

        for x in range(self.size_x):
            self.grid.append([initialize_with] * self.size_y)

    def reset(self, character='.'):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.set_value(Vector(i, j), character)

    def x_range(self):
        return range(self.start_x, self.stop_x + 1)

    def y_range(self):
        return range(self.start_y, self.stop_y + 1)

    def show(self):
        # print the top header
        print()
        for r in [2, 1, 0]:
            # print 4 blanks
            print(" " * 6, end="")
            for c in range(self.size_x):
                c_offset = c + self.offset.x
                # determine if the digit is visible
                if c_offset == 0 and r > 0:
                    print("|", end="")
                elif abs(c_offset) >= 10 ** r or (c_offset == 0 and r == 0):
                    # print("{}".format(math.floor(c_offset / 10 ** r)), end="")
                    print("{}".format(math.floor((abs(c_offset) % (10 ** (r + 1))) / 10 ** r)), end="")
                else:
                    print(" ", end="")
            print()

        for j in range(self.size_y):
            print("{}".format(abs(j + self.offset.y)).rjust(5, '-' if j + self.offset.y == 0 else ' '), end="")
            print(" ", end="")
            for i in range(self.size_x):
                print(self.get_value(Vector(i, j) + self.offset), end="")
            print()

    def dot(self, v: Vector, char='#'):
        # print(" > drawing dot at {}".format(v))
        self.set_value(v, char)

    def path(self, vectors: [Vector], char='#'):
        if len(vectors) == 1:
            self.dot(vectors[0], char)
        for i in range(len(vectors) - 1):
            # print("path {} {} -> {}".format(i, vectors[i], vectors[i + 1]))
            self.line(vectors[i], vectors[i + 1])

    def line(self, start_vector: Vector, end_vector: Vector, char='#'):
        # we only do straight lines:
        if start_vector.x == end_vector.x:
            for y in range(abs(end_vector.y - start_vector.y) + 1):
                self.dot(start_vector.add_y(y if end_vector.y > start_vector.y else -y), char)

        if start_vector.y == end_vector.y:
            # print("got here {}".format(end_vector.x - start_vector.x))
            for x in range(abs(end_vector.x - start_vector.x) + 1):
                # print("and here")
                self.dot(start_vector.add_x(x if end_vector.x > start_vector.x else -x), char)

    def get_value(self, vector: Vector):
        vector = vector - self.offset
        if self.contains(vector):
            return self.grid[vector.x][vector.y]
        else:
            return '.'

    def set_value(self, vector: Vector, val):
        vector = vector - self.offset
        if self.contains(vector):
            self.grid[vector.x][vector.y] = val

    def contains(self, vector: Vector):
        return 0 <= vector.x < self.size_x and 0 <= vector.y < self.size_y

    def count(self, character):
        c = 0
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.grid[x - self.offset.x][y - self.offset.y] == character:
                    c += 1
        return c


class Sensor:
    def __init__(self, position: Vector, beacon_position: Vector):
        self.position = position
        self.beacon_position = beacon_position
        self.sensor_range = position.dist(beacon_position)
        self.seen = False

    def in_range(self, other: Vector):
        return self.position.dist(other) <= self.sensor_range

    def matches_beacon(self, other: Vector):
        return self.beacon_position.dist(other) == 0

    def matches_self(self, other: Vector):
        return self.position.dist(other) == 0

    def get_outer_edges(self):
        edges = []
        # walk the outside edge of the beacon's range
        # y goes from -range to range
        # x = range - y
        new_range = self.sensor_range + 1
        for y in range(-new_range, new_range):
            x = new_range - abs(y)
            edges.append(self.position + Vector(x, y))
            edges.append(self.position + Vector(x, -y))

        return edges


def get_sensors(filename='input.txt'):
    sensors = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            sx, sy, bx, by = line \
                .replace("Sensor at", "") \
                .replace(": closest beacon is at ", ", ") \
                .replace(" x=", "") \
                .replace(" y=", "") \
                .split(",")
            sensors.append(Sensor(Vector(int(sx), int(sy)), Vector(int(bx), int(by))))
        f.close()
    return sensors


def non_detected_points_around_point(sensors, point, search_size):
    points = []
    for x in range(-1, 1):
        for y in range(-1, 1):
            check_point = point + Vector(x, y)
            if not(0 <= check_point.x <= search_size and 0 <= check_point.y <= search_size):
                continue

            # grid.set_value(check_point, "?")
            detected = False
            for s in sensors:
                if s.in_range(check_point):
                    detected = True
                    # grid.set_value(check_point, "+")
                    break
            if not detected:
                points.append(check_point)

    return points


def count_points_in_range(sensors, y=2000000):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for s in sensors:
        min_x = min(min_x, s.position.x - s.sensor_range)
        max_x = max(max_x, s.position.x + s.sensor_range)
        min_y = min(min_y, s.position.y - s.sensor_range)
        max_y = max(max_y, s.position.y + s.sensor_range)

    range_count = 0
    x = min_x - 1
    print("scan range for y = {} is {}..{}".format(y, min_x, max_x))
    print("starting scan at ... {},{}".format(x, y))
    while x < max_x + 1:
        # for x in range(min_x - 1, max_x + 1):
        # any_in_range = False
        any_in_range = False
        for s in sensors:
            # grid.set_value(s.position, "S")
            if s.in_range(Vector(x, y)) and not s.matches_beacon(Vector(x, y)):
                any_in_range = True
        if any_in_range:
            # grid.set_value(Vector(x, y), "#")
            range_count += 1

        x += 1
        if x % 500000 == 0:
            pct_complete = math.floor(abs(float((x - min_x))) / float((max_x - min_x)) * 100.0)
            pct_complete_str = "{}%".format(pct_complete).rjust(4, ' ')
            bar_complete_cnt = math.floor(pct_complete)
            bar_incomplete_cnt = 100 - math.floor(pct_complete)
            print(".. {}, {} \t\t[{}][{}{}]".format(x, y, pct_complete_str, "|" * bar_complete_cnt,
                                                    "-" * bar_incomplete_cnt))

    print("scan complete")
    return range_count


def find_beacon(sensors, search_size=4000000):
    # loop through each sensor, then loop through all "outer" edges of the sensor
    # if that spot is not in any sensor's range:
    # do the outer edges of *that* spot and check to make sure all those spots are in a sensor's range
    sensor_count = 0
    for s in sensors:
        sensor_count += 1
        # check if the sensor is in range of our search:
        if not (-s.sensor_range <= s.position.x <= search_size + s.sensor_range and -s.sensor_range <= s.position.y <= search_size + s.sensor_range):
            continue

        print("{}: sensor at {},{}: range = {}".format(sensor_count, s.position.x, s.position.y, s.sensor_range))
        print("getting edges...", end="")
        outer_edges = s.get_outer_edges()
        print("{}".format(len(outer_edges)))

        # print("edges: {}".format(outer_edges))
        # print()

        # now loop through the edges
        count = 0
        print("cycling edges", end="")
        for e in outer_edges:
            if count % 100000 == 0:
                print(".", end="")
            if not (0 <= e.x <= search_size and 0 <= e.y <= search_size):
                continue
            detected = non_detected_points_around_point(sensors, e, search_size)
            if len(detected) == 1:
                # grid.set_value(detected[0], "!")
                return detected[0]
            count += 1
        print()

# grid = Grid(0, 20, 0, 20, ' ')
#
# for y in range(grid.start_y, grid.stop_y + 1):
#     for x in range(grid.start_x, grid.stop_x + 1):
#         for s in get_sensors('input3.txt'):
#             if s.in_range(Vector(x, y)):
#                 grid.set_value(Vector(x, y), "#")


# print("in range count = {}".format(count_points_in_range(get_sensors('input.txt'), 2000000)))
file = 'input.txt'
beacon_pos = find_beacon(get_sensors(file), 4000000)
print("*** beacon_pos = {}".format(beacon_pos))
print("*** tuning frequency = {}".format(beacon_pos.x * 4000000 + beacon_pos.y))


# grid.show()

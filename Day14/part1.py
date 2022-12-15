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

    def add(self, other):
        return self + other

    def add_x(self, x_val: int):
        return self.add(Vector(x_val, 0))

    def add_y(self, y_val: int):
        return self.add(Vector(0, y_val))



class Grid:
    def __init__(self, size_x, size_y, offset: Vector = None, initialize_with='.'):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = []

        if offset is not None:
            self.offset = offset

        for x in range(self.size_x):
            self.grid.append([initialize_with] * self.size_y)

    def reset(self, character='.'):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid[i][j] = character

    def show(self):
        # print the top header
        print()
        for r in [2, 1, 0]:
            # print 4 blanks
            print("    ", end="")
            for c in range(self.size_x):
                c_offset = c - offset.x
                # determine if the digit is visible
                if c_offset >= 10 ** r or (c_offset == 0 and r == 0):
                    # print("{}".format(math.floor(c_offset / 10 ** r)), end="")
                    print("{}".format(math.floor((c_offset % (10 ** (r + 1)))/10 ** r)), end="")
                else:
                    print(" ", end="")
            print()

        for j in range(self.size_y):
            print("{}".format(j + offset.y).rjust(3, ' '), end="")
            print(" ", end="")
            for i in range(self.size_x):
                print(self.grid[i][j], end="")
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
        if self.contains(vector):
            return self.grid[vector.x][vector.y]
        else:
            return '.'

    def set_value(self, vector: Vector, val):
        if self.contains(vector):
            self.grid[vector.x][vector.y] = val

    def contains(self, vector: Vector):
        return 0 <= vector.x < self.size_x and 0 <= vector.y < self.size_y

    def count(self, character):
        c = 0
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.grid[x][y] == character:
                    c += 1
        return c


class Grain:
    def __init__(self, position: Vector, grid: Grid, char="o"):
        self.position = position
        self.grid = grid
        self.char = char
        self.at_rest = False

    def try_move(self, move_vector: Vector):
        if self.grid is not None or not self.grid.contains(self.position):
            new_position = self.position + move_vector
            # fell out of the grid
            if not self.grid.contains(new_position):
                self.grid.set_value(self.position, '.')
                self.position = new_position
            if self.grid.get_value(self.position + move_vector) == '.':
                self.grid.set_value(new_position, self.char)
                self.grid.set_value(self.position, '.')
                self.position = new_position
                self.at_rest = True

                return True
        return False

    def inside_grid(self):
        if self.grid is not None:
            return self.grid.contains(self.position)
        else:
            return False

    def update(self):
        # try to move, return true if moved and false if not
        down = Vector(0, 1)
        down_left = Vector(-1, 1)
        down_right = Vector(1, 1)

        if self.try_move(down):
            return True
        elif self.try_move(down_left):
            return True
        elif self.try_move(down_right):
            return True
        else:
            return False

lines = []
with open('input.txt') as f:
    lines = f.readlines()
    f.close()

paths = []

min_x = min_y = 10000000
max_x = max_y = 0
for line in lines:
    pairs = []
    for pair in line.split(" -> "):
        split_pair = pair.split(",")

        px = int(split_pair[0])
        min_x = min(min_x, px)
        max_x = max(max_x, px)

        py = int(split_pair[1])
        min_y = min(min_y, py)
        max_y = max(max_y, py)

        pairs.append(Vector(px, py))

    paths.append(pairs)
    # print(paths)

# make the floor
max_y += 2
print ("Making max y to {}".format(max_y))
max_x = 500 + max_y * 2
min_x = 500 - max_y * 2

# initialize a huge grid
print()
print("creating a grid of {}, {}".format(max_x - min_x + 1, max_y + 1))

offset = Vector(-min_x, 0)
grid = Grid(max_x - min_x + 1, max_y + 1, offset)

grid.line(Vector(min_x + offset.x, max_y), Vector(max_x + offset.x, max_y))


sand_source = Vector(500, 0)

grid.set_value(sand_source + offset, '+')

for p in paths:
    # offset all the vectors
    for i in range(len(p)):
        # print("{} + {} = {}".format(p[i], offset, p[i] + offset))
        p[i] += offset

    # draw the path
    # print("Drawing {}".format(p))
    grid.path(p)

# grid.show()

pebbles = []
keep_going = True
cycles = 0
while keep_going:

    if grid.get_value(sand_source + offset) == 'o':
        break

    g = Grain(sand_source + offset, grid)
    pebbles.append(g)
    while g.update() and g.inside_grid():
        cycles += 1
    if not g.inside_grid():
        break

    if len(pebbles) > 100000:
        break
    # grid.show()

grid.show()

# off by one error I don't care about fixing
print("Pebbles at rest = {}".format(grid.count('o')+1))
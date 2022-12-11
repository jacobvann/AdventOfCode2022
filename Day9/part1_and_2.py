# --- Day 9: Rope Bridge ---
# This rope bridge creaks as you walk along it. You aren't sure how old it is, or whether it can even support your
# weight.
#
# It seems to support the Elves just fine, though. The bridge spans a gorge which was carved out by the massive river
# far below you.
#
# You step carefully; as you do, the ropes stretch and twist. You decide to distract yourself by modeling rope physics;
# maybe you can even figure out where not to step.
#
# Consider a rope with a knot at each end; these knots mark the head and the tail of the rope. If the head moves far
# enough away from the tail, the tail is pulled toward the head.
#
# Due to nebulous reasoning involving Planck lengths, you should be able to model the positions of the knots on a
# two-dimensional grid. Then, by following a hypothetical series of motions (your puzzle input) for the head, you
# can determine how the tail will move.
#
# Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head (H) and tail (T) must
# always be touching (diagonally adjacent and even overlapping both count as touching):
#
# ....
# .TH.
# ....
#
# ....
# .H..
# ..T.
# ....
#
# ...
# .H. (H covers T)
# ...
# If the head is ever two steps directly up, down, left, or right from the tail, the tail must also move one step in
# that direction so it remains close enough:
#
# .....    .....    .....
# .TH.. -> .T.H. -> ..TH.
# .....    .....    .....
#
# ...    ...    ...
# .T.    .T.    ...
# .H. -> ... -> .T.
# ...    .H.    .H.
# ...    ...    ...
# Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step
# diagonally to keep up:
#
# .....    .....    .....
# .....    ..H..    ..H..
# ..H.. -> ..... -> ..T..
# .T...    .T...    .....
# .....    .....    .....
#
# .....    .....    .....
# .....    .....    .....
# ..H.. -> ...H. -> ..TH.
# .T...    .T...    .....
# .....    .....    .....
# You just need to work out where the tail goes as the head follows a series of motions. Assume the head and the tail
# both start at the same position, overlapping.
#
# For example:
#
# R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2
# This series of motions moves the head right four steps, then up four steps, then left three steps, then down one
# step, and so on. After each step, you'll need to update the position of the tail if the step means the head is no
# longer adjacent to the tail. Visually, these motions occur as follows (s marks the starting position as a reference
# point):
#
# == Initial State ==
#
# ......
# ......
# ......
# ......
# H.....  (H covers T, s)
#
# == R 4 ==
#
# ......
# ......
# ......
# ......
# TH....  (T covers s)
#
# ......
# ......
# ......
# ......
# sTH...
#
# ......
# ......
# ......
# ......
# s.TH..
#
# ......
# ......
# ......
# ......
# s..TH.
#
# == U 4 ==
#
# ......
# ......
# ......
# ....H.
# s..T..
#
# ......
# ......
# ....H.
# ....T.
# s.....
#
# ......
# ....H.
# ....T.
# ......
# s.....
#
# ....H.
# ....T.
# ......
# ......
# s.....
#
# == L 3 ==
#
# ...H..
# ....T.
# ......
# ......
# s.....
#
# ..HT..
# ......
# ......
# ......
# s.....
#
# .HT...
# ......
# ......
# ......
# s.....
#
# == D 1 ==
#
# ..T...
# .H....
# ......
# ......
# s.....
#
# == R 4 ==
#
# ..T...
# ..H...
# ......
# ......
# s.....
#
# ..T...
# ...H..
# ......
# ......
# s.....
#
# ......
# ...TH.
# ......
# ......
# s.....
#
# ......
# ....TH
# ......
# ......
# s.....
#
# == D 1 ==
#
# ......
# ....T.
# .....H
# ......
# s.....
#
# == L 5 ==
#
# ......
# ....T.
# ....H.
# ......
# s.....
#
# ......
# ....T.
# ...H..
# ......
# s.....
#
# ......
# ......
# ..HT..
# ......
# s.....
#
# ......
# ......
# .HT...
# ......
# s.....
#
# ......
# ......
# HT....
# ......
# s.....
#
# == R 2 ==
#
# ......
# ......
# .H....  (H covers T)
# ......
# s.....
#
# ......
# ......
# .TH...
# ......
# s.....
# After simulating the rope, you can count up all of the positions the tail visited at least once. In this diagram, s
# again marks the starting position (which the tail also visited) and # marks other positions the tail visited:
#
# ..##..
# ...##.
# .####.
# ....#.
# s###..
# So, there are 13 positions the tail visited at least once.
#
# Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least
# once?


# class to keep track of position on x,y grid
class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def set(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get(self):
        return self.x, self.y

    def move(self, direction):
        dx = dy = 0
        if direction == 'U':
            dy = -1
        elif direction == 'D':
            dy = 1
        elif direction == 'R':
            dx = 1
        elif direction == 'L':
            dx = -1

        self.x += dx
        self.y += dy

    def chase(self, other):

        # same column
        if other.x == self.x:
            if other.y < self.y - 1:
                self.move('U')
            elif other.y > self.y + 1:
                self.move('D')

        # same row
        elif other.y == self.y:
            if other.x < self.x - 1:
                self.move('L')
            elif other.x > self.x + 1:
                self.move('R')

        # diagonal
        elif other.x != self.x and other.y != self.y:
            # if we are touching, do nothing
            if abs(other.x - self.x) <= 1 and abs(other.y - self.y) <= 1:
                # do nothing
                # print("doing nothing ({},{}) -> ({},{})".format(self.x, self.y, other.x, other.y))
                return
            else:
                if other.x < self.x:
                    self.move('L')
                elif other.x > self.x:
                    self.move('R')

                if other.y < self.y:
                    self.move('U')
                elif other.y > self.y:
                    self.move('D')


# class to keep track of grid
class Grid:
    def __init__(self, size_x, size_y, initialize_with='.'):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = []

        for x in range(self.size_x):
            self.grid.append([initialize_with] * self.size_y)

    def reset(self, character='.'):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid[i][j] = character

    def show(self):
        for j in range(self.size_y):
            for i in range(self.size_x):
                print(self.grid[i][j], end="")
            print()

    def get_value(self, x, y):
        return self.grid[x][y]

    def set_value(self, x, y, val):
        self.grid[x][y] = val

    def count(self, character):
        c = 0
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.grid[x][y] == character:
                    c += 1
        return c

    def to_csv(self, filename):
        with open(filename, 'w') as csv:
            csv.write("x,y,value")
            for x in range(self.size_x):
                for y in range(self.size_y):
                    csv.write("{},{},{}\n".format(x, y, self.grid[x][y]))
            csv.close()


# initialize a huge grid
grid = Grid(600, 600)

# points to keep track of
start = Position(grid.size_x / 2, grid.size_y / 2)
head = Position(start.x, start.y)

# too lazy for array
k1 = Position(start.x, start.y)
k2 = Position(start.x, start.y)
k3 = Position(start.x, start.y)
k4 = Position(start.x, start.y)
k5 = Position(start.x, start.y)
k6 = Position(start.x, start.y)
k7 = Position(start.x, start.y)
k8 = Position(start.x, start.y)
tail = Position(start.x, start.y)

# create an array of points
knots = []
for i in range(9):
    knots.append(Position(start.x, start.y))

# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    # set the starting position
    hx = tx = grid.size_x / 2
    hy = ty = grid.size_y / 2

    # turn the text into a 2d grid
    for line in lines:
        d, n = line.replace("\n", "").split(" ")
        # move the head
        for i in range(int(n)):
            head.move(d)
            k1.chase(head)
            k2.chase(k1)
            k3.chase(k2)
            k4.chase(k3)
            k5.chase(k4)
            k6.chase(k5)
            k7.chase(k6)
            k8.chase(k7)
            tail.chase(k8)
            grid.set_value(tail.x, tail.y, '#')

    f.close()

    # grid.show()
    # for visualizing in Tableau :)
    # grid.to_csv("csv/final.csv")

    print("The tail of the rope moved {} times.".format(grid.count('#')))

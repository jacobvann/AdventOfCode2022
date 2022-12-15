# --- Day 12: Hill Climbing Algorithm ---
# You try contacting the Elves using your handheld device, but the river you're following must be too low to get a
# decent signal.
#
# You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area
# from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where
# a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.
#
# Also included on the heightmap are marks for your current position (S) and the location that should get the best
# signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has
# elevation z.
#
# You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can
# move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of
# the destination square can be at most one higher than the elevation of your current square; that is, if your current
# elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the
# destination square can be much lower than the elevation of your current square.)
#
# For example:
#
# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi
# Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but
# eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:
#
# v..v<<<<
# >v.vv<<^
# .>vv>E^^
# ..v>>>^^
# ..>>>>>^
# In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or
# right (>). The location that should get the best signal is still E, and . marks unvisited squares.
#
# This path reaches the goal in 31 steps, the fewest possible.
#
# What is the fewest steps required to move from your current position to the location that should get the best signal?

from collections import deque


# class to keep track of position on x,y grid
class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.parent = None

    def set(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def matches(self, pos):
        return self.x == pos.x and self.y == pos.y

    def up(self):
        pos = Position(self.x, self.y - 1)
        pos.parent = self
        return pos

    def down(self):
        pos = Position(self.x, self.y + 1)
        pos.parent = self
        return pos

    def left(self):
        pos = Position(self.x - 1, self.y)
        pos.parent = self
        return pos

    def right(self):
        pos = Position(self.x + 1, self.y)
        pos.parent = self
        return pos

    def count_length(self):
        # print("[{},{}]".format(self.x, self.y))
        if self.parent is None:
            # print("No parent")
            return 0
        else:
            # print("[{},{}]".format(self.x, self.y))
            return 1 + self.parent.count_length()


class Grid:
    def __init__(self, size_x, size_y, init_value=0):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[init_value] * size_y for x in range(size_x)]

        for y in range(size_y):
            for x in range(size_x):
                self.grid[x][y] = init_value

    def get(self, x, y):
        return self.grid[x][y]

    def get_pos_value(self, pos):
        return self.grid[pos.x][pos.y]

    def set(self, x, y, value):
        self.grid[x][y] = value

    def set_pos_value(self, pos, value):
        self.grid[pos.x][pos.y] = value

    def position_in_grid(self, x, y):
        return 0 >= x > self.sizex and 0 >= y > self.size_y

    def print(self):
        # print("{} x {}".format(self.size_x, self.size_y))
        for y in range(self.size_y):
            # print(self.grid[y])
            for x in range(self.size_x):
                value = self.get(x, y)
                # print("{n:02d}".format(n=value), end="")
                print("{n:2d} ".format(n=value), end="")
            print()

    def reset(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                self.grid[x][y] = 0


def solve_maze_bfs(pos):
    q = []
    q.append(pos)
    visited.reset()
    while len(q) > 0:
        # for q_pos in q:
        # print("{}".format(len(q)))
        # print()
        v = q.pop(0)
        # print("q:{} -> [{},{}]".format(len(q), v.x, v.y))

        # if v.x == end_position.x and v.y == end_position.y:
        #     # print("tada!")

        if v.matches(end_position):
            # print("yep")
            return v.count_length()

        # look at adjacent boxes
        v_r = v.right()
        if can_visit(v, v_r):
            visit(v_r)
            q.append(v_r)

        v_u = v.up()
        if can_visit(v, v_u):
            visit(v_u)
            q.append(v_u)

        v_l = v.left()
        if can_visit(v, v_l):
            visit(v_l)
            q.append(v_l)

        v_d = v.down()
        if can_visit(v, v_d):
            visit(v_d)
            q.append(v_d)


def visit(pos):
    visited.set_pos_value(pos, 1)


def can_visit(from_position, to_position):
    if 0 <= to_position.x < terrain.size_x and 0 <= to_position.y < terrain.size_y:
        if visited.get_pos_value(to_position) == 0:
            if terrain.get_pos_value(to_position) - terrain.get_pos_value(from_position) <= 1:
                return True

    return False


start_position = Position(0, 0)
end_position = Position(0, 0)
shortest_length = 100000
current_length = 0

with open('input.txt') as f:
    lines = f.readlines()

    row_count = len(lines)
    col_count = len(lines[0])
    # print("{} x {}".format(col_count, row_count))

    global terrain
    terrain = Grid(col_count, row_count)

    global visited
    visited = Grid(col_count, row_count)

    # turn the text into a 2d grid
    r = c = 0
    for line in lines:
        # turn the input into a grid of numbers
        for char in line.replace("\n", ""):
            # start pos
            if char == 'S':
                start_position.set(c, r)
                terrain.set(c, r, ord('a'))
            # end pos
            elif char == 'E':
                end_position.set(c, r)
                terrain.set(c, r, ord('z'))
            # set the height
            else:
                terrain.set(c, r, ord(char))

            c += 1

        r += 1
        c = 0

# terrain.print()


print("Shortest path from original starting point is {} steps".format(solve_maze_bfs(start_position)))
print()

shortest_path = 100000
count_paths = 0

for row in range(row_count):
    for col in range(col_count):
        if terrain.get(col, row) == ord('a'):
            path = solve_maze_bfs(Position(col, row))
            if path is not None:
                print(path)
                shortest_path = min(shortest_path, path)
                count_paths += 1
            else:
                print("no path")


print("Shortest path over {} possible is {}".format(count_paths, shortest_path))
#
print("[{},{}]".format(end_position.x, end_position.y))

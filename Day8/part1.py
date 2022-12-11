# --- Day 8: Treetop Tree House ---
# The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a
# previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good
# location for a tree house.
#
# First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count
# the number of trees that are visible from outside the grid when looking directly along a row or column.
#
# The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For
# example:
#
# 30373
# 25512
# 65332
# 33549
# 35390
# Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.
#
# A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider
# trees in the same row or column; that is, only look up, down, left, or right from any given tree.
#
# All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to
# block the view. In this example, that only leaves the interior nine trees to consider:
#
# The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of
# height 5 are in the way.)
# The top-middle 5 is visible from the top and right.
# The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height
# 0 between it and an edge.
# The left-middle 5 is visible, but only from the right.
# The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most
# height 2 between it and an edge.
# The right-middle 3 is visible from the right.
# In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
# With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this
# arrangement.
#
# Consider your map; how many trees are visible from outside the grid?


# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    # turn the text into a 2d grid
    grid = []
    for line in lines:
        grid.append(line.replace("\n", ""))

    f.close()

visible_trees_from_left = 0
visible_trees_from_right = 0
visible_trees_from_top = 0
visible_trees_from_bottom = 0

row_count = len(grid)
col_count = len(grid[0])

visible_grid = []
for i in range(row_count):
    visible_grid.append([0] * col_count)

# count by rows first
for i in range(row_count):
    max_height = 0
    first = True
    for j in range(col_count):
        # check if the new tree is visible
        if int(grid[i][j]) > max_height or first:
            visible_grid[i][j] = 1
            max_height = int(grid[i][j])
            first = False

    # now do it from the right
    # pull a row in reverse
    # iterate through row
    max_height = 0
    first = True
    for j in reversed(range(col_count)):
        # check if the new tree is visible
        if int(grid[i][j]) > max_height or first:
            visible_grid[i][j] = 1
            max_height = int(grid[i][j])
            first = False


# now count by columns (top down)
# I don't know a better way to iterate through arrays
for j in range(col_count):
    max_height = 0
    first = True
    for i in range(row_count):
        # check if the new tree is visible
        if int(grid[i][j]) > max_height or first:
            visible_grid[i][j] = 1
            max_height = int(grid[i][j])
            first = False

# now count by columns (bottom up)
# I don't know a better way to iterate through arrays
for j in range(col_count):
    max_height = 0
    first = True
    for i in reversed(range(row_count)):
        # check if the new tree is visible
        if int(grid[i][j]) > max_height or first:
            visible_grid[i][j] = 1
            max_height = int(grid[i][j])
            first = False


visible_trees = 0
for row in visible_grid:
    # print(row)
    for col in row:
        visible_trees += col

print("\n\n")

# print("x,y,height,visible")
# for x in range(row_count):
#     for y in range(col_count):
#         print("{},{},{},{}".format(x, y, grid[x][y], visible_grid[x][y]))


print("\n")

print("visible trees = {}".format(visible_trees))


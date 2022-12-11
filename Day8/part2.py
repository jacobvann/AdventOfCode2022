# --- Part Two ---
# Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house:
# they would like to be able to see a lot of trees.
#
# To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach
# an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right
# on the edge, at least one of its viewing distances will be zero.)
#
# The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has
# large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.
#
# In the example above, consider the middle 5 in the second row:
#
# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is not blocked; it can see 1 tree (of height 3).
# Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
# Looking right, its view is not blocked; it can see 2 trees.
# Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that
# blocks its view).
# A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this
# tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).
#
# However, you can do even better: consider the tree of height 5 in the middle of the fourth row:
#
# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
# Looking left, its view is not blocked; it can see 2 trees.
# Looking down, its view is also not blocked; it can see 1 tree.
# Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
# This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.
#
# Consider each tree on your map. What is the highest scenic score possible for any tree?


def scenic_score(x, y):
    return (
        # left
        scenic_score_dir(x, y, -1, 0)
        # right
        * scenic_score_dir(x, y, 1, 0)
        # up
        * scenic_score_dir(x, y, 0, 1)
        # down
        * scenic_score_dir(x, y, 0, -1)
    )


def scenic_score_dir(x, y, dx, dy):

    score = 0

    my_height = grid[x][y]

    # march in a direction until we hit the edge
    while True:
        x = x+dx
        y = y+dy
        if not(0 <= x < row_count and 0 <= y < col_count):
            break

        score += 1
        check_height = grid[x][y]

        if check_height >= my_height:
            break

    return score

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

scenic_grid = []
for row in range(row_count):
    scenic_grid.append([0]*col_count)

# go through every cell in the grid and calculate its scenic score
max_scenic_score = 0
max_i = 0
max_j = 0
for i in range(row_count):
    for j in range(col_count):
        scenic_grid[i][j] = scenic_score(i, j)
        if scenic_grid[i][j] >= max_scenic_score:
            max_scenic_score = scenic_grid[i][j]
            max_i = i
            max_j = j


print("Scenic score of best tree at {},{} is {}".format(max_i, max_j, max_scenic_score))

# # print it out
# for row in grid:
#     print(row)
#
# for row in scenic_grid:
#     print(row)

import sys


def load_cubes(filename):
    cube_list = []
    max_size = 0
    with open(filename) as f:
        for line in f.readlines():
            x, y, z = eval(line)
            max_size = max(max_size, x, y, z)
            cube_list.append([x, y, z])
        f.close()

        matrix_xyz = [[[0 for _ in range(max_size + 5)] for _ in range(max_size + 5)] for _ in range(max_size + 5)]

        for x in range(max_size):
            for y in range(max_size):
                for z in range(max_size):
                    if [x, y, z] in cube_list:
                        matrix_xyz[x+2][y+2][z+2] = 1

    return matrix_xyz


def is_outside(mat, mx, my, mz):
    # start in your spot.  If it's solid, then no
    # if it's not solid, then go up, down, left, right, toward, back ...
    # if any of those directions escapes the matrix, you are outside
    if mat[mx][my][mz] > 0:
        return False

    # top
    found_air = 6

    dz = 0
    while mz + dz < len(mat) - 1:
        dz += 1
        if mat[mx][my][mz + dz] > 0:
            found_air -= 1
            break

    # bottom
    dz = 0
    while mz + dz > 0:
        dz -= 1
        if mat[mx][my][mz + dz] > 0:
            found_air -= 1
            break

    # bottom
    dx = 0
    while mx + dx > 0:
        dx -= 1
        if mat[mx + dx][my][mz] > 0:
            found_air -= 1
            break

    # top
    dx = 0
    while mx + dx < len(mat) - 1:
        dx += 1
        if mat[mx + dx][my][mz] > 0:
            found_air -= 1
            break

    # toward
    dy = 0
    while my + dy > 0:
        dy -= 1
        if mat[mx][my + dy][mz] > 0:
            found_air -= 1
            break

    # back
    dy = 0
    while my + dy < len(mat) - 1:
        dy += 1
        if mat[mx][my + dy][mz] > 0:
            found_air -= 1
            break

    return found_air > 0


def flood_recursive(canvas, start_x=0, start_y=0, start_z=0, start_color=0, fill_color=-1):
    size = len(canvas)

    def fill(x, y, z, start_color, color_to_update):

        stack = [[x, y, z]]

        while len(stack) > 0:

            new_neighbors = []

            point = stack.pop()
            px = point[0]
            py = point[1]
            pz = point[2]

            if (px == 2 and py == 5 and pz == 10):
                print ("\n\n~~~~ here! ~~~~\n\n")

            # if the square is not the same color as the starting point
            if canvas[px][py][pz] != start_color:
                continue
            # if the square is not the new color
            elif canvas[px][py][pz] == color_to_update:
                continue
            else:
                # update the color of the current square to the replacement color
                canvas[px][py][pz] = color_to_update
                neighbors = [(px - 1, py, pz), (px + 1, py, pz), (px, py - 1, pz), (px, py + 1, pz), (px, py, pz - 1), (px, py, pz + 1)]
                for n in neighbors:
                    if 0 <= n[0] <= size - 1 and 0 <= n[1] <= size - 1 and 0 <= n[2] <= size - 1:
                        stack.append([n[0], n[1], n[2]])
                        new_neighbors.append([n[0], n[1], n[2]])

                if [px, py, pz] == [5, 1, 10]:
                    print("--- test ---")
                    print(new_neighbors)


            print()
            print([px, py, pz])
            z = 10
            for x in range(size):
                for y in range(size):
                    c = '.'
                    if px == x and py == y and pz == z:
                        c = '@'
                    elif [x, y, z] in new_neighbors:
                        c = 'X'
                    elif canvas[x][y][z] == 1:
                        c = '#'
                    elif canvas[x][y][z] == 2:
                        c = '@'
                    elif canvas[x][y][z] == -1:
                        c = 'O'
                    print("{}".format(c), end='')
                print()
            print()


    # pick a random starting point
    fill(start_x, start_y, start_z, start_color, fill_color)
    return canvas


def exposed_edges(mat, mx, my, mz):

    count = 0

    if mat[mx][my][mz] != 1:
        return 0

    # top
    if mz + 1 >= len(mat) or mat[mx][my][mz + 1] == -1:
        count += 1

    # bottom
    if mz - 1 < 0 or mat[mx][my][mz - 1] == -1:
        count += 1

    # left
    if mx - 1 < 0 or mat[mx - 1][my][mz] == -1:
        count += 1

    # right
    if mx + 1 >= len(mat) or mat[mx + 1][my][mz] == -1:
        count += 1

    # toward
    if my - 1 < 0 or mat[mx][my - 1][mz] == -1:
        count += 1

    # behind
    if my + 1 >= len(mat) or mat[mx][my + 1][mz] == -1:
        count += 1

    return count


matrix = load_cubes('input.txt')

area = 0

matrix = flood_recursive(matrix)

for z in range(len(matrix)):
    for x in range(len(matrix)):
        for y in range(len(matrix)):
            if matrix[x][y][z] != 1 and not is_outside(matrix, x, y, z):
                matrix[x][y][z] = 2

for z in range(len(matrix)):
    for x in range(len(matrix)):
        for y in range(len(matrix)):
            char = '.'
            if matrix[x][y][z] == 1:
                char = '#'
            elif matrix[x][y][z] == 2:
                char = '@'
            elif matrix[x][y][z] == -1:
                char = ' '
            print("{}".format(char), end='')
            area += exposed_edges(matrix, x, y, z)
        print()
    print("z = {} [area = {}]".format(z, area))

print(area)

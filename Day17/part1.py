import math
from time import sleep
import os
import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Tunnel:
    def __init__(self, height=20, width=9):
        self.rows = []
        self.width = width
        self.height = height
        self.stack_height = 0

        # walls
        for r in range(height - 1):
            self.rows.append((2 ** (width - 1) + 1))
        # floor
        self.rows.append((2 ** width - 1))

    def add_height(self, h):
        new_rows = [(2 ** (self.width - 1) + 1)] * h
        self.rows = new_rows + self.rows
        self.height += h

    def check_collision(self, pos_x, pos_y, rows, block_bit_width):
        # we are going from bottom up
        i = 0
        for r in reversed(rows):
            my_value = self.rows[self.height - (pos_y + i) - 1]
            # bitwise
            # bit-shift blocks value left by the position
            r_left_shift = r << (self.width - block_bit_width) # hack to shift by 5
            r_shifted = r_left_shift >> pos_x
            if r_shifted & my_value > 0:
                return True
            i += 1
        return False

    def bit_at_pos(self, x, y):
        # x and y passed in are the position in tunnel space we are probing
        # bitwise and

        if x < 0 or x >= self.width:
            return 0
        if y < 0 or y >= self.height:
            return 0

        return self.rows[self.height - y - 1] & (2 ** (self.width - x - 1))

    def add_block(self, pos_x, pos_y, rows, block_bit_width, block_height):
        # the block's data becomes one with the tunnel
        i = 0
        for r in reversed(rows):
            # bitwise
            # bit-shift blocks value left by the position
            r_left_shift = r << (self.width - block_bit_width) # hack to shift by 5
            r_shifted = r_left_shift >> pos_x
            # bitwise or
            self.rows[self.height - (pos_y + i)] = self.rows[self.height - (pos_y + i) ] | r_shifted
            i += 1
        self.stack_height = max(self.stack_height, (pos_y - 1) + (block_height - 1))

    def __str__(self):
        string = ""
        for row in self.rows:
            # convert to binary
            binary = format(row, 'b').rjust(self.width, '0').replace("0", "⬛").replace("1", "⬜")
            string += binary[-self.width:]
            string += "\n"
        return string

    def __repr__(self):
        return str(self)


class Block:
    def __init__(self, name, bitmask, start_x, start_y):
        self.name = name
        self.rows = []
        self.width = 0
        self.bit_width = len(bitmask[0])
        self.height = 0
        self.bit_height = len(bitmask)
        self.pos_x = start_x
        self.pos_y = start_y

        for r in range(self.bit_height):
            val = 0
            bit_count = 0
            for c in range(self.bit_width):
                bit = bitmask[r][(self.bit_width - 1) - c]
                if bit == 1:
                    bit_count += 1
                val += (bit * 2 ** c)
            self.rows.append(int(val))
            if val > 0:
                self.height += 1
            self.width = max(self.width, bit_count)

    def bit_at_pos(self, x, y):
        # x and y passed in are the position
        # need to use x, y to index into the bit array

        local_x = x - self.pos_x
        local_y = y - self.pos_y

        if local_x < 0 or local_x >= self.bit_width:
            return False
        if local_y < 0 or local_y >= self.bit_height:
            return False

        # bitwise and
        # e.g:
        #   if local pos = 0, and with 1000 (8 == 2^(width-0-1))
        #   if local pos = 1, and with 0100
        #   if local pos = 3, and with 0001 (1 == 2^(width-3-1))
        bit_check_ix = self.bit_height - local_y - 1
        bit_check_self = self.rows[bit_check_ix]
        bit_check_other = (2 ** (self.bit_width - local_x - 1))
        bit_and = bit_check_self & bit_check_other
        return bit_and

    def reset(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def __str__(self):
        string = ""
        for row in self.rows:
            # convert to binary
            binary = format(row, 'b').rjust(4, '0').replace("0", "⬛").replace("1", "🟩")
            string += binary[-self.width:]
            string += "\n"
        return string

    def __repr__(self):
        return str(self)

    def collides(self, tunnel):
        return tunnel.check_collision(self.pos_x, self.pos_y, self.rows, self.bit_width)

    def try_move(self, dx, dy, tunnel):
        original_pos_x = self.pos_x
        original_pos_y = self.pos_y

        self.pos_x += dx
        self.pos_y += dy
        if self.collides(tunnel):
            # move back
            self.pos_x = original_pos_x
            self.pos_y = original_pos_y
            return False
        return True

    def move_down(self, tunnel):
        did_move = self.try_move(0, -1, tunnel)
        if not did_move:
            tunnel.add_block(self.pos_x, self.pos_y + 1, self.rows, self.bit_width, self.height)
        return did_move

    def move_left(self, tunnel):
        return self.try_move(-1, 0, tunnel)

    def move_right(self, tunnel):
        return self.try_move(1, 0, tunnel)


def show_tunnel(tun, blk, height=10, show_block=True, sleep_time=0.1):
    # clear_screen()
    print('~'*(tun.width*2 + 5))
    top = y = tun.height - 1
    rows = []
    for r in range(min(tun.height, height)):
        # get a single row
        # set the height we are observing
        y = top - r
        # cycle through characters in row
        row = str(y).rjust(4, '0')+' '
        for x in range(tun.width):
            if tun.bit_at_pos(x, y) > 0:
                if y > 0 and (x == 0 or x == tun.width - 1):
                    row += '|'
                elif y == 0:
                    if x == 0 or x == tun.width - 1:
                        row += '+'
                    else:
                        row += '-'
                else:
                    row += '#'
            elif show_block and blk is not None and blk.bit_at_pos(x, y) > 0:
                row += 'O'
            else:
                row += ' '

        rows.append(row)
    for r in rows:
        print(r)
    print('~'*(tun.width*2 + 5))


def load_wind(filename):
    wind_str = ''
    with open(filename) as f:
        lines = f.readlines()
        wind_str = lines[0].replace("\n", "")
        f.close()
    return wind_str


def create_blocks():
    block_list = []
    block_list.append(Block(
        "h line",
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1]
        ],
        3, 3))

    block_list.append(Block(
        "plus",
        [
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 1, 0],
            [0, 1, 0, 0]
        ],
        3, 3))

    block_list.append(Block(
        "backwards L",
        [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [1, 1, 1, 0]
        ],
        3, 3))

    block_list.append(Block(
        "v line",
        [
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0]
        ],
        3, 3))

    block_list.append(Block(
        "box",
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0]
        ],
        3, 3))

    return block_list


def create_tunnel(height=15):
    return Tunnel(height)


def lists_are_equal(l1, l2):

    if len(l1) != len(l2):
        return False

    return l1 == l2

    # print("comparing lists:")
    # print([x for x in zip(l1, l2)])

    # for i in range(len(l1)):
    #     if l1[i] != l2[i]:
    #         return False

    return True


def simulate(tunnel, blocks, wind, num_blocks=1000, sleep_time=0.0):
    start_time = datetime.datetime.now()
    # print("Start time {}".format(start_time))
    block_count = 0
    block_index = 0
    wind_index = 0
    wind_cycle_count = 0
    height_at_block = [0]
    zero_blocks = []

    # loop for all blocks
    while block_count < num_blocks:
        block_count += 1
        block = blocks[block_index]
        block.reset(3, tunnel.stack_height + 4)
        hit_something = False
        prior_stack_height = tunnel.stack_height
        # loop with this block until we hit something
        while not hit_something:
            # parse the wind, move left or right
            w = wind[wind_index]
            if w == '>':
                block.move_right(tunnel)
            elif w == '<':
                block.move_left(tunnel)


            # draw the tunnel
            # show_tunnel(tunnel, block, 15, sleep_time)
            # print("[{}]".format(block.name))
            # sleep(sleep_time)

            # try to move down
            if not block.move_down(tunnel):
                hit_something = True

            # print("================================")
            # show_tunnel(tunnel, block, tunnel.height)
            # print("Pos {},{} | Wind: {} | landed? {}".format(block.pos_x, block.pos_y, w, hit_something))
            # print("================================")

            # # draw the tunnel
            # show_tunnel(tunnel, block, 15, sleep_time)
            # print("Blocks: {}\nStack: {}\nWind: {}\nBlock Height: {}".format(block_count, tunnel.stack_height, w,
            #                                                                  block.height))
            # sleep(sleep_time)

            # increase tunnel height if needed
            if tunnel.stack_height >= 10:
                # calculate how much height to add
                dh = tunnel.height - tunnel.stack_height
                if dh < 10:
                    tunnel.add_height(10 - dh)

            wind_index += 1
            if wind_index >= len(wind):
                wind_cycle_count += 1
                wind_index = wind_index % len(wind)


        # print("Block Count: {}   Block Name: {}   Stack Height: {}".
        #      format(str(block_count).rjust(4, '0'), block.name.ljust(12, ' '), str(tunnel.stack_height).rjust(4, '0')))
        # reset indices, looping around


        # check if we have a repeating pattern
        # must be at end of block cycle and have an even stacked height
        # if it repeats, we can guess the height after all the blocks
        # if block_count > 5 and len(previous_five_blocks) >= 5 and wind_cycle_count >= 1:
        #     if lists_are_equal(first_five_blocks, previous_five_blocks):
        #         repeating_height = height_at_block[block_count-5]
        #         repeating_count = block_count - 5
        #         print("found periodic matching at {} blocks, {} height: ".format(repeating_count, repeating_height))
        #         # found out how many times we'd repeat if we dropped all rocks
        #         pattern_count = int(num_blocks / repeating_count)
        #         # now how many are leftover?
        #         blocks_left = int(num_blocks % repeating_count)
        #         # print("{}, {}, {} = {}".format(pattern_count, repeating_height, blocks_left, pattern_count * repeating_height + height_at_block[blocks_left]))
        #         # break
        #         return pattern_count * repeating_height + height_at_block[blocks_left]

        # bring on the next block
        height_at_block.append(tunnel.stack_height)
        if block_index == 0:
            zero_block_meta = [block.pos_x, block.pos_y - tunnel.stack_height, wind_index]
            if zero_block_meta in zero_blocks:
                # find the first one
                for i in range(len(zero_blocks)):
                    if zero_block_meta == zero_blocks[i]:
                        break
                # we can calculate it now
                # first get the height up until the repeating cycle starts
                # then get the height of the repeating cycle, multiplied by count of cycles to reach the end
                initial_block_count = i * len(blocks)
                initial_height = height_at_block[initial_block_count]

                # remember the last block we dropped is a repeat
                cycling_height = height_at_block[block_count - 1] - initial_height
                cycle_block_count = (block_count - 1) - initial_block_count

                # now count num cycles to complete
                blocks_left = num_blocks - initial_block_count
                cycle_count = math.floor(blocks_left / cycle_block_count)

                # now how many blocks are left
                leftover_blocks = (num_blocks - initial_block_count) % cycle_block_count
                height_of_leftover = height_at_block[i * len(blocks) + leftover_blocks] - initial_height
                # add it all together

                print(">> {} - {} - {} = {} blocks left after cycle".format(num_blocks, initial_block_count, cycle_block_count, leftover_blocks))

                final_height = initial_height + (cycle_count * cycling_height) + height_of_leftover
                print(">> {} + {} * {} ({}) + {} = {}".format(initial_height, cycling_height, cycle_count, cycle_block_count,
                                                         height_of_leftover, final_height))
                return final_height

            else:
                zero_blocks.append(zero_block_meta)

        block_index = (block_index + 1) % len(blocks)
        if block_count % 5000 == 0:
            print("{} blocks...".format(block_count))

        # show_tunnel(tunnel, None, 100)


    # print("{} : {}".format(block_count, tunnel.stack_height))
    # end_time = datetime.datetime.now()
    # print("End time {}".format(end_time))


    return tunnel.stack_height


print("creating blocks...")
blk = create_blocks()

print("creating tunnel...")
tun = create_tunnel()

print("loading wind...")
wnd = load_wind('input.txt')

blocks_to_drop = 1000000000000
print("block height after {} blocks is {} ".format(blocks_to_drop, simulate(tun, blk, wnd, blocks_to_drop)))








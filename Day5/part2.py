# --- Part Two ---
# As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your
# prediction.
#
# Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a
# CrateMover 9000 - it's a CrateMover 9001.
#
# The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup
# holder, and the ability to pick up and move multiple crates at once.
#
# Again considering the example above, the crates begin in the same configuration:
#
#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3
# Moving a single crate from stack 2 to stack 1 behaves the same as before:
#
# [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3
# However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the
# same order, resulting in this new configuration:
#
#         [D]
#         [N]
#     [C] [Z]
#     [M] [P]
#  1   2   3
# Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:
#
#         [D]
#         [N]
# [C]     [Z]
# [M]     [P]
#  1   2   3
# Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:
#
#         [D]
#         [N]
#         [Z]
# [M] [C] [P]
#  1   2   3
# In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.
#
# Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to
# be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of
# each stack?


# the stacks from the input - gonna go ahead and just hard code these because why not
#
# [P]     [C]         [M]
# [D]     [P] [B]     [V] [S]
# [Q] [V] [R] [V]     [G] [B]
# [R] [W] [G] [J]     [T] [M]     [V]
# [V] [Q] [Q] [F] [C] [N] [V]     [W]
# [B] [Z] [Z] [H] [L] [P] [L] [J] [N]
# [H] [D] [L] [D] [W] [R] [R] [P] [C]
# [F] [L] [H] [R] [Z] [J] [J] [D] [D]
#  1   2   3   4   5   6   7   8   9

stacks = [
    ["F", "H", "B", "V", "R", "Q", "D", "P"],
    ["L", "D", "Z", "Q", "W", "V"],
    ["H", "L", "Z", "Q", "G", "R", "P", "C"],
    ["R", "D", "H", "F", "J", "V", "B"],
    ["Z", "W", "L", "C"],
    ["J", "R", "P", "N", "T", "G", "V", "M"],
    ["J", "R", "L", "V", "M", "B", "S"],
    ["D", "P", "J"],
    ["D", "C", "N", "W", "V"]
]


# move a crate from one stack to another
def move_crate(from_stack_index, to_stack_index):
    crate = stacks[from_stack_index].pop()
    stacks[to_stack_index].append(crate)


# move a crate from one stack to another
def move_crate_2(from_stack_index, to_stack_index, num_crates):

    # start of the new stack we are moving
    start = len(stacks[from_stack_index]) - num_crates

    # slice from the top of the list
    # 1. append to new stack

    print(">> input: {} -> {}, {}".format(stacks[from_stack_index], stacks[to_stack_index], num_crates))
    new_stack = stacks[from_stack_index][-num_crates::]
    print(" new stack -> {}".format(new_stack))
    for crate in new_stack:
        stacks[to_stack_index].append(crate)
    # 2. remove from old stack
    stacks[from_stack_index] = stacks[from_stack_index][:len(stacks[from_stack_index])-num_crates:]
    print(">> output: {} -> {}".format(stacks[from_stack_index], stacks[to_stack_index]))


# print(stacks[5])
# print(stacks[5][-2::])

# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    # read through all the lines
    for line in lines:
        # turn each line into an instruction
        clean_line = line.replace("\n", "").replace("move ", "").replace(" from ", ":").replace(" to ", ":")
        count, from_index, to_index = clean_line.split(":")
        move_crate_2(int(from_index) - 1, int(to_index) - 1, int(count))

    for stack in stacks:
        print(stack.pop())

    f.close()

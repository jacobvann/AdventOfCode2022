# --- Day 13: Distress Signal ---
# You climb the hill and again try contacting the Elves. However, you instead receive a signal you weren't expecting:
# a distress signal.
#
# Your handheld device must still not be working properly; the packets from the distress signal got decoded out of
# order. You'll need to re-order the list of received packets (your puzzle input) to decode the message.
#
# Your list consists of pairs of packets; pairs are separated by a blank line. You need to identify how many pairs of
# packets are in the right order.
#
# For example:
#
# [1,1,3,1,1]
# [1,1,5,1,1]
#
# [[1],[2,3,4]]
# [[1],4]
#
# [9]
# [[8,7,6]]
#
# [[4,4],4,4]
# [[4,4],4,4,4]
#
# [7,7,7,7]
# [7,7,7]
#
# []
# [3]
#
# [[[]]]
# [[]]
#
# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]
# Packet data consists of lists and integers. Each list starts with [, ends with ], and contains zero or more comma-
# separated values (either integers or other lists). Each packet is always a list and appears on its own line.
#
# When comparing two values, the first value is called left and the second value is called right. Then:
#
# If both values are integers, the lower integer should come first. If the left integer is lower than the right
# integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not
# in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
# If both values are lists, compare the first value of each list, then the second value, and so on. If the left list
# runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are
# not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue
# checking the next part of the input.
# If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then
# retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2);
# the result is then found by instead comparing [0,0,0] and [2].
# Using these rules, you can determine which of the pairs in the example are in the right order:
#
# == Pair 1 ==
# - Compare [1,1,3,1,1] vs [1,1,5,1,1]
#   - Compare 1 vs 1
#   - Compare 1 vs 1
#   - Compare 3 vs 5
#     - Left side is smaller, so inputs are in the right order
#
# == Pair 2 ==
# - Compare [[1],[2,3,4]] vs [[1],4]
#   - Compare [1] vs [1]
#     - Compare 1 vs 1
#   - Compare [2,3,4] vs 4
#     - Mixed types; convert right to [4] and retry comparison
#     - Compare [2,3,4] vs [4]
#       - Compare 2 vs 4
#         - Left side is smaller, so inputs are in the right order
#
# == Pair 3 ==
# - Compare [9] vs [[8,7,6]]
#   - Compare 9 vs [8,7,6]
#     - Mixed types; convert left to [9] and retry comparison
#     - Compare [9] vs [8,7,6]
#       - Compare 9 vs 8
#         - Right side is smaller, so inputs are not in the right order
#
# == Pair 4 ==
# - Compare [[4,4],4,4] vs [[4,4],4,4,4]
#   - Compare [4,4] vs [4,4]
#     - Compare 4 vs 4
#     - Compare 4 vs 4
#   - Compare 4 vs 4
#   - Compare 4 vs 4
#   - Left side ran out of items, so inputs are in the right order
#
# == Pair 5 ==
# - Compare [7,7,7,7] vs [7,7,7]
#   - Compare 7 vs 7
#   - Compare 7 vs 7
#   - Compare 7 vs 7
#   - Right side ran out of items, so inputs are not in the right order
#
# == Pair 6 ==
# - Compare [] vs [3]
#   - Left side ran out of items, so inputs are in the right order
#
# == Pair 7 ==
# - Compare [[[]]] vs [[]]
#   - Compare [[]] vs []
#     - Right side ran out of items, so inputs are not in the right order
#
# == Pair 8 ==
# - Compare [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]
#   - Compare 1 vs 1
#   - Compare [2,[3,[4,[5,6,7]]]] vs [2,[3,[4,[5,6,0]]]]
#     - Compare 2 vs 2
#     - Compare [3,[4,[5,6,7]]] vs [3,[4,[5,6,0]]]
#       - Compare 3 vs 3
#       - Compare [4,[5,6,7]] vs [4,[5,6,0]]
#         - Compare 4 vs 4
#         - Compare [5,6,7] vs [5,6,0]
#           - Compare 5 vs 5
#           - Compare 6 vs 6
#           - Compare 7 vs 0
#             - Right side is smaller, so inputs are not in the right order
# What are the indices of the pairs that are already in the right order? (The first pair has index 1, the second pair
# has index 2, and so on.) In the above example, the pairs in the right order are 1, 2, 4, and 6; the sum of these
# indices is 13.
#
# Determine which pairs of packets are already in the right order. What is the sum of the indices of those pairs?

import functools

def unfold(l, depth=0):
    if type(l) != list:
        l = [l]
    print("{}{}".format(" |---" * depth, l))
    if l is None or len(l) == 1:
        return
    for i in range(len(l)):
        unfold(l[i], depth + 1)

def compare(l1, l2, depth=0):

    # print("{}- Compare {} vs {}".format(" "*(depth+1), l1, l2))

    if type(l1) == int and type(l2) == int:
        if l1 < l2:
            # print("{}- {} is smaller than {} so they are in the right order".format(" " * (depth + 1), l1, l2))
            return 1
        elif l1 > l2:
            # print("{}- {} is larger than {} so they are not in the right order".format(" " * (depth + 1), l1, l2))
            return -1
        else:
            return 0
    elif type(l1) == list and type(l2) != list:
        # print("{}- Mixed types - converting left to {}".format(" " * (depth + 1), [l1]))
        return compare(l1, [l2], depth)
    elif type(l2) == list and type(l1) != list:
        # print("{}- Mixed types - converting left to {}".format(" " * (depth + 1), [l2]))
        return compare([l1], l2, depth)
    else:
        depth += 1
        for i in range(min(len(l1), len(l2))):
            r = compare(l1[i], l2[i], depth)
            if r != 0:
                return r
        # check if we run out of elements
        # ran out from the left side first
        if len(l2) > len(l1):
            # print("{}- the left side is ran out of items.  Correct order.".format(" " * (depth + 1), l1, l2))
            return 1
        # ran out from right side first
        elif len(l1) > len(l2):
            # print("{}- the right side ran out of items.  Incorrect order.".format(" " * (depth + 1), l1, l2))
            return -1
        else:
            return 0


with open('input.txt') as f:
    lines = f.readlines()
    f.close()

index = 0
correct_indices = []
# loop through the lines by 3

packets = []
for i in range(0, len(lines), 3):
    index += 1

    # print("=== Pair {} ===".format(index))
    left_list = eval(lines[i])
    packets.append(left_list)

    right_list = eval(lines[i + 1])
    packets.append(right_list)

    # print("comparing {} to {}".format(left_list, right_list))

    cmp = compare(left_list, right_list)
    if cmp == 1:
        # print("CORRECT ORDER {}".format(cmp))
        correct_indices.append(index)
    #else:
    # print("INCORRECT ORDER")

    #print()

#print("==================")
#print("Sum of indexes {} out of {} ({})".format(sum(correct_indices), index, correct_indices))

packets.append([[2]])
packets.append([[6]])
decoder = 1
sorted_packets = sorted(packets, key=functools.cmp_to_key(compare), reverse=True)

for p in range(len(sorted_packets)):
    print("{}: {}".format(p+1, sorted_packets[p]))
    if sorted_packets[p] == [[2]] or sorted_packets[p] == [[6]]:
        decoder *= (p+1)

print("\n\nDecoder = {}".format(decoder))
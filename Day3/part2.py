# --- Part Two ---
# As you finish identifying the misplaced items, the Elves come to you with another issue.
#
# For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For
# efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if
# a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most
# two of the Elves will be carrying any other item type.
#
# The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges
# need to be pulled out of the rucksacks so the new authenticity stickers can be attached.
#
# Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item
# type is the right one is by finding the one item type that is common between all three Elves in each group.
#
# Every set of three lines in your list corresponds to a single group, but each group can have a different badge item
# type. So, in the above example, the first group's rucksacks are the first three lines:
#
# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# And the second group's rucksacks are the next three lines:
#
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw
# In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges.
# In the second group, their badge item type must be Z.
#
# Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for
# the first group and 52 (Z) for the second group. The sum of these is 70.
#
# Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those
# item types?

def get_value(char):
    # get the ascii number of the char
    char_ord = ord(char)

    # default return value
    value = 0

    # check for lowercase
    if ord('a') <= char_ord <= ord('z'):
        value = char_ord - ord('a') + 1

    # uppercase
    elif ord('A') <= char_ord <= ord('Z'):
        value = char_ord - ord('A') + 27

    return value


def find_badge(group1, group2, group3):
    for c in group1:
        if group2.find(c) != -1 and group3.find(c) != -1:
            return c


def find_match(string1, string2):
    match_values = 0
    for c in string1:
        if string2.find(c) != -1:
            print("{},{}: match! {}".format(string1, string2, c))
            return get_value(c)

    return 0


# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    # read through all the lines
    # save the lines into an array
    line_array = []
    for line in lines:
        line_clean = line.replace("\n","")
        line_array.append(line_clean)

    total_value = 0

    # now loop through the array by 3s
    for i in range(0, len(line_array), 3):
        badge = find_badge(line_array[i], line_array[i+1], line_array[i+2])
        total_value += get_value(badge)

    print("Total priority value of badges = {}".format(total_value))

    f.close()

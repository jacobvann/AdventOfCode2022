# --- Part Two ---
# It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number
# of pairs that overlap at all.
#
# In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs
# (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:
#
# 5-7,7-9 overlaps in a single section, 7.
# 2-8,3-7 overlaps all of the sections 3 through 7.
# 6-6,4-6 overlaps in a single section, 6.
# 2-6,4-8 overlaps in sections 4, 5, and 6.
# So, in this example, the number of overlapping assignment pairs is 4.
#
# In how many assignment pairs do the ranges overlap?

# check for overlap in the assignments
def check_overlap(a1, a2):
    a1_start = int(a1[0])
    a1_end = int(a1[1])
    a2_start = int(a2[0])
    a2_end = int(a2[1])

    # check if the 1st assignment overlaps 2nd assignment at all
    # do this by checking if the first assignment begins before second and ends during
    if a1_start <= a2_start <= a1_end <= a2_end:
        print("{} {} - yes overlap ".format(a1, a2))
        return 1
    # check the inverse case
    elif a2_start <= a1_start <= a2_end <= a1_end:
        print("{} {} - yes overlap ".format(a1, a2))
        return 1
    # check the engulfing case
    elif a1_start <= a2_start <= a2_end <= a1_end:
        print("{} {} - yes overlap ".format(a1, a2))
        return 1
    # check the inverse engulfing case
    elif a2_start <= a1_start <= a1_end <= a2_end:
        print("{} {} - yes overlap ".format(a1, a2))
        return 1
    else:
        # print("{} {} - no overlap ".format(a1, a2))
        return 0


# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    total_overlaps = 0

    # read through all the lines
    for line in lines:
        clean_line = line.replace("\n", "")

        # split the pairs
        pair = clean_line.split(",")

        # get the assignments
        assignment1 = pair[0].split("-")
        assignment2 = pair[1].split("-")

        # determine if there's overlap
        total_overlaps += check_overlap(assignment1, assignment2)

    print("Total overlapping assignments = {}".format(total_overlaps))

    f.close()

# --- Day 1: Calorie Counting ---
# part 2
# By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most
# Calories of food might eventually run out of snacks.
#
# To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top
# three Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have
# two backups.
#
# In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf (with 11000
# Calories), then the fifth Elf (with 10000 Calories). The sum of the Calories carried by these three elves is 45000.
#
# Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?

# Jacob's Solution

# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    # initialize counters
    max_calories = 0
    min_calories = 999999
    cur_calories = 0
    total_calories = 0
    total_calorie_items = 0
    total_calorie_groups = 0

    # array to capture calorie groups
    calorie_groups = []

    # read through all the lines
    for line in lines:
        # condition where the line is blank
        if line == "\n":
            # check if the current calories are the new max
            if cur_calories > max_calories:
                max_calories = cur_calories
            if cur_calories < min_calories:
                min_calories = cur_calories
            calorie_groups.append(cur_calories)
            cur_calories = 0
            total_calorie_groups += 1
        # check if it's a number greater than 0
        elif int(line) > 0:
            # add it to the "current calories"
            cur_calories += int(line)
            total_calories += int(line)
            total_calorie_items += 1

    # append the last group
    calorie_groups.append(cur_calories)

    # last check
    if cur_calories > max_calories:
        max_calories = cur_calories
        total_calorie_groups += 1

    # sort the list descending
    calorie_groups.sort(reverse=True)

    print("Top 3 elves are carrying {} calories".format(calorie_groups[0] + calorie_groups[1] + calorie_groups[2]))

    f.close()

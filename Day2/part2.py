# --- Part Two ---
# The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round
# needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.
# Good luck!"
#
# The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round
# ends as indicated. The example above now goes like this:
#
# In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also
# choose Rock. This gives you a score of 1 + 3 = 4.
# In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of
# 1 + 0 = 1.
# In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
# Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.
#
# Following the Elf's instructions for the second column, what would your total score be if everything goes exactly
# according to your strategy guide?

# return the score based on the two players' choices
def score_round(theirs, yours):
    score = 0

    # add the score
    # rock
    if yours == "X":
        # score you get for just picking this option
        score += 1

        # determine score based on result
        if theirs == "A":
            #tie
            score += 3
        elif theirs == "C":
            #win
            score += 6

    # paper
    elif yours == "Y":
        score += 2

        # determine score based on result
        if theirs == "B":
            #tie
            score += 3
        elif theirs == "A":
            #win
            score += 6

    # scissors
    elif yours == "Z":
        score += 3

        # determine score based on result
        if theirs == "C":
            #tie
            score += 3
        elif theirs == "B":
            #win
            score += 6

    return score


# return the move that you should make based on whether you're supposed to win, lose or tie
def choose_move(theirs, desired_outcome):
    # lose
    if desired_outcome == "X":
        # they play rock
        if theirs == "A":
            # choose scissors
            return "Z"
        # they play paper
        if theirs == "B":
            # choose rock
            return "X"
        # they play scissors
        if theirs == "C":
            # choose paper
            return "Y"
    # tie
    elif desired_outcome == "Y":
        # return the same move
        # they play rock
        if theirs == "A":
            # choose rock
            return "X"
        # they play paper
        if theirs == "B":
            # choose paper
            return "Y"
        # they play scissors
        if theirs == "C":
            # choose scissors
            return "Z"
    # win
    elif desired_outcome == "Z":
        # they play rock
        if theirs == "A":
            # choose paper
            return "Y"
        # they play paper
        if theirs == "B":
            # choose scissors
            return "Z"
        # they play scissors
        if theirs == "C":
            # choose rock
            return "X"


# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    total_points = 0

    # read through all the lines
    for line in lines:
        # condition where the line is blank
        round_play = line.replace("\n", "").split(" ")
        desired_move = choose_move(round_play[0], round_play[1])
        score = score_round(round_play[0], desired_move)
        total_points += score

        print("{} : {} : {}".format(round_play, desired_move, score))

    print("Total score = {}".format(total_points))
    f.close()

# --- Part Two ---
# Your device's communication system is correctly detecting packets, but still isn't working. It looks like it also
# needs to look for messages.
#
# A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather
# than 4.
#
# Here are the first positions of start-of-message markers for all of the above examples:
#
# mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
# bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
# nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
# nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
# zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
# How many characters need to be processed before the first start-of-message marker is detected?

def is_unique(packet):
    unique = True

    if len(packet) == 14:
        for j in range(0, len(packet)):
            if len(packet.replace(packet[j], "")) < 13:
                unique = False
    else:
        unique = False

    return unique


# first open the file
with open('input.txt') as f:
    lines = f.readlines()

    # read through all the lines
    for line in lines:
        line_clean = line.replace("\n", "")
        for i in range(14, len(line_clean)):
            check_string = line_clean[i - 14:i:]
            if is_unique(check_string):
                print("found start-of-message {} at character {}".format(check_string, i))
                break

import random


class Valve:
    def __init__(self, flow=0):
        self.flow = int(flow)
        # self.open = False
        self.neighbors = []

    def __lt__(self, obj):
        return ((self.flow) < (obj.flow))

    def __gt__(self, obj):
        return ((self.flow) > (obj.flow))

    def __le__(self, obj):
        return ((self.flow) <= (obj.flow))

    def __ge__(self, obj):
        return ((self.flow) >= (obj.flow))

    def __eq__(self, obj):
        return (self.flow == obj.flow)

    def __repr__(self):
        return str((self.a, self.b))

    def add_neighbor(self, other):
        # if other not in self.neighbors:
        self.neighbors.append(other)

    # def __str__(self):
    #     string = "[Flow Rate: {}] -> ".format(self.flow)
    #     string += "{" + ", ".join(["{}".format(n) for n in self.neighbors]) + "}"
    #     return string
    #
    # def __repr__(self):
    #     string = "[Flow Rate: {}] -> ".format(self.flow)
    #     string += "{" + ", ".join(["{}".format(n) for n in self.neighbors]) + "}"
    #     return string

    # def choose_neighbor(self):
    #     if self.open:
    #         return self.neighbors[random.randint(0, len(self.neighbors))]
    #     else:
    #         return self.neighbors_with_self[random.randint(0, len(self.neighbors_with_self))]


def get_flow(valves):
    total = 0
    for v in valves:
        total += valves[v].flow

    return total


def open_valves(valves, room_chain, minutes_left, flow_total=0, opened_valves=[]):
    room = room_chain[-2:]
    # print(room)
    if minutes_left < 0:
        return flow_total
    else:
        # print("{} [{} minutes left | {} flow total]".
        #      format(room, minutes_left, flow_total))

        for o in opened_valves:
            flow_total += valves[o].flow

        opened = False
        opened_valves = list(opened_valves)
        if room not in opened_valves:
            if valves[room].flow > 0 and minutes_left >= 1:
                opened_valves.append(room)
                opened = True

        # room = valves[room].neighbors[0]
        # print("{} {}: {} {} --> {}".format(minutes_left, room_chain, opened_valves, opened, flow_total))

        # print("{}".format(room_chain + room))
        if opened:
            return open_valves(valves, room_chain, minutes_left-1, flow_total, opened_valves)
        else:
            return max([open_valves(valves, room_chain + neighbor, minutes_left-1, flow_total, opened_valves) for neighbor in valves[room].neighbors])


def load_valves(filename):
    new_valves = {}
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            # parse the lines
            part1, part2 = line.replace("\n", "").split(";")
            valve, flow = part1.replace("Valve ", "").replace(" has flow rate=", ",").split(",")

            # check if it exists
            if valve in new_valves.keys():
                new_valves[valve].flow = int(flow)
            else:
                # create a new valve and add to the dict
                new_valves[valve] = Valve(flow)

            # parse the neighbors
            neighbors = part2.replace(" tunnels lead to valves ", "").replace(" tunnel leads to valve ", "").split(", ")

            # add neighbors
            for neighbor in sorted(neighbors, reverse=True):
                # add it if it's not in the dict
                if neighbor not in new_valves.keys():
                    new_valves[neighbor] = Valve(flow)

                new_valves[valve].add_neighbor(neighbor)

        f.close()
    return new_valves


valve_list = load_valves('example.txt')

for v in valve_list:
    print("{}: {} -> [{}]".format(v, valve_list[v].flow, ", ".join([n for n in valve_list[v].neighbors])))

print()

print("pressure released = {}".format(open_valves(valve_list, 'AA', 30)))

# follow_path(valve_list, path_list)
#
# valves = {}
# valves['AA'] = Valve('AA', 0)
# valves['BB'] = Valve('BB', 10)
# valves['CC'] = Valve('CC', 5)
# valves['DD'] = Valve('DD', 5)
# valves['EE'] = Valve('EE', 20)
#
# valves['AA'].add_neighbor(valves['BB'])
# valves['AA'].add_neighbor(valves['CC'])
# valves['DD'].add_neighbor(valves['EE'])
#
# print(valves['AA'])

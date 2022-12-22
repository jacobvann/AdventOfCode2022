class ValveState:
    def __init__(self,  room_chain, total_flow, minutes_left, opened_valves, room):
        self.room_chain = room_chain
        self.total_flow = total_flow
        self.minutes_left = minutes_left
        self.opened_valves = opened_valves
        self.room = room

    def __lt__(self, obj):
        return ((self.total_flow) < (obj.total_flow))

    def __gt__(self, obj):
        return ((self.total_flow) > (obj.total_flow))

    def __le__(self, obj):
        return ((self.total_flow) <= (obj.total_flow))

    def __ge__(self, obj):
        return ((self.total_flow) >= (obj.total_flow))

    def __eq__(self, obj):
        return (self.total_flow == obj.total_flow)

    def __repr__(self):
        return str((self.a, self.b))

    def __str__(self):
        return "rooms visited: {} | total flow: {} | mins left : {} | valves opened : {}".\
            format(self.room_chain, self.total_flow, self.minutes_left, self.opened_valves)


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


def open_valves(valves, room="AA", minutes_left=30, flow_total=0, opened_valves=[], should_open=False, room_chain="", depth=0, two_players=False):

    # initialize the "room chain"
    # this is just used for de-bugging
    if depth == 0 and room_chain == "":
        room_chain = room
    else:
        if should_open:
            room_chain += "->(open)"
        else:
            room_chain += "->" + room

    if should_open:
        opened_valves.append(room)

    if minutes_left <= 0:
        states.append(ValveState(room_chain, flow_total, minutes_left, opened_valves, room))
        return flow_total
    else:
        opened_valves = list(opened_valves)
        for o in opened_valves:
            flow_total += valves[o].flow

        candidates = []
        # build list of candidate rooms
        for n in valves[room].neighbors:
            candidates.append(n)

        # should I stay and open?
        if room not in opened_valves and valves[room].flow > 0:
            candidates.append(room)

        return max([open_valves(valves, next_room, minutes_left-1, flow_total, list(opened_valves), True if next_room == room else False, room_chain, depth+1, two_players)
                    for next_room in reversed(sorted(candidates, key=lambda x: valves[x].flow))])



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


valve_list = load_valves('input.txt')

for v in valve_list:
    print("{}: {} -> [{}]".format(v, valve_list[v].flow, ", ".join([n for n in valve_list[v].neighbors])))

print()

states = []

# pressure_released = open_valves(valve_list, 'AA', 10)

# run for the first 10 minutes
open_valves(valve_list, 'AA', 10)

# take the top 100 scenarios after 10 minutes, and run those for 10 more minutes
states_to_run = int(len(states) / 10)
for s in sorted(states)[-100:-1]:
    links = s.room_chain.split("->")
    links.pop()
    new_room_chain = "->".join(links)
    open_valves(valve_list, s.room, 10, s.total_flow, s.opened_valves, False, new_room_chain)

# then do it again
states_to_run = int(len(states) / 10)
for s in sorted(states)[-100:-1]:
    links = s.room_chain.split("->")
    links.pop()
    new_room_chain = "->".join(links)
    open_valves(valve_list, s.room, 10, s.total_flow, s.opened_valves, False, new_room_chain)

# get the best scenario
print(sorted(states)[-1])

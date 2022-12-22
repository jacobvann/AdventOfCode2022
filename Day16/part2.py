import itertools


class ValveState:
    def __init__(self,  chain1, chain2, room1, room2, total_flow, minutes_left, opened_valves):
        self.chain1 = chain1
        self.chain2 = chain2
        self.room1 = room1
        self.room2 = room2
        self.total_flow = total_flow
        self.minutes_left = minutes_left
        self.opened_valves = opened_valves

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
        return "total flow: {} | mins left : {} | valves opened : {}\nelf journey: {}\nelephant journey: {}".\
            format(self.total_flow, self.minutes_left, self.opened_valves, self.chain1, self.chain2)


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


# yep this is ugly - i just duplicated code for elf and elephant.  If i were smarter I would for loop some of it
def open_valves(valves, minutes_left, flow_total, opened_valves, room1='AA', room2='AA', open1='', open2='', chain1='', chain2='', two=False):

    # initialize the "room chain"
    # this is just used for de-bugging
    # elf
    if chain1 == '':
        chain1 = room1
    else:
        if room1 == open1:
            chain1 += "->(open)"
        else:
            chain1 += "->" + room1

    if open1 in valves and open1 not in opened_valves:
        opened_valves.append(open1)

    # elephant
    if chain2 == '':
        chain2 = room2
    else:
        if room2 == open2:
            chain2 += "->(open)"
        else:
            chain2 += "->" + room2

    if open2 in valves and open2 not in opened_valves:
        opened_valves.append(open2)

    if minutes_left <= 0:
        states.append(ValveState(chain1, chain2, room1, room2, flow_total, minutes_left, opened_valves))
        return flow_total
    else:
        opened_valves = list(opened_valves)
        for o in opened_valves:
            if o in valves:
                flow_total += valves[o].flow

        # the elf
        candidates1 = []
        # build list of candidate rooms
        if room1 in valves:
            for n in valves[room1].neighbors:
                candidates1.append(n)

        # should I stay and open?
        if room1 not in opened_valves and valves[room1].flow > 0:
            candidates1.append(room1)

        sorted_candidates1 = sorted(candidates1)

        # the elephant
        if two:
            candidates2 = []
            # build list of candidate rooms
            if room2 in valves:
                for n in valves[room2].neighbors:
                    candidates2.append(n)

            # should I stay and open?
            if room2 not in opened_valves and valves[room2].flow > 0:
                candidates2.append(room2)

            sorted_candidates2 = sorted(candidates2)

            # create a cartesian of all the elf's possible choices and elephant's possible choices
            candidates_combined = itertools.product(sorted_candidates1, sorted_candidates2)

            # I'm not sure, but it works :)
            # cycles through all the possible candidates and recursively calls open_valves
            # returns the max value returned
            # ... need to make it work with two players by updating both "next rooms"
            return max([open_valves(valves, minutes_left - 1, flow_total, list(opened_valves), n1, n2,
                                    n1 if n1 == room1 else '', n2 if n2 == room2 else '',
                                    chain1, chain2, two)
                        for n1, n2 in candidates_combined])

        else:
            # I'm not sure, but it works :)
            # cycles through all the possible candidates and recursively calls open_valves
            # returns the max value returned
            # ... need to make it work with two players by updating both "next rooms"
            return max([open_valves(valves, minutes_left-1, flow_total, list(opened_valves), nxt, '',
                                    nxt if nxt == room1 else '',  '',
                                    chain1, '', two)
                        for nxt in sorted_candidates1])


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

list_one = ["AA", "BB", "CC", "DD"]
list_two = ["BB", "CC", "AA"]

# print(["--{}-{}--".format(n[0], n[1]) for n in list(zip(list_one, list_two))])
# new_list = list(itertools.product(list_one, list_two))
#
# print(new_list)
# for x, y in new_list:
#     print("{}, {}".format(x, y))

states = []

# pressure_released = open_valves(valve_list, ['AA'], 10)

# run for the first 10 minutes
# valves, minutes_left, flow_total, opened_valves, room1, room2, open1, open2, chain1='', chain2='', two=False

two_players = True
open_valves(valve_list, 7, 0, [], two=two_players)

state_count = 1
print("{} .".format(state_count))

# take the top 100 scenarios after 8 minutes, then repeat with those
states_to_run = int(len(states) / 10)
i = 0
for s in sorted(states)[-100:-1]:
    links = list(s.chain1.split("->"))
    links.pop()
    _chain1 = "->".join(links)
    links = list(s.chain2.split("->"))
    links.pop()
    _chain2 = "->".join(links)
    open_valves(valve_list, 7, s.total_flow, s.opened_valves, s.room1, s.room2, '', '', _chain1, _chain2, two_players)
    i += 1
    print("{}:{} .".format(state_count, i))

# take the top 100 scenarios after 8 minutes, then repeat with those
i = 0
states_to_run = int(len(states) / 10)
for s in sorted(states)[-100:-1]:
    links = list(s.chain1.split("->"))
    links.pop()
    _chain1 = "->".join(links)
    links = list(s.chain2.split("->"))
    links.pop()
    _chain2 = "->".join(links)
    open_valves(valve_list, 6, s.total_flow, s.opened_valves, s.room1, s.room2, '', '', _chain1, _chain2, two_players)
    i += 1
    print("{}:{} .".format(state_count, i))

# take the top 100 scenarios after 8 minutes, then repeat with those
states_to_run = int(len(states) / 10)
i = 0
for s in sorted(states)[-100:-1]:
    links = list(s.chain1.split("->"))
    links.pop()
    _chain1 = "->".join(links)
    links = list(s.chain2.split("->"))
    links.pop()
    _chain2 = "->".join(links)
    i += 1
    print("{}:{} .".format(state_count, i))

# get the best scenario
print(sorted(states)[-1])

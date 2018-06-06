import argparse
import random
from collections import defaultdict

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--nodes", type=int, help="number of nodes")
parser.add_argument("-i", '--iterations', type=int, help="number of iterations")
parser.add_argument('--your-algorithm', action='store_true')

args = parser.parse_args()
random.seed()
not_visited_nodes = list(range(args.nodes))

class Tree:
    def __init__(self, value):
        self.value = value
        self.children = []  # list of node objects
        self.sent = []  # list of numbers of nodes

    def add_child(self, obj):
        self.children.append(Tree(obj))
        self.sent.append(obj)

    def create_children(self):
        random.seed()
        children = random.sample(range(args.nodes), 4)
        for node in children:
            self.add_child(node)

    def create_better_children(self):
        random.seed()
        global not_visited_nodes
        children = random.sample(not_visited_nodes, 4)
        for node in children:
            self.add_child(node)


def put_children(node):
    for child in node.children:
        network[child.value] = True



def spread(node):
    if not forest[node.value]:
        node.create_children()
        forest[node.value] = node.sent
        network[node.value] = True
        for child in node.children:
            network[child.value] = True
        for child in node.children:
            spread(child)

def better_spread():
    not_visited = list(range(nodes))

    while not_visited:
        visited = []
        for node in not_visited:
            next_nodes = random.sample(range(nodes), 4)
            for n in next_nodes:
                if not network[n]:
                    visited.append(n)
                    network[n] = True
        not_visited = visited

all_runs = []
iterations = args.iterations
while iterations:
    nodes = args.nodes
    network = dict.fromkeys(range(nodes))  # nodes visited
    forest = defaultdict(list)  # nodes paths

    starting_node = random.randint(0, len(network) - 1)
    starting_tree = Tree(starting_node)
    network[starting_node] = True
    if args.your_algorithm:
        better_spread()
    else:
        spread(starting_tree)

    not_v = 0
    for k, v in network.items():
        if not v:
            not_v += 1
    suc_percent = (len(network) - not_v) * 100 / len(network)
    all_runs.append(suc_percent)
    iterations -= 1

fails = 0
for i in all_runs:
    if i != 100:
        fails += 1
precision = (len(all_runs) - fails) * 100 / len(all_runs)

print(f'In {precision :.2f}% cases all nodes received the packet')

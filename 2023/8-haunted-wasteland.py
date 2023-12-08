import math

def traverse(dirs, nodes_map):
    D, d = len(dirs), 0
    node = "AAA"
    while node != "ZZZ":
        nx = 0 if dirs[d % D] == "L" else 1
        node = nodes_map[node][nx]
        d += 1
    return d


def traverse_single(node, dirs, nodes_map):
    D, d = len(dirs), 0
    while not node.endswith("Z"):
        nx = 0 if dirs[d % D] == "L" else 1
        node = nodes_map[node][nx]
        d += 1
    return d



def traverse2(dirs, nodes_map):
    nodes = (n for n in nodes_map.keys() if n.endswith("A"))
    single_len = [traverse_single(node, dirs, nodes_map) for node in nodes]
    return math.lcm(*single_len)

if __name__ == "__main__":
    with open("../inputs/2023/8.txt") as f:
        dirs, nodes = f.read().strip().split("\n\n")
        nodes_map = {node.strip(): tuple(p.strip() for p in paths.strip()[1:-1].split(','))
            for node, paths in (nmap.split("=") for nmap in nodes.strip().split("\n"))}

    print(traverse(dirs, nodes_map))
    print(traverse2(dirs, nodes_map))

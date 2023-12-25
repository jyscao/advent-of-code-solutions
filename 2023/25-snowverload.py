import networkx as nx
import matplotlib.pyplot as plt


def get_edge_list(data):
    conn_map = {src: dests.strip().split() for src, dests in data}
    edges_map = []
    for src, dests in conn_map.items():
        for dst in dests:
            edges_map.append((src, dst))
    return edges_map


def remove_edges(edge_list, edges_to_remove):
    N, R = len(edge_list), len(edges_to_remove)

    to_remove = set()
    for a, b in edges_to_remove:
        to_remove.add((a, b))
        to_remove.add((b, a))

    reduced_list = [edge for edge in edge_list if edge not in to_remove]
    assert len(reduced_list) == N - R
    return reduced_list



if __name__ == "__main__":
    with open("../inputs/2023/25.txt") as f:
        data = [line.strip().split(": ") for line in f.readlines()]

    test_data = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
    """
    data = [line.strip().split(": ") for line in test_data.strip().splitlines()]

    edge_list = get_edge_list(data)

    # (zhg, fmr), (krf, crg), (rgv, jct) <- these are obtained by inspecting the graph
    edge_list = remove_edges(edge_list, (("zhg", "fmr"), ("krf", "crg"), ("rgv", "jct")))

    G = nx.Graph(edge_list)
    nx.draw_networkx(G, with_labels=True)
    plt.show()

    # "dcl" and "jvd" are in separate partitions
    g_a = nx.node_connected_component(G, "dcl")
    g_b = nx.node_connected_component(G, "jvd")
    a, b = len(g_a), len(g_b)
    print(a, b, a * b)

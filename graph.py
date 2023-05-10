import ast
from graphviz import Digraph


def draw_graph(nodes, critical_path):
    def parse(nodes):
        new = []
        for i in nodes:
            nodes = i[0].split(',')
            if len(nodes) > 1:
                for node in nodes:
                    new.append((node, i[1]))
            else:
                new.append((i[0], i[1]))
        return new

    parsed_nodes = parse(nodes)

    def get_unoq_nodes(nodes):
        uniq_nodes = set()
        for i in nodes:
            nodes = i[0].split(',')
            if len(nodes) > 1:
                for node in nodes:
                    uniq_nodes.add(i[1])
            else:
                uniq_nodes.add(i[1])
                uniq_nodes.add(i[0])
        return sorted(uniq_nodes)

    def get_edges(parsed_nodes):
        edges = []
        for node in parsed_nodes:
            edges.append(((node[0]), node[1]))
        return edges

    def get_critical_path_edges(critical_path):
        edges = []
        for i in range(len(critical_path) - 1):
            edges.append((critical_path[i], critical_path[i + 1]))
        return edges

    def get_all_edges(edges, critical_path_edges):
        all_edges = []
        for edge in edges:
            all_edges.append(edge)
            if edge in critical_path_edges:
                all_edges.append(edge)
        return all_edges

    dot = Digraph(comment='The Test Table')
    dot.body.append("rankdir=LR")

    uniq_nodes = get_unoq_nodes(nodes)
    for node in uniq_nodes:
        dot.node(node, node)
    critical_path_edges = get_critical_path_edges(ast.literal_eval(critical_path))
    edges = get_edges(parsed_nodes)
    all_edges = get_all_edges(get_edges(parsed_nodes), critical_path_edges)

    # dot.edges(edges)
    # dot.edges(all_edges)
    for edge in edges:
        color = 'red' if edge in critical_path_edges else 'black'
        dot.edge(edge[0], edge[1], color=color)

    dot.view('test-output/test-table.gv')

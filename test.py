from graphviz import Digraph
import ast


# dot = Digraph(comment='The Test Table')
# critical_path = "['A', 'B', 'C', 'E', 'G', 'I']"
# critical_path = ast.literal_eval(critical_path)
# nodes = [('A', 'B'), ('B', 'C'), ('B', 'D'), ('C,D', 'E'), ('A', 'F'), ('E', 'G'), ('E', 'H'), ('F,G,H', 'I')]
# parsed_nodes = [('A', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('A', 'F'), ('E', 'G'), ('E', 'H'),
#               ('F', 'I'), ('G', 'I'), ('H', 'I')]

# dot = Digraph(comment='The Test Table')
# critical_path = "['A', 'B', 'C', 'E', 'F', 'J', 'L', 'N', 'O']"
# critical_path = ast.literal_eval(critical_path)
# nodes = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('C', 'E'), ('C', 'I'), ('D', 'G'), ('G, E', 'H'), ('E', 'F'),
#          ('F,I', 'J'),  ('H', 'M'), ('J', 'K'), ('J', 'L'), ('K,L', 'N'), ('M', 'O'), ('N', 'O'), ]
# parsed_nodes = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('C', 'E'), ('C', 'I'), ('D', 'G'), ('E', 'H'), ('E', 'F'),
#                 ('F', 'J'), ('I', 'J'), ('G', 'H'), ('J', 'K'), ('J', 'L'),  ('H', 'M'), ('K', 'N'), ('L', 'N'),
#                ('M', 'O'), ('N', 'O')]

dot = Digraph(comment='The Test Table')
critical_path = "['A', 'C', 'E', 'G']"
critical_path = ast.literal_eval(critical_path)
nodes = [('Нач узел', 'B'), ('Нач узел', 'A'), ('B', 'E'), ('A', 'C'), ('C', 'E'), ('E', 'G'), ('A', 'D'), ('D', 'F'), ('G', 'Конеч узел'), ('F', 'Конеч узел')]
parsed_nodes = [('Нач узел', 'B'), ('Нач узел', 'A'), ('B', 'E'), ('A', 'C'), ('C', 'E'), ('E', 'G'), ('A', 'D'), ('D', 'F'), ('G', 'Конеч узел'), ('F', 'Конеч узел')]



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


uniq_nodes = get_unoq_nodes(nodes)
for node in uniq_nodes:
    dot.node(node, node)
critical_path_edges = get_critical_path_edges(critical_path)
edges = get_edges(parsed_nodes)
all_edges = get_all_edges(get_edges(parsed_nodes), critical_path_edges)

dot.body.append("rankdir=LR")
# dot.edges(edges)
# dot.edges(all_edges)
for edge in edges:
    color = 'red' if edge in critical_path_edges else 'black'
    dot.edge(edge[0], edge[1], color=color)
pass

# Сохранить исходный код в файл и предоставить движок Graphviz
# dot.render('test-output/test-table.gv', view=True)
dot.view('test-output/test-table.gv')

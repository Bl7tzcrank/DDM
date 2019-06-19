import networkx as nx

g = nx.DiGraph()
g.add_node("1", label = "3[0,3,1]0 E:1.5")
g.add_node("2", label = "4[0,3,3]1 E:0.5")
g.add_node("3", label = "3[0,3,2]0 E:0.0")

g.add_edges_from([("1", "2")], label = 1)
g.add_edges_from([("1", "3")], label = 1)
p=nx.drawing.nx_pydot.to_pydot(g)
p.write_png('test.png')

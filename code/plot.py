import networkx as nx

def createGraph(dict):
    g = nx.DiGraph()
    for k in dict.keys():
        g.add_node(k)
    for k in dict.keys():
        for s in dict[k]["successors"]:
            g.add_edges_from(([(k, s[0])]))
    p=nx.drawing.nx_pydot.to_pydot(g)
    p.write_png('example.png')

def createGraphWithStates(dict):
    g = nx.DiGraph()
    for k in dict.keys():
        g.add_node(k, label = str(dict[k]["obj"].getDestination()) + str(dict[k]["obj"].getRequests()) + str(dict[k]["obj"].getDelta()) + ' E:' + str(round(dict[k]["obj"].getExpectedValue(),2)))
    for k in dict.keys():
        for s in dict[k]["successors"]:
            g.add_edges_from([(k, s[0])], label = str(' ') + str(round(s[1],2)))
    p=nx.drawing.nx_pydot.to_pydot(g)
    p.write_png('example.png')

"""G = nx.DiGraph()

G.add_node("ROOT")

for i in range(30):
    G.add_node("Child_%i" % i)
    G.add_node("Grandchild_%i" % i)
    G.add_node("Greatgrandchild_%i" % i)

    G.add_edge("ROOT", "Child_%i" % i)
    G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
    G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

A = nx.nx_agraph.to_agraph(G)
A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
A.draw('test.png')

p=nx.drawing.nx_pydot.to_pydot(G)
p.write_png('example.png')"""
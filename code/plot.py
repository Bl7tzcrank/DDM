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

#prints a graph
def createGraphWithStates(dict):
    g = nx.DiGraph()
    for k in dict.keys():
        g.add_node(k, label = str(dict[k]["obj"].getDestination()) + str(dict[k]["obj"].getRequests()) + str(dict[k]["obj"].getDelta()) + ' E:' + str(round(dict[k]["obj"].getExpectedValue(),2)))
    for k in dict.keys():
        for s in dict[k]["successors"]:
            g.add_edges_from([(k, s[0])], label = str(' ') + str(round(s[1],2)))
    p=nx.drawing.nx_pydot.to_pydot(g)
    p.write_png('example.png')

#prints a seperated graph 
def createSplitGraphWithStates(dict):
    splitters = dict[dict["root"]["successors"][0][0]]["successors"][:]
    nodes_persplitter = []
    for s in splitters:
        nodes = [s]
        buffer = [s]
        while len(buffer) > 0:
            nodes = nodes + (dict[buffer[0][0]]["successors"])
            buffer = buffer + (dict[buffer[0][0]]["successors"])
            del buffer[0]
        nodes_persplitter.append(nodes)

    splitters.append(("root","x"))
    splitters.append((dict["root"]["successors"][0][0],"x"))
    r = nx.DiGraph()
    for k in splitters:
        r.add_node(k[0], label = str(dict[k[0]]["obj"].getDestination()) + str(dict[k[0]]["obj"].getRequests()) + str(dict[k[0]]["obj"].getDelta()) + ' E:' + str(round(dict[k[0]]["obj"].getExpectedValue(),2)))
    for k in splitters:
        if k[1] == "x":
            for s in dict[k[0]]["successors"]:
                r.add_edges_from([(k[0], s[0])], label = str(' ') + str(round(s[1],2)))
    p=nx.drawing.nx_pydot.to_pydot(r)
    p.write_png("example.png")

    file_number = 0
    for n in nodes_persplitter:
        g = nx.DiGraph()
        for k in n:
            g.add_node(k[0], label = str(dict[k[0]]["obj"].getDestination()) + str(dict[k[0]]["obj"].getRequests()) + str(dict[k[0]]["obj"].getDelta()) + ' E:' + str(round(dict[k[0]]["obj"].getExpectedValue(),2)))
        for k in n:
            for s in dict[k[0]]["successors"]:
                g.add_edges_from([(k[0], s[0])], label = str(' ') + str(round(s[1],2)))
        p=nx.drawing.nx_pydot.to_pydot(g)
        output_name = ('example' + str(file_number) + '.png')
        file_number = file_number + 1
        p.write_png(output_name)
class Node:
    def __init__(self, name, childs):
        self.name = name
        self.childs = childs
    
    def getName(self):
        return self.name
    
    def getChilds(self):
        return self.childs

def getTree(node):
    print(node.getName())
    if(len(node.getChilds()) > 0):
        for child in node.getChilds():
            getTree(child)

node1 = Node("node1",[])
node2 = Node("node2",[])
node3 = Node("node3",[node1, node2])
node4 = Node("node4",[node3])
getTree(node4)
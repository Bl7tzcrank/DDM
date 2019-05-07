import itertools

class Node:
    def __init__(self, destination, requests, delta, predecision):
        self.childs = []
        self.state = {
            "destination": destination,
            "requests": requests,
            "delta": delta
        }
        self.predecision = predecision
    
    def getChilds(self):
        return self.childs
    
    def getState(self):
        return self.state
    
    #creates a list of nodes
    def getSuccessorStates(self):
        w = [0,1]
        #in case of S0->S0x    

        #in case of S0x->S1, covers to exegeneous influence on request states
        if not(self.predecision):
            #all the possible request realisations for each customer: list with sublist for each customer
            realisations = []
            for i in range(len(self.state["requests"])): 
                #all possible realisations of r per customer
                client_realisations = []
                for w1 in w:              
                    if (w1 == 1) and self.state["requests"][i] == 0:
                        client_realisations.append(1)
                    else: 
                        client_realisations.append(self.state["requests"][i])
                realisations.append(client_realisations)
            #build all possible combinations taking into account the realisations per customer: 1 can be 0,1; 2 can be 1 --> 0,1 and 1,1. Case distinction if only 1 customer.
            if(len(realisations) > 1):
                listoflists = [list(p) for p in (list(set(itertools.product(*realisations))))]
                return listoflists
            else:
                listoflists = [[p] for p in set(realisations[0])]
                return listoflists

def getManhattan(coordinates):
    distances = []
    for c1 in coordinates:
        row = []
        for c2 in coordinates:    
            row.append(abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]))
        distances.append(row)
    return(distances)

Node1 = Node("Hamburg", [1], 3, False)
print(Node1.getSuccessorStates())
#coordinates = [(1,1),(2,2),(3,3)]
#print(getManhattan(coordinates))
import itertools

#Classes
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
    
    def getDestination(self):
        return self.state["destination"]

    def getRequests(self):
        return self.state["requests"]
    
    def getDelta(self):
        return self.state["delta"]
    
    def getPredecision(self):
        return self.predecision

class StateSpaceCreator:
    def __init__(self, init, coordinates):
        self.init = init
        self.coordinates = coordinates
        self.distances = getManhattan(coordinates)

    def getInit(self):
        return self.init

    def getCoordinates(self):
        return self.coordinates

    def getDistances(self):
        return self.distances

    def createStateSpace(self):
        new_states=(self.getSuccessorStates(self.init))
        for n in new_states:
            print(n.getState())

    #creates a list of successor state-nodes for a given state-node
    def getSuccessorStates(self, node):
        
        #in case of S0->S0x, covers the decision's influence on request states
        if(node.getPredecision()):
        #1.Calculate Route in case there are new requests (=1). Include =2. Transmit old route from parent for the case that it does not need to be recalculated?

        #2.Distinct the case wait/no wait if route takes max remaining time-1
            return 0

        #in case of S0x->S1, covers to exegeneous influence on request states
        if not(node.getPredecision()):
            w = [0,1]
            #1.Regarding customer requests
            #all the possible request realisations for each customer: list with sublist for each customer
            realisations = []
            for i in range(len(node.getRequests())): 
                #all possible realisations of r per customer
                client_realisations = []
                for w1 in w:              
                    if (w1 == 1) and node.getRequests()[i] == 0:
                        client_realisations.append(1)
                    else: 
                        client_realisations.append(node.getRequests()[i])
                realisations.append(client_realisations)
            #build all possible combinations taking into account the realisations per customer: 1 can be 0,1; 2 can be 1 --> 0,1 and 1,1. Case distinction if only 1 customer.
            if(len(realisations) > 1):
                requestlist = [list(p) for p in (list(set(itertools.product(*realisations))))]
            else:
                requestlist = [[p] for p in set(realisations[0])]
            #2.Regarding delta
            new_delta = node.getDelta()-1 if node.getDelta() != 0 else 0
            #create new states
            new_states = []
            for r in requestlist:
                new_states.append(Node(node.getDestination(), r, new_delta, not(node.getPredecision())))     
            return new_states

#Helpers
def getManhattan(coordinates):
    distances = []
    for c1 in coordinates:
        row = []
        for c2 in coordinates:    
            row.append(abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]))
        distances.append(row)
    return(distances)

##experiments
coordinates = [(1,1),(2,2),(3,3)]
Node1 = Node("Hamburg", [0,0], 3, False)
stateSpaceCreator = StateSpaceCreator(Node1, coordinates)
#print(Node1.getRequests())
stateSpaceCreator.createStateSpace()
#print(stateSpaceCreator.getDistances())

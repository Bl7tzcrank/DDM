import itertools
from tsp_solver import * 

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
    def __init__(self, init, start, end, customer_coordinates):
        self.init = init
        self.start = start
        self.end = end
        self.customer_coordinates = customer_coordinates  
        self.distances = getManhattan(start+end+customer_coordinates)
        self.route = []

    def getInit(self):
        return self.init

    def getCustomerCoordinates(self):
        return self.customer_coordinates

    def getDistances(self):
        return self.distances

    def createStateSpace(self):
        """new_states=(self.getSuccessorStates(self.init))
        for n in new_states:
            print(n.getState())"""
        self.getSuccessorStates(self.init)

    #returns list of coordinates of customers with request state 2
    def getOldCustomer(self,requests):
        cors = []
        for i in range(len(self.customer_coordinates)):
            if requests[i] == 2:
                cors.append(self.customer_coordinates[i])
        return cors

    #returns list of coordinates of customers with request state 1
    def getNewCustomers(self,requests):
        cors = []
        for i in range(len(self.customer_coordinates)):
            if requests[i] == 1:
                cors.append(self.customer_coordinates[i])
        return cors

    #creates a list of successor state-nodes for a given state-node
    def getSuccessorStates(self, node):
        
        ##in case of S0->S0x, covers the decision's influence on request states
        if(node.getPredecision()):
        #1.Calculate Route 
            if(not self.route): #in case there has never been a route calculated, in case there are new requests (=1). Include =2. Transmit old route from parent for the case that it does not need to be recalculated?
                tsp = tsp_solver(self.start,self.end,self.getOldCustomer(node.getRequests()),self.getNewCustomers(node.getRequests()),node.getDelta())
                self.tour = tsp.solveTSP()
        #2.Distinct the case wait/no wait if route takes max remaining time-1
            

        ##in case of S0x->S1, covers to exegeneous influence on request states
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
start = [(1,1)]
end = [(2,1)]
customer_coordinates = [(4,1),(4,4)]
Node1 = Node("Hamburg", [1,1], 11, True)
stateSpaceCreator = StateSpaceCreator(Node1, start, end, customer_coordinates)
#print(Node1.getRequests())
stateSpaceCreator.createStateSpace()
#print(stateSpaceCreator.getDistances())

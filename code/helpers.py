import itertools
from tsp_solver import * 

#Classes
class Node:
    def __init__(self, destination, requests, delta, time_left, predecision, id=None):
        self.state = {
            "destination": destination,
            "requests": requests,
            "delta": delta
        }
        self.time_left = time_left
        self.predecision = predecision #True: St -> Stx, False: Stx -> St+1
        self.id = id if id is not None else 'root'
    
    def getState(self):
        return self.state
    
    def getDestination(self):
        return self.state["destination"]

    def getRequests(self):
        return self.state["requests"]
    
    def getDelta(self):
        return self.state["delta"]
    
    def getTimeLeft(self):
        return self.time_left
    
    def getPredecision(self):
        return self.predecision
    
    def getID(self):
        return self.id

class Graph:
    def __init__(self):
        self.graphdict = {}
    
    def getGraph(self):
        return self.graphdict
    
    def addNode(self, node, predecessor, successors):
        successor_ids = []
        for c in successors:
            successor_ids.append((c[0].getID(),c[1]))
        self.graphdict[node.getID()].update({
            "successors": successor_ids # der ist schon da und es muss nur successor angepasst werden
        })
        for s in successors:
            self.graphdict[s[0].getID()] = {
                "obj": s[0],
                "predecessor": (node.getID(), s[1]),
                "successors": []
            }   

class StateSpaceCreator:
    def __init__(self, init, start, end, customer_coordinates, getCustomerBehavior, tour=None):
        self.init = init
        self.start = start
        self.end = end
        self.customer_coordinates = customer_coordinates
        self.all_coordinates = start+end+customer_coordinates  
        self.distances = getManhattan(start+end+customer_coordinates)
        self.tour = tour if tour is not None else []
        self.id_counter = 0
        self.getCustomerBehavior = getCustomerBehavior

    def getInit(self):
        return self.init

    def getCustomerCoordinates(self):
        return self.customer_coordinates

    def getDistances(self):
        return self.distances

    def getID(self, time_left):
        self.id_counter = self.id_counter + 1
        return (str(time_left) + str('.') + str(self.id_counter))

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
    
    def createStateSpace(self):

        """state_space = Graph()
        active = self.init
        state_space.graphdict[active.getID()] = {
                "obj": active,
                "predecessor": [],
                "successors": []
            }   
        new_states=(self.getSuccessorStates(active)) 
        for n in new_states:
            print(n[0].getState())
        state_space.addNode(active, [], new_states)
        print(state_space.getGraph())"""

        state_space = Graph()
        childs = [self.init]
        active = self.init
        state_space.graphdict[active.getID()] = {
                "obj": active,
                "predecessor": [],
                "successors": []
            }   
        while len(childs) > 0:
            new_states=(self.getSuccessorStates(active)) 
            for n in new_states:
                print("#####STATE#####")
                print(n[0].getState())
                childs.append(n[0])
            state_space.addNode(active, [], new_states)
            del childs[0]
            if len(childs) > 0:
                active = childs[0]    
        print(state_space.getGraph())

    #creates a list of successor state-nodes for a given state-node
    def getSuccessorStates(self, node):  
        new_states = []
        ##in case of S0->S0x, covers the decision's influence on request states
        if(node.getPredecision()):
            #counts the confirmed customer requests
            profit = 0
            new_requestStates = []
            #calculate Route 
            if(True): #in case there has never been a route calculated, in case there are new requests (=1). Include =2. Transmit old route from parent for the case that it does not need to be recalculated?
                print('TSP-Input')
                print(self.start)
                print(self.end)
                print(self.getOldCustomer(node.getRequests()))
                print(self.getNewCustomers(node.getRequests()))
                print(node.getTimeLeft()-node.getDelta())
                print(self.all_coordinates[node.getDestination()])
                tsp = tsp_solver([self.all_coordinates[node.getDestination()]],self.end,self.getOldCustomer(node.getRequests()),self.getNewCustomers(node.getRequests()),node.getTimeLeft()-node.getDelta())
                self.tour = tsp.solveTSP()
                print('Tour:')
                print(self.tour)
            #accecpt/reject: set customers to 2 or 3 depending on whether they are included in the tour or not. Keep if 0 or 3
            for i in range(len(node.getRequests())):
                if i+2 in self.tour:
                    new_requestStates.append(2)
                    profit = profit + 1
                elif (i+2 not in self.tour) and (node.getRequests()[i] == 1):                       
                    new_requestStates.append(3)
                else:
                    new_requestStates.append(node.getRequests()[i])
            #check if arrived and open customer requests
            if (node.getDelta() == 0) and (2 in new_requestStates):#muss auch losfahren, wenn Zeit knapp wird
                tour_length = getTourDistance(self.tour, self.distances)
                wait_possible = node.getTimeLeft()-tour_length > 0

                #wait possible
                if wait_possible:
                    new_states.append((Node(node.getDestination(), new_requestStates, node.getDelta(), node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
                #wait not possible and default
                #Set next destination. Set to 3 for next customer
                changed_new_requestStates = [] #necessary!
                for i in range(len(new_requestStates)):
                    if (i+2 == self.tour[1]):
                        changed_new_requestStates.append(3)
                    else:
                        changed_new_requestStates.append(new_requestStates[i])
                new_states.append((Node(self.tour[1], changed_new_requestStates, self.distances[node.getDestination()][self.tour[1]], node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
            #if arrived and no open customer request --> wait only if enough time left
            elif (node.getDelta() == 0) and not (2 in new_requestStates):
                tour_length = getTourDistance(self.tour, self.distances)
                wait_possible = node.getTimeLeft()-tour_length > 0

                #wait possible
                if wait_possible:
                    new_states.append((Node(node.getDestination(), new_requestStates, node.getDelta(), node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
                else:
                    new_states.append((Node(self.tour[1], new_requestStates, self.distances[node.getDestination()][self.tour[1]], node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
            #if not arrived or no open customer request
            else:
                new_states.append((Node(node.getDestination(), new_requestStates, node.getDelta(), node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
            
            return (new_states)    

        ##in case of S0x->S1, covers to exegeneous influence on request states
        else:
            if((node.getTimeLeft()-1) > 0):
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
                    new_states.append((Node(node.getDestination(), r, new_delta, node.getTimeLeft()-1, not(node.getPredecision()), self.getID(node.getTimeLeft())), self.getCustomerBehavior(node.getTimeLeft()-1,r)))
                return new_states
            else: 
                return([])

#Helpers
def getManhattan(coordinates):
    distances = []
    for c1 in coordinates:
        row = []
        for c2 in coordinates:    
            row.append(abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]))
        distances.append(row)
    return(distances)

def getTourDistance(tour, distances):
    dist = 0
    for t in range(len(tour)-1):
        dist = dist + distances[tour[t]][tour[t+1]]
    return(dist)

##experiments
start = [(1,1)] #dest 0
end = [(3,1)] #dest 1
customer_coordinates = [(2,1)] #dest2,...
def getCustomerBehavior(time_left, customers):
    return 0.4

Node1 = Node(0, [0], 0, 3, True)
stateSpaceCreator = StateSpaceCreator(Node1, start, end, customer_coordinates, getCustomerBehavior)
#print(Node1.getRequests())
stateSpaceCreator.createStateSpace()
#print(stateSpaceCreator.getDistances())
#print(getTourDistance([0,2,1],getManhattan([(1,1),(2,1),(4,1),(4,4)])))
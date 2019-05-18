import itertools
from tsp_solver import * 
from plot import *

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

    def printStateSpace(self, dict):
        for k in dict.keys():
            print("-----")
            print(k)
            print("State:" , end =" ")
            print(dict[k]["obj"].getState())
            print("Predecessor:" , end =" ")
            print(dict[k]["predecessor"]) 
            print("Successors:" , end =" ")
            print(dict[k]["successors"])

    def createStateSpace(self):

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
                childs.append(n[0])
                print('####')
                print(n[0].getState())
            state_space.addNode(active, [], new_states)
            del childs[0]
            if len(childs) > 0:
                active = childs[0]    
        self.printStateSpace(state_space.getGraph())
        createGraphWithStates(state_space.getGraph())

    #creates a list of successor state-nodes for a given state-node including edge weight (profit or likelihood)
    def getSuccessorStates(self, node):  
        new_states = []
        ##in case of S0->S0x, covers the decision's influence on request states
        if(node.getPredecision()):
            if((node.getTimeLeft()) > 0):
                #counts the confirmed customer requests
                profit = 0
                new_requestStates = []
                #calculate Route 
                if(True): #in case there has never been a route calculated, in case there are new requests (=1). Include =2. Transmit old route from parent for the case that it does not need to be recalculated?
                    #Create a customer dictionary to assign customer ids to tour input. The tour input is start+end+active+new customers. The customers are numbered 2,3,...
                    #For a customer request status of [0,1], the dict would be [0,1,3] while the tour might return a [0,2,1] where customer 3 is on the second step of the route, but indicated by a 2.
                    #The dictionary can now identify, that the 2 is customer 3 by doing tour_dict[2] = 3
                    tour_dict = [] #3 in tour -> tour_dict[3]
                    tour_dict.append(node.getDestination())
                    tour_dict.append(1)
                    for i in range(len(node.getRequests())):
                        if node.getRequests()[i] == 2:
                            tour_dict.append(i+2)
                    for i in range(len(node.getRequests())):
                        if node.getRequests()[i] == 1:
                            tour_dict.append(i+2)
                    print('#TSPINPUT#')
                    print(str([self.all_coordinates[node.getDestination()]]) + str(self.end) + str(self.getOldCustomer(node.getRequests())) + str(self.getNewCustomers(node.getRequests())) + str(node.getTimeLeft()-node.getDelta()))
                    print(tour_dict)
                    tsp = tsp_solver([self.all_coordinates[node.getDestination()]],self.end,self.getOldCustomer(node.getRequests()),self.getNewCustomers(node.getRequests()),node.getTimeLeft()-node.getDelta())
                    try_tour = tsp.solveTSP()
                    #convert tsp_solver output. Ids in self.tour are then equal to customer ids 2,3,4,.... Regarding customer requests its i+2
                    if try_tour:
                        print(try_tour)
                        self.tour = []
                        for t in try_tour:
                            self.tour.append(tour_dict[t])
                    print('Tour:')
                    print(self.tour)
                #accecpt/reject: set customers to 2 or 3 depending on whether they are included in the tour or not. Keep if 0 or 3
                for i in range(len(node.getRequests())):
                    if (i+2 in self.tour) and (node.getRequests()[i] == 1):
                        new_requestStates.append(2)
                        profit = profit + 1
                    elif (i+2 not in self.tour) and (node.getRequests()[i] == 1):                       
                        new_requestStates.append(3)
                    else:
                        new_requestStates.append(node.getRequests()[i])
                #check if arrived 
                if node.getDelta() == 0:
                    tour_length = getTourDistance(self.tour, self.distances)
                    wait_possible = node.getTimeLeft()-tour_length > 0
                    #check if open customer requests
                    if 2 in new_requestStates:
                        #wait possible: wait for 1. Case distinction here: Two child nodes added if waiting possible
                        if wait_possible:
                            new_states.append((Node(node.getDestination(), new_requestStates, node.getDelta(), node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
                        #Set next destination. Set to 3 for next customer
                        changed_new_requestStates = [] #necessary!
                        for i in range(len(new_requestStates)):
                            if (i+2 == self.tour[1]):
                                changed_new_requestStates.append(3)
                            else:
                                changed_new_requestStates.append(new_requestStates[i])
                        new_states.append((Node(self.tour[1], changed_new_requestStates, self.distances[node.getDestination()][self.tour[1]], node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
                    #check if no open customer request --> wait only if enough time left to reach final destination
                    else: 
                        #wait possible: wait for 1
                        if wait_possible:
                            new_states.append((Node(node.getDestination(), new_requestStates, node.getDelta(), node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
                        else:
                            new_states.append((Node(self.tour[1], new_requestStates, self.distances[node.getDestination()][self.tour[1]], node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
                #if not arrived at a destination              
                else: #no tour recalculation necessary
                    new_states.append((Node(node.getDestination(), new_requestStates, node.getDelta(), node.getTimeLeft(), not(node.getPredecision()), self.getID(node.getTimeLeft())), profit))
                return (new_states)
            else: 
                return([])    

        ##in case of S0x->S1, covers to exegeneous influence on request states
        else:
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
end = [(2,1)] #dest 1
customer_coordinates = [(3,1),(4,1)] #dest2,...
def getCustomerBehavior(time_left, customers):
    return 0.4

Node1 = Node(0, [0,0], 0, 6, True)
stateSpaceCreator = StateSpaceCreator(Node1, start, end, customer_coordinates, getCustomerBehavior)
#print(Node1.getRequests())
stateSpaceCreator.createStateSpace()
#print(stateSpaceCreator.getDistances())
#print(getTourDistance([0,2,1],getManhattan([(1,1),(2,1),(4,1),(4,4)])))
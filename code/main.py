from helpers import * 

##experiment1
start = [(1,1)] #dest 0
end = [(2,1)] #dest 1
customer_coordinates = [(3,1),(4,1)] #dest2,...

def getCustomerBehavior(time_left, customers):
    customer_likelihood = [0.4,0.3]
    total = 0
    for c in range(len(customers)):
        if total == 0 and customers[c] < 2:
            total = customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c])
        elif customers[c] < 2: 
            k = (customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c]))
            total = total * k
    if total == 0:
        return 1.0
    else:
        return total
    
Node1 = Node(0, [0,0], 0, 6, True) #first node/state


"""##experiment2
start = [(1,2)] #dest 0
end = [(3,2)] #dest 1
customer_coordinates = [(2,2)] #dest2,...
def getCustomerBehavior(time_left, customers):
    customer_likelihood = [0.5]
    total = 0
    for c in range(len(customers)):
        if total == 0 and customers[c] < 2:
            total = customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c])
        elif customers[c] < 2: 
            k = (customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c]))
            total = total * k
    if total == 0:
        return 1.0
    else:
        return total
Node1 = Node(0, [0], 0, 3, True) #first node/state"""

"""##experiment3
start = [(1,1)] #dest 0
end = [(2,1)] #dest 1
customer_coordinates = [(3,1),(4,1),(3,3),(3,2)] #dest2,...

def getCustomerBehavior(time_left, customers):
    customer_likelihood = [0.4,0.4,0.4,0.4]
    total = 0
    for c in range(len(customers)):
        if total == 0 and customers[c] < 2:
            total = customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c])
        elif customers[c] < 2: 
            k = (customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c]))
            total = total * k
    if total == 0:
        return 1.0
    else:
        return total

Node1 = Node(0, [0,0,0,0], 0, 8, True) #first node/state"""

"""##experiment4
start = [(1,2)] #dest 0
end = [(4,2)] #dest 1
customer_coordinates = [(3,1),(2,3),(3,3)] #dest2,...

def getCustomerBehavior(time_left, customers):
    customer_likelihood = [0.5,0.5,0.5]
    total = 0
    for c in range(len(customers)):
        if total == 0 and customers[c] < 2:
            total = customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c])
        elif customers[c] < 2: 
            k = (customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c]))
            total = total * k
    if total == 0:
        return 1.0
    else:
        return total

Node1 = Node(0, [0,0,0], 0, 9, True) #first node/state"""

"""##experiment5
start = [(1,2)] #dest 0
end = [(4,2)] #dest 1
customer_coordinates = [(2,1),(2,3),(3,1),(3,3)] #dest2,...

def getCustomerBehavior(time_left, customers):
    customer_likelihood = [0.5,0.5,0.5,0.5]
    total = 0
    for c in range(len(customers)):
        if total == 0 and customers[c] < 2:
            total = customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c])
        elif customers[c] < 2: 
            k = (customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c]))
            total = total * k
    if total == 0:
        return 1.0
    else:
        return total

Node1 = Node(0, [0,0,0,0], 0, 10, True) #first node/state"""

"""#experiment 6
start = [(1,2)] #dest 0
end = [(4,2)] #dest 1
customer_coordinates = [(3,1), (1,4), (2,4), (3,4)]


def getCustomerBehavior(time_left, customers):
    customer_likelihood = [0.5,0.5,0.5,0.5]
    total = 0
    for c in range(len(customers)):
        if total == 0 and customers[c] < 2:
            total = customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c])
        elif customers[c] < 2: 
            k = (customers[c] * customer_likelihood[c] + abs(customers[c]-1) * (1-customer_likelihood[c]))
            total = total * k
    if total == 0:
        return 1.0
    else:
        return total

Node1 = Node(0, [0,0,0,0], 0, 14, True) #first node/state"""

stateSpaceCreator = StateSpaceCreator(Node1, start, end, customer_coordinates, getCustomerBehavior, True)
policy = stateSpaceCreator.createPolicy()
print("State space size:" + str(len(policy)))
print("EX:" + str(policy["root"]["obj"].getExpectedValue()))
#createGraphWithStates(policy) #be careful as the file can get very large
#createSplitGraphWithStates(policy) #be careful as the file can get very large
#stateSpaceCreator.printStateSpace(policy)
#print(policy)
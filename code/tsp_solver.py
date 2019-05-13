# Based on Solution by Copyright 2019, Gurobi Optimization, LLC

# Solve a vehicle routing problem on a set of
# points including start and end point using lazy constraints. 
# The base MIP model includes 'degree-2' constraints for the intermediate points 
# and 'degree-1' constraints for start and end point.
# Solutions to this model may contain subtours - The lazy constraint callback
# adds new constraints to cut them off.

import sys
import math
import random
import itertools
import gurobipy as gurobipy 

class tsp_solver:
    def __init__(self, start, end, active, new, t):
        self.start = start
        self.end = end
        self.active = active
        self.new = new
        self.n = len(start+end+active+new)
        self.t = t

    #Solves the tsp by creating a model and optimizing it
    def solveTSP(self):
        points = self.start + self.end + self.active + self.new
        dist = {(i,j) :
            (sum(abs(points[i][k]-points[j][k]) for k in range(2)))
            for i in range(self.n) for j in range(i)}

        print('')
        print('points')
        print(points)
        print('')
        print('')
        print('dist')
        print(dist)
        print('')

        m = gurobipy.Model()

        vars = gurobipy.tupledict()
        vars = m.addVars(dist.keys(), vtype=gurobipy.GRB.BINARY, name='e')
        for i,j in vars.keys():
            vars[j,i] = vars[i,j]

        print('')
        print('vars')
        print(vars)
        print('')

        #For 0 and 1
        m.addConstr(vars.sum('*',0) == 1)
        m.addConstr(vars.sum('*',1) == 1)

        #For active nodes
        m.addConstrs(vars.sum(i,'*') == 2 for i in range(2,2+len(self.active)))

        #For new nodes
        m.addConstrs((vars.sum(i,'*')-1)*(vars.sum(i,'*')-1) == 1 for i in range(2+len(self.active),2+len(self.active)+len(self.new)))

        #For t
        init1 = True
        for i,j in dist.keys():
            if(init1):
                expr1 = gurobipy.LinExpr(vars[i,j]*dist[i,j])
                init1 = False
            else:
                expr1 = expr1 + gurobipy.LinExpr(vars[i,j]*dist[i,j])
        m.addConstr(expr1 <= self.t)
        
        #Objective: Max visited customers
        init2 = True
        for i,j in dist.keys():
            if(init2):
                expr2 = gurobipy.LinExpr(vars[i,j])
                init2 = False
            else:
                expr2 = expr2 + gurobipy.LinExpr(vars[i,j])
        m.setObjective(expr2, sense=gurobipy.GRB.MAXIMIZE)

        #m.setObjective(vars.sum(), sense=gurobipy.GRB.MAXIMIZE)

        m._vars = vars
        m.Params.lazyConstraints = 1
        m.optimize(subtourelim)
        vals = m.getAttr('x', vars)

        print('')
        print("vals")
        print(vals)

        return(getTour(vals))    

# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
        if where == gurobipy.GRB.Callback.MIPSOL:
            # make a list of edges selected in the solution
            vals = model.cbGetSolution(model._vars)
            selected = gurobipy.tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
            # find the shortest cycle in the selected edge list which is not the route from 0 to 1
            tour = subtour(selected)
            print(selected)
            if len(tour) >= 3: #only important if there is a cycle with 3 or more members involved (no duplicate, because subtour may return empty list)
                print('')
                print('Added constraint')
                print(tour)
                print('')
                # add subtour elimination constraint for every pair of cities in tour
                model.cbLazy(gurobipy.quicksum(model._vars[i,j]
                                    for i,j in itertools.combinations(tour, 2))
                            <= len(tour)-1)

# Given a tuplelist of edges, find the shortest subtour which is not the route from 0 to 1
def subtour(edges):
    unvisited = elements(edges) #filters for the points involved in the solution, as not all points must be in the solution
    cycle = []
    while unvisited: # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors: # true if list is non-empty. Finds subtours in the remaining set of unvisited nodes.
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i,j in edges.select(current,'*') if j in unvisited] 
        print('')
        print('Found Cycle')
        print(thiscycle)
        if not((0 in thiscycle) or (1 in thiscycle)) and len(thiscycle) >= 3: #if it not found the route from start to end and the tour has 3 or more members
            if ((len(cycle) > len(thiscycle)) or (len(cycle) == 0)):  #if the cycle found is the first one or smaller then previous ones  
                cycle = thiscycle
    return cycle

def getTour(tupledict):
    visited = []
    current = 0
    nodes = []
    while current != 1:
        visited.append(current)
        #filter for edges outgoing from current
        for t in tupledict:
                if t[0] == current and tupledict.select(t[0],t[1])[0] == 1.0:
                    nodes.append(t) #possible successor with ==1
        #check which ones of the filtered ones were already visited
        for n in nodes:
            if n[1] not in visited:
                current = n[1]
    visited.append(1)
    return(visited)  

#Returns list of unique values in a tupledict
def elements(tuplelist):
    k = []
    for i,j in tuplelist:
        if(i not in k):
            k.append(i)
        if(j not in k):
            k.append(j)
    return k

start = [(1,1)]
end = [(2,1)]
active = [(4,1)]
new = [(4,4),(3,4)]
t = 11
tsp = tsp_solver(start,end,active,new,t)
print(tsp.solveTSP())

"""start = [(1,1)]
end = [(2,1)]
active = []
new = []
t = 9
tsp = tsp_solver(start,end,active,new,t)
tsp.solveTSP()"""

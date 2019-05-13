#!/usr/bin/python

# Copyright 2019, Gurobi Optimization, LLC

# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints.   The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.  The lazy constraint callback
# adds new constraints to cut them off.

import sys
import math
import random
import itertools
import gurobipy as gurobipy 

# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where):
    if where == gurobipy.GRB.Callback.MIPSOL:
        # make a list of edges selected in the solution
        vals = model.cbGetSolution(model._vars)
        selected = gurobipy.tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
        # find the shortest cycle in the selected edge list
        tour = subtour(selected)
        if len(tour) < n:
            # add subtour elimination constraint for every pair of cities in tour
            model.cbLazy(gurobipy.quicksum(model._vars[i,j]
                                  for i,j in itertools.combinations(tour, 2))
                         <= len(tour)-1)


# Given a tuplelist of edges, find the shortest subtour

def subtour(edges):
    unvisited = list(range(n))
    cycle = range(n+1) # initial length has 1 more city
    while unvisited: # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

# Points
start = [(1,1)]
end = [(4,4)]
active = [(2,1)]
new = [(4,1),(1,3)]
points = start + end + active + new
n = len(points)
t = 6

# Dictionary of Manhattan distance between each pair of points

dist = {(i,j) :
    (sum(abs(points[i][k]-points[j][k]) for k in range(2)))
    for i in range(n) for j in range(i)}

print('########')
print('points')
print(points)
print('')

print('########')
print('dist')
print(dist)
print('')

m = gurobipy.Model()
vars = gurobipy.tupledict()

vars[1,0] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e10')
vars[2,0] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e20')                 
vars[2,1] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e21')                      
vars[3,0] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e30')                  
vars[3,1] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e31')
vars[3,2] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e32')
vars[4,0] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e40')
vars[4,1] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e41')
vars[4,2] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e42')
vars[4,3] = m.addVar(vtype=gurobipy.GRB.BINARY,
                        name='e43')
for i,j in vars.keys():
    vars[j,i] = vars[i,j] # edge in opposite direction
#m.update()

print('')
print("vars")
print(vars)
print('')

#constraint: Define for each, but consider special case for start and end
m.addConstr((vars[1,0] + vars[2,0] + vars[3,0] + vars[4,0]) == 1) #Node0
m.addConstr((vars[1,0] + vars[2,1] + vars[3,1] + vars[4,1]) == 1) #Node1
m.addConstr((vars[2,0] + vars[2,1] + vars[3,2] + vars[4,2]) == 2) #Node2
m.addConstr(((vars[3,0] + vars[3,1] + vars[3,2] + vars[4,3] - 1)*(vars[3,0] + vars[3,1] + vars[3,2] + vars[4,3] - 1)) == 1) #Node3 --> 0 or 2
m.addConstr(((vars[4,0] + vars[4,1] + vars[4,2] + vars[4,3] - 1)*(vars[4,0] + vars[4,1] + vars[4,2] + vars[4,3] - 1)) == 1) #Node4 --> 0 or 2
m.addConstr((vars[1,0]*dist[1,0] + vars[2,0]*dist[2,0] + 
                vars[3,0]*dist[3,0] + vars[4,0]*dist[4,0] + 
                vars[2,1]*dist[2,1] + vars[3,1]*dist[3,1] + 
                vars[4,1]*dist[4,1] + vars[3,2]*dist[3,2] + 
                vars[4,2]*dist[4,2] + vars[4,3]*dist[4,3]) <= t)

#m.addConstrs(vars.sum(i,'*') == 2 for i in range(n))
# für das objective einfach die distanze matrix nehmen und mit vars multiplizieren
m.setObjective((vars[1,0] + vars[2,0] + 
                vars[3,0] + vars[4,0] + 
                vars[2,1] + vars[3,1] + 
                vars[4,1] + vars[3,2] + 
                vars[4,2] + vars[4,3]), sense=gurobipy.GRB.MAXIMIZE)
"""m.setObjective((vars[1,0]*dist[1,0] + vars[2,0]*dist[2,0] + 
                vars[3,0]*dist[3,0] + vars[4,0]*dist[4,0] + 
                vars[2,1]*dist[2,1] + vars[3,1]*dist[3,1] + 
                vars[4,1]*dist[4,1] + vars[3,2]*dist[3,2] + 
                vars[4,2]*dist[4,2] + vars[4,3]*dist[4,3]), sense=gurobipy.GRB.MINIMIZE)"""

#m.update()

m._vars = vars
m.Params.lazyConstraints = 1
#m.optimize(subtourelim)
m.optimize()
vals = m.getAttr('x', vars)

print('')
print("vals")
print(vals)
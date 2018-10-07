"""
This example solves a variant of the bin packing problem using IBM CP Optimizer

Similar problem as bin-packing-variant.py but with new built-in constraint
http://ibmdecisionoptimization.github.io/docplex-doc/cp/docplex.cp.modeler.py.html#docplex.cp.modeler.pack

Given:
    - A set of M identical items. Item size is 4-dimensional
    - A set of N bins with different size. Bin size is 4-dimensional
    - Allocation constraint: an item can be assigned to some specific bins,
        represented by a MxN binary matrix, 0: cannot be allocated, 1: can be allocated
An item can be allocated to at most one bin that is big to store it.
Objective:
    - Maximize the number of allocated items
    
"""
from docplex.cp.model import *
from docplex.cp.modeler import *
from docplex.cp.solution import *
import numpy as np
import pandas as pd
    
class Item(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        
class Bin(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        
#===============IMPORT DATA===============
items_data = np.loadtxt('set3-items.txt', dtype = np.integer, delimiter=',')
bins_data = np.loadtxt('set3-bins.txt', dtype = np.integer, delimiter=',')
alloc_constraint = np.loadtxt('set3-alloc-constraint.txt', dtype = np.integer, delimiter=',')
        
#===============INITIALIZE DATA===============   
#items        
items = []
for i in range(0,len(items_data)):
    items.append(Item(i, items_data[i]))
#bins
bins = []
for i in range(len(bins_data)):
    bins.append(Bin(i, bins_data[i]))

#===============CREATE MODEL===============
mdl = CpoModel(name = "bin-packing-variant")

#===============SETUP DECISION VARIABLES===============
#array of integer variables saying which bin an item goes into
wheres = []
for item in items:
    bin_list = ()
    for bin in bins:
        #print('item:'+str(item.id)+' - bin: '+str(bin.id)+': '+str(alloc_constraint[item.id, bin.id]))
        if(alloc_constraint[item.id, bin.id] == 1):
            bin_list += int(bin.id),
    wheres.append(integer_var(domain=(bin_list)))

#bin capacity constraint, 4-dimensions
loads_d = []
for k in range(4):
    loads = []
    for bin in bins:
        loads.append(mdl.sum((wheres[int(item.id)] == int(bin.id)) * item.size[k] for item in items) <= bin.size[k])
    loads_d.append(loads)
     
#===============SETUP CONSTRAINTS===============   

#4 dimensional size -> 4 pack constraints
for k in range(4):
    mdl.add(mdl.pack(loads_d[k], wheres, items_data[:,k]))
    
#===============SETUP OBJECTIVE=============== 
print("...setting up objective")
#maximize number of allocated items
nb_allocated_items = mdl.sum((wheres[int(item.id)] == int(bin.id)) for bin in bins for item in items)
mdl.add(maximize(nb_allocated_items))
print("...solving...")
#solve the problem and print the solution
msol = mdl.solve(url = None, key = None, TimeLimit = None, SearchType = 'Auto')
msol.print_solution()
mdl.export_as_cpo(out='cpo.txt')
with open('log.txt', "w") as text_file:
    print(msol.get_solver_log(), file=text_file)
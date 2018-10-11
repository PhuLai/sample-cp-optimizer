"""
This example solves a variant of the bin packing problem using IBM CP Optimizer

THIS VERSION IS VERY INEFFICIENT, DO NOT USE THIS

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
items_data = np.loadtxt('set2-items.txt', dtype = np.float, delimiter=',')
bins_data = np.loadtxt('set2-bins.txt', dtype = np.float, delimiter=',')
alloc_constraint = np.loadtxt('set2-alloc-constraint.txt', dtype = np.integer, delimiter=',')
        
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
#x is a binary matrix. 0 if the item cannot be assigned to the bin; 1 if can be
x = pd.DataFrame(index=range(len(items)), columns=range(len(bins)))
for bin in bins:
    for item in items:
        if alloc_constraint[item.id, bin.id] == 0:
            x.iloc[item.id][bin.id] = 0
        else:
            x.iloc[item.id][bin.id] = mdl.binary_var()
            
#===============SETUP CONSTRAINTS===============   
print("...setting up 1-item-1-bin constraint")
#each item is allocated to at most 1 bin
for item in items:
    mdl.add(mdl.sum(x.iloc[item.id][bin.id] for bin in bins) <= 1)

print("...setting up size constraint")
#size constraints
for bin in bins:
    #get all items that can be allocated to bin i (due to allocation constraint)
    items_of_bin=[]
    for item in items:
        if(alloc_constraint[item.id, bin.id] == 1):
            items_of_bin.append(item)
    #get number of items to be allocated to a bin
    nb_items_in_bin = mdl.sum((x.iloc[item.id][bin.id] for item in items_of_bin))
    #size has 4 dimensions
    for k in range(4):
        #total size of dimention k generated by all items found above
        total_w = mdl.times(items[item.id].size[k], nb_items_in_bin)
        #resource constraint
        mdl.add(total_w <= bin.size[k])    
    
#===============SETUP OBJECTIVE=============== 
print("...setting up objective")
#maximize number of allocated items
nb_allocated_items = mdl.sum((x.iloc[item.id][bin.id] for bin in bins for item in items))
mdl.add(maximize(nb_allocated_items))
print("...solving...")
#solve the problem and print the solution
msol = mdl.solve(url = None, key = None, TimeLimit = None, SearchType = 'Auto')
msol.print_solution()

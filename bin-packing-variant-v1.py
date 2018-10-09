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
items_data = np.loadtxt('set2-items.txt', dtype = np.integer, delimiter=',')
bins_data = np.loadtxt('set2-bins.txt', dtype = np.integer, delimiter=',')
alloc_constraint = np.loadtxt('set2-alloc-constraint.txt', dtype = np.integer, delimiter=',')

nb_bins = len(bins_data)
        
#===============INITIALIZE DATA===============   
#items        
items = []
for i in range(0,len(items_data)):
    items.append(Item(i, items_data[i]))
#bins
bins = []
for i in range(len(bins_data)):
    bins.append(Bin(i, bins_data[i]))
    
#add a new bin at the end of the list, big enough to accommodate ALL items
bins.append(Bin(nb_bins, sum(items_data)))

#===============CREATE MODEL===============
mdl = CpoModel(name = "bin-packing-variant")

#===============SETUP DECISION VARIABLES===============
#array of integer variables saying which bin an item goes into
wheres = []
for item in items:
    bin_list = ()
    for bin in bins[0:nb_bins]:
        if(alloc_constraint[item.id, bin.id] == 1):
            bin_list += int(bin.id),
    #add the last bin (the big one)    
    bin_list += nb_bins,
    wheres.append(integer_var(domain=(bin_list), name = "whereItem"+str(item.id)))
     
#===============SETUP CONSTRAINTS===============   
#one pack constraint for each dimension
for k in range(4):
    #each bin's load can range(0..bin size)
    loads = [integer_var(0,bins[int(bin.id)].size[k], name="sizeBin"+str(bin.id)+",d"+str(k)) for bin in bins]
    mdl.add(mdl.pack(loads, wheres, items_data[:,k]))
    
#===============SETUP OBJECTIVE=============== 
#maximize number of items allocated to all bins EXCEPT the big bin
print("...setting up objective")
nb_allocated_items = mdl.sum([(wheres[int(item.id)] == int(bin.id)) for bin in bins[0:nb_bins] for item in items])
mdl.add(maximize(nb_allocated_items))

#solve the problem and print the solution
print("...solving...")
msol = mdl.solve(url = None, key = None, TimeLimit = None, SearchType = 'Auto')
msol.print_solution()
mdl.export_as_cpo(out='cpo.txt')
with open('log.txt', "w") as text_file:
    print(msol.get_solver_log(), file=text_file)
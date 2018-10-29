"""
This example solves a variant of the bin packing problem using IBM CP Optimizer

Given:
    - A set of m identical items. Item size is 4-dimensional
    - A set of n bins with different size. Bin size is 4-dimensional
    - Allocation constraint: an item can be assigned to some specific bins,
        represented by a mxn binary matrix, 0: cannot be allocated, 1: can be allocated
An item can be allocated to at most one bin that is big to store it.
Objective:
    - Maximize x_1 + x_2 + ... + x_n
    - Maximize x_1 * x_2 + ... * x_n
    where x is the number of items allocated to bin i for all i in [1..n]
    
"""
from docplex.cp.model import CpoModel
import numpy as np
    
class Item(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        
class Bin(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        
#===============IMPORT DATA===============
items_data = np.loadtxt('set-items.txt', dtype = np.integer, delimiter=',')
bins_data = np.loadtxt('set-bins.txt', dtype = np.integer, delimiter=',')
alloc_constraint = np.loadtxt('set-alloc-constraint.txt', dtype = np.integer, delimiter=',')

nb_bins = len(bins_data)
nb_items = len(items_data)
        
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
#needed so that all items can be allocated, CPO won't return any solution if an item unallocated    
bins.append(Bin(nb_bins, sum(items_data)))

#===============CREATE MODEL===============
mdl = CpoModel(name = "bin-packing-variant")

#===============SETUP DECISION VARIABLES===============
#array of integer variables saying which bin an item goes into
wheres = []
bin_idx_of_dump_item = 0
for item in items:
    bin_list = ()
    for bin in bins[0:nb_bins]:
        if(alloc_constraint[item.id, bin.id] == 1):
            bin_list += int(bin.id),
    #add the last bin (the big one)    
    bin_list += nb_bins,
    wheres.append(mdl.integer_var(domain=(bin_list), name = "whereItem"+str(item.id)))
     
#===============SETUP CONSTRAINTS===============   
#one pack constraint for each dimension
for k in range(4):
    #each bin's load can range(0..bin size)
    loads = [mdl.integer_var(0,bins[int(bin.id)].size[k], name="sizeBin"+str(bin.id)+",d"+str(k)) for bin in bins]
    mdl.add(mdl.pack(loads, wheres, [item.size[k] for item in items]))
    
#===============SETUP OBJECTIVE=============== 
#maximize number of items allocated to all bins EXCEPT the big bin
nb_allocated_items = mdl.sum([(wheres[int(item.id)] != nb_bins) for item in items])

#maximize x_1 * x_2 * ... *x_n, where x_1, x_2,..., x_n is the number of items in bin 1, 2, ..., n
product_x = 1
for bin in bins[0:len(bins)-1]:
    #get the number of items in the bin
    nb_items_in_bin = mdl.sum([(wheres[int(item.id)] == int(bin.id)) for item in items])
    #if the bin is empty, assume it has 1 item so that the product won't be zero
    x = mdl.conditional(nb_items_in_bin != 0, nb_items_in_bin, 1)
    #divided by 10 so that CPO won't have to handle big integer
    product_x = mdl.times(product_x, x/10)
        
#add lecicographic objs
mdl.add(mdl.maximize_static_lex([nb_allocated_items, product_x]))

#solve the problem and print the solution
print("...solving...")
msol = mdl.solve(url = None, key = None, TimeLimit = None, SearchType = 'Auto')
msol.print_solution()
print("Obj vals: " + str(msol.get_objective_values()))
print("x_1 * x_2 * ... * x_n = ",msol.get_objective_values()[1]*(10**nb_bins))
mdl.export_as_cpo(out='cpo.txt')
with open('log.txt', "w") as text_file:
    print(msol.get_solver_log(), file=text_file)
    
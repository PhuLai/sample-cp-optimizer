"""
This example solves a variant of the bin packing problem using BRUTE-FORCE !
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
import numpy as np
import itertools
from collections import Counter
    
class Item(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        
class Bin(object):
    def __init__(self, id, size):
        self.id = id
        self.size = size
        
#===============IMPORT DATA===============
items_data = np.loadtxt('set8-items.txt', dtype = np.integer, delimiter=',')
bins_data = np.loadtxt('set8-bins.txt', dtype = np.integer, delimiter=',')
alloc_constraint = np.loadtxt('set8-alloc-constraint.txt', dtype = np.integer, delimiter=',')

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
bins.append(Bin(nb_bins, sum(items_data)))

#===============FINDING POSSIBLE BINS THAT CAN STORE ITEMS===============
wheres = []
bin_idx_of_dump_item = 0
for item in items:
    bin_list = ()
    for bin in bins[0:nb_bins]:
        if(alloc_constraint[item.id, bin.id] == 1):
            bin_list += int(bin.id),
    #add the last bin (the big one)    
    bin_list += nb_bins,
    wheres.append(bin_list)

#find all possible combinations of bin assignment
possible_solutions_proximity = list(itertools.product(*wheres))
possible_solutions_capacity = []
for sol in possible_solutions_proximity:
    counts = Counter(sol)
    is_resource_constraint_valid = True
    for s in range(len(bins)):
        #resource constraint (users are identical)
        if((counts[s]*items[0].size > bins[s].size).any()):
            is_resource_constraint_valid = False
            break
    if(is_resource_constraint_valid):
        possible_solutions_capacity.append(sol)

#find the solution with maximum number of items allocated
nb_users_allocated = [len([s for s in sol if s is not nb_bins]) for sol in possible_solutions_capacity]
max_user_sol_idx = [index for index, value in enumerate(nb_users_allocated) if value == max(nb_users_allocated)]

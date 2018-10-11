# sample-cp-optimizer

This example (bin-packing-variant.py) solves a variant of the bin packing problem using IBM CP Optimizer.

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

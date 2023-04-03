#!/usr/bin/env python
# coding: utf-8

# # A Python Program to Solve a Sumaddle puzzle
# 
# ## Author: Owen Chen
# ## Last Modified: 4/3/2023
# 
# ## Run Time:
# O( n!*(n-1)!*(n-2)!...2!*1!)
# 
# ## Sumaddle Puzze
# A Sumaddle puzzle is to fill numbers into a nxn grid with constraints.  For each row and each column of a size n, you need to fill them with these numbers exactly once:
# 
# - 0, 0, 1, 2, 3, ..., n-1
# 
# The sum of the numbers between two 0s in each row must equal to a row sum given on the right side of the table.  
# 
# Similiarly, the sum of the numbers between two 0s in each column must equal to a column sum given on the bottom of the table.  
# 
# ## Inventor
# The puzzle was first invented by Kazunori Saito, who contributed an example to the Japan Puzzle Championship 2006. He named it ビトゥイーンサム, meaning "between sum".
# 
# 
# ## Example
# - Here is a 5x5 example:
# 
# <center><img src="https://sumaddle.com/uploads/1/3/6/1/136147655/published/examplepuzzle.png?1666011815"></center>
# 
# The blocks greyed out are the blockers with a value of 0.
# 
# ## Basic rules:
# 
# 1. Every row and every column must contain exactly two filled squares ("blocks").
# 2. Remaining squares contain the numbers 1, 2, 3 (etc.), with each number appearing exactly once in every row and in every column.
# 3. A value is shown at the end of a row or at the base of a column, the numbers in the squares between the two blocks of that row or column must add up to the value shown.
# 4. A sum value of 0 is a special case for rule 3. If a row or column has a sum of 0, it means the two blocks must be next to each other, with no intervening squares.
# 
# 
# See the detailed description of the puzzle in 
# - https://sumaddle.com/fundamentals.html
# 

# In[ ]:


## Version 3- changes from V2:

# - add a global dictionary map for a split from a list into two sub lists.  This will be used to keep track what numbers being used and what numbers remaining
# - add a global dictionary map for every permutation with its block sum value


# In[192]:



from itertools import combinations, permutations

#Global Variables for two dictionary maps

SUBSET_SPLIT_MAP = {}

ROW_SUM_MAP = {}

def get_subset_list(n, parent_list):
    fulllist = [0] + [i for i in range(n-1)]
    return  [e for e in fulllist if not e in parent_list or parent_list.remove(e)]

def initialize_subset_split_map(n):
    global SUBSET_SPLIT_MAP
    SUBSET_SPLIT_MAP = {}
    fullset = set(i for i in range(n-1))
    fulllist = [0] + [i for i in range(n-1)]
    for i in range(1, n):
        combos = [val for val in combinations(fulllist, i)]
        for subset in combos:
            subset = tuple(sorted(subset))
            if subset not in SUBSET_SPLIT_MAP:
                SUBSET_SPLIT_MAP[subset] = subtract_a_set(fullset, subset)

def subtract_a_set(fullset:set, subset:tuple) -> set:
    """
    Subtract a fullset all emlements from a given subset
    Return a subset of remaining elements
    """
    zerocount = subset.count(0)    
    remaining_set = fullset - set(subset)
    if zerocount < 2:
        return remaining_set.union({0})
    else:
        return remaining_set
        
    
def initialize_row_sum_map(n):
    global ROW_SUM_MAP
    ROW_SUM_MAP = {}
    fullset_tuple = (0,) + tuple(i for i in range(n-1))
    perms = [val for val in permutations(fullset_tuple, n)] 
    for perm in perms:
        zeroindex = perm.index(0) + 1
        if perm[zeroindex] == 0:
            ROW_SUM_MAP[perm] = 0
        else:
            row_sum = 0
            for k in perm[zeroindex:]:
                if k == 0:
                     ROW_SUM_MAP[perm] = row_sum
                     break
                else:
                     row_sum += k

    
# Check patterns of each row

def check_zero_zero(row):   
    return ROW_SUM_MAP[row] == 0

def check_blocksum(row, s):
    return ROW_SUM_MAP[row] == s

def get_num_list(n, row_list, col_list):  
    zeros_allowed = 1
    if row_list:
        zeros_in_row = row_list.count(0)
        if col_list:
            zero_in_col = col_list.count(0)
            constraint = set(row_list + tuple(col_list))
            if  zero_in_col > 1 or zeros_in_row > 1:                
                num_list = tuple(k for k in range(1, n-1) if k not in constraint)          
            else:
                num_list = (0,) + tuple(k for k in range(1, n-1) if k not in constraint)     
        else:
            if  zeros_in_row > 1:
                num_list = tuple(k for k in range(1, n-1) if k not in row_list) 
            else:
                num_list = (0,) + tuple(k for k in range(1, n-1) if k not in row_list) 
    elif col_list:
        zero_in_col = col_list.count(0)
        if zero_in_col > 1:
            num_list = tuple(k for k in range(1, n-1) if k not in col_list)       
        else:
            num_list = (0,) + tuple(k for k in range(1, n-1) if k not in col_list)
                 
    else:
            num_list = tuple(i for i in range(n-1))        
        
    return num_list


def get_last_num(n, exclude_list):    
    num_list =  [i for i in range(n-1) if i not in exclude_list]
    if len(num_list):
        return num_list[0]
    else:
        return 0
    

def generate_last_row(n,row_sum, prefix):
    row = tuple()
    for i in range(n):
        last_num = get_last_num(n, prefix[i])
        row += (last_num,)
    if row not in ROW_SUM_MAP:
        return None
    else:
        if row_sum > 0:
            if check_blocksum(row, row_sum):
                return row
            else:
                return None
        elif row_sum == 0:
            if check_zero_zero(row):
                return row
            else:
                return None
        else:
            return row

def check_prefix_constraint(n,row, prefix):
    """
    Check if current row has a duplicate value in prefix
    """    
    for i in range(n):
        exclude_numbers = prefix[i]
        if row[i] > 0:
            if row[i] in exclude_numbers:
                return False
        else:
            if exclude_numbers.count(0) == 2:
                return False
    return True
    
    
def generate_permutations(n, prefix):
    # Prefix has been transformed into columns
    if prefix:
        num_perms = [] 
        num_list0  = get_num_list(n,None, prefix[0])        
        for r0 in num_list0:     
            parent_list = (r0,)
            num_list1 = get_num_list(n,parent_list, prefix[1])
            for r1 in num_list1:                        
                parent_list = (r0,r1)
                num_list2 = get_num_list(n,parent_list,prefix[2]) 
                for r2 in num_list2:
                    parent_list = (r0,r1,r2)
                    if n == 4:
                        r3 = get_last_num(n,parent_list)
                        if (r0, r1, r2, r3) in ROW_SUM_MAP:
                            num_perms.append((r0, r1, r2, r3))
                    elif n > 4:
                        num_list3 = get_num_list(n,parent_list,prefix[3]) 
                        for r3 in num_list3:
                            parent_list = (r0, r1, r2, r3)   
                            if n == 5:
                                r4 = get_last_num(n,parent_list)
                                if (r0, r1, r2, r3, r4) in ROW_SUM_MAP:
                                    num_perms.append((r0, r1, r2, r3, r4))
                            elif n > 5:
                                num_list4 = get_num_list(n,parent_list,prefix[4]) 
                                for r4 in num_list4:
                                    parent_list = (r0, r1, r2, r3, r4)  
                                    if n == 6:
                                        r5 = get_last_num(n,parent_list)
                                        if (r0, r1, r2, r3, r4, r5) in ROW_SUM_MAP:
                                            num_perms.append((r0, r1, r2, r3, r4, r5))
                                    elif n > 6:
                                        num_list5 = get_num_list(n,parent_list,prefix[5]) 
                                        for r5 in num_list5:
                                            parent_list = (r0, r1, r2, r3, r4, r5)  
                                            r6 = get_last_num(n, parent_list)
                                            if (r0, r1, r2, r3, r4, r5, r6) in ROW_SUM_MAP:
                                                num_perms.append((r0, r1, r2, r3, r4, r5, r6))
        return num_perms
                            
    else:
        return list(ROW_SUM_MAP.keys())

def generate_row_candidates(n,row_sum, prefix):
    rows = generate_permutations(n, prefix) 
    if rows:
        # Filter row candidates
        if row_sum == 0:
            return [row for row in rows if check_zero_zero(row)]
        elif row_sum > 0: 
            return [row for row in rows if check_blocksum(row, row_sum)]  
        else:
            return rows
        
            """
            # Redundent check_blocksum() is sufficent

            # Check patterns - courtesy of Brian Mansfield
            if row_sum in (1, 2):
                candidates = [row for row in candidates if check_zero_x_zero(row)]   
            elif row_sum > n-2:
                candidates = [row for row in candidates if not check_zero_x_zero(row)]   
            """
    else:
        return []
            
def check_col_constraint(sol, col_sums, n): 
    nrow = len(sol)
    for i in range(n):
        col = tuple(row[i] for row in sol)
        if col_sums[i] == 0:
            if not check_zero_zero(col):
                return False
        elif col_sums[i] > 0:
            if not check_blocksum(col, col_sums[i]):
                return False
    return True

# Generate solutions for 5x5, 6x6 or 7x7
def generate_solutions(row_sums,col_sums, n):
    row_candidates0 = generate_row_candidates(n,row_sums[0], None)
    for r0 in row_candidates0:
        prefix = [[r0[i]] for i in range(n)]
        row_candidates1 = generate_row_candidates(n,row_sums[1], prefix) 
        for r1 in row_candidates1:  
            prefix = [[r0[i], r1[i]] for i in range(n)]
            row_candidates2 = generate_row_candidates(n,row_sums[2], prefix)             
            for r2 in row_candidates2:
                prefix = [[r0[i], r1[i], r2[i]] for i in range(n)]
                if n == 4:
                    r3 = generate_last_row(n,row_sums[3], prefix) 
                    if r3:  
                        sol = (r0,r1,r2,r3)
                        if check_col_constraint(sol, col_sums, n): 
                            return sol
                elif n > 4:    
                    row_candidates3 = generate_row_candidates(n,row_sums[3], prefix)  
                    for r3 in row_candidates3:  
                        prefix = [(r0[i], r1[i], r2[i], r3[i]) for i in range(n)]
                        if n == 5:
                            r4 = generate_last_row(n,row_sums[4], prefix) 
                            if r4:  
                                sol = (r0,r1,r2,r3,r4)
                                if check_col_constraint(sol, col_sums, n): 
                                    return sol
                        elif n > 5:
                            row_candidates4 = generate_row_candidates(n,row_sums[4], prefix)   
                            for r4 in row_candidates4:  
                                prefix = [(r0[i], r1[i], r2[i], r3[i], r4[i]) for i in range(n)] 
                                if n == 6:
                                    r5 = generate_last_row(n,row_sums[5], prefix) 
                                    if r5:  
                                        sol = (r0,r1,r2,r3,r4,r5)
                                        if check_col_constraint(sol, col_sums, n): 
                                            return sol  
                                elif n == 7: 
                                    row_candidates5 = generate_row_candidates(n,row_sums[5], prefix)               
                                    for r5 in row_candidates5:  
                                        prefix = [(r0[i], r1[i], r2[i], r3[i], r4[i], r5[i]) for i in range(n)]    
                                        r6 = generate_last_row(n,row_sums[6],prefix)
                                        if r6:  
                                            sol = (r0,r1,r2,r3,r4,r5,r6)
                                            if check_col_constraint(sol, col_sums, n): 
                                                return sol 
                                else:                                        
                                    raise Exception("Sorry, the input n must be 4, 5, 6, or 7")
    return None

def print_matrix(sol):
    for col in sol:
        print(col, flush=True)
        
def solve_sumaddle_puzzle(row_sums, col_sums):
    n = len(row_sums)
    initialize_subset_split_map(n)
    initialize_row_sum_map(n)
    sol = generate_solutions(row_sums,col_sums, n)    
    if sol:
        print(f"Solution for a {n}x{n} with row constraint:{row_sums}, and column constraint:{col_sums}", flush=True)
        print_matrix(sol)
    else:
        print("No solution", flush=True)    


# In[193]:


import time
start_time = time.time()
solve_sumaddle_puzzle([3, 1, 0, 2], [3, 0, 0,0])
print(f"Run time: {time.time() - start_time} seconds", flush=True)


# In[194]:


import time
start_time = time.time()
solve_sumaddle_puzzle([5, 0, 5, 6, 0], [0, 6, 3, 0, 3])
print(f"Run time: {time.time() - start_time} seconds", flush=True)


# In[195]:


start_time = time.time()
solve_sumaddle_puzzle([5, 1, 0, 5, 0], [2, 1, 0, 0, 6])
print(f"Run time: {time.time() - start_time} seconds", flush=True)


# In[196]:


start_time = time.time()
solve_sumaddle_puzzle([9, 2, 4, -1 ,-1 , 3],  [7, 10, 2, -1,-1 , -1])
print(f"Run time: {time.time() - start_time} seconds", flush=True)


# In[ ]:


start_time = time.time()
solve_sumaddle_puzzle([10, 0, 9, 1 ,3, 7, 3], [0, 11, 0, 8, 14, 9, 15])
print(f"Run time: {time.time() - start_time} seconds")


#!/usr/bin/env python
# coding: utf-8

# # A Python Program to Solve a Sumaddle puzzle
# 
# ## Author: Owen Chen
# ## Version 5: Multiprocessing of Version 4
# ## Last Modified: 4/11/2023
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

# ### Version 5 changes from V4
# 
# - Parallel execution of V4

# In[1]:


import time
import numpy as np
import concurrent.futures
import os
from tqdm import tqdm
from itertools import combinations, permutations

#Global Variables for two dictionary maps

SUBSET_SPLIT_MAP = {}

ROW_SUM_MAP = {}


def get_subset_list(n, parent_row):
    fulllist = [0] + [i for i in range(n-1)]
    return  [e for e in fulllist if not e in parent_row or parent_row.remove(e)]

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
    #Remove duplicates
    perms = list(set(perms))
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


def get_firstrow_permutations(row_sum):
	"""
	Get the first row permutations with row_sum as a constraint only
	"""
	if row_sum >= 0:
		return [ perm for perm, sum in ROW_SUM_MAP.items() if sum == row_sum]
	else:
		return list(ROW_SUM_MAP.keys())
		
def get_firstcol_permutations(col_sum, first):
	"""
	Get the first column permutations with col_sum as a constraint and the first element is first.
	"""
	if col_sum >= 0:
		return [ perm for perm, sum in ROW_SUM_MAP.items() if sum == col_sum and perm[0] == first]
	else:
		return [ perm for perm in ROW_SUM_MAP.values() if perm[0] == first]
 
def get_num_list(n, row_list, col_list):  
    zeros_allowed = 1
    if row_list:
        zeros_in_row = row_list.count(0)
        if col_list:
            if type(col_list) is list:
                zero_in_col = col_list.count(0)
                constraint = set(row_list + tuple(col_list))
            else:
                if col_list == 0:
                    zero_in_col = 1
                else:
                    zero_in_col = 0
                constraint = set(row_list + (col_list,))
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
        if type(col_list) is list:
            zero_in_col = col_list.count(0)
        else:
            if col_list == 0:
                zero_in_col = 1
            else:
                zero_in_col = 0
            col_list = list(col_list)
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
    
def check_row_constraint(row, row_sum): 
    if row in ROW_SUM_MAP:
        if row_sum >=0:
            return ROW_SUM_MAP[row] == row_sum
        else:
            return True
    else:
        return False
    
def generate_row_permutations(n,row_num,row_sum, parent_row, parent_col):
    # parent_col has been transformed into columns
    num_perms = [] 
    parent_row = tuple(parent_row)
    k = n -1 - row_num
    row = parent_row
    if k == 0:
        r0 = get_last_num(n,row)
        row = parent_row + (r0,)
        if check_row_constraint(row, row_sum):
            num_perms.append(row)
    elif k > 0:     
        num_list0 = get_num_list(n,row, parent_col[0]) 
        for r0 in num_list0:
            row = parent_row + (r0,)
            if k ==1:         
                r1 = get_last_num(n,row)
                row = parent_row + (r0,r1)
                if check_row_constraint(row, row_sum):
                    num_perms.append(row)
            elif k > 1:
                num_list1 = get_num_list(n,row, parent_col[1])             
                for r1 in num_list1:      
                    row = parent_row + (r0,r1)
                    if k == 2:      
                        r2 = get_last_num(n,row)
                        row = parent_row + (r0,r1,r2)
                        if check_row_constraint(row, row_sum):
                            num_perms.append(row)
                    elif k > 2: 
                        num_list2 = get_num_list(n,row, parent_col[2])
                        for r2 in num_list2:      
                            row = parent_row + (r0,r1,r2)
                            if k == 3:      
                                r3 = get_last_num(n,row)
                                row = parent_row + (r0,r1,r2,r3)
                                if check_row_constraint(row, row_sum):
                                    num_perms.append(row)
                            elif k > 3:        
                                num_list3 = get_num_list(n,row, parent_col[3])
                                for r3 in num_list3:      
                                    row = parent_row + (r0,r1,r2,r3)
                                    if k == 4:      
                                        r4 = get_last_num(n,row)
                                        row = parent_row + (r0,r1,r2,r3,r4)
                                        if check_row_constraint(row, row_sum):
                                            num_perms.append(row)
                                    elif k > 4:    
                                        num_list4 = get_num_list(n,row, parent_col[4])
                                        for r4 in num_list4:      
                                            row = parent_row + (r0,r1,r2,r3,r4)
                                            if k == 5:      
                                                r5 = get_last_num(n,row)
                                                row = parent_row + (r0,r1,r2,r3,r4,r5)
                                                if check_row_constraint(row, row_sum):
                                                    num_perms.append(row)

    return num_perms

def generate_col_permutations(n,col_num,col_sum, parent_col, parent_row):
    # parent_col has been transformed into columns
    num_perms = [] 
    parent_col = tuple(parent_col)
    k = n-2 - col_num
    col = parent_col
    if k == 0:
        r0 = get_last_num(n,col)
        col = parent_col + (r0,)
        if check_row_constraint(col, col_sum):
            num_perms.append(col)
    elif k > 0:     
        num_list0 = get_num_list(n,col, parent_row[0])
        for r0 in num_list0:
            col = parent_col + (r0,)
            if k ==1:         
                r1 = get_last_num(n,col)
                col = parent_col + (r0,r1)
                if check_row_constraint(col, col_sum):
                    num_perms.append(col)
            elif k > 1:
                num_list1 = get_num_list(n,col, parent_row[1])    
                for r1 in num_list1:      
                    col = parent_col + (r0,r1)
                    if k == 2:      
                        r2 = get_last_num(n,col)
                        col = parent_col + (r0,r1,r2)
                        if check_row_constraint(col, col_sum):
                            num_perms.append(col)
                    elif k > 2: 
                        num_list2 = get_num_list(n,col, parent_row[2])
                        for r2 in num_list2:      
                            col = parent_col + (r0,r1,r2)
                            if k == 3:      
                                r3 = get_last_num(n,col)
                                col = parent_col + (r0,r1,r2,r3)
                                if check_row_constraint(col, col_sum):
                                    num_perms.append(col)
                            elif k > 3:        
                                num_list3 = get_num_list(n,col, parent_row[3])
                                for r3 in num_list3:      
                                    col = parent_col + (r0,r1,r2,r3)
                                    if k == 4:      
                                        r4 = get_last_num(n,col)
                                        col = parent_col + (r0,r1,r2,r3,r4)
                                        if check_row_constraint(col, col_sum):
                                            num_perms.append(col)
    return num_perms
            
def sub_generate_solutions(r0, row_sums, col_sums, n):
    grid = np.full((n,n), -1)    
    grid[0] = r0
    cols0 =  get_firstcol_permutations(col_sums[0], grid[0,0])
    for c0 in cols0:
        grid[:,0] = c0         
        rows1 = generate_row_permutations(n,1,row_sums[1], (grid[1,0],), grid[0,1:].tolist())            
        for r1 in rows1:                                   
            grid[1] = r1
            cols1 = generate_col_permutations(n,1,col_sums[1], tuple(grid[:2,1]), grid[2:, 0].tolist())
            #cols1 = get_col_permutations(n,1,grid[:2,1].tolist())
            for c1 in cols1:                                               
                grid[:,1]=c1
                rows2 = generate_row_permutations(n,2,row_sums[2], tuple(grid[2,:2]), grid[:2,2:].T.tolist())                    
                for r2 in rows2:
                    grid[2]=r2
                    cols2 = generate_col_permutations(n,2,col_sums[2], tuple(grid[:3,2]), grid[3:, :2].tolist())
                    for c2 in cols2:
                        grid[:,2] = c2                    
                        if n == 4:
                            last = get_last_num(n, grid[-1,:-1])
                            if last is not None:
                                grid[3,3] = last
                                if check_row_constraint(tuple(grid[3]), row_sums[3]) and check_row_constraint(tuple(grid[:,3]), col_sums[3]):
                                    return grid
                        elif n > 4:
                            # Get row 3
                            rows3 = generate_row_permutations(n,3,row_sums[3], tuple(grid[3,:3]), grid[:3,3:].T.tolist())
                            for r3 in rows3:
                                grid[3] = r3
                                cols3 = generate_col_permutations(n,3,col_sums[3], tuple(grid[:4,3]), grid[4:, :3].tolist())
                                for c3 in cols3:
                                    grid[:,3] = c3                             
                                    if n == 5:
                                        last = get_last_num(n, grid[-1,:-1])
                                        if last is not None:
                                            grid[4,4] = last
                                            if check_row_constraint(tuple(grid[4]),row_sums[4]) and check_row_constraint(tuple(grid[:,4]),col_sums[4]):
                                                return grid
                                    elif n > 5:
                                        rows4 = generate_row_permutations(n,4,row_sums[4], tuple(grid[4,:4]), grid[:4,4:].T.tolist())
                                        for r4 in rows4:
                                            grid[4] = r4
                                            cols4 = generate_col_permutations(n,4,col_sums[4], tuple(grid[:5,4]), grid[5:, :4].tolist())
                                            for c4 in cols4:
                                                grid[:,4] = c4
                                                if n == 6:
                                                    last = get_last_num(n, grid[-1,:-1])
                                                    if last is not None:
                                                        grid[5,5] = last                  
                                                        if check_row_constraint(tuple(grid[5]),row_sums[5]) and check_row_constraint(tuple(grid[:,5]),col_sums[5]):
                                                            return grid
                                                elif n > 6:
                                                    rows5 = generate_row_permutations(n,5,row_sums[5], tuple(grid[5,:5]), grid[:5,5:].T.tolist())
                                                    for r5 in rows5:
                                                        grid[5] = r5
                                                        cols5 = generate_col_permutations(n,5,col_sums[5], tuple(grid[:6,5]), grid[6:, :5].tolist())
                                                        for c5 in cols5:
                                                            grid[:,5] = c5
                                                            last = get_last_num(n, grid[-1,:-1])
                                                            if last is not None:
                                                                grid[6,6] = last
                                                                if check_row_constraint(tuple(grid[6]),row_sums[6]) and check_row_constraint(tuple(grid[:,6]),col_sums[6]):
                                                                    return grid
    return None


def main_generate_solutions(row_sums,col_sums, n):

    grid = np.full((n,n), -1)    
    # get row 0
    rows0 = get_firstrow_permutations(row_sums[0]) 
    nworkers = 2 * os.cpu_count()
    print(f"running parallel processing jobs with max_workers={nworkers}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=nworkers) as executor:
        # Submit jobs
        futures = {executor.submit(sub_generate_solutions, r0, row_sums, col_sums, n):r0 for r0 in rows0}
        
        print(f"Jobs submitted: {len(futures)}")
        
        # Check jobs
        # Wait for the first job to completed
        concurrent.futures.wait(futures, timeout=None, return_when=concurrent.futures.FIRST_COMPLETED)
        number_of_processes = len(rows0)
        count = 0
        jobs_completed = set()
        while count < number_of_processes:
            for future in futures:
                if future.done():
                    if future not in jobs_completed:
                        jobs_completed.add(future)
                        count += 1
                        data = future.result()
                        if data is not None:
                            return data
            print(f"Jobs completed: {count}.")
            time.sleep(2)
            
        """
        for future in concurrent.futures.as_completed(futures):
            r0 = futures[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f"input {r0} generated an exception: {exc}")
            else:
                if data is not None:
                    return data
        """
    return None


        
# Generate solutions for 5x5, 6x6 or 7x7
def generate_solutions(row_sums,col_sums, n, debug=True):

    grid = np.full((n,n), -1)    
    # get row 0
    rows0 = get_firstrow_permutations(row_sums[0]) 
    for r0 in rows0:           
        grid[0] = r0
        cols0 =  get_firstcol_permutations(col_sums[0], grid[0,0])
        for c0 in cols0:
            grid[:,0] = c0         
            rows1 = generate_row_permutations(n,1,row_sums[1], (grid[1,0],), grid[0,1:].tolist())            
            for r1 in rows1:                                   
                grid[1] = r1
                cols1 = generate_col_permutations(n,1,col_sums[1], tuple(grid[:2,1]), grid[2:, 0].tolist())
                #cols1 = get_col_permutations(n,1,grid[:2,1].tolist())
                for c1 in cols1:                                               
                    grid[:,1]=c1
                    rows2 = generate_row_permutations(n,2,row_sums[2], tuple(grid[2,:2]), grid[:2,2:].T.tolist())                    
                    for r2 in rows2:
                        grid[2]=r2
                        cols2 = generate_col_permutations(n,2,col_sums[2], tuple(grid[:3,2]), grid[3:, :2].tolist())
                        for c2 in cols2:
                            grid[:,2] = c2                    
                            if n == 4:
                                last = get_last_num(n, grid[-1,:-1])
                                if last is not None:
                                    grid[3,3] = last
                                    if check_row_constraint(tuple(grid[3]), row_sums[3]) and check_row_constraint(tuple(grid[:,3]), col_sums[3]):
                                        return grid
                            elif n > 4:
                                # Get row 3
                                rows3 = generate_row_permutations(n,3,row_sums[3], tuple(grid[3,:3]), grid[:3,3:].T.tolist())
                                for r3 in rows3:
                                    grid[3] = r3
                                    cols3 = generate_col_permutations(n,3,col_sums[3], tuple(grid[:4,3]), grid[4:, :3].tolist())
                                    for c3 in cols3:
                                        grid[:,3] = c3                             
                                        if n == 5:
                                            last = get_last_num(n, grid[-1,:-1])
                                            if last is not None:
                                                grid[4,4] = last
                                                if check_row_constraint(tuple(grid[4]),row_sums[4]) and check_row_constraint(tuple(grid[:,4]),col_sums[4]):
                                                    return grid
                                        elif n > 5:
                                            rows4 = generate_row_permutations(n,4,row_sums[4], tuple(grid[4,:4]), grid[:4,4:].T.tolist())
                                            for r4 in rows4:
                                                grid[4] = r4
                                                cols4 = generate_col_permutations(n,4,col_sums[4], tuple(grid[:5,4]), grid[5:, :4].tolist())
                                                for c4 in cols4:
                                                    grid[:,4] = c4
                                                    if n == 6:
                                                        last = get_last_num(n, grid[-1,:-1])
                                                        if last is not None:
                                                            grid[5,5] = last                  
                                                            if check_row_constraint(tuple(grid[5]),row_sums[5]) and check_row_constraint(tuple(grid[:,5]),col_sums[5]):
                                                                return grid
                                                    elif n > 6:
                                                        rows5 = generate_row_permutations(n,5,row_sums[5], tuple(grid[5,:5]), grid[:5,5:].T.tolist())
                                                        for r5 in rows5:
                                                            grid[5] = r5
                                                            cols5 = generate_col_permutations(n,5,col_sums[5], tuple(grid[:6,5]), grid[6:, :5].tolist())
                                                            for c5 in cols5:
                                                                grid[:,5] = c5
                                                                last = get_last_num(n, grid[-1,:-1])
                                                                if last is not None:
                                                                    grid[6,6] = last
                                                                    if check_row_constraint(tuple(grid[6]),row_sums[6]) and check_row_constraint(tuple(grid[:,6]),col_sums[6]):
                                                                        return grid   
    return None
                                        
                                                      
def print_matrix(sol):
    for col in sol:
        print(col)
        
def solve_sumaddle_puzzle(row_sums, col_sums):
    n = len(row_sums)
    initialize_subset_split_map(n)
    initialize_row_sum_map(n)   
    #sol = generate_solutions(row_sums,col_sums, n)
    sol = main_generate_solutions(row_sums,col_sums,n)        
    if sol is not None:
        print(f"Solution for a {n}x{n} with row constraint:{row_sums}, and column constraint:{col_sums}")
        print(sol)
    else:
        print("No solution")    


# In[2]:


start_time = time.time()
solve_sumaddle_puzzle([3, 1, 0, 2], [3, 0, 0,0])
print(f"Run time: {time.time() - start_time} seconds")


# In[3]:


import time
start_time = time.time()
solve_sumaddle_puzzle([5, 0, 5, 6, 0], [0, 6, 3, 0, 3])
print(f"Run time: {time.time() - start_time} seconds")


# In[4]:


start_time = time.time()
solve_sumaddle_puzzle([5, 1, 0, 5, 0], [2, 1, 0, 0, 6])
print(f"Run time: {time.time() - start_time} seconds")


# In[5]:


start_time = time.time()
solve_sumaddle_puzzle([9, 2, 4, -1 ,-1 , 3],  [7, 10, 2, -1,-1 , -1])
print(f"Run time: {time.time() - start_time} seconds")


# In[ ]:


start_time = time.time()
solve_sumaddle_puzzle([10, 0, 9, 1 ,3, 7, 3], [0, 11, 0, 8, 14, 9, 15])
print(f"Run time: {time.time() - start_time} seconds")


# In[ ]:





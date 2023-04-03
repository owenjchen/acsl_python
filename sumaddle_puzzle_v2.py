#!/usr/bin/env python
# coding: utf-8

# In[1]:


# A Python Program to Solve a Sumaddle

from itertools import combinations, permutations

# Check patterns of each row

def check_zero_zero(row):    
    for i in range(1, len(row)):
        if row[i] == 0 and row[i-1] == 0:
            return True
    return False

def check_zero_x_zero(row):    
    for i in range(2, len(row)):
        if row[i-2] == 0 and row[i-1] > 0 and row[i] == 0:
            return True
    return False

def check_zero_x_x_zero(row):
    first_zero = -1
    for i in range(len(row)):
        if row[i] == 0:
            if first_zero < 0:
                first_zero = i
            else:
                if i > (first_zero + 2):
                    return True
    return False

# Check row or column sum constraint
def check_blocksum_v2(row, s):
    if s >= 0:
        n = len(row)
        zero_index = row.index(0)
        blocksum = 0
        for i in range(zero_index+1, n):
            if row[i] > 0:
                blocksum +=row[i]
            else:
                break
        return s == blocksum
    else:
        return True

def check_blocksum(row, s):
    n = len(row)
    blocksum = 0
    found = False
    for i in range(n):
        if not found:
            if row[i] == 0:
                found = True
        elif row[i] > 0:
            blocksum +=row[i]
        else:
            break
    return s == blocksum

        
def get_num_list(n, exclude_list):
    if exclude_list:
        num_of_zeros = exclude_list.count(0)
        if num_of_zeros == 1:
            num_list = [0] + [i for i in range(1, n-1) if i not in exclude_list]
        elif num_of_zeros == 2:
             num_list =  [i for i in range(1, n-1) if i not in exclude_list]
        else:
            num_list = [0] +  [i for i in range(1, n-1) if i not in exclude_list]   
    else:
        num_list = [ i for i in range(n-1)]
    return sorted(num_list)

def get_last_num(n, exclude_list):    
    num_list =  [i for i in range(n-1) if i not in exclude_list]
    if len(num_list) == 0:
        return 0
    else:
        return num_list[0]
  

def generate_last_row(n,row_sum, prefix):
    row = []
    for i in range(n):
        exclude_numbers = prefix[i]
        last_num = get_last_num(n, exclude_numbers)
        row.append(last_num)
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
        exclude_numbers =  [r[i] for r in prefix]
        if row[i] > 0:
            if row[i] in exclude_numbers:
                return False
        else:
            if exclude_numbers.count(0) == 2:
                return False
    return True
        
    
def generate_permutations_v1(n, prefix):
    """
    Generate permutations for [0, 0, 1, 2, ... n-2] with a constraint given by a prefix
    """
    num_list_full = [0] + [ i for i in range(n-1)]
    perms = [list(val) for val in permutations(num_list_full, n)] 
    if len(prefix) and len(prefix[0]):        
        return  [row for row in perms if check_prefix_constraint(n, row, prefix)]
    else:
        return perms
    
    
def generate_permutations(n, prefix):
    # Prefix has been transformed into columns
    if prefix:
        num_perms = []   
        exclude_numbers = prefix[0]
        num_list0  = get_num_list(n, exclude_numbers)
        
        if n == 4:
            for r0 in num_list0:                
                if r0 > 0:
                    exclude_numbers =  prefix[1] + [r0]
                else:
                    exclude_numbers =  prefix[1]
                num_list1 = get_num_list(n, exclude_numbers)
                for r1 in num_list1:                 
                    parent_list = [r0, r1]           
                    exclude_numbers =  prefix[2] + [k for k in parent_list if k > 0]
                    if parent_list.count(0) > 1:
                        exclude_numbers +=[0,0]
                    num_list2 = get_num_list(n, exclude_numbers) 
                    for r2 in num_list2:
                        exclude_numbers = [r0, r1, r2]
                        r3 = get_last_num(n, exclude_numbers)
                        num_perms.append((r0, r1, r2, r3))    
        elif n == 5:      
            for r0 in num_list0:
                if r0 > 0:
                    exclude_numbers =  prefix[1] + [r0]
                else:
                    exclude_numbers =  prefix[1]
                num_list1 = get_num_list(n, exclude_numbers)
                for r1 in num_list1:                 
                    parent_list = [r0, r1]           
                    exclude_numbers =  prefix[2] + [k for k in parent_list if k > 0]
                    if parent_list.count(0) > 1:
                        exclude_numbers +=[0,0]
                    num_list2 = get_num_list(n, exclude_numbers) 
                    for r2 in num_list2:
                        parent_list = [r0, r1, r2]
                        exclude_numbers =  prefix[3] + [k for k in parent_list if k > 0]
                        if parent_list.count(0) > 1:
                            exclude_numbers +=[0,0]                 
                        num_list3 = get_num_list(n, exclude_numbers)  
                        for r3 in num_list3:
                            exclude_numbers = [r0, r1, r2, r3]
                            r4 = get_last_num(n, exclude_numbers)
                            num_perms.append((r0, r1, r2, r3,r4))
        elif n == 6:      
            for r0 in num_list0:
                if r0 > 0:
                    exclude_numbers =  prefix[1] + [r0]
                else:
                    exclude_numbers =  prefix[1]
                num_list1 = get_num_list(n, exclude_numbers)
                for r1 in num_list1:                 
                    parent_list = [r0, r1]           
                    exclude_numbers =  prefix[2] + [k for k in parent_list if k > 0]
                    if parent_list.count(0) > 1:
                        exclude_numbers +=[0,0]
                    num_list2 = get_num_list(n, exclude_numbers) 
                    for r2 in num_list2:
                        parent_list = [r0, r1, r2]
                        exclude_numbers =  prefix[3] + [k for k in parent_list if k > 0]
                        if parent_list.count(0) > 1:
                            exclude_numbers +=[0,0]               
                        num_list3 = get_num_list(n, exclude_numbers)  
                        for r3 in num_list3:
                            parent_list = [r0, r1, r2, r3]
                            exclude_numbers =  prefix[4] + [k for k in parent_list if k > 0]
                            if parent_list.count(0) > 1:
                                exclude_numbers +=[0,0]                 
                            num_list4 = get_num_list(n, exclude_numbers)                          
                            for r4 in num_list4:
                                exclude_numbers = [r0,r1,r2,r3,r4]
                                r5 = get_last_num(n, exclude_numbers)
                                num_perms.append((r0,r1,r2,r3,r4,r5))
        elif n == 7:      
            for r0 in num_list0:
                if r0 > 0:
                    exclude_numbers =  prefix[1] + [r0]
                else:
                    exclude_numbers =  prefix[1]
                num_list1 = get_num_list(n, exclude_numbers)
                for r1 in num_list1:                 
                    parent_list = [r0, r1]           
                    exclude_numbers =  prefix[2] + [k for k in parent_list if k > 0]
                    if parent_list.count(0) > 1:
                        exclude_numbers +=[0,0]
                    num_list2 = get_num_list(n, exclude_numbers) 
                    for r2 in num_list2:
                        parent_list = [r0, r1, r2]
                        exclude_numbers =  prefix[3] + [k for k in parent_list if k > 0]
                        if parent_list.count(0) > 1:
                            exclude_numbers +=[0,0]               
                        num_list3 = get_num_list(n, exclude_numbers)  
                        for r3 in num_list3:
                            parent_list = [r0, r1, r2, r3]
                            exclude_numbers =  prefix[4] + [k for k in parent_list if k > 0]
                            if parent_list.count(0) > 1:
                                exclude_numbers +=[0,0]                    
                            num_list4 = get_num_list(n, exclude_numbers)                               
                            for r4 in num_list4:
                                parent_list = [r0, r1, r2, r3, r4]
                                exclude_numbers =  prefix[5] + [k for k in parent_list if k > 0]
                                if parent_list.count(0) > 1:
                                    exclude_numbers +=[0,0]                       
                                num_list5 = get_num_list(n, exclude_numbers)                          
                                for r5 in num_list5:
                                    exclude_numbers = [r0,r1,r2,r3,r4,r5]
                                    r6 = get_last_num(n, exclude_numbers)
                                    num_perms.append((r0,r1,r2,r3,r4,r5,r6))   
                                                     
                            
    else:
        num_list_full = [0] + [i for i in range(n-1)]
        num_perms = [ val for val in permutations(num_list_full, n)]
    
    return num_perms

def generate_row_candidates(n,row_sum, prefix):
    candidates = generate_permutations(n, prefix) 
    if candidates:
        # Filter row candidates
        if row_sum == 0:
            return [row for row in candidates if check_zero_zero(row)]
        elif row_sum > 0: 
            return [row for row in candidates if check_blocksum(row, row_sum)]  
        else:
            return candidates
        
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
        col = [row[i] for row in sol]
        if col_sums[i] == 0:
            if not check_zero_zero(col):
                return False
        elif col_sums[i] > 0:
            if not check_blocksum(col, col_sums[i]):
                return False
    return True

# Generate solutions for 5x5, 6x6 or 7x7
def generate_solutions(row_sums,col_sums, n):
    if n == 4:
        row_candidates0 = generate_row_candidates(n,row_sums[0], None)
        for r0 in row_candidates0:
            prefix = [[r0[i]] for i in range(n)]
            row_candidates1 = generate_row_candidates(n,row_sums[1], prefix) 
            for r1 in row_candidates1:  
                prefix = [[r0[i], r1[i]] for i in range(n)]
                row_candidates2 = generate_row_candidates(n,row_sums[2], prefix)             
                for r2 in row_candidates2:  
                    prefix = [[r0[i], r1[i], r2[i]] for i in range(n)]
                    r3 = generate_last_row(n,row_sums[3], prefix) 
                    if r3:  
                        sol = [r0,r1,r2,r3] 
                        if check_col_constraint(sol, col_sums, n): 
                            return sol
    elif n == 5:
        row_candidates0 = generate_row_candidates(n,row_sums[0], None)
        for r0 in row_candidates0:
            prefix = [[r0[i]] for i in range(n)]
            row_candidates1 = generate_row_candidates(n,row_sums[1], prefix) 
            for r1 in row_candidates1:  
                prefix = [[r0[i], r1[i]] for i in range(n)]
                row_candidates2 = generate_row_candidates(n,row_sums[2], prefix)             
                for r2 in row_candidates2:
                    prefix = [[r0[i], r1[i], r2[i]] for i in range(n)]
                    row_candidates3 = generate_row_candidates(n,row_sums[3], prefix)  
                    for r3 in row_candidates3:  
                        prefix = [[r0[i], r1[i], r2[i], r3[i]] for i in range(n)]
                        r4 = generate_last_row(n,row_sums[4], prefix) 
                        if r4:  
                            sol = [r0,r1,r2,r3,r4] 
                            if check_col_constraint(sol, col_sums, n): 
                                return sol
    elif n == 6:
        row_candidates0 = generate_row_candidates(n,row_sums[0], None)
        for r0 in row_candidates0:
            prefix = [[r0[i]] for i in range(n)]
            row_candidates1 = generate_row_candidates(n,row_sums[1], prefix) 
            for r1 in row_candidates1:  
                prefix = [[r0[i], r1[i]] for i in range(n)]
                row_candidates2 = generate_row_candidates(n,row_sums[2], prefix)  
                for r2 in row_candidates2:
                    prefix = [[r0[i], r1[i], r2[i]] for i in range(n)]
                    row_candidates3 = generate_row_candidates(n,row_sums[3], prefix)
                    for r3 in row_candidates3:  
                        prefix = [[r0[i], r1[i], r2[i], r3[i]] for i in range(n)]
                        row_candidates4 = generate_row_candidates(n,row_sums[4], prefix)   
                        for r4 in row_candidates4:  
                            prefix = [[r0[i], r1[i], r2[i], r3[i], r4[i]] for i in range(n)]                            
                            r5 = generate_last_row(n,row_sums[5], prefix) 
                            if r5:  
                                sol = [r0,r1,r2,r3,r4,r5] 
                                if check_col_constraint(sol, col_sums, n): 
                                    return sol                              
    elif n == 7:
        row_candidates0 = generate_row_candidates(n,row_sums[0], None)
        for r0 in row_candidates0:
            prefix = [[r0[i]] for i in range(n)]
            row_candidates1 = generate_row_candidates(n,row_sums[1], prefix) 
            for r1 in row_candidates1:  
                prefix = [[r0[i], r1[i]] for i in range(n)]
                row_candidates2 = generate_row_candidates(n,row_sums[2], prefix)             
                for r2 in row_candidates2:
                    prefix = [[r0[i], r1[i], r2[i]] for i in range(n)]
                    row_candidates3 = generate_row_candidates(n,row_sums[3], prefix)  
                    for r3 in row_candidates3:  
                        prefix = [[r0[i], r1[i], r2[i], r3[i]] for i in range(n)]
                        row_candidates4 = generate_row_candidates(n,row_sums[4], prefix)                      
                        for r4 in row_candidates4:  
                            prefix = [[r0[i], r1[i], r2[i], r3[i], r4[i]] for i in range(n)]    
                            row_candidates5 = generate_row_candidates(n,row_sums[5], prefix)               
                            for r5 in row_candidates5:  
                                prefix = [[r0[i], r1[i], r2[i], r3[i], r4[i], r5[i]] for i in range(n)]    
                                r6 = generate_last_row(n,row_sums[6],prefix)
                                if r6:  
                                    sol = [r0,r1,r2,r3,r4,r5,r6] 
                                    if check_col_constraint(sol, col_sums, n): 
                                        return sol    
        
    else:
        raise Exception("Sorry, the input n must be 5, 6, or 7")
    return None

def print_matrix(sol):
    for col in sol:
        print(col)
        
def solve_sumaddle_puzzle(row_sums, col_sums):
    n = len(row_sums)
    sol = generate_solutions(row_sums,col_sums, n)    
    if sol:
        print(f"Solution for a {n}x{n} with row constraint:{row_sums}, and column constraint:{col_sums}")
        print_matrix(sol)
    else:
        print("No solution")    


# In[2]:


import time
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


# In[6]:


"""
## 7x7 will run a long time
start_time = time.time()
solve_sumaddle_puzzle([10, 0, 9, 1 ,3, 7, 3], [0, 11, 0, 8, 14, 9, 15])
print(f"Run time: {time.time() - start_time} seconds")
"""


# In[ ]:





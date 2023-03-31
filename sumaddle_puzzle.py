# A Python Program to Solve a Sumaddle

from itertools import combinations, permutations

def check_consecutive_zeros(row):    
    for i in range(1, len(row)):
        if row[i] == 0 and row[i-1] == 0:
            return True
    return False
                   
def generate_candidates(n):
    num_ranges = [0] + [ i for i in range(n-1)]
    num_perms = [ val for val in permutations(num_ranges, n)]
    candidates_separate_zeros= []
    candidates_consecutive_zeros = []
    for row in num_perms:
        if check_consecutive_zeros(row):
            candidates_consecutive_zeros.append(row)
        else:
            candidates_separate_zeros.append(row)
    return candidates_separate_zeros, candidates_consecutive_zeros

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

def generate_constrained_candidates(sums, n):    
    candidates1, candidates2 = generate_candidates(n)
    # Generate puzzle candidates from each combination of row_candidates
    candidates = [[] for i in range(n)]
    for i in range(n):
        row = []
        if sums[i] == 0:
            row = candidates2
        elif sums[i] > 0:
            for candidate in candidates1:
                if check_blocksum(candidate, sums[i]):
                    row.append(candidate)
        else:
            row = candidates1 + candidates2
        candidates[i] = row        
    return candidates


def check_col(col):
    seen = {}
    for val in col:
        if val in seen.keys():
            if val > 0:
                return False
            elif seen[val] > 1:
                return False
            else:
                seen[val] +=1
        else:
            seen[val]  = 1
    return True

def check_sol(sol,n):
    for i in range(n):
        col = [row[i] for row in sol]
        if not check_col(col):
            return False
    return True

def check_col_constraint(sol, col_sums, n): 
    nrow = len(sol)
    for i in range(n):
        col = [row[i] for row in sol]
        if not check_col(col):
            return False
        if col_sums[i] == 0:
            if not check_consecutive_zeros(col):
                return False
        elif col_sums[i] > 0:
            if not check_blocksum(col, col_sums[i]):
                return False
    return True

# Generate solutions for 5x5, 6x6 or 7x7
def generate_solutions(row_candidates,col_sums, n):
    r = [i for i in range(n)]
    if n == 5:
        for r[0] in row_candidates[0]:
                sol = r[0]
                for r[1] in row_candidates[1]:
                    sol = [r[0], r[1]]
                    if not check_sol(sol,n):
                        continue
                    else:                  
                        for r[2] in row_candidates[2]:
                            sol = [r[0], r[1], r[2]]
                            if not check_sol(sol,n):
                                continue
                            else:                                                                 
                                for r[3] in row_candidates[3]:    
                                    sol = [r[i] for i in range(4)]
                                    if not check_sol(sol,n):
                                        continue                                    
                                    for r[4] in row_candidates[4]:
                                        sol = [r[i] for i in range(5)]            
                                        if check_col_constraint(sol, col_sums, n): 
                                            return sol
    elif n == 6:
        for r[0] in row_candidates[0]:
                sol = r[0]
                for r[1] in row_candidates[1]:
                    sol = [r[0], r[1]]
                    if not check_sol(sol,n):
                        continue
                    else:                  
                        for r[2] in row_candidates[2]:
                            sol = [r[0], r[1], r[2]]
                            if not check_sol(sol,n):
                                continue
                            else:                                                                 
                                for r[3] in row_candidates[3]:    
                                    sol = [r[i] for i in range(4)]
                                    if not check_sol(sol,n):
                                        continue                                    
                                    for r[4] in row_candidates[4]:                                        
                                        sol = [r[i] for i in range(5)]            
                                        if not check_sol(sol,n):
                                            continue                                                 
                                        else:
                                            for r[5] in row_candidates[5]:
                                                sol = [r[i] for i in range(6)]                                           
                                                if check_col_constraint(sol, col_sums, n): 
                                                    return sol                                        
    elif n == 7:
        for r[0] in row_candidates[0]:
                sol = r[0]
                for r[1] in row_candidates[1]:
                    sol = [r[0], r[1]]
                    if not check_sol(sol,n):
                        continue
                    else:                  
                        for r[2] in row_candidates[2]:
                            sol = [r[0], r[1], r[2]]
                            if not check_sol(sol,n):
                                continue
                            else:                                                                 
                                for r[3] in row_candidates[3]:    
                                    sol = [r[i] for i in range(4)] 
                                    if not check_sol(sol,n):
                                        continue
                                    else:
                                        for r[4] in row_candidates[4]:    
                                            sol = [r[i] for i in range(5)]  
                                            if not check_sol(sol,n):
                                                continue
                                            else:                                        
                                                for r[5] in row_candidates[5]:
                                                    sol = [r[i] for i in range(6)]                          
                                                    if not check_sol(sol,n):
                                                        continue
                                                    else:                                        
                                                        for r[6] in row_candidates[6]:
                                                            sol = [r[i] for i in range(7)]                      
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
    row_candidates = generate_constrained_candidates(row_sums, n)
    sol = generate_solutions(row_candidates,col_sums, n)    
    if sol:
        print(f"Solution for a {n}x{n} with row constraint:{row_sums}, and column constraint:{col_sums}")
        print_matrix(sol)
    else:
        print("No solution")    

        
# Test problem on 5x5
solve_sumaddle_puzzle([5, 0, 5, 6, 0], [0, 6, 3, 0, 3])

# Brian's problems
# 5x5
solve_sumaddle_puzzle([5, 1, 0, 5, 0], [2, 1, 0, 0, 6])

# 6x6
solve_sumaddle_puzzle([9, 2, 4, -1 ,-1 , 3],  [7, 10, 2, -1,-1 , -1])

# 7x7
solve_sumaddle_puzzle([10, 0, 9, 1 ,3, 7, 3], [0, 11, 0, 8, 14, 9, 15])
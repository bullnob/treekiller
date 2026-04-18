import subprocess
import time
import random
import os


N = 10000        # Using 10k instead of 100k so the Genetic Algorithm evolves faster
P_LEN = N - 2
T_LIM = 2.0      # Timeout in seconds (Fitness cap)
POP_SZ = 30      # Population size per generation
GENS = 50        # Number of generations
MUT_RT = 0.1     # 10% chance to mutate a node in the sequence

def prufer_to_tree(p):
    """Prufer sequence to Tree Edges"""
    deg = [1] * (N + 1)
    for node in p:
        deg[node] += 1
    
    ptr = 1
    while deg[ptr] != 1:
        ptr += 1
    leaf = ptr
    
    edges = []
    for node in p:
        edges.append(f"{leaf} {node}")
        deg[node] -= 1
        if node < ptr and deg[node] == 1:
            leaf = node
        else:
            ptr += 1
            while ptr <= N and deg[ptr] != 1:
                ptr += 1
            leaf = ptr
            
    # Connect the last two remaining nodes
    u, v = -1, -1
    for i in range(1, N + 1):
        if deg[i] == 1:
            if u == -1:
                u = i
            else:
                v = i
                break
    edges.append(f"{u} {v}")
    return edges

def gen_input(p):
    """ Formats the test case exactly how CF expects it """
    edges = prufer_to_tree(p)
    # Generate random values for the 'a' array (XOR values)
    a_vals = [str(random.randint(0, 1000000)) for _ in range(N)]
    
    tc = f"{N}\n"
    tc += " ".join(a_vals) + "\n"
    tc += "\n".join(edges) + "\n"
    return tc

def get_fit(p):
    """ Fitness function: Execution time of the C++ binary """
    tc = gen_input(p)
    st = time.perf_counter()
    try:
        # Pass the generated test case to the C++ executable via stdin
        subprocess.run(
            ["./target"], 
            input=tc.encode(), 
            timeout=T_LIM, 
            capture_output=True
        )
    except subprocess.TimeoutExpired:
        return T_LIM # Target hit TLE!
    
    return time.perf_counter() - st

def init_pop():
    return [[random.randint(1, N) for _ in range(P_LEN)] for _ in range(POP_SZ)]

def cx(p1, p2):
    """ Single point crossover """
    mid = random.randint(0, P_LEN - 1)
    return p1[:mid] + p2[mid:]

def mut(p):
    """ Mutate random nodes in the sequence """
    for i in range(P_LEN):
        if random.random() < MUT_RT:
            p[i] = random.randint(1, N)
    return p

def run_ga():
    print("Initializing Population...")
    pop = init_pop()
    
    for g in range(GENS):
        print(f"--- Generation {g} ---")
        
        # 1. Evaluate Fitness (Execution Time)
        fits = []
        for i, p in enumerate(pop):
            fit = get_fit(p)
            fits.append((fit, p))
            
        # Sort descending (longest execution time is best)
        fits.sort(reverse=True, key=lambda x: x[0])
        best_fit = fits[0][0]
        
        print(f"Best Execution Time: {best_fit:.4f} seconds")
        
        # 2. Check for TLE
        if best_fit >= T_LIM:
            print("\n TLE TRIGGERED! Killer testcase found!")
            killer_tc = gen_input(fits[0][1])
            with open("killer_testcase.txt", "w") as f:
                f.write(killer_tc)
            print("Saved to 'killer_testcase.txt'.")
            break
            
        # 3. Selection (Keep top 20%)
        keep = int(POP_SZ * 0.2)
        nx_pop = [x[1] for x in fits[:keep]]
        
        # 4. Crossover & Mutation to refill population
        while len(nx_pop) < POP_SZ:
            p1 = random.choice(fits[:keep])[1]
            p2 = random.choice(fits[:keep])[1]
            ch = mut(cx(p1, p2))
            nx_pop.append(ch)
            
        pop = nx_pop

if __name__ == "__main__":
    if not os.path.exists("target"):
        print("Error: Compile 'target.cpp' to 'target' first.")
    else:
        run_ga()
# TreeKiller: ML-Guided Structural Fuzzer

An evolutionary fuzzer designed to automatically discover worst-case execution paths (Time Limit Exceeded) in C++ tree algorithms. 

Unlike standard binary fuzzers (like AFL) that feed random bytes into a program, **Treekiller** uses a Genetic Algorithm to evolve heavily structured inputs—specifically ensuring that every generated test case is a perfectly valid, fully connected mathematical Tree.

## The Problem :

In Competitive Programming and Systems Engineering, an algorithm might have an optimal average-case time complexity, but degrade to $O(N^2)$ under highly specific structural conditions (e.g., deep "Line Graphs" or dense "Star Graphs"). 

Standard random fuzzing is useless for tree problems because mutating raw edge lists almost always creates invalid graphs (cycles or disconnected components), which the target program immediately rejects. 

## The Solution: Genetic Algorithms + Prüfer Sequences

To ensure the fuzzer only explores valid tree states, this project represents trees internally as **Prüfer Sequences**.

1. **Representation:** By Cayley's formula, every labeled tree of $N$ vertices can be uniquely represented by a sequence of $N-2$ integers.
2. **Evaluation:** The Python fuzzer decodes the sequence in $O(N)$ time, formats it as a valid competitive programming test case, and pipes it into the compiled C++ binary via `stdin`.
3. **Fitness:** The "Fitness Score" is the actual execution time of the C++ binary measured via OS-level subprocess monitoring.
4. **Evolution:** The Genetic Algorithm selects the arrays that took the longest to execute, applying crossover and mutation to "breed" increasingly difficult tree topologies over successive generations.

## Example Target: Breaking Naive State Merging

The provided `target.cpp` contains a DFS algorithm that merges `std::set` data structures. 
* It is missing the standard "Small-to-Large" swap optimization.
* Under normal/random tree conditions, it executes in `< 0.05s`.
* When run through PruferFuzz, the Genetic Algorithm naturally learns to filter out duplicate numbers in the Prüfer sequence, evolving the tree from a shallow, random structure into a massive $10,000$-node "Line Graph", successfully triggering a `2.0s` TLE timeout.

## Usage

**1. Compile the target C++ binary (with optimizations):**
```bash
g++ -O2 target.cpp -o target
```

**2. Run the fuzzer:**
```bash
python3 main.py
```

**3. Retrieve the killer testcase:**

he fuzzer will output the best execution time per generation. Once it hits the time limit, it halts and saves the exact input array and edge list to ```killer_testcase.txt```.

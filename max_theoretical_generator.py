import os
from collections import defaultdict

def generate_automaton(n, output_dir):
    states = list(range(n))
    alphabet = ['0', '1']
    initial = 0
    accepting = [0]
    transitions = defaultdict(list)
    
    # Rule 1: (i,0,i+1) for 0≤i≤n-2
    for i in range(n-1):
        transitions[(i, '0')].append(i+1)
    
    # Rule 2: (n−1,0,0)
    transitions[(n-1, '0')].append(0)
    
    # Rule 3: (i,1,i) for 1≤i≤n−1
    for i in range(1, n):
        transitions[(i, '1')].append(i)
    
    # Rule 4: (i,1,0) for 1≤i≤n−1
    for i in range(1, n):
        transitions[(i, '1')].append(0)
    
    # Format the NFA in the specified format
    lines = []
    lines.append(f"states: {','.join(map(str, states))}")
    lines.append(f"alphabet: {','.join(alphabet)}")
    lines.append(f"initial: {initial}")
    lines.append(f"accepting: {','.join(map(str, accepting))}")
    
    for (src, sym), targets in transitions.items():
        for tgt in targets:
            lines.append(f"transition: {src},{sym} -> {tgt}")

    # Make sure the directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"automaton_n{n}.txt")

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Automaton written to: {output_path}")

# Generate automata for n from 2 to 10
for n in range(2, 11):
    generate_automaton(n, "max_nfa_output")
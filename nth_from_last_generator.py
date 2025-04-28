import os
from collections import defaultdict

def generate_nfa_text(n, output_dir):
    states = list(range(n + 2))
    alphabet = ['0', '1']
    initial = 0
    accepting = [n + 1]
    transitions = defaultdict(list)

    # Self-loops on state 0 to consume any number of characters
    for symbol in alphabet:
        transitions[(0, symbol)].append(0)

    # On seeing '1', nondeterministically guess that it is the nth-from-last character
    transitions[(0, '1')].append(1)

    # From state 1 to n+1, consume exactly (n-1) more characters
    for i in range(1, n + 1):
        for symbol in alphabet:
            transitions[(i, symbol)].append(i + 1)

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
    output_path = os.path.join(output_dir, f"nfa_nth_from_last_n{n}.txt")

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"NFA written to: {output_path}")

for n in range(2, 10):  # Generate NFAs for n from 1 to 20
    generate_nfa_text(n, "nfa_nth_from_last")

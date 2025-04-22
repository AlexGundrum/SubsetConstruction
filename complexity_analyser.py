import os
import time
import re
from nfa import NFA
from dfa import DFA
from nfa_parser import parse_nfa_file

def extract_state_count(filename):
    match = re.search(r'nfa_(\d+)_states\.txt', filename)
    return int(match.group(1)) if match else float('inf')  # 'inf' pushes unknowns to end

def analyze_dfa_complexity(nfa_folder_path):
    results = []

    # Properly sort by number of states in the filename
    filenames = sorted(
        [f for f in os.listdir(nfa_folder_path) if f.endswith(".txt")],
        key=extract_state_count
    )

    for filename in filenames:
        filepath = os.path.join(nfa_folder_path, filename)

        # Parse NFA
        nfa_tuple = parse_nfa_file(filepath)
        nfa = NFA(nfa_tuple[0], nfa_tuple[2], nfa_tuple[3], nfa_tuple[4], nfa_tuple[1])

        # Measure time for subset construction
        start_time = time.time()
        dfa = DFA(nfa)
        elapsed_time = time.time() - start_time

        num_dfa_states = len(dfa.states)
        num_dfa_transitions = len(dfa.delta_transition)

        results.append({
            "filename": filename,
            "nfa_states": len(nfa_tuple[0]),
            "dfa_states": num_dfa_states,
            "dfa_transitions": num_dfa_transitions,
            "construction_time_sec": elapsed_time
        })

        print(f"{filename} → DFA States: {num_dfa_states}, Transitions: {num_dfa_transitions}, Time: {elapsed_time:.6f}s")

    return results

import matplotlib.pyplot as plt

def plot_dfa_complexity(results):
    # Sort results by NFA size for consistency
    results.sort(key=lambda x: x["nfa_states"])

    nfa_sizes = [r["nfa_states"] for r in results]
    dfa_states = [r["dfa_states"] for r in results]
    dfa_transitions = [r["dfa_transitions"] for r in results]
    construction_times = [r["construction_time_sec"] for r in results]

    plt.figure(figsize=(12, 6))

    # Subplot 1: DFA states and transitions vs NFA states
    plt.subplot(1, 2, 1)
    plt.plot(nfa_sizes, dfa_states, marker='o', label='DFA States')
    plt.plot(nfa_sizes, dfa_transitions, marker='x', label='DFA Transitions')
    plt.xlabel("Number of NFA States")
    plt.ylabel("Count")
    plt.title("DFA Size vs NFA Size")
    plt.legend()
    plt.grid(True)

    # Subplot 2: Time vs NFA states
    plt.subplot(1, 2, 2)
    plt.plot(nfa_sizes, construction_times, marker='s', color='red')
    plt.xlabel("Number of NFA States")
    plt.ylabel("Construction Time (seconds)")
    plt.title("DFA Subset Construction Time")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# Run the analysis
nfa_dir = "generated_nfas"
results=analyze_dfa_complexity(nfa_dir)
print("Analysis Results:")
for result in results:
    print(result)
plot_dfa_complexity(results)
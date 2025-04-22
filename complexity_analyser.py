import os
import time
import re
import matplotlib.pyplot as plt
import numpy as np
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

        # Count total transitions and epsilon transitions
        total_transitions = 0
        epsilon_transitions = 0
        for key, value in nfa_tuple[2].items():
            if key[1] == "epsilon":
                epsilon_transitions += len(value)
            total_transitions += len(value)

        # Calculate transition density (transitions per state)
        transition_density = total_transitions / len(nfa_tuple[0])
        epsilon_density = epsilon_transitions / total_transitions if total_transitions > 0 else 0

        # Measure time for subset construction
        start_time = time.time()
        dfa = DFA(nfa)
        elapsed_time = time.time() - start_time

        num_dfa_states = len(dfa.states)
        num_dfa_transitions = len(dfa.delta_transition)

        # Calculate theoretical maximum (2^n)
        theoretical_max = 2 ** len(nfa_tuple[0])

        results.append({
            "filename": filename,
            "nfa_states": len(nfa_tuple[0]),
            "dfa_states": num_dfa_states,
            "dfa_transitions": num_dfa_transitions,
            "construction_time_sec": elapsed_time,
            "transition_density": transition_density,
            "epsilon_density": epsilon_density,
            "theoretical_max": theoretical_max,
            "percentage_of_theoretical": (num_dfa_states / theoretical_max) * 100 if theoretical_max > 0 else 0
        })

        print(f"{filename} → NFA States: {len(nfa_tuple[0])}, DFA States: {num_dfa_states}, "
              f"Transitions: {num_dfa_transitions}, Time: {elapsed_time:.6f}s, "
              f"Transition Density: {transition_density:.2f}, Epsilon Density: {epsilon_density:.2f}")

    return results

def plot_enhanced_complexity(results):
    # Sort results by NFA size for consistency
    results.sort(key=lambda x: x["nfa_states"])

    nfa_sizes = [r["nfa_states"] for r in results]
    dfa_states = [r["dfa_states"] for r in results]
    theoretical_max = [r["theoretical_max"] for r in results]
    percentage_theoretical = [r["percentage_of_theoretical"] for r in results]
    transition_density = [r["transition_density"] for r in results]
    epsilon_density = [r["epsilon_density"] for r in results]

    plt.figure(figsize=(15, 10))

    # Subplot 1: DFA states vs NFA states with theoretical max
    plt.subplot(2, 2, 1)
    plt.plot(nfa_sizes, dfa_states, marker='o', label='Actual DFA States')
    plt.plot(nfa_sizes, theoretical_max, marker='x', linestyle='--', label='Theoretical Max (2^n)')
    
    # Use logarithmic scale for y-axis to better show exponential relationship
    plt.yscale('log')
    plt.xlabel("Number of NFA States")
    plt.ylabel("Number of DFA States (log scale)")
    plt.title("DFA States vs NFA States")
    plt.legend()
    plt.grid(True)

    # Subplot 2: Percentage of theoretical maximum
    plt.subplot(2, 2, 2)
    plt.bar(nfa_sizes, percentage_theoretical, alpha=0.7)
    plt.xlabel("Number of NFA States")
    plt.ylabel("% of Theoretical Maximum (2^n)")
    plt.title("DFA States as % of Theoretical Maximum")
    plt.grid(True, axis='y')

    # Subplot 3: Relationship between transition density and DFA state count
    plt.subplot(2, 2, 3)
    plt.scatter(transition_density, dfa_states, c=nfa_sizes, cmap='viridis')
    plt.colorbar(label='NFA State Count')
    plt.xlabel("Transition Density (Transitions per State)")
    plt.ylabel("DFA States")
    plt.title("Impact of Transition Density on DFA Size")
    plt.grid(True)

    # Subplot 4: Relationship between epsilon density and DFA state count
    plt.subplot(2, 2, 4)
    plt.scatter(epsilon_density, dfa_states, c=nfa_sizes, cmap='plasma')
    plt.colorbar(label='NFA State Count')
    plt.xlabel("Epsilon Transition Density")
    plt.ylabel("DFA States")
    plt.title("Impact of Epsilon Transitions on DFA Size")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("nfa_dfa_complexity_analysis.png")
    plt.show()

# Run the analysis on the improved NFAs
improved_nfa_dir = "nfa_nth_from_last"  # Directory containing improved NFAs

print("Analyzing improved NFAs...")
improved_results = analyze_dfa_complexity(improved_nfa_dir)
plot_enhanced_complexity(improved_results)

# # If you want to compare with the original NFAs:
# original_nfa_dir = "generated"  # Directory containing original NFAs
# if os.path.exists(original_nfa_dir):
#     print("\nAnalyzing original NFAs for comparison...")
#     # Just analyze a small sample of the original NFAs for comparison
#     sample_original_results = analyze_dfa_complexity(original_nfa_dir)
    
#     # Create comparison plot
#     plt.figure(figsize=(12, 6))
    
#     # Get data
#     orig_nfa_sizes = [r["nfa_states"] for r in sample_original_results]
#     orig_dfa_states = [r["dfa_states"] for r in sample_original_results]
#     improved_nfa_sizes = [r["nfa_states"] for r in improved_results]
#     improved_dfa_states = [r["dfa_states"] for r in improved_results]
    
#     # Plot comparison
#     plt.plot(orig_nfa_sizes, orig_dfa_states, marker='o', label='Original NFAs')
#     plt.plot(improved_nfa_sizes, improved_dfa_states, marker='x', label='Improved NFAs')
    
#     # Add theoretical maximum line for reference
#     x_range = range(1, max(max(orig_nfa_sizes), max(improved_nfa_sizes)) + 1)
#     theoretical = [2**x for x in x_range]
#     plt.plot(x_range, theoretical, linestyle='--', label='Theoretical Max (2^n)')
    
#     plt.yscale('log')
#     plt.xlabel("Number of NFA States")
#     plt.ylabel("Number of DFA States (log scale)")
#     plt.title("Comparison: Original vs Improved NFA-DFA Relationship")
#     plt.legend()
#     plt.grid(True)
#     plt.savefig("nfa_dfa_comparison.png")
#     plt.show()
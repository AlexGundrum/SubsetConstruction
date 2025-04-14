from collections import defaultdict

def parse_nfa_file(file_path):
    nfa_set_of_states = set()
    nfa_alphabet = []
    nfa_delta_transition = defaultdict(list)
    nfa_initial_state = None
    nfa_accepting_states = set()

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("states:"):
                nfa_set_of_states = set(map(int, line.split(":")[1].split(",")))
            elif line.startswith("alphabet:"):
                nfa_alphabet = list(map(int, line.split(":")[1].split(",")))
            elif line.startswith("initial:"):
                nfa_initial_state = int(line.split(":")[1])
            elif line.startswith("accepting:"):
                nfa_accepting_states = set(map(int, line.split(":")[1].split(",")))
            elif line.startswith("transition:"):
                raw = line.split("->")
                left = raw[0].split(":")[1].strip().split(",")
                right = list(map(int, raw[1].strip().split(",")))
                state = int(left[0])
                symbol = left[1].strip()
                symbol = symbol if symbol == "epsilon" else int(symbol)
                nfa_delta_transition[(state, symbol)].extend(right)

    return (nfa_set_of_states, nfa_alphabet, nfa_delta_transition,
            nfa_initial_state, nfa_accepting_states)

# Example usage
nfa_file = "sample_nfa.txt"
(states, alphabet, transitions, initial, accepting) = parse_nfa_file(nfa_file)

print("States:", states)
print("Alphabet:", alphabet)
print("Initial:", initial)
print("Accepting:", accepting)
print("Transitions:")
for key, value in transitions.items():
    print(f"  {key} -> {value}")

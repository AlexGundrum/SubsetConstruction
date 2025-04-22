import random
import os

def generate_random_nfa(n_states, n_transitions_per_state=2, alphabet=[0, 1]):
    lines = []

    states = list(range(1, n_states + 1))
    initial_state = states[0]
    accepting_states = random.sample(states, k=max(1, n_states // 3))

    lines.append("states: " + ",".join(map(str, states)))
    lines.append("alphabet: " + ",".join(map(str, alphabet)))
    lines.append(f"initial: {initial_state}")
    lines.append("accepting: " + ",".join(map(str, accepting_states)))

    for state in states:
        for _ in range(n_transitions_per_state):
            symbol = random.choice(alphabet + ["epsilon"])
            to_states = random.sample(states, k=random.randint(1, 2))
            line = f"transition: {state},{symbol} -> {','.join(map(str, to_states))}"
            lines.append(line)

    return "\n".join(lines)

# Create directory for generated NFAs
output_dir = "generated_nfas"
os.makedirs(output_dir, exist_ok=True)

# Generate and save NFA files
for n in range(2, 1000):  # Can go higher if needed
    text = generate_random_nfa(n)
    filepath = os.path.join(output_dir, f"nfa_{n}_states.txt")
    with open(filepath, "w") as f:
        f.write(text)
    print(f"Generated {filepath}")

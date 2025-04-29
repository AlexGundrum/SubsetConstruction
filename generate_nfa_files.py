import random
import os

def generate_improved_nfa(n_states, alphabet=[0, 1], epsilon_density=0.3):
    """
    Generate an NFA with better connectivity to demonstrate exponential DFA growth.
    
    Key improvements:
    1. Scale transition count with state count
    2. Ensure all states are reachable
    3. Control epsilon transition density
    4. Better state connectivity patterns
    """
    lines = []

    # Generate states
    states = list(range(1, n_states + 1))
    initial_state = states[0]
    accepting_states = random.sample(states, k=max(1, n_states // 3))

    # Write basic NFA structure
    lines.append("states: " + ",".join(map(str, states)))
    lines.append("alphabet: " + ",".join(map(str, alphabet)))
    lines.append(f"initial: {initial_state}")
    lines.append("accepting: " + ",".join(map(str, accepting_states)))

    # Create a dictionary to track transitions
    transitions = {}
    
    # Track which states are connected to ensure full reachability
    reachable_states = {initial_state}
    
    # IMPROVEMENT 1: Scale transitions with state count - no fixed cap
    # This creates consistent density as NFA grows
    min_transitions = min(2, n_states - 1)
    
    
  
    max_transitions = max(min_transitions + 1, n_states - 1)
    
    
    # Ensure every state is reachable by creating a spanning tree first
    unreached_states = set(states) - reachable_states
    
    # IMPROVEMENT 2: Create a spanning tree of states to ensure connectivity
    # This guarantees all states are reachable from the initial state
    while unreached_states:
        from_state = random.choice(list(reachable_states))
        to_state = random.choice(list(unreached_states))
        
        # Randomly choose either a regular or epsilon transition
        use_epsilon = random.random() < epsilon_density
        symbol = "epsilon" if use_epsilon else random.choice(alphabet)
        
        transition_key = (from_state, symbol)
        if transition_key in transitions:
            transitions[transition_key] = list(set(transitions[transition_key] + [to_state]))
        else:
            transitions[transition_key] = [to_state]
            
        reachable_states.add(to_state)
        unreached_states.remove(to_state)
    
    # IMPROVEMENT 3: Add additional transitions to create non-determinism
    # The number of additional transitions scales with the state count
    # This creates the potential for exponential behavior
    additional_transitions = n_states + random.randint(n_states // 2, n_states)
    
    for _ in range(additional_transitions):
        from_state = random.choice(states)
        
        # Decide how many target states (non-determinism factor)
        # More states = more potential for non-determinism
        target_count = random.randint(1, min(3, max(1, n_states // 5)))
        to_states = random.sample(states, k=target_count)
        
        # Choose between epsilon and regular transitions
        use_epsilon = random.random() < epsilon_density
        symbol = "epsilon" if use_epsilon else random.choice(alphabet)
        
        transition_key = (from_state, symbol)
        if transition_key in transitions:
            transitions[transition_key] = list(set(transitions[transition_key] + to_states))
        else:
            transitions[transition_key] = to_states
    
    # IMPROVEMENT 4: Add cycles to create more complex DFA behavior
    # Cycles significantly increase DFA state count
    cycle_count = random.randint(1, max(1, n_states // 3))
    for _ in range(cycle_count):
        cycle_length = random.randint(2, min(5, n_states))
        cycle_states = random.sample(states, k=cycle_length)
        
        for i in range(cycle_length):
            from_state = cycle_states[i]
            to_state = cycle_states[(i + 1) % cycle_length]
            
            # Choose between epsilon and regular transitions
            use_epsilon = random.random() < epsilon_density
            symbol = "epsilon" if use_epsilon else random.choice(alphabet)
            
            transition_key = (from_state, symbol)
            if transition_key in transitions:
                transitions[transition_key] = list(set(transitions[transition_key] + [to_state]))
            else:
                transitions[transition_key] = [to_state]
    
    # Add all transitions to the NFA definition
    for (state, symbol), to_states in transitions.items():
        line = f"transition: {state},{symbol} -> {','.join(map(str, to_states))}"
        lines.append(line)

    return "\n".join(lines)

# Create directory for improved generated NFAs
output_dir = "improved_nfas"
os.makedirs(output_dir, exist_ok=True)

# Generate a sequence of NFAs with gradually increasing size
# Focus on smaller sizes first to clearly see the pattern
# We use fewer, more strategic sizes to see the exponential pattern clearly



for n in range(2,200):
    # Variable epsilon density provides some randomness but keeps overall pattern
    epsilon_density = random.uniform(0.3, 0.5)
    
    text = generate_improved_nfa(n, epsilon_density=epsilon_density)
    
    filepath = os.path.join(output_dir, f"nfa_{n}_states.txt")
    with open(filepath, "w") as f:
        f.write(text)
    print(f"Generated {filepath}")
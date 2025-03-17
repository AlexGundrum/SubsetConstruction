class NFA:
    def __init__(self, states, delta_transition, initial_state, accepting_states, alphabet):
            self.states = states
            self.delta_transition = delta_transition
            self.initial_state = initial_state
            self.accepting_states = accepting_states
            self.alphabet = alphabet
            
    def get_epsilon_closure(self, state):
        '''
        Finds all states that can be achieved through epsilon transitions only. Includes the state given.
        :param state: The starting state
        :return: set of states that can be achieved through epsilon transitions
        '''
        states = [state]
        states_possible_through_epsilon = set()
        states_possible_through_epsilon.add(state)
        while len(states) > 0:
            state_epsilon_tuple = tuple([states[0], "epsilon"])
            states.pop(0)
            epsilon_states = self.delta_transition[state_epsilon_tuple]

            for epsilon_state in epsilon_states:
                if epsilon_state not in states_possible_through_epsilon:
                    states_possible_through_epsilon.add(epsilon_state)
                    states.append(epsilon_state)

        return states_possible_through_epsilon
from collections import defaultdict

class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.states = set()
        self.delta_transition = defaultdict(tuple)
        self.initial_state = None
        self.accepting_states = set()
        self.alphabet = nfa.alphabet.copy()
        self.construct_from_nfa()
    
    def construct_from_nfa(self):
        initial_epsilons = list(self.nfa.get_epsilon_closure(self.nfa.initial_state))
        initial_epsilons.sort()
        initial_state_closed = set(initial_epsilons)
        
        self.subset_construction_steps(initial_state_closed, True)
        self.have_missing_dfa_transitions_go_to_null()
        
    def subset_construction_steps(self, states, is_initial_state):
        '''
        Walks through the NFA and updates DFA 5-tuple values
        :param states:
        :param is_initial_state:
        :return:
        '''
        transition_letters = self.get_possible_inputs(states)

        states_tuple = tuple(sorted(states))

        if is_initial_state:
            self.initial_state = states_tuple

        self.states.add(states_tuple)
        if any(state in self.nfa.accepting_states for state in states):
            self.accepting_states.add(states_tuple)

        transitionable_states = self.get_next_states_from_transitions(states, transition_letters)

        #checked_nfa_states.add(state)

        for next_state in transitionable_states:
            if next_state is not None and next_state not in self.states:
                self.subset_construction_steps(next_state, False)
                
    def print_dfa_information(self):
        '''
        prints dfa information. Should be updated
        :return: void
        '''
        print("DFA States: " + str(self.states))
        print("DFA Initial State: " + str(self.initial_state))
        print("DFA Delta transition: " + str(self.delta_transition))
        print("DFA Alphabet: " + str(self.alphabet))
        print("DFA Accepting States: " + str(self.accepting_states))
        
    def get_possible_inputs(self, states):
        '''
        Finds all alphabet characters that lead to a state for the given set of states
        :param states: All states that need to have their input characters foudn
        :return: Set of letters that lead to valid states.
        '''
        letters_with_transitions = set()
        for state in states:
            for letter in self.nfa.alphabet:
                state_letter_tuple = tuple([state, letter])
                if len(self.nfa.delta_transition[state_letter_tuple]) > 0:
                    letters_with_transitions.add(letter)
        return letters_with_transitions
    
    def get_next_states_from_transitions(self, states, transition_letters):
        #FIXME on the comment, figure out what the tuple of nfa states that makes a single dfa state is called
        '''
        Given a set of NFA states, characters, returns set of tuples of reachable states.
        :param states: set of NFA states
        :param transition_letters: Letters that lead to valid nfa transitions
        :return: set of tuples of reachable states
        '''
        next_states = set()

        for letter in transition_letters:
            states_possible_from_this_letter = set()

            for state in states:
                transitionable_states_on_this_letter = self.nfa.delta_transition[tuple([state, letter])]

                for transitionable_state in transitionable_states_on_this_letter:
                    epsilon_states = self.nfa.get_epsilon_closure(transitionable_state)
                    #states_possible_from_this_letter.add(transitionable_state)
                    states_possible_from_this_letter.update(epsilon_states)


            start_state_tuple = tuple(sorted(states))
            #states_possible_from_this_letter = makeStateSetToTuple(states_possible_from_this_letter)
            end_state_tuple = tuple(sorted(states_possible_from_this_letter))

            state_letter_tuple = tuple([start_state_tuple, letter])

            self.delta_transition[state_letter_tuple] = end_state_tuple

            next_states.add(end_state_tuple)

        return next_states
    
    def have_missing_dfa_transitions_go_to_null(self):
        '''
        Checks if NFA has transitions that let the branch of computation "die"
        if so, creates a null set state for the dfa, and adds null state transitions as needed.
        :return: Void
        '''
        needNullState = False
        states_letters_needing_null = []
        for state in self.states:
            for letter in self.alphabet:
                if len(self.delta_transition[tuple([state, letter])]) == 0:
                        needNullState = True
                        states_letters_needing_null.append([state, letter])

        if needNullState:
            self.states.add("Null set")

            for letter in self.alphabet:
                self.delta_transition[tuple(["Null set", letter])] = tuple(["Null set"])

            for element in states_letters_needing_null:
                self.delta_transition[tuple([element[0], element[1]])] = tuple(["Null set"])
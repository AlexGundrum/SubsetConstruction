from collections import defaultdict
'''
Questions for Ghosh
1) is .txt input fine, or terminal needed?
2) is lazy subset construction fine?

'''

'''
todo: 
1) test on small nfa,
2) test on on big nfa
3) edge cases nfas

'''
test = True

nfa_set_of_states = set()
nfa_alphabet = []
nfa_delta_transition = defaultdict(list)
nfa_initial_state = None
nfa_accepting_states = set()

if test:
    nfa_set_of_states = set([1,2,3,4])
    nfa_alphabet=[0,1]

    nfa_delta_transition[tuple([1, 0])] = [2]
    nfa_delta_transition[tuple([1, "epsilon"])] = [3]
    nfa_delta_transition[tuple([2, 1])] = [2, 4]
    nfa_delta_transition[tuple([3, "epsilon"])] = [2]
    nfa_delta_transition[tuple([3, 0])] = [4]
    nfa_delta_transition[tuple([4, 0])] = [3]

    nfa_accepting_states.add(4)
    nfa_accepting_states.add(3)
    nfa_initial_state = 1


dfa_set_of_states = set()
dfa_alphabet = []
dfa_delta_transition = defaultdict(tuple)
dfa_initial_state = None
dfa_accepting_states = set()

def initializeNfaValues():
    print("FIXME, figure out how NFA information will be inputted")


def getEpsilonTransitionStates(state):
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
        epsilon_states = nfa_delta_transition[state_epsilon_tuple]

        for epsilon_state in epsilon_states:
            if epsilon_state not in states_possible_through_epsilon:
                states_possible_through_epsilon.add(epsilon_state)
                states.append(epsilon_state)

    return states_possible_through_epsilon



def makeStateSetToTuple(states):
    '''
    Takes a set of states, sorts them, and creates a tuple so that the DFA
    subset states are ordered and hashable.
    :param states: The set of states to be made into a tuple
    :return: Tuple of inputted states, sorted.
    '''
    states_list = list(states)
    states_list.sort()
    states_tuple = tuple(states_list)
    return states_tuple


def getTransitionInputsForStates(states):
    '''
    Finds all alphabet characters that lead to a state for the given set of states
    :param states: All states that need to have their input characters foudn
    :return: Set of letters that lead to valid states.
    '''
    letters_with_transitions = set()
    for state in states:
        for letter in nfa_alphabet:
            state_letter_tuple = tuple([state, letter])
            if len(nfa_delta_transition[state_letter_tuple]) > 0:
                letters_with_transitions.add(letter)
    return letters_with_transitions

def shouldDfaStateBeAccepting(states):
    '''
    Takes a set of states, checks to see if any of the elements are accepting NFA states, thus the
    corresponding DFA state will be an accepting state.
    :param states: set of NFA states
    :return: Boolean
    '''
    for state in states:
        if state in nfa_accepting_states:
            return True
    return False

def get_next_states_from_transitions(states, transition_letters):
    #FIXME on the comment, figure out what the tuple of nfa states that makes a single dfa state is called
    '''
    Given a set of NFA states, characters, returns set of tuples of reachable states.
    :param states: set of NFA states
    :param transition_letters: Letters that lead to valid nfa transitions
    :return: set of tuples of reachable states
    '''
    global dfa_delta_transition
    next_states = set()

    for letter in transition_letters:
        states_possible_from_this_letter = set()

        for state in states:
            transitionable_states_on_this_letter = nfa_delta_transition[tuple([state, letter])]

            for transitionable_state in transitionable_states_on_this_letter:
                epsilon_states = getEpsilonTransitionStates(transitionable_state)
                #states_possible_from_this_letter.add(transitionable_state)
                states_possible_from_this_letter.update(epsilon_states)


        start_state_tuple = makeStateSetToTuple(states)
        #states_possible_from_this_letter = makeStateSetToTuple(states_possible_from_this_letter)
        end_state_tuple = makeStateSetToTuple(states_possible_from_this_letter)

        state_letter_tuple = tuple([start_state_tuple, letter])

        dfa_delta_transition[state_letter_tuple] = end_state_tuple

        next_states.add(end_state_tuple)

    return next_states

checked_nfa_states = set()


def subsetConstructionSteps(states, is_initial_state):
    '''
    Walks through the NFA and updates DFA 5-tuple values
    :param states:
    :param is_initial_state:
    :return:
    '''
    global dfa_set_of_states, dfa_initial_state



    transition_letters = getTransitionInputsForStates(states)



    states_tuple = makeStateSetToTuple(states)

    if is_initial_state:
        dfa_initial_state = states_tuple

    dfa_set_of_states.add(states_tuple)

    is_dfa_state_accepting = shouldDfaStateBeAccepting(states)
    if is_dfa_state_accepting:
        dfa_accepting_states.add(states_tuple)

    transitionable_states = get_next_states_from_transitions(states, transition_letters)

    #checked_nfa_states.add(state)

    for next_state in transitionable_states:
        if next_state is not None and next_state not in dfa_set_of_states:
            subsetConstructionSteps(next_state, False)




def initialize_dfa_alphabet():
    global dfa_alphabet
    dfa_alphabet = nfa_alphabet.copy()


def have_missing_dfa_transitions_go_to_null():
    '''
    Checks if NFA has transitions that let the branch of computation "die"
    if so, creates a null set state for the dfa, and adds null state transitions as needed.
    :return: Void
    '''
    needNullState = False
    states_letters_needing_null = []
    for state in dfa_set_of_states:
        for letter in dfa_alphabet:
            if len(dfa_delta_transition[tuple([state, letter])]) == 0:
                    needNullState = True
                    states_letters_needing_null.append([state, letter])

    if needNullState:
        dfa_set_of_states.add("Null set")

        for letter in dfa_alphabet:
            dfa_delta_transition[tuple(["Null set", letter])] = tuple(["Null set"])

        for element in states_letters_needing_null:
            dfa_delta_transition[tuple([element[0], element[1]])] = tuple(["Null set"])



def print_dfa_information():
    '''
    prints dfa information. Should be updated
    :return: void
    '''
    print("DFA States: " + str(dfa_set_of_states))
    print("DFA Initial State: " + str(dfa_initial_state))
    print("DFA Delta transition: " + str(dfa_delta_transition))
    print("DFA Alphabet: " + str(dfa_alphabet))
    print("DFA Accepting States: " + str(dfa_accepting_states))

initial_epsilons = list(getEpsilonTransitionStates(nfa_initial_state))
initial_epsilons.sort()
initial_state_closed = set(initial_epsilons)

subsetConstructionSteps(initial_state_closed, True)
initialize_dfa_alphabet()
have_missing_dfa_transitions_go_to_null()
print_dfa_information()









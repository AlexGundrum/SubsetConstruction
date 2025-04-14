from collections import defaultdict
from nfa import NFA
from dfa import DFA
from nfa_parser import parse_nfa_file

nfa_set_of_states = set([1, 2, 3, 4])
nfa_alphabet = [0, 1]
nfa_delta_transition = defaultdict(list)
nfa_initial_state = 1
nfa_accepting_states = {3, 4}

nfa_delta_transition[tuple([1, 0])] = [2]
nfa_delta_transition[tuple([1, "epsilon"])] = [3]
nfa_delta_transition[tuple([2, 1])] = [2, 4]
nfa_delta_transition[tuple([3, "epsilon"])] = [2]
nfa_delta_transition[tuple([3, 0])] = [4]
nfa_delta_transition[tuple([4, 0])] = [3]

nfa = NFA(nfa_set_of_states, nfa_delta_transition, nfa_initial_state, nfa_accepting_states, nfa_alphabet)
dfa = DFA(nfa)
dfa.print_dfa_information()

nfa_tuple=parse_nfa_file("sample_nfa.txt")
nfa=NFA(nfa_tuple[0], nfa_tuple[2], nfa_tuple[3], nfa_tuple[4], nfa_tuple[1])
dfa=DFA(nfa)
dfa.print_dfa_information()

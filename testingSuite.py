import unittest
from collections import defaultdict

from nfa import NFA
from dfa import DFA

class TestingSuite(unittest.TestCase):

    def check_dfa_against_expected(
        self,
        dfa,
        expected_states,
        expected_initial_state,
        expected_delta_transition,
        expected_accepting_states
    ):
        """
        A helper function to compare the constructed DFA with expected values.
        """
        dfa_delta_dict = dict(dfa.delta_transition)

        self.assertEqual(
            dfa.states,
            expected_states,
            "DFA states differ from expected."
        )
        self.assertEqual(
            dfa.initial_state,
            expected_initial_state,
            "DFA initial state differs from expected."
        )
        self.assertEqual(
            dfa_delta_dict,
            expected_delta_transition,
            "DFA transitions differ from expected."
        )
        self.assertEqual(
            dfa.accepting_states,
            expected_accepting_states,
            "DFA accepting states differ from expected."
        )

    def test_empty_nfa(self):
        """
        Edge case: An NFA with an empty set of states.
        """
        nfa_states = set()
        nfa_alphabet = [0, 1]
        nfa_delta_transition = defaultdict(list)
        nfa_initial_state = None  
        nfa_accepting_states = set()

        nfa = NFA(
            nfa_states,
            nfa_delta_transition,
            nfa_initial_state,
            nfa_accepting_states,
            nfa_alphabet
        )
        dfa = DFA(nfa)

        expected_states = set() 
        expected_initial_state = None 
        expected_delta_transition = {}
        expected_accepting_states = set()

        self.check_dfa_against_expected(
            dfa,
            expected_states,
            expected_initial_state,
            expected_delta_transition,
            expected_accepting_states
        )

    def test_single_state_no_transitions(self):
        """
        Edge case: An NFA with one state and no transitions.
        """
        nfa_states = {1}
        nfa_alphabet = [0, 1]
        nfa_delta_transition = defaultdict(list)
        nfa_initial_state = 1
        nfa_accepting_states = set()

        nfa = NFA(
            nfa_states,
            nfa_delta_transition,
            nfa_initial_state,
            nfa_accepting_states,
            nfa_alphabet
        )
        dfa = DFA(nfa)

        expected_states = {(1,), "Null set"}
        expected_initial_state = (1,)
        expected_delta_transition = {
            ((1,), 0): ("Null set",),
            ((1,), 1): ("Null set",),
            ("Null set", 0): ("Null set",),
            ("Null set", 1): ("Null set",)
        }
        expected_accepting_states = set()

        self.check_dfa_against_expected(
            dfa,
            expected_states,
            expected_initial_state,
            expected_delta_transition,
            expected_accepting_states
        )

    def test_single_state_accepting_no_transitions(self):
        """
        Edge case: A single-state NFA which is both initial and accepting, no transitions.
        """
        nfa_states = {1}
        nfa_alphabet = [0, 1]
        nfa_delta_transition = defaultdict(list)
        nfa_initial_state = 1
        nfa_accepting_states = {1}

        nfa = NFA(
            nfa_states,
            nfa_delta_transition,
            nfa_initial_state,
            nfa_accepting_states,
            nfa_alphabet
        )
        dfa = DFA(nfa)

        expected_states = {(1,), "Null set"}
        expected_initial_state = (1,)
        expected_delta_transition = {
            ((1,), 0): ("Null set",),
            ((1,), 1): ("Null set",),
            ("Null set", 0): ("Null set",),
            ("Null set", 1): ("Null set",)
        }
        expected_accepting_states = {(1,)}

        self.check_dfa_against_expected(
            dfa,
            expected_states,
            expected_initial_state,
            expected_delta_transition,
            expected_accepting_states
        )

    def test_only_epsilon_transitions(self):
        """
        Edge case: An NFA with epsilon transitions only.
        """
        nfa_states = {1, 2}
        nfa_alphabet = [0, 1]
        nfa_delta_transition = defaultdict(list)
        nfa_initial_state = 1
        nfa_accepting_states = {2}

        nfa_delta_transition[(1, "epsilon")] = [2]

        nfa = NFA(
            nfa_states,
            nfa_delta_transition,
            nfa_initial_state,
            nfa_accepting_states,
            nfa_alphabet
        )
        dfa = DFA(nfa)

        expected_states = {(1, 2), "Null set"}
        expected_initial_state = (1, 2)
        expected_delta_transition = {
            ((1, 2), 0): ("Null set",),
            ((1, 2), 1): ("Null set",),
            ("Null set", 0): ("Null set",),
            ("Null set", 1): ("Null set",)
        }

        expected_accepting_states = {(1, 2)}

        self.check_dfa_against_expected(
            dfa,
            expected_states,
            expected_initial_state,
            expected_delta_transition,
            expected_accepting_states
        )

    def test_nfa_example(self):
        """
        Edge case: A random NFA
        """
        nfa_set_of_states = {1, 2, 3, 4}
        nfa_alphabet = [0, 1]
        nfa_delta_transition = defaultdict(list)
        nfa_initial_state = 1
        nfa_accepting_states = {3, 4}

        nfa_delta_transition[(1, 0)] = [2]
        nfa_delta_transition[(1, "epsilon")] = [3]
        nfa_delta_transition[(2, 1)] = [2, 4]
        nfa_delta_transition[(3, "epsilon")] = [2]
        nfa_delta_transition[(3, 0)] = [4]
        nfa_delta_transition[(4, 0)] = [3]

        nfa = NFA(
            nfa_set_of_states,
            nfa_delta_transition,
            nfa_initial_state,
            nfa_accepting_states,
            nfa_alphabet
        )
        dfa = DFA(nfa)

        expected_states = {
            (1, 2, 3),
            (2, 4),
            (2, 3),
            (4,),
            "Null set"
        }
        expected_initial_state = (1, 2, 3)
        expected_delta_transition = {
            ((1, 2, 3), 0): (2, 4),
            ((1, 2, 3), 1): (2, 4),
            ((2, 4), 0): (2, 3),
            ((2, 4), 1): (2, 4),
            ((2, 3), 0): (4,),
            ((2, 3), 1): (2, 4),
            ((4,), 0): (2, 3),
            ((4,), 1): ("Null set",),
            ("Null set", 0): ("Null set",),
            ("Null set", 1): ("Null set",)
        }
        expected_accepting_states = {
            (1, 2, 3),
            (2, 4),
            (2, 3),
            (4,)
        }

        self.check_dfa_against_expected(
            dfa,
            expected_states,
            expected_initial_state,
            expected_delta_transition,
            expected_accepting_states
        )

if __name__ == "__main__":
    unittest.main()

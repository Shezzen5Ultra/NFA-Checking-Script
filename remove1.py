import sys

class NFANode:
    def __init__(self, name):
        self.name = name
        self.transitions = {}


# To compute the epsilon closure of a set of states
def epsilon_closure(states, nfa):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if state in nfa and 'ε' in nfa[state].transitions:
            for eps_state in nfa[state].transitions['ε']:
                if eps_state not in closure:
                    closure.add(eps_state)
                    stack.append(eps_state)
    return closure

def parse_input_file(file_path):
    epsilon_nfa = {'accepting_states': set(), 'transitions': {}}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        epsilon_nfa['accepting_states'] = set(map(int, lines[2].strip().split()[2:]))
        epsilon_nfa['alphabet'] = set()
        for i in range(3, len(lines)):
            transitions = lines[i].strip().split()
            state_transitions = {}
            for j, transition in enumerate(transitions):
                if transition != '{}':
                    if j != len(transitions) - 1:
                        symbol = chr(ord('a') + j)
                        state_transitions[symbol] = list(map(int, transition[1:-1].split(',')))
                    else:
                        state_transitions['ε'] = list(map(int, transition[1:-1].split(',')))
                        epsilon_nfa['alphabet'].add('ε')
            epsilon_nfa['transitions'][i - 3] = state_transitions
    return epsilon_nfa


def nfa_without_epsilon(epsilon_nfa):
    nfa = {}
    for state in range(len(epsilon_nfa['transitions'])):
        nfa[state] = {'transitions': {}, 'is_accepting': state in epsilon_nfa['accepting_states']}
        for symbol in epsilon_nfa['alphabet']:
            next_states = set()
            for next_state in epsilon_nfa['transitions'].get(state, {}).get(symbol, {}):
                next_states.add(next_state)
                next_states.update(epsilon_nfa['transitions'].get('ε', {}).get(next_state, {}))
            nfa[state]['transitions'][symbol] = next_states
    return nfa

def main():
    if len(sys.argv) != 2:
        print("Usage: ./removetest.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]

    # Parse the input file to get ε-NFA
    epsilon_nfa = parse_input_file(input_file)

    # Convert ε-NFA to NFA
    nfa = nfa_without_epsilon(epsilon_nfa)

    # Print the resulting NFA
    print("Equivalent NFA without epsilon-transitions:")
    for state, node in nfa.items():
        print(f"State: {state}")
        print("Transitions:")
        for symbol, next_states in node['transitions'].items():
            # Replace epsilon symbol with 'eps' for printing
            symbol_str = 'eps' if symbol == 'ε' else symbol
            print(f"  {symbol_str}: {next_states}")
        
        # Check if the state is accepting and print accordingly
        is_accepting = " (Accepting)" if node['is_accepting'] else ""
        print(f"State {state} is{is_accepting}")

    print("\nAccepting States:", [state for state, node in nfa.items() if node['is_accepting']])
if __name__ == "__main__":
    main()
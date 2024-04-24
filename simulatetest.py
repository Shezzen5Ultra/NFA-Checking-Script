import sys

# Create a class to represent a non-deterministic finite automaton
class NFA:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def run(self, string):
        current_states = {self.initial_state}

        for char in string:
            next_states = set()
            for state in current_states:
                if (state, char) in self.transitions:
                    next_states.update(self.transitions[(state, char)])
            current_states = next_states

        result = any(state in self.accepting_states for state in current_states)

        if string == '' and self.initial_state in self.accepting_states:
            result = True

        return result


# Create the NFA from text input
def create_nfa_from_file(file_path):
    states = set()
    alphabet = set()
    transitions = {}
    initial_state = None
    accepting_states = set()

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            if line.startswith("Number of states:"):
                num_states = int(line.split(":")[1].strip())
                states = {str(i) for i in range(num_states)}
            elif line.startswith("Alphabet size:"):
                alphabet_size = int(line.split(":")[1].strip())
                alphabet = {chr(ord('a') + i) for i in range(alphabet_size)}
            elif line.startswith("Accepting states:"):
                accepting_states = set(line.split(":")[1].strip().split())
            else:
                origin_state, *transitions_info = line.split()
                states.add(origin_state)
                for i in range(0, len(transitions_info), 2):
                    symbol = transitions_info[i]
                    dest_states = transitions_info[i + 1]
                    if dest_states != "{}":
                        dest_states = dest_states[1:-1].split()
                        dest_states = [int(state) for state in dest_states]
                    else:
                        dest_states = []
                    if (origin_state, symbol) not in transitions:
                        transitions[(origin_state, symbol)] = set()
                    transitions[(origin_state, symbol)].update(dest_states)
    if not initial_state:
        initial_state = states.pop()
    return NFA(states, alphabet, transitions, initial_state, accepting_states)


def main():
    if len(sys.argv) != 3:
        print("Usage: simulatetest.py nfa_file.txt strings_file.txt")
        return

    nfa_file = sys.argv[1]
    strings_file = sys.argv[2]

    nfa = create_nfa_from_file(nfa_file)

    with open(strings_file, 'r') as file:
        for line in file:
            string = line.strip()
            result = "accept" if nfa.run(string) else "reject"
            print(f"String '{string}': {result}")

if __name__ == "__main__":
    main()
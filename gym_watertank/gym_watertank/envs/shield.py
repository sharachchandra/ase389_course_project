class Shield:

    def __init__(self):
        print("Initializing the real shield")
        print("The shielded actions function returns the set of safe actions in a state")


    def shielded_actions(self, state_val, switch_state):
        # always returns a list
        if 1 <= state_val <= 3 and switch_state == 1: 
            return [1]
        elif 97 <= state_val <= 99 and switch_state == -1:
            return [0]
        elif switch_state in [2,3]:
            return [1]
        elif switch_state in [-2,-3]:
            return [0]
        else:
            return [0,1]

import numpy as np

class Shield:

    def __init__(self, shield_file):
        print("Initializing the real shield")
        print("The shielded actions function returns the set of safe actions in a state")

        self.shield = np.load(shield_file, allow_pickle=True).item()
        print(self.shield)

        print("loaded shield")
        

    def shielded_actions(self, state_val, switch_state):
        #print('always returns a list')
        if switch_state == 1 or switch_state == -1: 
            return self.shield[state_val]
        elif switch_state in [2,3]:
            return [1]
        elif switch_state in [-2,-3]:
            return [0]
        else:
            return [0,1]
    
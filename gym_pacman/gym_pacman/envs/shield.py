import numpy as np 

class Shield():

    def __init__(self, shield_file=None):
        self.shield = np.load(shield_file, allow_pickle=True).item()
        print(self.shield)

    def shielded_actions(self, state):
        return self.shield[state]
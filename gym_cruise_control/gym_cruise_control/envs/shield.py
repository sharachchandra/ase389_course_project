import numpy as np 

class Shield():

    def __init__(self, shield_file=None):
        self.shield = np.load(shield_file, allow_pickle=True).item()

    def shielded_actions(self, rel_dist, rel_vel):
        return self.shield[(rel_dist, rel_vel)]
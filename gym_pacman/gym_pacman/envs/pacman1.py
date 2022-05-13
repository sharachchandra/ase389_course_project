import gym
from gym_pacman.envs.shield import Shield
import numpy as np

class Pacman1(gym.Env):
    def __init__(self):
        super().__init__()

        self.n_action = 5
        self.action_space = gym.spaces.Discrete(self.n_action)
        
        self.n = 5
        self.observation_space = gym.spaces.Tuple((gym.spaces.Discrete(self.n),
                                                   gym.spaces.Discrete(self.n),
                                                   gym.spaces.Discrete(self.n),
                                                   gym.spaces.Discrete(self.n)))
        # (row, column)
        self.max_episode_steps = 100
        self.goal = (4,4)
    
        self.shield = Shield('gym_pacman/gym_pacman/envs/pacman1_shield.npy')
        self.shield_active = False

    def activate_shield(self, val = True):
        self.shield_active = val

    def trans_right(self, state):
        next_state_row = state[0]
        next_state_col = min(state[1] + 1, self.n - 1)
        
        return (next_state_row, next_state_col)
    
    def trans_left(self, state):
        next_state_row = state[0]
        next_state_col = max(state[1] - 1, 0)
        
        return (next_state_row, next_state_col)

    def trans_up(self, state):
        next_state_row = min(state[0] + 1, self.n - 1)
        next_state_col = state[1]
        
        return (next_state_row, next_state_col)

    def trans_down(self, state):
        next_state_row = max(state[0] - 1, 0)
        next_state_col = state[1]
        
        return (next_state_row, next_state_col)

    def trans_stay(self, state):
        return state

    def trans(self, state, action):
        if action < 0 or action >= self.n_action:
            raise ValueError("Action value out of bounds")
        if state[0] < 0 or state[0] >= self.n or state[1] < 0 or state[1] >= self.n:
            print(state)
            raise ValueError("State value out of bounds")
        
        if action == 0:
            return self.trans_up(state)
        if action == 3:
            return self.trans_right(state)
        if action == 1:
            return self.trans_down(state)
        if action == 2:
            return self.trans_left(state)
        if action == 4:
            return self.trans_stay(state) # Only for pacman and not for ghost (adversary)

    def step(self, action):
        
        action_ghost = np.random.randint(0, self.n_action - 1) # ghost cannot stay in place
        self.ghost = self.trans(self.ghost, action_ghost)
        
        state  = (*self.pacman, *self.ghost)
        info   = {'pacman': tuple(reversed(self.pacman)),
                  'ghost' : tuple(reversed(self.ghost))}
        if self.ghost == self.pacman:
            print('eaten')
            reward = -1
            done   = True
            return state, reward, done, info
        
        shielded_actions = self.shield.shielded_actions(state)
        if self.shield_active:
            if action in shielded_actions:
                pass
            elif len(shielded_actions):
                action = np.random.choice(shielded_actions)

        self.pacman = self.trans(self.pacman, action)
        info   = {'pacman': tuple(reversed(self.pacman)),
                  'ghost' : tuple(reversed(self.ghost))}
        state  = (*self.pacman, *self.ghost)
        if self.pacman == self.goal:
            reward = 1
            done   = True
            return state, reward, done, info
        
        self.episode_steps += 1
        reward = 0
        done = False
        if self.episode_steps > self.max_episode_steps:
            done = True

        return state, reward, done, info

    def reset(self):
        self.pacman = (0,0)
        self.ghost  = (2,2)
        self.episode_steps = 0
        
        state = (*self.pacman, *self.ghost)
        return state


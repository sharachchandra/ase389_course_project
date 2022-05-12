import gym

import numpy as np

class Pacman(gym.Env):
    def __init__(self):
        super().__init__()

        self.n_action = 4
        self.action_space = gym.spaces.Discrete(self.n_action)
        
        self.n = 5
        self.observation_space = gym.spaces.Tuple((gym.spaces.Discrete(self.n**2),
                                                   gym.spaces.Discrete(self.n**2)))

        self.max_episode_steps = 100
        self.goal = 24

    def trans_right(self, state):
        q, r = divmod(state, self.n)
        
        next_state = state + 1
        qn, qr = divmod(next_state, self.n)
        if qn != q:
            next_state = state
        
        return next_state
    
    def trans_left(self, state):
        q, r = divmod(state, self.n)
        
        next_state = state - 1
        qn, qr = divmod(next_state, self.n)
        if qn != q:
            next_state = state
        
        return next_state

    def trans_up(self, state):
        next_state = state + 5

        qn, qr = divmod(next_state, self.n**2)
        if qn != 0:
            next_state = state

        return next_state

    def trans_down(self, state):
        next_state = state - 5

        qn, qr = divmod(next_state, self.n**2)
        if qn != 0:
            next_state = state

        return next_state

    def trans(self, state, action):
        if action < 0 or action >= self.n_action:
            raise ValueError("Action value out of bounds")
        if state < 0 or action >= self.n**2:
            raise ValueError("Action value out of bounds")
        
        if action == 0:
            return self.trans_up(state)
        if action == 1:
            return self.trans_right(state)
        if action == 2:
            return self.trans_down(state)
        if action == 3:
            return self.trans_left(state)
        
    def state_to_grid(self, state):
        return tuple(reversed(divmod(state, self.n)))

    def step(self, action):
        
        action_ghost = np.random.randint(0, self.n_action)
        # action_ghost = 0
        self.ghost = self.trans(self.ghost, action_ghost)
        
        state  = (self.pacman, self.ghost)
        print(state)
        info   = {'pacman': self.state_to_grid(self.pacman),
                  'ghost' : self.state_to_grid(self.ghost)}
        if self.ghost == self.pacman:
            reward = -1
            done   = True
            return state, reward, done, info
        
        self.pacman = self.trans(self.pacman, action)
        info   = {'pacman': self.state_to_grid(self.pacman),
                  'ghost' : self.state_to_grid(self.ghost)}
        state  = (self.pacman, self.ghost)
        if self.pacman == self.goal:
            state  = (self.pacman, self.ghost)
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
        self.pacman = 0
        self.ghost  = 12
        self.episode_steps = 0
        
        state = (self.pacman, self.ghost)
        return state


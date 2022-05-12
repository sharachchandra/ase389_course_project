import gym

import numpy as np

class CruiseControl1(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(5)
        self.observation_space = gym.spaces.Tuple((gym.spaces.Discrete(26),
                                                   gym.spaces.Discrete(11)))
        
        self.min_dis = 0
        self.max_dis = 25
        self.min_vel = -5
        self.max_vel = 5
        self.min_acc = -2
        self.max_acc = 2
        
        self.max_rel_dis_noise = 3

        self.max_episode_steps = 100

    def step(self, action):
        acc_ego = action + self.min_acc
        acc_fv  = 0
        rel_acc = acc_fv - acc_ego
        # print(acc_ego, acc_fv, rel_acc)

        if self.rel_vel + rel_acc > self.max_vel:
            if self.rel_vel < self.max_vel:
                rel_acc = self.max_vel - self.rel_vel
            else:
                rel_acc = 0
        if self.rel_vel + rel_acc < -self.max_vel:
            if self.rel_vel > -self.max_vel:
                rel_acc = -self.max_vel - self.rel_vel
            else:
                rel_acc = 0

        delta_rel_dis = self.rel_vel
        self.rel_dis  = self.rel_dis + delta_rel_dis
        self.rel_vel  = self.rel_vel + rel_acc

        # print(self.rel_dis, self.rel_vel)

        rel_dis_noisy = self.rel_dis + \
                        np.random.randint(-self.max_rel_dis_noise, self.max_rel_dis_noise + 1)

        state = (rel_dis_noisy - self.min_dis, 
                 self.rel_vel - self.min_vel)

        reward = -delta_rel_dis # Positive reward for decrease in relative distance
        
        if self.rel_dis < 5:
            reward -= 10
        
        self.episode_steps += 1
        done = False
        if self.rel_dis >= 25 or self.rel_dis <= 0 or self.episode_steps > self.max_episode_steps:
            done = True
        
        info = {
                'rel_dis': self.rel_dis,
                'rel_dis_noisy': rel_dis_noisy,
                'rel_vel': self.rel_vel,
                'rel_acc': rel_acc
                }

        return state, reward, done, info

    def reset(self):
        self.rel_dis = 15
        self.rel_vel = 0
        self.episode_steps = 0
        
        state = (self.rel_dis, self.rel_vel)
        # print(self.rel_dis, self.rel_vel)
        return state


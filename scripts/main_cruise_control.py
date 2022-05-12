from turtle import done
import gym

import gym_cruise_control

env = gym.make("cruisecontrol-v0")
env.reset()

for i in range(10):
    action = 1
    obs, _, done, _ = env.step(action)
    print(obs)
    if done:
        break
from turtle import done
import gym 
import os

import gym_cruise_control
from q_learning import q_learning, q_learning_test_cc
import plotting

env_name = "cruisecontrol-v0"
env = gym.make(env_name)
env.activate_shield(True)
env.reset()

img_dir = 'data/img3/'
os.makedirs(img_dir, exist_ok=True)

if env_name == "cruisecontrol-v0":
    Q, stats = q_learning(env, 5000, discount_factor = 1, alpha=0.1, epsilon=0.2, shield=True) #v-0
elif env_name == "cruisecontrol-v1":
    Q, stats = q_learning(env, 5000, discount_factor = 0.95, alpha=0.1, epsilon=0.1) #v-1

fig1, fig2, fig3 = plotting.plot_episode_stats(stats, noshow=True)
fig1.savefig(img_dir + 'img1.png')
fig2.savefig(img_dir + 'img2.png')
fig3.savefig(img_dir + 'img3.png')

stats = q_learning_test_cc(env, Q, epsilon = 0.0, shield=True)
fig = plotting.plot_test_stats_cc(stats, noshow=True)
fig.savefig(img_dir + 'img4.png')
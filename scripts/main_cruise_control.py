from turtle import done
import gym

import gym_cruise_control
from q_learning import q_learning, q_learning_test_cc
import plotting

env = gym.make("cruisecontrol-v1")
env.reset()

# Q, stats = q_learning(env, 5000, discount_factor = 1, alpha=0.1, epsilon=0.2) #v-0
# Q, stats = q_learning(env, 5000, discount_factor = 0.95, alpha=0.1, epsilon=0.1) #v-1
Q, stats = q_learning(env, 5000, discount_factor = 0.95, alpha=0.1, epsilon=0.05)
fig1, fig2, fig3 = plotting.plot_episode_stats(stats, noshow=True)
fig1.savefig('./imgs/img1.png')
fig2.savefig('./imgs/img2.png')
fig3.savefig('./imgs/img3.png')

stats = q_learning_test_cc(env, Q, epsilon = 0.0)
fig = plotting.plot_test_stats_cc(stats, noshow=True)
fig.savefig('./imgs/img4.png')
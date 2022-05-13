import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5,5))
rel_dis1 = np.load('data/rel_dis1.npy')
rel_dis2 = np.load('data/rel_dis2.npy')
rel_dis3 = np.load('data/rel_dis3.npy')
plt.plot(rel_dis1, label = 'No noise in relative depth measurement')
plt.plot(rel_dis2, label = 'Without shield')
plt.plot(rel_dis3, label = 'With shield')
plt.xlabel("Time steps")
plt.ylabel("Relative distance (units)")
plt.title("Relative distance over time")
plt.legend()
plt.grid()
plt.show()
fig.savefig('data/report/cc1_rel_dis.png')

fig = plt.figure(figsize=(5,5))
reward1 = np.load('data/reward1.npy')
reward2 = np.load('data/reward2.npy')
reward3 = np.load('data/reward3.npy')
plt.plot(reward1, label = 'No noise in relative depth measurement')
plt.plot(reward2, label = 'Without shield')
plt.plot(reward3, label = 'With shield')
plt.xlabel("Time steps")
plt.ylabel("Reward to go")
plt.title("Reward accumulated over time")
plt.legend()
plt.grid()
plt.show()
fig.savefig('data/report/cc1_reward.png')

fig = plt.figure(figsize=(5,5))
train1 = np.load('data/train1.npy')
train2 = np.load('data/train2.npy')
plt.plot(train1, label = 'Without shield')
plt.plot(train2, label = 'With shield')
plt.xlabel("Episodes")
plt.ylabel("Episode rewad")
plt.title("Episode reward over time")
plt.legend()
plt.grid()
plt.show()
fig.savefig('data/report/cc1_train.png')
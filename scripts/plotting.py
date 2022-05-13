from cProfile import label
from sre_parse import State
import matplotlib
import numpy as np
import pandas as pd
from collections import namedtuple
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

EpisodeStats = namedtuple("Stats",["episode_lengths", "episode_rewards"])
TestStats_cc = namedtuple("TestStats_cc",["rel_dis", "rel_dis_noisy", "rel_vel", "rel_acc", "reward", "max_steps"])
TestStats_pm = namedtuple("TestStats_pm",["pacman", "ghost", "reward"])

def plot_cost_to_go_mountain_car(env, estimator, num_tiles=20):
    x = np.linspace(env.observation_space.low[0], env.observation_space.high[0], num=num_tiles)
    y = np.linspace(env.observation_space.low[1], env.observation_space.high[1], num=num_tiles)
    X, Y = np.meshgrid(x, y)
    Z = np.apply_along_axis(lambda _: -np.max(estimator.predict(_)), 2, np.dstack([X, Y]))

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                           cmap=matplotlib.cm.coolwarm, vmin=-1.0, vmax=1.0)
    ax.set_xlabel('Position')
    ax.set_ylabel('Velocity')
    ax.set_zlabel('Value')
    ax.set_title("Mountain \"Cost To Go\" Function")
    fig.colorbar(surf)
    plt.show()


def plot_value_function(V, title="Value Function"):
    """
    Plots the value function as a surface plot.
    """
    min_x = min(k[0] for k in V.keys())
    max_x = max(k[0] for k in V.keys())
    min_y = min(k[1] for k in V.keys())
    max_y = max(k[1] for k in V.keys())

    x_range = np.arange(min_x, max_x + 1)
    y_range = np.arange(min_y, max_y + 1)
    X, Y = np.meshgrid(x_range, y_range)

    # Find value for all (x, y) coordinates
    Z_noace = np.apply_along_axis(lambda _: V[(_[0], _[1], False)], 2, np.dstack([X, Y]))
    Z_ace = np.apply_along_axis(lambda _: V[(_[0], _[1], True)], 2, np.dstack([X, Y]))

    def plot_surface(X, Y, Z, title):
        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                               cmap=matplotlib.cm.coolwarm, vmin=-1.0, vmax=1.0)
        ax.set_xlabel('Player Sum')
        ax.set_ylabel('Dealer Showing')
        ax.set_zlabel('Value')
        ax.set_title(title)
        ax.view_init(ax.elev, -120)
        fig.colorbar(surf)
        plt.show()

    plot_surface(X, Y, Z_noace, "{} (No Usable Ace)".format(title))
    plot_surface(X, Y, Z_ace, "{} (Usable Ace)".format(title))

def plot_episode_stats(stats, smoothing_window=10, noshow=False):
    # Plot the episode length over time
    fig1 = plt.figure(figsize=(10,5))
    plt.plot(stats.episode_lengths)
    plt.xlabel("Episode")
    plt.ylabel("Episode Length")
    plt.title("Episode Length over Time")
    if noshow:
        plt.close(fig1)
    else:
        plt.show(fig1)

    # Plot the episode reward over time
    fig2 = plt.figure(figsize=(10,5))
    rewards_smoothed = pd.Series(stats.episode_rewards).rolling(smoothing_window, min_periods=smoothing_window).mean()
    plt.plot(rewards_smoothed)
    plt.xlabel("Episode")
    plt.ylabel("Episode Reward (Smoothed)")
    plt.title("Episode Reward over Time (Smoothed over window size {})".format(smoothing_window))
    if noshow:
        plt.close(fig2)
    else:
        plt.show(fig2)

    np.save('data/train1', rewards_smoothed)
    # Plot time steps and episode number
    fig3 = plt.figure(figsize=(10,5))
    plt.plot(np.cumsum(stats.episode_lengths), np.arange(len(stats.episode_lengths)))
    plt.xlabel("Time Steps")
    plt.ylabel("Episode")
    plt.title("Episode per time step")
    if noshow:
        plt.close(fig3)
    else:
        plt.show(fig3)

    return fig1, fig2, fig3

def plot_test_stats_cc(stats, smoothing_window=10, noshow=False):
    # Plot the episode length over time
    fig, axes = plt.subplots(1,2,figsize=(20,5))
    axes[0].plot(stats.rel_dis, label = 'Relative Distance (unit)')
    axes[0].plot(stats.rel_dis_noisy, label = 'Relative Distance noisy(unit)')
    axes[0].plot(stats.rel_vel, label = 'Relative Velocity (unit/sec)')
    axes[0].plot(stats.rel_acc, label = 'Relative Acceleration (unit/sec^2)')
    axes[0].set_xlabel("Time steps")
    axes[0].set_ylabel("Relative information")
    axes[0].set_title("States over time")
    axes[0].set_xlim([0, stats.max_steps])
    axes[0].legend()
    axes[0].grid()

    axes[1].plot(stats.reward)
    axes[1].set_xlabel("Time steps")
    axes[1].set_ylabel("Reward to go")
    axes[1].set_title("Reward accumulated over time")
    axes[1].set_xlim([0, stats.max_steps])
    axes[1].grid()

    np.save('data/rel_dis1', stats.rel_dis)
    np.save('data/reward1', stats.reward)
    if noshow:
        plt.close(fig)
    else:
        plt.show(fig)

    return fig

def plot_test_stats_pm(stats, smoothing_window=10, noshow=False):
    # Plot the episode length over time
    fig, axes = plt.subplots(1,1)
    axes.plot(*zip(*stats.pacman), label = 'Pacman path')
    axes.plot(*zip(*stats.ghost), label = 'Ghost path')
    axes.plot(*stats.pacman[-1], marker='o',color='blue')
    axes.plot(*stats.ghost[-1], marker='o',color='orange')
    axes.set_xlabel("X-Axis")
    axes.set_ylabel("Y-Axis")
    axes.set_title("Paths")
    axes.set_xlim([-1, 5])
    axes.set_ylim([-1, 5])
    axes.legend()

    if noshow:
        plt.close(fig)
    else:
        plt.show(fig)

    return fig

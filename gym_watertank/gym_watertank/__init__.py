from gym.envs.registration import register
from importlib_metadata import entry_points

register(id = 'watertank-v0', entry_point = 'gym_watertank.envs:WaterTank')

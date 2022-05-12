from gym.envs.registration import register

register(id = 'cruisecontrol-v0', entry_point = 'gym_cruise_control.envs:CruiseControl')
register(id = 'cruisecontrol-v1', entry_point = 'gym_cruise_control.envs:CruiseControl1')

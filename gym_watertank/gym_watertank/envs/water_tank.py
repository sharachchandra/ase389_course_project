import gym

import math
import random
import numpy as np

from gym_watertank.envs.no_shield import DummyShield
from gym_watertank.envs.shield import Shield 

class WaterTank(gym.Env):

	def __init__(self, use_shield):

		self.num_states = 100
		self.start_state = 1
		self.end_state = 100
		self.switch_states = [-3, -2, -1, 0, 1, 2, 3]
		self.transition_switch_states = [-3, -2, -1, 1, 2, 3]

		# state_mapper maps the (state_val, switch_state) to an integer value

		self.state_mapper = {}
		for state_val in range(1,100):
			for switch_state in self.switch_states:
				state_num = len(self.state_mapper)
				self.state_mapper[(state_val, switch_state)] = state_num

		# Add error state to the state mapper. 
		# The error state is the last state of the state mapper

		self.error_state = len(self.state_mapper)
		error_state_key = (-1, 0)
		self.state_mapper[error_state_key] = self.error_state

		# creating a reverse state mapper for easier lookup
		# the reverse state mapper maps the integer value to the corresponding (state_val, switch_state)

		self.reverse_state_mapper = {}
		for (a,b) in self.state_mapper.items():
			self.reverse_state_mapper[b] = a

		# Adding a bunch of error states to the state_mapper

		for state_val in [0, -1, -2, -3, 100, 101, 102, 103]:
			for switch_state in self.switch_states:
				self.state_mapper[(state_val, switch_state)] = self.error_state

		# Getting the list of transitions 
		# Each transition is given as [current state, action, next state, probability of the transition]
		# The current state and the next state are represented in interger values

		self.transitions = []

		for state_val in range(1,100):
			for switch_state in self.transition_switch_states:
				current_state = self.state_mapper[(state_val, switch_state)]
		
				po = (math.sin(state_val / 12.345 ) + 1.0) * 0.35
				pi = (math.sin(state_val / 18 + 1.2345) + 1.0) * 0.45

				# At switch_state = 1, there is a choice of open / close. 
				# If open is chosen, the switch_state remains at 1
				# If close is chosen, the switch_state is set to -3 
				# It then reduces to -2 and then to -1. 
				# At switch_state = -1, there is a choice of open / close.
				# If close is chosen, the switch_state remains at -1. 
				# If open is chosen, the switch_state is set to 3. 
				# It then reduces to 2 and then 1. 
				# The loop  continues ......

				# If open is chosen, the water level can 
				# 1. stay at the same level.
				# 2. increase by one level. 
				# 3. increase by two levels.

				# If close is chosen, the water level can 
				# 1. stay at the same level.
				# 2. decrease by one level.

				# If the switch_state is greater than 1, 
				# Then close action will take to an error state 

				# If the switch_state is lesser than -1, 
				# The open action will take to an error state

				# Gathering transitions when the valve is closed.

				if switch_state > 1:
					self.transitions.append([current_state, 0, self.error_state, 1.0])

				elif switch_state == 1:
					self.transitions.append([current_state, 0, self.state_mapper[(state_val, -3)], po])
					self.transitions.append([current_state, 0, self.state_mapper[(state_val - 1, -3)], 1 - po])
				else:
					self.transitions.append([current_state, 0, self.state_mapper[(state_val, min(-1, switch_state + 1))], po])
					self.transitions.append([current_state, 0, self.state_mapper[(state_val - 1, min(-1, switch_state + 1))], 1 - po])

				# Gathering transitions when the valve is opened.
		
				if switch_state < -1:
					self.transitions.append([current_state, 1, self.error_state, 1.0])
				elif switch_state == -1:
					self.transitions.append([current_state, 1, self.state_mapper[(state_val + 2, 3)], po * (1 - pi)])
					self.transitions.append([current_state, 1, self.state_mapper[(state_val + 1, 3)], po * pi + (1 - po) * (1 - pi)])
					self.transitions.append([current_state, 1, self.state_mapper[(state_val + 0, 3)], (1 - po) * pi])
				else:
					self.transitions.append([current_state, 1, self.state_mapper[(state_val + 2, max(1, switch_state - 1))], po * (1 - pi)])
					self.transitions.append([current_state, 1, self.state_mapper[(state_val + 1, max(1, switch_state - 1))], po * pi + (1 - po) * (1 - pi)])
					self.transitions.append([current_state, 1, self.state_mapper[(state_val + 0, max(1, switch_state - 1))], (1 - po) * pi])

		# Defining the dictonary for reward

		rewards_list = []
		for state_val in range(0,101):
			rewards_list.append(-1 * state_val * (1 + math.sin(state_val * 0.4 + 0.5) * 0.95))

		rmax = max(rewards_list)
		rmin = min(rewards_list)


		self.state_to_reward_mapper = {self.error_state : -2.0}
		for state_val in range(0,101):
			for switch_state in self.transition_switch_states:
				reward_for_state_val = (2 * ((-1 * state_val * (1 + math.sin(state_val * 0.4 + 0.5) * 0.95)) - rmin)/(rmax - rmin)) - 1
				self.state_to_reward_mapper[self.state_mapper[(state_val, switch_state)]] = reward_for_state_val 


		self.transition_lists = {}
		for (a, b, c, d) in self.transitions:
			if not (a, b) in self.transition_lists:
				self.transition_lists[(a, b)] = [(c, d)]
			else:
				self.transition_lists[(a, b)].append((c, d))


		# Initializations for the environment
		# self.state represents the integer state
		# Whenever we reset, we start at the water level of 50 L.
		# To get the corresponding state as an integer, we use the self.state_mapper with (50, 1)
		# This means that after reset, we are free to choose between both open and close. 

		self.state = self.state_mapper[(50, 1)]  


		# shield
		if use_shield:
			self.shield = Shield()
		else:
			self.shield = DummyShield()
		

	def step(self, action):

		# There are only two allowed actions - Open (True) and Close (False)

		done = False

		(state_val, switch_state) = self.reverse_state_mapper[self.state]
		allowed_actions = self.shield.shielded_actions(state_val, switch_state)

		if action not in allowed_actions:
			action = random.choice(allowed_actions)

		possible_transitions = self.transition_lists[(self.state, action)]


		next_state = None
		random_prob_val = random.random()

		# here, we iterate only in ascending order of transition probabilities
		transition_probabilities = []
		for (possible_next_state, transition_prob) in possible_transitions:
			transition_probabilities.append(transition_prob)

		num_possible_next_states = len(possible_transitions)
		choice = np.random.choice(list(range(num_possible_next_states)), p=transition_probabilities)

		next_state = possible_transitions[choice][0]
		self.state = next_state 

		reward = self.state_to_reward_mapper[self.state]
		if next_state == self.error_state:
			#reward = -2
			done = True

		
		#print("reward : ", reward)


		return self.state, reward, done, None

	def reset(self):

		self.state = self.state_mapper[(50, 1)]

		return self.state 

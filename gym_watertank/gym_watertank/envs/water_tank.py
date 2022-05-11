import gym

import math

class WaterTank(gym.Env):

	def __init__(self):

		self.num_states = 100
		self.start_state = 1
		self.end_state = 100
		self.switch_states = [-3, -2, -1, 0, 1, 2, 3]
		self.transition_switch_states = [-3, -2, -1, 1, 2, 3]

		# state_mapper maps the (state_val, switch_state) to an integer value

		self.state_mapper = {}
		for state_val in range(1,100):
			for switch_state in self.switch_states:
				state_num = len(state_mapper)
				self.state_mapper[(state_val, switch_state)] = state_num

		# Add error state to the state mapper. 
		# The error state is the last state of the state mapper

		self.error_state = len(state_mapper)
		self.error_state_key = (-1,0)
		self.state_mapper[error_state_key] = self.error_state

		# creating a reverse state mapper for easier lookup

		self.reverse_state_mapper = {}
		for (a,b) in self.state_mapper.items():
    		self.reverse_state_mapper[b] = a

    	# Adding a bunch of error states to the state_mapper

		for state_val in [0, -1, -2, -3, 100, 101, 102, 103]:
    		for switch_state in self.switch_states:
        		self.state_mapper[(state_val, switch_state)] = self.error_state

		# Getting the list of transitions 
		# Each transition is given as [current state, action, next state, probability of the transition]

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

		norm_max = max(normlist)
		norm_min = min(normlist)


		self.state_to_reward_mapper = {self.error_state : 0.0}
		for state_val in range(0,101):
			for switch_state in self.transition_switch_states:
				reward_for_state_val = (2 * ((-1 * state_val * (1 + math.sin(state_val * 0.4 + 0.5) * 0.95)) - norm_min)/(norm_max - norm_min)) - 1
				self.state_to_reward_mapper[self.state_mapper[(state_val, switch_state)]] = reward_for_state_val 


		self.transition_lists = {}
		for (a, b, c, d) in transitions:
			if not (a, b) in self.transition_lists:
				self.transition_lists[(a, b)] = [(c, d)]
			else:
				self.transition_lists[(a, b)].append((c, d))

		


	def step(self, action):




	def reset(self)
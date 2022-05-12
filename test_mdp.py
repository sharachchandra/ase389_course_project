import os 

water_tank_mdp_file = 'noisy_cruise_control.prism'

file = open(water_tank_mdp_file, 'w+')

min_rel_dist = 0 
max_rel_dist = 25 
num_dist_states = int(max_rel_dist - min_rel_dist + 1)

min_rel_vel = -5 
max_rel_vel = 5 
num_vel_states = int(max_rel_vel - min_rel_vel + 1)

ego_acc_list = [-2, -1, 0, 1, 2]
fv_acc_list = [0]

noise_list = [-3, -2, -1, 0, 1, 2, 3]

for dist_idx in range(num_dist_states):
	rel_dist = dist_idx 
	rel_dist_str = "(s=%d)" % rel_dist  

	for vel_idx in range(num_vel_states):
		rel_vel = -5 + vel_idx
		rel_vel_str = "(v=%d)" % rel_vel 

		print("generating transitions for rel_dist = " + rel_dist_str + " and rel_vel = " + rel_vel_str)

		next_rel_dist = max(min_rel_dist, min(rel_dist + rel_vel, max_rel_dist))
		next_rel_dist_str = "(s'=%d)" % next_rel_dist

		for ego_acc in ego_acc_list:
			ego_acc_command = "[a" +  str(ego_acc+ 2) + "]"

			for fv_acc in fv_acc_list:

				print("generating the transition for the particular ego acc = " + str(ego_acc) + " and fv acc = " + str(fv_acc))

				rel_acc = fv_acc - ego_acc 
				next_rel_vel = max(min_rel_vel, min(rel_vel + rel_acc, max_rel_vel))
				next_rel_vel_str = "(v'=%d)" % next_rel_vel

				print("iterating over all possible observations")
				i = 0
				string = ""
				string += ego_acc_command
				string += rel_dist_str
				string += " & "
				string += rel_vel_str
				string += " -> "				

				for noise in noise_list:

					next_obs = next_rel_dist + noise 
					next_obs_str = "(o'=%d)" % next_obs  

					string += "1/7:"
					string += next_rel_dist_str
					string += " & "
					string += next_rel_vel_str
					string += " & "
					string += next_obs_str

					if i < len(noise_list) - 1:
						string += " + "

					i += 1
				
				string += ";"
				string += "\n"

				print(string)
				file.write(string)

		file.write('\n')

	file.write('\n')

file.close()
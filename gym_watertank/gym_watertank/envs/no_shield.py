class DummyShield:

	def __init__(self):
		print("Initializing a dummy shield")
		print("No actions are filtered here")

	def shielded_actions(self, state_val, switch_state):
		return [0, 1]
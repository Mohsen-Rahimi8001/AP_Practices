class User:
	"""User class"""

	user_count = 0
	
	def __init__(self, username:str) -> None:
		"""
		initializer of the User class
		paramters: 
			username: username of the user.
		"""
		self.username = username
		User.user_count += 1

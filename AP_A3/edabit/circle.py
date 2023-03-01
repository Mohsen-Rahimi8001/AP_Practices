import math

class Circle:
	"""Circle class"""

	def __init__(self, radius:float) -> None:
		"""
		initializer of the Circle class
		parameters: 
			radius: radius of the circle
		"""
		self.radius = radius
		
	def getArea(self) -> "float":
		"""calculate circle area"""
		return math.pi * self.radius ** 2
		
	def getPerimeter(self) -> "float":
		"""calculate circle perimeter"""
		return 2 * math.pi * self.radius

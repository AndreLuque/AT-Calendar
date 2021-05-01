from typing import List, Optional, NoReturn, TypeVar

class AlertType():
	def __init__(self, description: str):
		self.__description: str = description

	def __str__(self):
		return self.__description	
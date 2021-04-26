from typing import List, Optional, NoReturn, TypeVar

class AlertType():
	def __init__(self, description: str):
		self.__description = description

	def __str__(self):
		return self.__description	
from typing import List, Optional, NoReturn, TypeVar
from abc import ABC, abstractmethod
from message import Message
from date import Date
from time import Time
from alertType import AlertType

T = TypeVar('T')

class Alert(ABC):
	def __init__(self, message: Message, date: Date, time: Time, alertType: str):
		self.__message: Message = message
		self.__date: Date = date
		self.__time: Time = time
		self.__alert_type: AlertType = alertType

	#los metodos son privados entonces definimos properties para visualizarlos
	@property
	def message(self) -> Message:
		return self.__message

	@property
	def date(self) -> Date:
		return self.__date

	@property 
	def time(self) -> Time:
		return self.__time

	@property
	def alert_type(self) -> AlertType:
		return self.__type			

	#para poder cambiarlo a string definimos el metodo magico __str__. Tendremos que definir str para los otros parametros tambien ya que tampoco son de tipo str
	def __str__(self):
		return 'ALERT' + '\n' + str(self.alert_type) + '\n' + str(self.date) + '\n' + str(self.time) + '\n' + str(self.message)

	#para poder ordenar una lista de Alerts debemos tener un criterio para ordenarlo, usamos el metodo __lt__. utlizamos como referencia date y time por lo que definiremos __lt__ en esas clases tambien
	def __lt__(self, other):
		return self.date < other.date and self.time < other.time 

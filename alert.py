from typing import List, Optional, NoReturn, TypeVar
from abc import ABC, abstractmethod
from message import Message
from date import Date
from time1 import Time
from alertType import AlertType
from datetime import datetime
import time

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

	@message.setter
	def message(self, value: Message) -> NoReturn:
		self.__message = value	

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
		return 'ALERT: ' + str(self.__alert_type) + '\n' + str(self.__date) + '\n' + str(self.__time) + '\n' + str(self.__message)

	#para poder ver si hay una alerta redundante debebmos poder ver si dos son iguales, tenemos que definir el metodo magico __eq__
	#tendremos que definir este mismo metodo magico en cada una de las clases
	def __eq__(self, other):
		self.__message == other.message and self.__date == other.date and self.__time == other.time	

	#para poder ordenar una lista de Alerts debemos tener un criterio para ordenarlo, usamos el metodo __lt__. utlizamos como referencia date y time por lo que definiremos __lt__ en esas clases tambien
	def __lt__(self, other):
		return self.date < other.date or (self.date == other.date and self.time < other.time) 



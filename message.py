from typing import List, Optional, NoReturn, TypeVar

T = TypeVar('T')

class Message():
	def __init__(self, title: str, body:str):
		self.__title: str = title
		self.__body: str = body

	@property
	def title(self):
		return self.__title

	@property
	def body(self):
		return self.__body

	def __str__(self):
		return str(self.__title).upper() + '\n' + str(self.__body)

#lo probamos con un código de ejemplo
mensaje1: Message = Message('Examen', 'Recordad que tienes examen de Cálculo II, ponte a estudiar')

print(mensaje1)	#debeeria imprimir el titulo del mensaje en mayusculas y luego el cuerpo del mensaje					
from typing import List, Optional, NoReturn, TypeVar

class Time():
	def __init__(self, hour:int, minute:int):
		#debemos comprobar que el horario dado tenga sentido
		if hour < 0 or hour >= 24:
			raise ValueError('Hours in the day must be 0-23')
		if minute < 0 or minute >= 60:
			raise ValueError('Minutes in an hour must be 0-59')

		self.__hour: int = hour
		self.__minute: int = minute

	@property
	def hour(self):
		return self.__hour

	@property
	def minute(self):
		return self.__minute

	def __str__(self):
		if self.__hour < 10:
			if self.__minute < 10:
				return f'0{self.__hour}:0{self.__minute}'
			else: 
				return f'0{self.__hour}:{self.__minute}'
		else:
			if self.__minute < 10:
				return f'{self.__hour}:0{self.__minute}'
			else: 
				return f'{self.__hour}:{self.__minute}'		

	def __eq__(self, other):
		return self.__minute == other.minute and self.__hour == other.hour

	def __lt__(self, other):
		return (self.__hour < other.hour) or (self.__hour == other.hour and self.__minute < other.minute)

#lo probamos con un código de ejemplo
hora1: Time = Time(3, 46)
hora2: Time = Time(13, 47)
hora3: Time = Time(3, 47)
hora4: Time = Time(13, 2)
hora5: Time = Time(6, 0)

print(hora1) #debe ser '03:46'
print(hora4) #debe ser '13:02'
print(hora5) #debe ser '06:00'
print(hora1 < hora2) #debe ser True
print(hora1 < hora3) #debe ser True
print(hora2 == hora3) #debe ser False

#debe dar error y saltar la excepcion
print()
try:
	hora6: Time = Time(123, 6)
except:	
	print('ERROR. Hours in the day must be 0-23')
try:
	hora7: Time = Time(12, -4)
except:
	print('ERROR. Minutes in an hour must be 0-59')		
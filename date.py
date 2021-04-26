from typing import List, Optional, NoReturn, TypeVar

#funcion para ver si a fecha introducida es correcta. tenemos que tener en cuenta los años bisiestos por los dias que varian en febrero.
def correctDate(month:int, day:int, year:int) -> bool:
	if (year % 4 == 0) and ((year % 100 != 0) or (year % 100 == 0 and year % 400 == 0)):
		if month == 2:
			if 0 < day < 30:
				return True
			else:
				return False
		elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
			if 0 < day < 32:
				return True
			else:
				return False
		elif month == 4 or month == 6 or month == 9 or month == 11:
			if 0 < day < 31:
				return True			 			    
			else:	
				return False
	else:
		if month == 2:
			if 0 < day < 29:
				return True
			else:
				return False
		elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
			if 0 < day < 32:
				return True
			else:
				return False
		elif month == 4 or month == 6 or month == 9 or month == 11:
			if 0 < day < 31:
				return True			 			    
			else:	
				return False


class Date():
	def __init__(self, day:int, month:int, year:int):
		if not correctDate(month, day, year):
			raise ValueError('Incorrect Date')
		self.__month: int = month
		self.__day: int = day 
		self.__year: int = year

	@property
	def month(self):
		return self.__month				

	@property
	def day(self):
		return self.__day

	@property 
	def year(self):
		return self.__year

	def __str__(self):
		if self.__month < 10:
			if self.__day < 10:
				return f'0{self.__day}/0{self.__month}/{self.__year}'
			else:
				return f'{self.__day}/0{self.__month}/{self.__year}'	
		else:
			if self.__day < 10:
				return f'0{self.__day}/{self.__month}/{self.__year}'
			else:
				return f'{self.__day}/{self.__month}/{self.__year}'

	def __eq__(self, other):
		return self.__day == other.day and self.__month == other.month and self.__year == other.year			

	def __lt__(self, other):
		return (self.__year < other.year) or (self.__year == other.year and self.__month < other.month) or (self.__year == other.year and self.__month == other.month and self.__day < other.day)									

#código de prueba
try: 
	fecha1: Date(29, 2, 2017)
except:
	print('ERROR')
#debe dar error

fecha1: Date = Date(29, 2, 2020)
fecha2: Date =  Date(29, 3, 2017)
fecha3: Date = Date(29, 3, 2020)
fecha4: Date = Date(2, 2, 2017)
fecha5: Date = Date(2, 10, 2017)

print(fecha1 > fecha2) #debe imprimir True
print(fecha1 < fecha3) #debe imprimir True
print(fecha3) #debe ser 29/03/2020 
print(fecha4) #debe ser 02/02/2017
print(fecha5) #debe ser 02/10/2017

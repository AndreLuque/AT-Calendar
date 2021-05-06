#código que creara la ventana de la applicacion
from alert import Alert
from message import Message
from date import Date, correctDate
from time1 import Time
from alertType import AlertType
from typing import List, NoReturn, TypeVar
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMessageBox, QGridLayout, QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit, QComboBox, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore
import datetime
import pickle
from threading import *
import time
from pushbullet import *

T = TypeVar('T')

class MainWindow(QMainWindow):
	"""Main Window."""
	def __init__(self, parent = None):
		"""Initializer."""
		super().__init__(parent)
		self.setWindowTitle('AT-Calendar')
		#self.setCentralWidget(QLabel('YAAAY'))
		#self.__createMenu()
		self.__createToolBar()
		self.__createStatusBar()

		#cambiamos a la pagina de inicio
		self.__change_to_home_screen()

		#recogemos la informacion de la app
		self.__restoreInfo()

		#establecemos la aplicacion como abiertas
		self.__open: bool = True
		#inciamos un thread separado para ejecutar el checkeo de las alertas. Asi no se congela el programa y se ejecutan a la vez
		t1 = Thread(target = self.__checkAlerts)
		t1.start()

		#print(self.__listTodaysSchedule)
		#print(self.__listTommorowsTasks)
		#print(self.__listAlerts)

	def __checkAlerts(self) -> NoReturn:
		while self.__open == True:
			#primero comprobamos que la lista de tommorow no tiene la fecha de hoy, si es el caso, ponemos la lista de hoy como la de mañana y vaciamos la de mañana
			#si la fecha de tommorow es anterior a la de hoy vaciamos las dos listas
			if len(self.__listTodaysSchedule) != 0:
				if str(self.__listTodaysSchedule[0].date) != str(datetime.date.today()):
					self.__listTodaysSchedule = []
			if len(self.__listTommorowsTasks) != 0:
				if str(self.__listTommorowsTasks[0].date) == str(datetime.date.today()):
					self.__listTodaysSchedule = self.__listTommorowsTasks
					self.__listTommorowsTasks = []
				elif str(self.__listTommorowsTasks[0].date) == str(datetime.date.today() + datetime.timedelta(days = 1)):
					None	
				else:
					self.__listTommorowsTasks = []

			#despues, vemos si alguna alerta es de fecha anterior a la de hoy, si lo es lo borramos, por otro lado , si es de hoy, la añadimos a nuestro schedule y borramos. finalemente, si es de mañana mandamos pushbullet y añadimos a listtommorow
			#creamos una instancia de date para poder compararlo
			todayDate: Date = Date(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)
			for alert in self.__listAlerts:
				if str(alert.date) == str(datetime.date.today()):
					#lo añadimos a nuestra lista de hoy y volvenos a ordernarla
					self.__listTodaysSchedule += [alert]
					self.__listTodaysSchedule.sort()
					#lo borramos de la lista de alertas
					self.__listAlerts.remove(alert)
				elif str(alert.date) == str(datetime.date.today() + datetime.timedelta(days = 1)):
					#lo añadimos a nuestra lista para mañana y volvemos a ordernarla
					self.__listTommorowsTasks += [alert]
					self.__listTommorowsTasks.sort()
					#mandamos la notificacion pushbullet
					send_notification_via_pushbullet(alert.message.title, str(alert.date) + '\n' + str(alert.time) + '\n' + alert.message.body)
					#lo borramos de las alertas
					self.__listAlerts.remove(alert)
				elif alert.date < todayDate:
					#lo borramos de la lista
					self.__listAlerts.remove(alert)


			#lo ultimo es checkear si alguna de las tareas del dia se tiene que realizar en los proximos 10 min, si es asi, mandara pushbullet
			t = time.localtime()
			current_hour = time.strftime("%H", t)
			current_minute = time.strftime("%M", t)
			current_time: Time = Time(int(current_hour), int(current_minute))
			for task in self.__listTodaysSchedule:
				if current_time == task.time:
					send_notification_via_pushbullet(task.message.title, str(task.date) + '\n' + str(task.time) + '\n' + task.message.body)

			#dormimos el progama otros 5 min	
			time.sleep(5)

	def __restoreInfo(self) -> NoReturn:
		#abrimos el archivo y recuperamos la info
		listInfo = []
		with open('taskInfo.pkl', 'rb') as input:
			listInfo = pickle.load(input)

		#inicializamos la lista de alertas
		self.__listAlerts: List[Alert] = listInfo[0]
		#inicializamos la lista de tareas para mañana 
		self.__listTommorowsTasks: List[Alert] = listInfo[1]
		#inicializamos la lista de tareas de hoy
		self.__listTodaysSchedule: List[Alert] = listInfo[2]


	def closeEvent(self, event):
		#primero cerramos el thread del check alerts
		self.__open = False

		#cuando se cierra la pantalla vamos a guardar toda la informacion de las tareas
		listInfo = [self.__listAlerts, self.__listTommorowsTasks, self.__listTodaysSchedule]

		#abrimos el archivo de pickle y guardamos la informacion alli
		with open('taskInfo.pkl', 'wb') as output:
			pickle.dump(listInfo, output, pickle.HIGHEST_PROTOCOL)


	def __createMenu(self) -> NoReturn:
		self.menu = self.menuBar().addMenu("&Menu")
		self.menu.addAction('&Exit', self.close)

	def __createToolBar(self) -> NoReturn:
		tools = QToolBar()
		self.addToolBar(tools)

		#añadimos boton para ir a la pantalla inicial 
		tools.addAction('Home', lambda: self.__change_to_home_screen())

		#añadimos boton para ver las tareas del dia
		tools.addAction('Today´s Schedule', lambda: self.__change_to_todays_schedule_screen())

		#añadimos el boton para ver el calendario de alertas
		tools.addAction('Alert Calendar', lambda: self.__change_to_alert_calendar_screen())

		#añadimos boton para ir a la pantalla de añadir alerta
		tools.addAction('Add Alert', lambda: self.__change_to_alert_screen())

		#añadimos boton para planear su siguente dia
		tools.addAction('Plan for Tommorow', lambda: self.__change_to_plan_tommorow_screen(False))

		#añadimos boton para ir a ajustes
		tools.addAction('Settings', lambda: self.__change_to_settings_screen())

		#añadimos boton para salirse de la app
		tools.addAction('Exit', self.close)

	def __createStatusBar(self) -> NoReturn:
		status = QStatusBar()
		status.showMessage("Current Status: Home Page")
		self.setStatusBar(status)

	def __change_to_home_screen(self) -> NoReturn:
		#cargando e insertando la imagen de fondo
		bgImage = QLabel() 
		bgImage.setText('      AT' + '\n' + ' Calendar')
		bgImage.setStyleSheet('background-image : url(bg.png)')
		bgImage.setFont(QFont('Garamond', 40, QFont.Bold))

		self.setCentralWidget(bgImage)


		#cambiamos el estado del programa, ahora estamos en la ventana de añadir alerta
		self.statusBar().showMessage('Current Status: Home Page')
		self.setWindowTitle('AT-Calendar')
		#cambiamos el color de la barra
		self.statusBar().setStyleSheet('background-color : gainsboro')

	def __change_to_alert_screen(self) -> NoReturn:
		#cambiamos el estado del programa, ahora estamos en la ventana de añadir alerta
		self.statusBar().showMessage('Current Status: Adding Alert')
		self.setWindowTitle('Add Alert')
		#cambiamos el color de la barra a rosa
		self.statusBar().setStyleSheet('background-color : gainsboro')
	
		layout = QVBoxLayout()

		#############################################################################################

		sublayout1 = QHBoxLayout()

		#ponemos el titulo de Date, aqui es donde pondran las fechas de sus alertas    	
		date = QLabel('Date:')
		sublayout1.addWidget(date)

		#ponemos una caja desplegable donde podran elegir el mes 
		self.__month = QComboBox()
		listMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		self.__add_elements_comboBox(self.__month, listMonths)
		self.__month.setMaximumWidth(500)
		sublayout1.addWidget(self.__month)

		#ponemos un hueco para que el usuario introduzca el año
		self.__year = QComboBox()
		listYears = ['2021', '2022']
		self.__add_elements_comboBox(self.__year, listYears)
		sublayout1.addWidget(self.__year)

		#ponemos un hueco para que el usuario introduzca el dia
		self.__day = QLineEdit(placeholderText = 'Day')
		self.__day.setMaxLength(2)
		sublayout1.addWidget(self.__day)

		layout.addLayout(sublayout1)

		######################################################################################################

		sublayout2 = QHBoxLayout()

		#ponemos el titulo de Time, aqui es donde pondran el horario que quieran
		time = QLabel('Time: ')
		sublayout2.addWidget(time)

		#ponemos un hueco para que el usuario indique una hora
		self.__hour = QLineEdit(placeholderText = 'Hour')
		self.__hour.setMaxLength(2)
		sublayout2.addWidget(self.__hour)

		sublayout2.addWidget(QLabel(':'))

		#ponemos un hueco para que el usuario indique el minute
		self.__minute = QLineEdit(placeholderText = 'Minute')
		self.__minute.setMaxLength(2)
		sublayout2.addWidget(self.__minute)

		layout.addLayout(sublayout2)

		#########################################################################################################

		sublayout3 = QHBoxLayout()

		#ponemos el titulo de alertype para que el usuario nos indique un tipo de alerta
		sublayout3.addWidget(QLabel('Alert Type:'))

		#ponemos una caja desplegable para que elija un tipo de alerta
		self.__alertType = QComboBox()
		listAlertTypes = ['Exam', 'Friends&Family Event', 'Meeting', 'Other']
		self.__add_elements_comboBox(self.__alertType, listAlertTypes)
		sublayout3.addWidget(self.__alertType)

		self.__alertType_other = QLineEdit(placeholderText = 'Specify Other (Optional)')
		sublayout3.addWidget(self.__alertType_other)


		layout.addLayout(sublayout3)

		##########################################################################################################

		#ponemos el hueco para que nos escriba el titulo de su alerta
		self.__title = QLineEdit(placeholderText = 'Alert Description')
		self.__title.setMaximumWidth(500)
		self.__title.setMaxLength(20)
		layout.addWidget(self.__title)

		#ponemos un hueco para que escriba un mensaje mas en detalle
		self.__body = QLineEdit(placeholderText = 'Message (Optional)')
		self.__body.setMaximumHeight(300)
		layout.addWidget(self.__body)

		##########################################################################################################

		sublayout4 = QHBoxLayout()

		addAlertButton = QPushButton()
		addAlertButton.setText('Add Alert')
		addAlertButton.setStyleSheet('background-color : lawngreen; font-weight : bold')
		addAlertButton.setMaximumWidth(150)
		addAlertButton.setMaximumHeight(50)
		sublayout4.addWidget(addAlertButton)

		layout.addLayout(sublayout4)

		#como el layout del mainwindow esta predefinido por pyqt, creamos nuestro propio layout y lo ponemos dentro del preestablecido
		centralWidget = QWidget()
		centralWidget.setLayout(layout)
		self.setCentralWidget(centralWidget)
		#hacemos que cuando se pulse el boton se llame a la funcion añadir alerta.
		addAlertButton.clicked.connect(lambda: self.__addAlert())

	def __addAlert(self):
		#obtenemos los datos que estan en las casillas
		monthTextInt: int = self.__convertMonthText() #cambiamos el mes a un numero
		dayText = self.__day.text()
		yearText = self.__year.currentText()
		hourText = self.__hour.text()
		minuteText = self.__minute.text()
		alertTypeText = self.__alertType.currentText()
		titleText = self.__title.text()
		bodyText = self.__body.text()

		#vemos si todas las casillas que son obligatorias estan rellenadas
		fill = True
		if dayText == '':
			self.__day.setStyleSheet('border : 2px solid red')
			self.__day.setPlaceholderText('!!MISSING DAY!!')
			fill = False
		else:
			self.__day.setStyleSheet('')	
		if hourText == '':
			self.__hour.setStyleSheet('border : 2px solid red')
			self.__hour.setPlaceholderText('!!MISSING HOUR!!')
			fill = False
		else:
			self.__hour.setStyleSheet('')		
		if minuteText == '':
			self.__minute.setStyleSheet('border : 2px solid red')
			self.__minute.setPlaceholderText('!!MISSING MINUTE!!')
			fill = False
		else:
			self.__minute.setStyleSheet('')		
		if titleText == '':
			self.__title.setStyleSheet('border : 2px solid red')
			self.__title.setPlaceholderText('!!MISSING DESCRIPTION!!')
			fill = False				
		else:
			self.__title.setStyleSheet('')		
		
		#estan las casillas rellenadas pasamos al siguente paso
		if fill:
			correct = True
			#ahora debemos comprobar que los datos insertados son correctos
			#en caso afirmativo reiniciaremos las casillas quitando el bordado rojo y poniendo un mensaje de alerta añadida
			try:
				date = Date(int(dayText), int(monthTextInt), int(yearText))
				self.__day.setStyleSheet('')
			except:
				correct = False
				self.__day.setStyleSheet('border : 2px solid red')
				self.__day.setText('')
				self.__day.setPlaceholderText('!!INCORRECT DAY!!')

			time = Time(0, 0)
			try:
				time.hourSetter(int(hourText))
				self.__hour.setStyleSheet('')
			except:
				correct = False
				self.__hour.setStyleSheet('border : 2px solid red')
				self.__hour.setText('')
				self.__hour.setPlaceholderText('!!INCORRECT HOUR!!')
			try:
				time.minuteSetter(int(minuteText))
				self.__minute.setStyleSheet('')
			except:
				correct = False
				self.__minute.setStyleSheet('border : 2px solid red')
				self.__minute.setText('')
				self.__minute.setPlaceholderText('!!INCORRECT MINUTE!!')

			alertType = AlertType(alertTypeText)
			message = Message(titleText, bodyText)

			#si todas las casillas estan BIEN rellanadas, pasamos al siguente paso
			if correct:
				#creamos la alerta y lo añadimos a nuestra lista de alertas que almacenaremos
				alert: Alert = Alert(message, date, time, alertType)
				self.__listAlerts += [alert]
				#desplegamos una pantalla en verde 
				self.__change_to_alert_added_screen()

	def __change_to_alert_added_screen(self) -> NoReturn:
		self.statusBar().showMessage('Current Status: Alert Added')
		self.statusBar().setStyleSheet('background-color : gainsboro')	

		greenscreen = QLabel()
		greenscreen.setAlignment(QtCore.Qt.AlignCenter)
		greenscreen.setStyleSheet('background-color : springgreen; color : whitesmoke')
		greenscreen.setText('ALERT ADDED!')
		greenscreen.setFont(QFont('Garamond', 50, QFont.Bold))

		#desplegamos la pantalla
		self.setCentralWidget(greenscreen)

	def __change_to_plan_tommorow_screen(self, update: bool) -> NoReturn:
		#cambiamos el estado del programa, ahora estamos en la ventana de añadir alerta
		self.statusBar().showMessage('Current Status: Planning Tommorow´s Day')
		self.setWindowTitle('Plan for Tommorow')
		#cambiamos el color de la barra a rosa
		self.statusBar().setStyleSheet('background-color : gainsboro')

		#diferenciamos entre cuando simplemente querenos actualizar la pantalla o cuando se inicia desde otra
		if not update:
			#creamos listas donde almacenaremos la informacion de nuestras tareas
			#tendremos que crear widgets vacios para que las casillas empiecen arriba
			self.__listHours: List[QLineEdit] = [QLineEdit(placeholderText = '9'), QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget(), QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget()]
			self.__listMinutes: List[QLineEdit] = [QLineEdit(placeholderText = '30'),  QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget(), QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget()]
			self.__listTaskDescription: List[QLineEdit] = [QLineEdit(placeholderText = 'Wakeup'),  QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget(), QWidget(),  QWidget(),  QWidget(),  QWidget(), QWidget()]
	
		layout = QGridLayout()

		#ponemos el titulo de las dos casillas que tendran que rellenar por cada actividad
		layout.addWidget(QLabel('Time'), 0, 0)
		layout.addWidget(QLabel('Task Description'), 0, 3)

		for i in range(len(self.__listHours)):
			#solo podremos usar ese atrubuto si es un QLineEdit
			if type(self.__listHours[i]) == QLineEdit:
				self.__listHours[i].setMaxLength(2)
				self.__listMinutes[i].setMaxLength(2)
				self.__listTaskDescription[i].setMaxLength(40)

			layout.addWidget(self.__listHours[i], i + 1, 0)

			#solo ponemos ':' si hay horarios, es decir, si hay casillas
			if type(self.__listHours[i]) == QLineEdit:
				layout.addWidget(QLabel(':'), i + 1, 1)
			
			layout.addWidget(self.__listMinutes[i], i + 1, 2)
			layout.addWidget(self.__listTaskDescription[i], i + 1, 3)

		deleteTaskButton: QPushButton = QPushButton('Delete Task')
		deleteTaskButton.setStyleSheet('background-color : tomato')
		layout.addWidget(deleteTaskButton, len(self.__listHours) + 1, 0)
		#si presiona el boton borramos la ultima casilla puesta
		deleteTaskButton.clicked.connect(lambda: self.__deleteTask())

		addTaskButton: QPushButton = QPushButton('Add Task')
		layout.addWidget(addTaskButton, len(self.__listHours) + 1, 2)
		#si presiona el boton añadimos una nueva casilla para rellenar otra
		addTaskButton.clicked.connect(lambda: self.__addTask())

		saveTasksButton: QPushButton = QPushButton('Save Tasks')
		saveTasksButton.setStyleSheet('background-color : lawngreen')
		layout.addWidget(saveTasksButton, len(self.__listHours) + 1, 3)
		#si presiona el boton se guardan las tareas para el siguente dia 
		saveTasksButton.clicked.connect(lambda: self.__saveTasks())


		#como el layout del mainwindow esta predefinido por pyqt, creamos nuestro propio layout y lo ponemos dentro del preestablecido
		centralWidget = QWidget()
		centralWidget.setLayout(layout)
		self.setCentralWidget(centralWidget)


	def __addTask(self) -> NoReturn:
		#recorremos la lista y vemos cual es el primer hueco donde podemos poner una casillas mas 
		exit: bool = False
		i: int = 0
		while i < len(self.__listHours) and not exit:
			if type(self.__listHours[i]) == QWidget:
				exit = True
			else:
				i += 1
		if i < len(self.__listHours):
			self.__listHours[i] = QLineEdit(placeholderText = 'Hour')
			self.__listMinutes[i] = QLineEdit(placeholderText = 'Minute')
			self.__listTaskDescription[i] = QLineEdit(placeholderText = 'Description')			

			#actualizamos la pantalla
			self.__change_to_plan_tommorow_screen(True)

	def __deleteTask(self) -> NoReturn:	
		#recorremos la lista buscando la ultima casilla y lo borramos
		exit: bool = False
		i: int = 0
		while i < len(self.__listHours) and not exit:
			if type(self.__listHours[i]) == QWidget:
				exit = True
			else:
				i += 1
		if i != 1:
			self.__listHours[i - 1] = QWidget()
			self.__listMinutes[i - 1] = QWidget()
			self.__listTaskDescription[i - 1] = QWidget()			

			#actualizamos la pantalla
			self.__change_to_plan_tommorow_screen(True)


	def __saveTasks(self) -> NoReturn:	
		#recorrer las listas que guardan la info de las tareas y mirar que las casillas esten rellenadas y comprobar a la vez que esten bien rellenadas
		#sino poner el bordillo rojo y cambia el placeholder. Si esta todo correcto almacenar la informacion como clases de alertas y dejarlo en una lista siguenet dia
		fill: bool = True
		correct: bool = True
		for i in range(len(self.__listHours)):
			if type(self.__listHours[i]) == QLineEdit:
				if self.__listHours[i].text() == '':
					self.__listHours[i].setStyleSheet('border: 2px solid red')
					self.__listHours[i].setText('')
					self.__listHours[i].setPlaceholderText('!!MISSING HOUR!!')
					fill = False
				else:
					self.__listHours[i].setStyleSheet('')
				if self.__listMinutes[i].text() == '':
					self.__listMinutes[i].setStyleSheet('border: 2px solid red')
					self.__listMinutes[i].setText('')
					self.__listMinutes[i].setPlaceholderText('!!MISSING MINUTE!!')
					fill = False
				else:
					self.__listMinutes[i].setStyleSheet('')	
				if self.__listTaskDescription[i].text() == '':
					self.__listTaskDescription[i].setStyleSheet('border: 2px solid red')
					self.__listTaskDescription[i].setText('')
					self.__listTaskDescription[i].setPlaceholderText('!!MISSING DESCRIPTION!!')
					fill = False
				else:
					self.__listTaskDescription[i].setStyleSheet('')	
				
				#pasamos a ver que los datos rellenados son correctos despues que sepamos que todas las casillas estan rellenadas    				
				if fill:
					time = Time(0, 0)
					#primero vemos si la hora es correcta
					try:
						time.hourSetter(int(self.__listHours[i].text()))
						self.__listHours[i].setStyleSheet('')
					except:
						self.__listHours[i].setStyleSheet('border : 2px solid red')
						self.__listHours[i].setText('')
						self.__listHours[i].setPlaceholderText('!!INCORRECT HOUR!!')
						correct = False
					#despues vemos si el mintuo es correcto 
					try:
						time.minuteSetter(int(self.__listMinutes[i].text()))
						self.__listMinutes[i].setStyleSheet('')
					except:
						self.__listMinutes[i].setStyleSheet('border : 2px solid red')
						self.__listMinutes[i].setText('')
						self.__listMinutes[i].setPlaceholderText('!!INCORRECT MINUTE!!')
						correct = False		

		#ahora si estan todas las casillas bien guardaremos todas las tareas 	
		if fill and correct:
			#conseguimos la fecha del dia de mañana
			tommorow = datetime.date.today() + datetime.timedelta(days = 1)

			for i in range(len(self.__listHours)):
				if type(self.__listHours[i]) == QLineEdit:
					#creamos la tarea y lo añadimos a nuestra lista de tareas para mañana
					task: Alert = Alert(Message(self.__listTaskDescription[i].text(), ''), Date(tommorow.day, tommorow.month, tommorow.year), Time(int(self.__listHours[i].text()), int(self.__listMinutes[i].text())), AlertType(''))
					self.__listTommorowsTasks += [task]


			self.__change_to_saved_tommorows_tasks_screen()

	def __change_to_saved_tommorows_tasks_screen(self) -> NoReturn:
		#cambiamos la barra de estado
		self.statusBar().showMessage('Current Status: Alert Added')
		self.statusBar().setStyleSheet('background-color : lightgray')	

		purplescreen = QLabel()
		purplescreen.setAlignment(QtCore.Qt.AlignCenter)
		purplescreen.setStyleSheet('background-color : mediumpurple; color : lightgray')
		purplescreen.setText('TOMMOROW´S' + '\n' + 'TASKS SAVED!')
		purplescreen.setFont(QFont('Garamond', 50, QFont.Bold))

		#desplegamos la pantalla
		self.setCentralWidget(purplescreen)

	def __change_to_todays_schedule_screen(self) -> NoReturn:
		#cambiamos el estado del programa, ahora estamos en la ventana de añadir alerta
		self.statusBar().showMessage('Current Status: Checking Today´s Schedule')
		self.setWindowTitle('Today´s Schedule')

		#si no hay tareas para hoy saltara una pantalla diciendo que no hay planes para hoy
		if len(self.__listTodaysSchedule) == 0:
			noSchedule = QLabel()
			noSchedule.setAlignment(QtCore.Qt.AlignCenter)
			noSchedule.setStyleSheet('background-color : indianred; color : gainsboro')
			noSchedule.setText('NO PLANS TODAY')
			noSchedule.setFont(QFont('Garamond', 50, QFont.Bold))

			#cambiamos el color de la barra a rosa
			self.statusBar().setStyleSheet('background-color : gainsboro')

			self.setCentralWidget(noSchedule)
		#en caso contrario pondremos una tabla con las tareas del dia
		else:
			#inicializamos el layout, como se van a distribuir los objetos
			layout = QVBoxLayout()

			#ponemos el titulo
			title = QLabel('Schedule:')
			title.setStyleSheet('font-size : 50px; font-weight : bold')
			layout.addWidget(title)

			#creamos la tabla y definimos su tamaño
			tableSchedule = QTableWidget()
			tableSchedule.setRowCount(len(self.__listTodaysSchedule))
			tableSchedule.setColumnCount(2)

			#ordenamos las tareas antes de ponerlo en la tabla
			self.__listTodaysSchedule.sort()
			for i in range(len(self.__listTodaysSchedule)):
				tableSchedule.setItem(i, 0, QTableWidgetItem(str(self.__listTodaysSchedule[i].time)))
				tableSchedule.setItem(i, 1, QTableWidgetItem(self.__listTodaysSchedule[i].message.title))

			#ponemos el titulo de las columnas
			tableSchedule.setHorizontalHeaderLabels(['Time', 'Task Description'])

			#hacemos que la tabla se extiedna para todo el ancho de la pantalla
			tableSchedule.horizontalHeader().setStretchLastSection(True)
			tableSchedule.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)	

			#modificamos el esstilo
			tableSchedule.setStyleSheet('background-color : whitesmoke')


			layout.addWidget(tableSchedule)		


			#cambiamos el color de la barra a rosa
			self.statusBar().setStyleSheet('background-color : gainsboro')


			centralWidget = QWidget()
			centralWidget.setLayout(layout)
			centralWidget.setStyleSheet('background-color :  salmon')
			self.setCentralWidget(centralWidget)





	def __change_to_alert_calendar_screen(self) -> NoReturn:
		print()	

	def __change_to_settings_screen(self) -> NoReturn:
		print()	

	def __add_elements_comboBox(self, comboBox: QComboBox, listElements: List[T]) -> NoReturn:
		for element in listElements:
			comboBox.addItem(str(element))

	def __convertMonthText(self, monthStr: str = '', monthInt: int = 0) -> int:
		listMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		monthStr = self.__month.currentText()
		for i in range(len(listMonths)):
			if monthStr == listMonths[i]:
				monthInt = i + 1
		return monthInt				

	def __correctDays(self, year: str, month: str) -> List[int]:
		year = int(year)
		if (year % 4 == 0) and ((year % 100 != 0) or (year % 100 == 0 and year % 400 == 0)):
			if month == 'February':
				return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
			elif month == 'January' or month == 'March' or month == 'May' or month == 'July' or month == 'August' or month == 'October' or month == 'December':
				return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
			elif month == 'April' or month == 'June' or month == 'September' or month == 'November':
				return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
		else:
			if month == 'February':
				return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
			elif month == 'January' or month == 'March' or month == 'April' or month == 'July' or month == 'August' or month == 'October' or month == 'December':
				return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
			elif month == 'April' or month == 'June' or month == 'September' or month == 'November':	
				return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]		

def main ():

	app = QApplication([]) #se necesita ejecutar QApplication siempre al crear una app con Qt
							#dentro de los corchetes van los paramteros que pasamos al cmd, aqui no es nada. podriamos pasar sys.argv si quisieramos que acepatara argumentos de la linea de cmd.

	window1: MainWindow = MainWindow()
	window1.setGeometry(425, 200, 1000, 700) #posicion en la pantalla x e y, y luego su longitud y anchura
	window1.show() #por defecto se omiten los objetos, hay q poner el .show() para mostrarlo

	app.exec() #debemos poner el .exec() para que el programa siga hasta que el usuario salga de la ventana 

if __name__ == '__main__': main()

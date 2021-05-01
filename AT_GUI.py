#código que creara la ventana de la applicacion
from alert import Alert
from message import Message
from date import Date, correctDate
from time1 import Time
from alertType import AlertType
from typing import List, NoReturn, TypeVar
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMessageBox, QGridLayout, QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap

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

       	#inicializamos la lista de alertas
       	listAlerts: List[Alert] = []

    def __createMenu(self) -> NoReturn:
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def __createToolBar(self) -> NoReturn:
        tools = QToolBar()
        self.addToolBar(tools)

        #añadimos boton para ir a la pantalla inicial 
        tools.addAction('Home', lambda: self.__change_to_home_screen())

        #añadimos boton para ir a la pantalla de añadir alerta
        tools.addAction('Add Alert', lambda: self.__change_to_alert_screen())

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


		#cambiamos el color de la barra a plata
    	self.statusBar().setStyleSheet('background-color : silver')

    def __change_to_alert_screen(self) -> NoReturn:
    	#cambiamos el estado del programa, ahora estamos en la ventana de añadir alerta
    	self.statusBar().showMessage('Current Status: Adding Alert')
    	self.setWindowTitle('Add Alert')
    	#cambiamos el color de la barra a rosa
    	self.statusBar().setStyleSheet('background-color : pink')
   	
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
    	listAlertTypes = []
    	self.__add_elements_comboBox(self.__alertType, listAlertTypes)
    	sublayout3.addWidget(self.__alertType)


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
    	addAlertButton.setStyleSheet('background-color : lime; font-weight : bold')
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
    		self.__day.setStyleSheet('border : 1px solid red')
    		self.__day.setPlaceholderText('!!MISSING DAY!!')
    		fill = False
    	else:
    		self.__day.setStyleSheet('')	
    	if hourText == '':
    		self.__hour.setStyleSheet('border : 1px solid red')
    		self.__hour.setPlaceholderText('!!MISSING HOUR!!')
    		fill = False
    	else:
    		self.__hour.setStyleSheet('')		
    	if minuteText == '':
    		self.__minute.setStyleSheet('border : 1px solid red')
    		self.__minute.setPlaceholderText('!!MISSING MINUTE!!')
    		fill = False
    	else:
    		self.__minute.setStyleSheet('')		
    	if titleText == '':
    		self.__title.setStyleSheet('border : 1px solid red')
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
    			self.__day.setStyleSheet('border : 1px solid red')
    			self.__day.setText('')
    			self.__day.setPlaceholderText('!!INCORRECT DAY!!')

    		time = Time(0, 0)
    		try:
    			time.hourSetter(int(hourText))
    			self.__hour.setStyleSheet('')
    		except:
    			correct = False
    			self.__hour.setStyleSheet('border : 1px solid red')
    			self.__hour.setText('')
    			self.__hour.setPlaceholderText('!!INCORRECT HOUR!!')
    		try:
    			time.minuteSetter(int(minuteText))
    			self.__minute.setStyleSheet('')
    		except:
    			correct = False
    			self.__minute.setStyleSheet('border : 1px solid red')
    			self.__minute.setText('')
    			self.__minute.setPlaceholderText('!!INCORRECT MINUTE!!')

    		alertType = AlertType(alertTypeText)
    		message = Message(titleText, bodyText)

    		#si todas las casillas estan BIEN rellanadas, pasamos al siguente paso
    		if correct:
    			#creamos la alerta y lo añadimos a nuestra lista de alertas que almacenaremos, ademas desplegamos una pantalla en verde copnfirmado la alerta. reiniciamos las casillas

    				
    		
    								









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

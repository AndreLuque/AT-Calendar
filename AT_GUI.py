#código que creara la ventana de la applicacion
from typing import List, NoReturn, TypeVar
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMessageBox, QGridLayout, QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit, QComboBox

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

    def __createMenu(self) -> NoReturn:
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def __createToolBar(self) -> NoReturn:
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)
        tools.addAction('Add Alert', lambda: self.__change_to_alert_screen())

    def __createStatusBar(self) -> NoReturn:
        status = QStatusBar()
        status.showMessage("Current Status: Home Page")
        self.setStatusBar(status)

        #setting status bar color to pink
        self.statusBar().setStyleSheet('background-color : pink')

    def __change_to_alert_screen(self) -> NoReturn:
    	#cambiamos el estado del programa, ahora estamos en la ventana de añadir alerta
    	self.statusBar().showMessage('Current Status: Adding Alert')
    	self.setWindowTitle('Add Alert')
   	
    	layout = QGridLayout()
		
		#ponemos el titulo de Date, aqui es donde pondran las fechas de sus alertas    	
    	date = QLabel('Date:')
    	layout.addWidget(date, 0, 0)

    	#ponemos una caja desplegable donde podran elegir el mes 
    	month = QComboBox()
    	listMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    	self.__add_elements_comboBox(month, listMonths)
    	layout.addWidget(month, 1, 0)

    	#ponemos un hueco para que el usuario introduzca el dia
    	day = QLineEdit(placeholderText = 'Day')
    	layout.addWidget(day, 1, 1)

    	#ponemos un hueco para que el usuario introduzca el año
    	year = QLineEdit(placeholderText = 'Year')
    	layout.addWidget(year, 1, 2)

    	#ponemos el titulo de Time, aqui es donde pondran el horario que quieran
    	time = QLabel('Time: ')
    	layout.addWidget(time, 2, 0)

    	#ponemos un hueco para que el usuario indique una hora
    	hour = QLineEdit(placeholderText = 'Hour')
    	layout.addWidget(hour, 3, 0)

    	layout.addWidget(QLabel(':'), 3, 1)

    	#ponemos un hueco para que el usuario indique el minute
    	minute = QLineEdit(placeholderText = 'Minute')
    	layout.addWidget(minute, 3, 2)

    	#ponemos el titulo de alertype para que el usuario nos indique un tipo de alerta
    	layout.addWidget(QLabel('Alert Type:'), 4, 0)

    	#ponemos una caja desplegable para que elija un tipo de alerta
    	alertType = QComboBox()
    	listAlertTypes = []
    	self.__add_elements_comboBox(alertType, listAlertTypes)
    	layout.addWidget(alertType, 5, 0)

    	#ponemos el hueco para que nos escriba el titulo de su alerta
    	title2 = QLineEdit(placeholderText = 'Alert Description')
    	layout.addWidget(title2, 6, 0)

    	#ponemos un hueco para que escriba un mensaje mas en detalle
    	message = QLineEdit(placeholderText = 'Message (Optional)')
    	layout.addWidget(message, 7, 0)



    	#como el layout del mainwindow esta predefinido por pyqt, creamos nuestro propio layout y lo ponemos dentro del preestablecido
    	centralWidget = QWidget()
    	centralWidget.setLayout(layout)
    	self.setCentralWidget(centralWidget)

    def __add_elements_comboBox(self, comboBox: QComboBox, listElements: List[T]) -> NoReturn:
    	for element in listElements:
    		comboBox.addItem(element)

def main ():

	app = QApplication([]) #se necesita ejecutar QApplication siempre al crear una app con Qt
							#dentro de los corchetes van los paramteros que pasamos al cmd, aqui no es nada. podriamos pasar sys.argv si quisieramos que acepatara argumentos de la linea de cmd.

	window1: MainWindow = MainWindow()
	window1.setGeometry(425, 200, 1000, 700) #posicion en la pantalla x e y, y luego su longitud y anchura
	window1.show() #por defecto se omiten los objetos, hay q poner el .show() para mostrarlo

	app.exec() #debemos poner el .exec() para que el programa siga hasta que el usuario salga de la ventana 

if __name__ == '__main__': main()

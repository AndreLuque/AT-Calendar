#código que creara la ventana de la applicacion

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMessageBox, QGridLayout, QMainWindow, QStatusBar, QToolBar, QAction

class MainWindow(QMainWindow):
    """Main Window."""
    def __init__(self, parent = None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('AT-Calendar')
        self.setCentralWidget(QLabel('YAAAY'))
       	self.__createMenu()
       	self.__createToolBar()
       	self.__createStatusBar()

    def __createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

        action1: QAction = QAction('action1', self)
        self.menu.addAction(action1)
        label = QLabel('heyo', self)
        label.setGeometry(100, 200, 300, 80)

        action1.triggered.connect(lambda: label.setText('hello'))
        #probar usar lambda para separarlo en dos ventanas !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def __createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def __createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


def main ():

	app = QApplication([]) #se necesita ejecutar QApplication siempre al crear una app con Qt
							#dentro de los corchetes van los paramteros que pasamos al cmd, aqui no es nada. podriamos pasar sys.argv si quisieramos que acepatara argumentos de la linea de cmd.

	window1: MainWindow = MainWindow()
	window1.setGeometry(425, 200, 1000, 700) #posicion en la pantalla x e y, y luego su longitud y anchura
	window1.show() #por defecto se omiten los objetos, hay q poner el .show() para mostrarlo

	app.exec() #debemos poner el .exec() para que el programa siga hasta que el usuario salga de la ventana 

if __name__ == '__main__': main()

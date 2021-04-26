#código que creara la ventana de la applicacion

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMessageBox

app = QApplication([]) #se necesita ejecutar QApplication siempre al crear una app con Qt
						#dentro de los corchetes van los paramteros que pasamos al cmd, aqui no es nada. podriamos pasar sys.argv si quisieramos que acepatara argumentos de la linea de cmd.


window = QWidget()
window.setGeometry(425, 200, 1000, 700) #posicion en la pantalla x e y, y luego su longitud y anchura
window.setWindowTitle("AT-CALENDAR") #titulo de la ventana
window.show() #por defecto se omiten los objetos, hay q poner el .show() para mostrarlo

app.exec() #debemos poner el .exec() para que el programa siga hasta que el usuario salga de la ventana 


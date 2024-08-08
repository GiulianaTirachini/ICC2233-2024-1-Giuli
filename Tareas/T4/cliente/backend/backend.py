from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QRandomGenerator
import threading
import parametros
from puzzle import TableroJuego

class MovimientoPepa(QObject):
    evento_entidad_se_movio = pyqtSignal(int, int, int, int, object)

    def __init__(self, fila, columna):
        super().__init__()
        self.mutex = threading.Lock() 
        self.fila = fila
        self.columna = columna
        self.direccion = ""
        self.paso_animacion = 0
        self.animacion_actual = ""
        self.animaciones = {}

        self.velocidad = 1000 
        self.bucle_velocidad = QTimer()
        self.bucle_velocidad.setInterval(self.velocidad)
        self.bucle_velocidad.timeout.connect(self.movimiento)
        self.bucle_velocidad.start()   
    
    def animacion(self, paso_animacion: int | None = None):
        if paso_animacion != None:
            self.paso_animacion = paso_animacion
        if (n := self.animaciones.get(self.animacion_actual)) is None:
            return
        self.paso_animacion = (self.paso_animacion + 1 if self.paso_animacion + 1 < len(n) else 0)

    def movimiento(self):
        with self.mutex: 
            if self.direccion == "W":
                self.subir()
            elif self.direccion == "S":
                self.bajar()
            elif self.direccion == "D":
                self.derecha()
            elif self.direccion == "A":
                self.izquierda()

    def subir(self):
        self.evento_entidad_se_movio.emit(self.fila, self.columna, self.fila - 1, self.columna, self)

    def bajar(self):
        self.evento_entidad_se_movio.emit(self.fila, self.columna, self.fila + 1, self.columna, self)

    def derecha(self):
        self.evento_entidad_se_movio.emit(self.fila, self.columna, self.fila, self.columna + 1, self)

    def izquierda(self):
        self.evento_entidad_se_movio.emit(self.fila, self.columna, self.fila, self.columna - 1, self)

    def actualizar_posicion_pepa(tablero, fila_actual, col_actual, fila_nueva, col_nueva, entidad):
        TableroJuego.liberar_casilla(fila_actual, col_actual)  
        TableroJuego.ocupar_casilla(fila_nueva, col_nueva, entidad)

class Sandia(QObject):
    sandia_capturada_signal = pyqtSignal(int, int)
    sandia_eliminada_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click_de_sandia = False
        self.tiempo_duracion = QTimer(self)
        self.tiempo_duracion.timeout.connect(self.desaparecer_sandia)
        self.tiempo_aparicion = QTimer(self)
        self.tiempo_aparicion.timeout.connect(self.aparecer_sandia)
        self.tiempo_aparicion.setSingleShot(True)

    def aparecer_sandia(self):
        self.click_de_sandia = False
        self.tiempo_duracion.start(parametros.TIEMPO_DURACION * 1000)
        posicion_x = QRandomGenerator.global_().bounded(50, 1150)
        posicion_y = QRandomGenerator.global_().bounded(50, 650)
        self.sandia_capturada_signal.emit(posicion_x, posicion_y)

    def desaparecer_sandia(self):
        if not self.click_de_sandia:
            self.click_de_sandia = True
            self.tiempo_duracion.stop()
            self.sandia_eliminada_signal.emit()
            self.timer_verificar_duracion = QTimer()
            self.timer_verificar_duracion.setSingleShot(True)
            self.timer_verificar_duracion.timeout.connect(self.verificar_tiempo_duracion)
            self.timer_verificar_duracion.start(parametros.TIEMPO_DURACION * 1000)

    def verificar_tiempo_duracion(self):
        if not self.click_de_sandia:
            self.click_de_sandia = True
            self.sandia_eliminada_signal.emit()

    def capturar_sandia(self):
        if not self.click_de_sandia:
            self.click_de_sandia = True
            self.tiempo_duracion.stop()
            self.sandia_eliminada_signal.emit()
            self.tiempo_aparicion.start(parametros.TIEMPO_APARICION * 1000)
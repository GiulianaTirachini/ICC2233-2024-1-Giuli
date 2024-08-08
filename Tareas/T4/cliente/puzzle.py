from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QKeyEvent
from PyQt6.QtMultimedia import QSoundEffect
import os
from leer_archivos import leer_base_puzzle, leer_solucion_puzzle
import parametros

class TableroJuego(QWidget):
    senal_casilla_cambiada = pyqtSignal(int, int)
    senal_puzzle_resuelto = pyqtSignal()

    def __init__(self, nombre_puzzle):
        super().__init__()
        self.columnas, self.filas = leer_base_puzzle(nombre_puzzle)
        self.puzzle = Puzzle(nombre_puzzle)
        self.matriz = [[None for _ in range(len(self.columnas))] for _ in range(len(self.filas))]
        self.personaje_label = QLabel(self)
        self.estado = self.puzzle.estado
        self.solucion = leer_solucion_puzzle(nombre_puzzle)
        self.init_ui(nombre_puzzle)
        self.fila_personaje = 0
        self.columna_personaje = 0
        self.ocupar_casilla(0, 0, "personaje")
        self.imagenes_movimiento = {
            'arriba': [QPixmap('cliente/assets/sprites/pepa/up_0.png'), 
                       QPixmap('cliente/assets/sprites/pepa/up_1.png'),
                       QPixmap('cliente/assets/sprites/pepa/up_2.png'),
                       QPixmap('cliente/assets/sprites/pepa/up_3.png')],
            'abajo': [QPixmap('cliente/assets/sprites/pepa/down_0.png'), 
                      QPixmap('cliente/assets/sprites/pepa/down_1.png'),
                      QPixmap('cliente/assets/sprites/pepa/down_2.png'),
                      QPixmap('cliente/assets/sprites/pepa/down_3.png')],
            'izquierda': [QPixmap('cliente/assets/sprites/pepa/left_0.png'), 
                          QPixmap('cliente/assets/sprites/pepa/left_1.png'),
                          QPixmap('cliente/assets/sprites/pepa/left_2.png'),
                          QPixmap('cliente/assets/sprites/pepa/left_3.png')],
            'derecha': [QPixmap('cliente/assets/sprites/pepa/right_0.png'), 
                        QPixmap('cliente/assets/sprites/pepa/right_1.png'),
                        QPixmap('cliente/assets/sprites/pepa/right_2.png'),
                        QPixmap('cliente/assets/sprites/pepa/right_3.png')],}
        
        self.indices_movimiento = {'arriba': 0,
                                   'abajo': 0,
                                   'izquierda': 0,
                                   'derecha': 0,}
        
        self.timer_animacion = QTimer(self)
        self.timer_animacion.timeout.connect(self.actualizar_animacion)
        self.direccion_actual = None

        self.timer_inactividad = QTimer(self)
        self.timer_inactividad.setSingleShot(True)
        self.timer_inactividad.timeout.connect(self.detener_animacion)

        self.sound_comer = QSoundEffect(self)
        self.sound_poop = QSoundEffect(self)

        self.sound_comer.setSource(QUrl.fromLocalFile
                                   (os.path.join('cliente/assets/sonidos', 'comer.wav')))
        self.sound_poop.setSource(QUrl.fromLocalFile
                                  (os.path.join('cliente/assets/sonidos', 'poop.wav')))


    def init_ui(self, nombre_puzzle):
        layout = QGridLayout()

        self.botones = []
        for i in range(len(self.filas)):
            fila_botones = []
            for j in range(len(self.columnas)):
                boton = QPushButton('')
                boton.setStyleSheet("background-color: green;")
                pixmap = QPixmap('cliente/assets/sprites/lechuga.png')
                icono = QIcon(pixmap)
                boton.setIcon(icono)
                boton.setIconSize(pixmap.size())
                boton.clicked.connect(lambda _, x=i, y=j: self.cambiar_estado_casilla(x, y))
                layout.addWidget(boton, i + 1, j + 1)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

        for j, columna in enumerate(self.columnas):
            texto_columna = "\n".join(map(str, columna))
            label = QLabel(texto_columna)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
            layout.addWidget(label, 0, j + 1)

        for i, fila in enumerate(self.filas):
            texto_fila = " ".join(map(str, fila))
            label = QLabel(texto_fila)
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(label, i + 1, 0)

        self.personaje_label = QLabel(self)
        self.personaje_label.setPixmap(QPixmap('cliente/assets/sprites/pepa/down_0'))
        self.personaje_label.setGeometry(0, 0, 20, 20)
        self.personaje_label.setScaledContents(True)
        self.personaje_label.setVisible(False)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def cambiar_estado_casilla(self, fila, columna):
        estado_actual = self.puzzle.estado[fila][columna]
        boton = self.botones[fila][columna]

        if estado_actual == '1':
            self.puzzle.estado[fila][columna] = '0'
            boton.setIcon(QIcon()) 
            boton.setStyleSheet("background-color: white;")
            self.sound_comer.play()

        else:
            self.puzzle.estado[fila][columna] = '1'
            self.mostrar_poop_y_cambiar_a_lechuga(boton)

    def mostrar_poop_y_cambiar_a_lechuga(self, boton):
        pixmap_poop = QPixmap('cliente/assets/sprites/poop.png')
        icono_poop = QIcon(pixmap_poop)
        boton.setIcon(icono_poop)
        boton.setIconSize(pixmap_poop.size())
        self.sound_poop.play()

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.mostrar_lechuga(boton, timer))
        timer.start(parametros.TIEMPO_TRANSICION * 1000)

    def mostrar_lechuga(self, boton, timer):
        pixmap_lechuga = QPixmap('cliente/assets/sprites/lechuga.png')
        icono_lechuga = QIcon(pixmap_lechuga)
        boton.setIcon(icono_lechuga)
        boton.setIconSize(pixmap_lechuga.size())
        boton.setStyleSheet("background-color: green;")
        timer.stop()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_W:
            self.mover_tortuga("W")
        elif event.key() == Qt.Key.Key_S:
            self.mover_tortuga("S")
        elif event.key() == Qt.Key.Key_A:
            self.mover_tortuga("A")
        elif event.key() == Qt.Key.Key_D:
            self.mover_tortuga("D")

    def mover_tortuga(self, direccion):
        fila_nueva = self.fila_personaje
        columna_nueva = self.columna_personaje

        if direccion == "W":
            fila_nueva -= 1
        elif direccion == "S":
            fila_nueva += 1
        elif direccion == "A":
            columna_nueva -= 1
        elif direccion == "D":
            columna_nueva += 1

        if 0 <= fila_nueva < len(self.botones) and 0 <= columna_nueva < len(self.botones[0]):
            self.liberar_casilla(self.fila_personaje, self.columna_personaje)
            self.ocupar_casilla(fila_nueva, columna_nueva, "personaje")
            self.fila_personaje = fila_nueva
            self.columna_personaje = columna_nueva
            self.direccion_actual = direccion
            if not self.timer_animacion.isActive():
                self.timer_animacion.start(100)
            self.timer_inactividad.start(300)

    def detener_animacion(self):
        self.timer_animacion.stop()
        self.direccion_actual = None

    def actualizar_animacion(self):
        if self.direccion_actual:
            self.cambiar_imagen(self.direccion_actual)
        
    def cambiar_imagen(self, direccion):
        if direccion == "W":
            key = 'arriba'
        elif direccion == "S":
            key = 'abajo'
        elif direccion == "A":
            key = 'izquierda'
        elif direccion == "D":
            key = 'derecha'
        
        indice_actual = self.indices_movimiento[key]
        self.personaje_label.setPixmap(self.imagenes_movimiento[key][indice_actual])
        self.indices_movimiento[key] = (indice_actual + 1) % len(self.imagenes_movimiento[key])

    def liberar_casilla(self, fila, columna):
        self.matriz[fila][columna] = None

    def ocupar_casilla(self, fila, columna, entidad): # la nueva 
        self.matriz[fila][columna] = entidad
        if entidad == "personaje":
            self.personaje_label.setVisible(True)
            self.personaje_label.move(
                self.botones[fila][columna].x() + self.botones[fila][columna].width() // 2 - 
                self.personaje_label.width() // 2,
                self.botones[fila][columna].y() + self.botones[fila][columna].height() // 2 - 
                self.personaje_label.height() // 2)
            self.personaje_label.raise_()
            
    def actualizar_posicion_pepa(self, fila_actual, col_actual, fila_nueva, col_nueva, entidad):
        self.liberar_casilla(fila_actual, col_actual)
        self.ocupar_casilla(fila_nueva, col_nueva, entidad)

class Puzzle:
        def __init__(self, nombre_puzzle):
            columnas, filas = leer_base_puzzle(nombre_puzzle)
            solucion = leer_solucion_puzzle(nombre_puzzle)
            self.columnas = columnas
            self.filas = filas
            self.solucion = solucion
            self.estado = [['1' for _ in range(len(columnas))] for _ in range(len(filas))]

        def cambiar_estado_casilla(self, fila, columna):
            if self.estado[fila][columna] == '1':
                self.estado[fila][columna] = '0'
            else:
                self.estado[fila][columna] = '1'

        def verificar_solucion(self):
            for fila in range(len(self.filas)):
                for columna in range(len(self.columnas)):
                    if self.estado[fila][columna] != self.solucion[fila][columna]:
                        return False
            return True
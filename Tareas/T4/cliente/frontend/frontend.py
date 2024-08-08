from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QComboBox,
    QListWidget, QScrollArea, QApplication, QMessageBox, QHBoxLayout, QStackedLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, pyqtSignal, Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
import os
import parametros
from backend.backend import Sandia, MovimientoPepa
from puzzle import TableroJuego 
from leer_archivos import dimencion_tablero

class MiVentanaInicio(QWidget):
    senal_comenzar_partida = pyqtSignal(str, str)
    senal_salir_programa = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.iniciar_musica()

    def init_gui(self):
        self.setGeometry(500, 35, 400, 500)
        self.setWindowTitle("DCCome Lechuga")

        self.label_imagen = QLabel(self)  # logo
        self.label_imagen.setGeometry(15, 15, 30, 30)
        ruta_logo = os.path.join('cliente', 'assets', 'sprites', 'logo')
        pixeles = QPixmap(ruta_logo)
        self.label_imagen.setPixmap(pixeles)
        self.label_imagen.setScaledContents(True)        

        self.label_nombre = QLabel("Nombre de usuario: ", self)  # nombre de usuario
        self.entry_nombre = QLineEdit(self)

        self.label_puzzle = QLabel("Selecciona el puzzle:", self)  # menú desplegable
        self.combo_puzzles = QComboBox(self)
        self.combo_puzzles.addItems(self.obtener_archivos_puzzle())

        label_salon_fama = QLabel("Salón de la Fama:", self)  # salón de la fama
        self.lista_puntajes = QListWidget(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.lista_puntajes)
        scroll_area.setFixedHeight(95) 

        boton_comenzar = QPushButton("Comenzar partida", self)  # comenzar la partida
        boton_comenzar.clicked.connect(self.iniciar_partida)

        boton_salir = QPushButton("Salir", self)  # salir del programa
        boton_salir.clicked.connect(self.salir_programa)

        layout_vertical = QVBoxLayout()
        layout_vertical.addWidget(self.label_imagen)
        layout_vertical.addWidget(self.label_nombre)
        layout_vertical.addWidget(self.entry_nombre)
        layout_vertical.addWidget(self.label_puzzle)
        layout_vertical.addWidget(self.combo_puzzles)
        layout_vertical.addWidget(label_salon_fama)
        layout_vertical.addWidget(scroll_area)
        layout_vertical.addWidget(boton_comenzar)
        layout_vertical.addWidget(boton_salir)

        self.setLayout(layout_vertical)

        self.actualizar_salon_fama()

    def obtener_archivos_puzzle(self):
        ruta_base_puzzles = os.path.join('cliente', 'assets', 'base_puzzles')
        lista_puzzles = os.listdir(ruta_base_puzzles)  # lista de todos los elementos.
        archivos = []
        for nombre_puzzle in lista_puzzles:
            ruta_completa_archivo = os.path.join(ruta_base_puzzles, nombre_puzzle)
            if os.path.isfile(ruta_completa_archivo):
                archivos.append(nombre_puzzle)
        return archivos
    
    def obtener_puntajes(self):
        puntajes = []
        if os.path.isfile("puntaje.txt"):
            with open("puntaje.txt", "r") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if ' - ' in linea:
                        puntajes.append(linea)
        return sorted(puntajes, key=lambda x: float(x.split(' - ')[1]), reverse=True)
    
    def actualizar_salon_fama(self):
        self.lista_puntajes.clear()
        puntajes_ordenados = self.obtener_puntajes()
        self.lista_puntajes.addItems(puntajes_ordenados)

    def validar_nombre_usuario(self, nombre):
        if not nombre:
            return "El nombre de usuario no puede estar vacío"
        tiene_mayuscula = False
        tiene_numero = False
        for letra in nombre:
            if letra.isupper():
                tiene_mayuscula = True
            if letra.isdigit():
                tiene_numero = True
        if not nombre.isalnum():
            return "El nombre de usuario debe ser alfanumérico"        
        if not tiene_mayuscula:
            return "El nombre de usuario debe contener al menos una letra mayúscula"
        if not tiene_numero:
            return "El nombre de usuario debe contener al menos un número"
        
    def iniciar_partida(self):
        nombre_usuario = self.entry_nombre.text()
        mensaje_error = self.validar_nombre_usuario(nombre_usuario)
        if mensaje_error:
            QMessageBox.warning(self, "Error de Validación", mensaje_error)
        else:
            puzzle_seleccionado = self.combo_puzzles.currentText()
            self.senal_comenzar_partida.emit(nombre_usuario, puzzle_seleccionado)
            self.close()

    def salir_programa(self):
        self.senal_salir_programa.emit()
        self.close()

    def mostrar_ventana_inicial(self):
        self.entry_nombre.clear()
        self.actualizar_salon_fama()
        self.show()

    def iniciar_musica(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)
        ruta_musica = os.path.join('cliente', 'assets', 'sonidos', "musica_1.wav")
        self.media_player.setSource(QUrl.fromLocalFile(ruta_musica))
        self.media_player.mediaStatusChanged.connect(self.repetir_musica)
        self.media_player.play()

    def repetir_musica(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

class MiVentanaJuego(QWidget, Sandia):
    senal_salir_programa = pyqtSignal()
    senal_tiempo_agotado = pyqtSignal()

    def __init__(self, nombre, puzzle):
        super().__init__()
        
        self.nombre = nombre
        self.tipo_puzzle_nombre = puzzle
        self.tiempo_restante = parametros.TIEMPO_JUEGO
        self.juego_pausado = False

        self.setWindowTitle(f"DCCome Lechuga - Juego: {self.tipo_puzzle_nombre}")
        self.setGeometry(170, 60, 100, 100)

        layout_principal = QVBoxLayout()

        self.area_central = QWidget()
        self.layout_area_central = QStackedLayout(self.area_central)

        self.tablero = TableroJuego(self.tipo_puzzle_nombre)
        self.layout_area_central.addWidget(self.tablero)

        self.label_pausa_logo = QLabel(self)
        ruta_logo = os.path.join('cliente', 'assets', 'sprites', 'logo.png')
        pixeles = QPixmap(ruta_logo)
        self.label_pausa_logo.setPixmap(pixeles)
        self.label_pausa_logo.setScaledContents(True)
        self.layout_area_central.addWidget(self.label_pausa_logo)

        layout_principal.addWidget(self.area_central)

        botones = self.crear_botones()
        layout_principal.addWidget(botones)

        self.setLayout(layout_principal)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_cuenta_regresiva)
        self.timer.start(1000)

        self.sandia = Sandia()
        self.sandia.sandia_capturada_signal.connect(self.mostrar_sandia)
        self.sandia.sandia_eliminada_signal.connect(self.ocultar_sandia)
        self.label_sandia = QLabel(self)
        ruta_sandia = os.path.join('cliente', 'assets', 'sprites', 'sandia')
        self.label_sandia.setStyleSheet(f"background-image: url('{ruta_sandia}'); "
        "background-repeat: no-repeat; background-position: center;")
        self.label_sandia.setGeometry(0, 0, 50, 50)
        self.label_sandia.hide()

        self.media_player_derrota = QSoundEffect()
        ruta_derrota = os.path.join('cliente', 'assets', 'sonidos', "juego_perdido.wav")
        self.media_player_derrota.setSource(QUrl.fromLocalFile(ruta_derrota))

        self.media_player_victoria = QSoundEffect()
        ruta_victoria = os.path.join('cliente', 'assets', 'sonidos', "juego_ganado.wav")
        self.media_player_victoria.setSource(QUrl.fromLocalFile(ruta_victoria))

        self.label_pausa_logo.hide()

        self.pepa = MovimientoPepa(fila=0, columna=0)
        self.pepa.evento_entidad_se_movio.connect(self.actualizar_posicion_pepa)

        self.label_pepa = QLabel(self)
        ruta_pepa = os.path.join('cliente', 'assets', 'sprites', 'pepa.png')
        self.label_pepa.setPixmap(QPixmap(ruta_pepa))
        self.label_pepa.setScaledContents(True)
        self.label_pepa.setGeometry(0, 0, 50, 50)
        self.label_pepa.hide()

    def keyPressEvent(self, event):
        if not self.juego_pausado:
            if event.key() == Qt.Key.Key_W:
                self.pepa.direccion = "W"
            elif event.key() == Qt.Key.Key_S:
                self.pepa.direccion = "S"
            elif event.key() == Qt.Key.Key_A:
                self.pepa.direccion = "A"
            elif event.key() == Qt.Key.Key_D:
                self.pepa.direccion = "D"

    def actualizar_posicion_pepa(self, fila_actual, columna_actual, fila_nueva, 
                                 columna_nueva, entidad):
        self.tablero.liberar_casilla(fila_actual, columna_actual)
        self.tablero.ocupar_casilla(fila_nueva, columna_nueva, entidad)
        self.label_pepa.setGeometry(columna_nueva * 50, fila_nueva * 50, 50, 50)
        self.label_pepa.show()
            
    def resizeEvent(self, event):
        self.label_pausa_logo.setGeometry(0, 0, 800, 700)
        self.label_pausa_logo.move((self.width() - self.label_pausa_logo.width()) // 2, 
                                   (self.height() - self.label_pausa_logo.height()) // 2)
        super().resizeEvent(event)

    def crear_botones(self):
        widget_contenedor = QWidget()
        layout_estadisticas = QHBoxLayout(widget_contenedor)
        self.label_cuenta_regresiva = QLabel(f"Tiempo restante: {self.tiempo_restante} segundos")
        layout_estadisticas.addWidget(self.label_cuenta_regresiva)
        self.boton_comprobar_solucion = QPushButton("Comprobar Solución")
        layout_estadisticas.addWidget(self.boton_comprobar_solucion)
        self.boton_comprobar_solucion.clicked.connect(self.comprobar_solucion)
        self.boton_pausar_juego = QPushButton("Pausar Juego")
        layout_estadisticas.addWidget(self.boton_pausar_juego)
        self.boton_pausar_juego.clicked.connect(self.pausar_juego)        
        self.boton_salir_programa = QPushButton("Salir del Programa")
        layout_estadisticas.addWidget(self.boton_salir_programa)
        self.boton_salir_programa.clicked.connect(QApplication.instance().quit)
        return widget_contenedor

    def pausar_juego(self):
        if self.juego_pausado:
            self.timer.start(1000)
            self.tablero.show()
            self.label_sandia.show()
            self.label_pausa_logo.hide()
            self.boton_pausar_juego.setText("Pausar Juego")
        else:
            self.timer.stop()
            self.tablero.hide()
            self.label_sandia.hide()
            self.label_pausa_logo.show()
            self.boton_pausar_juego.setText("Reanudar Juego")
        self.juego_pausado = not self.juego_pausado   

    def actualizar_cuenta_regresiva(self):
        self.tiempo_restante -= 1
        self.label_cuenta_regresiva.setText(f"Tiempo restante: {self.tiempo_restante} segundos")
        if self.tiempo_restante == 0:
            self.timer.stop()
            self.reproducir_musica_derrota()
            QMessageBox.information(self, "Fin del Juego", "¡Tiempo agotado! El juego terminó.")
            self.senal_tiempo_agotado.emit()

    def reproducir_musica_derrota(self):
        self.media_player_derrota.play()

    def reproducir_musica_victoria(self):
        self.media_player_victoria.play()
              
    def comprobar_solucion(self):
        if self.tablero.puzzle.verificar_solucion():
            self.timer.stop()
            self.reproducir_musica_victoria()
            puntaje = self.calcular_puntaje()
            mensaje = "¡Felicidades!\nHas resuelto el puzzle correctamente.\n"
            mensaje += f"Tu puntaje es: {puntaje} puntos."
            QMessageBox.information(self, "¡Felicidades!", mensaje)
            self.guardar_puntaje(self.nombre, puntaje)
            self.senal_tiempo_agotado.emit()
        else:
            self.timer.stop()
            mensaje = "Lo Siento :(\nTu solución no es correcta."
            QMessageBox.warning(self, "Intenta de nuevo", mensaje)
            self.timer.start(1000)

    def calcular_puntaje(self):
        n = dimencion_tablero(self.tipo_puzzle_nombre)
        numerador = self.tiempo_restante * n * n * parametros.CONSTANTE
        puntaje = numerador / (parametros.TIEMPO_JUEGO - self.tiempo_restante)
        return round(puntaje, 2)
    
    def guardar_puntaje(self, nombre_usuario, puntaje):
        with open("puntaje.txt", "a") as archivo:
            archivo.write(f"{nombre_usuario} - {puntaje}\n")

    def salir_programa(self):
        self.senal_salir_programa.emit()
        self.close()

    def mostrar_sandia(self, posicion_x, posicion_y):
        self.label_sandia.setGeometry(posicion_x, posicion_y, 50, 50)
        self.label_sandia.show()

    def ocultar_sandia(self):
        self.label_sandia.hide()
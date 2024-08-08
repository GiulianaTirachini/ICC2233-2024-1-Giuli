import sys
from PyQt6.QtWidgets import QApplication
from frontend.frontend import MiVentanaInicio, MiVentanaJuego

if __name__ == "__main__":
   
    app = QApplication(sys.argv)

    ventana_inicio = MiVentanaInicio()

    def iniciar_juego(nombre, puzzle):
        global ventana_juego
        ventana_juego = MiVentanaJuego(nombre, puzzle)
        ventana_juego.senal_tiempo_agotado.connect(mostrar_ventana_inicial_desde_juego)
        ventana_juego.senal_salir_programa.connect(mostrar_ventana_inicial_desde_juego)
        ventana_juego.show()

    def mostrar_ventana_inicial_desde_juego():
        ventana_inicio.mostrar_ventana_inicial()
        ventana_juego.close()

    ventana_inicio.senal_comenzar_partida.connect(iniciar_juego)
    ventana_inicio.senal_salir_programa.connect(lambda: sys.exit(app.quit()))
    ventana_inicio.show()

    sys.exit(app.exec())
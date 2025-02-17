import sys
import unittest

# Advertencia, la siguiente línea solo es utilizada por el cuerpo docente.
# Se considerará una mala práctica ocuparlo en sus evaluaciones.
sys.path.append("..")

from red import RedMetro


class TestInformacionRed(unittest.TestCase):

    def shortDescription(self):
        doc = self._testMethodDoc
        return doc or None

    def test_0(self):
        """
        Verifica que la cantidad de estaciones y conexiones por estación estén correctas.
        """
        conexiones = [[1, 1, 0], [0, 0, 1], [1, 1, 1]]
        estaciones = ["A", "B", "C"]

        red = RedMetro(conexiones, estaciones)
        resultado_estudiante = red.informacion_red()
        resultado_esperado = [3, [2, 1, 3]]

        self.assertListEqual(resultado_estudiante, resultado_esperado)

    def test_1(self):
        """
        Verifica que la cantidad de estaciones y conexiones por estación
        estén correctas para N + 1 estaciones, todas conectadas.
        """
        conexiones = [
            [0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
        estaciones = [
            "San Joaquin",
            "Pedro de Valdivia",
            "La Cisterna",
            "La Moneda",
            "Las Mercedes",
            "Baquedano",
            "Cal y Canto",
            "Tobalaba",
            "Las Rejas"
        ]

        red = RedMetro(conexiones, estaciones)
        resultado_estudiante = red.informacion_red()
        resultado_esperado = [9, [8, 8, 8, 8, 8, 8, 8, 8, 8]]

        self.assertListEqual(resultado_estudiante, resultado_esperado)

    def test_2(self):
        """
        Verifica que la cantidad de estaciones y conexiones por estación
        estén correctas para M estaciones, ninguna conectada.
        """
        conexiones = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        estaciones = [
            "San Joaquin",
            "La Cisterna",
            "La Moneda",
            "Las Mercedes",
            "Baquedano"
        ]

        red = RedMetro(conexiones, estaciones)
        resultado_estudiante = red.informacion_red()
        resultado_esperado = [5, [0, 0, 0, 0, 0]]

        self.assertListEqual(resultado_estudiante, resultado_esperado)

    def test_3(self):
        """
        Verifica que la cantidad de estaciones y conexiones por estación
        estén correctas para J estaciones, conectadas de manera mixta con diagonales.
        """
        conexiones = [
            [1, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1],
        ]
        estaciones = [
            "San Joaquin",
            "La Cisterna",
            "La Moneda",
            "Baquedano",
            "Cal y Canto",
        ]

        red = RedMetro(conexiones, estaciones)
        resultado_estudiante = red.informacion_red()
        resultado_esperado = [5, [2, 1, 2, 0, 4]]

        self.assertListEqual(resultado_estudiante, resultado_esperado)


if __name__ == "__main__":
    unittest.main(verbosity=2)

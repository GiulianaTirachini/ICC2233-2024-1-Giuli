from copy import copy
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator

from parametros import RUTA_PELICULAS, RUTA_GENEROS
from utilidades import (
    Pelicula, Genero, obtener_unicos, imprimir_peliculas,
    imprimir_generos, imprimir_peliculas_genero, imprimir_dccmax
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_peliculas(ruta: str) -> Generator:
    with open (ruta, "r") as archivo:
        lineas = archivo.readlines()
        for i in range(1, len(lineas)):
            pelicula = lineas[i].strip().split(",")
            yield Pelicula(int(pelicula[0]), pelicula[1], pelicula[2], int(pelicula[3]), float(pelicula[4]))

def cargar_generos(ruta: str) -> Generator:
    with open (ruta, "r") as archivo:
        lineas = archivo.readlines()
        for i in range(1, len(lineas)):
            genero = lineas[i].strip().split(",")
            yield Genero(genero[0], int(genero[1]))

# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_directores(generador_peliculas: Generator) -> set:
    directores = map(lambda pelicula: pelicula.director, generador_peliculas)
    return obtener_unicos(directores)

def obtener_str_titulos(generador_peliculas: Generator) -> str:
    peliculas = map(lambda pelicula: pelicula.titulo, generador_peliculas)
    return ", ".join(peliculas)

def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None
) -> filter:
    if director != None and rating_max != None and rating_min != None:
        return filter(lambda pelicula: pelicula.director == director and pelicula.rating <= rating_max and pelicula.rating >= rating_min, generador_peliculas)
    if director != None:
        return filter(lambda pelicula: pelicula.director == director, generador_peliculas)
    if rating_max != None:
        return filter(lambda pelicula: pelicula.rating <= rating_max, generador_peliculas)
    if rating_min != None:
        return filter(lambda pelicula: pelicula.rating >= rating_min, generador_peliculas)

def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None
) -> Generator:
    generadores = product(generador_peliculas, generador_generos)
    if genero != None:
        return filter(lambda pares: pares[0].id_pelicula == pares[1].id_pelicula and pares[1].genero == genero, generadores)
    else:
        return filter(lambda pares: pares[0].id_pelicula == pares[1].id_pelicula, generadores)

# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class DCCMax:
    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:
    def __init__(self, iterable_peliculas: list) -> None:
        self.peliculas = copy(iterable_peliculas)
        self.peliculas = list(sorted(self.peliculas, key=lambda pelicula: (pelicula.estreno, -pelicula.rating), reverse=True))


    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        if len(self.peliculas) == 0:
        # Se levanta la excepción correspondiente
            raise StopIteration()
        return self.peliculas.pop()


if __name__ == '__main__':
    print('> Cargar películas:')
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print('> Cargar géneros')
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print('> Obtener directores:')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print('> Obtener string títulos')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print('> Filtrar películas (por director):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(
        generador_peliculas, director='Christopher Nolan'
    ))
    print('\n> Filtrar películas (rating min):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print('\n> Filtrar películas (rating max):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print('> Filtrar películas por género')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, 'Biography'
    ))
    print()

    print('> DCC Max...')
    imprimir_dccmax(DCCMax(list(cargar_peliculas(RUTA_PELICULAS))))
    
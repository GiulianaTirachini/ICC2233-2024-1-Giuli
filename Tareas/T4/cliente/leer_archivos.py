import os

def leer_base_puzzle(nombre_puzzle):
    ruta = os.path.join('cliente', 'assets', 'base_puzzles', f'{nombre_puzzle}')
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
        columnas = lineas[0].strip().split(';')
        filas = lineas[1].strip().split(';')
        lista_columnas = []
        for linea in columnas:
            lista = [int(valor) if valor != "-" else 0 for valor in linea.split(',')]
            lista_columnas.append(lista)
        lista_filas = []
        for linea in filas:
            lista = [int(valor) if valor != "-" else 0 for valor in linea.split(',')]
            lista_filas.append(lista)
    return lista_columnas, lista_filas
 
def dimencion_tablero(nombre_puzzle):
    ruta = os.path.join('cliente', 'assets', 'base_puzzles', f'{nombre_puzzle}')
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
        columnas = lineas[0].strip().split(';')
    return len(columnas)

def leer_solucion_puzzle(nombre_puzzle):
    ruta = os.path.join('servidor', 'assets', 'solucion_puzzles', f'{nombre_puzzle}')
    with open(ruta, 'r') as archivo:
        solucion = [linea.strip() for linea in archivo.readlines()]
    return solucion
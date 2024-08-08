import sys, os
import dcciudad
from red import RedMetro

def mostrar_red(red, estaciones):
    dcciudad.imprimir_red(red, estaciones)

def encontrar_ciclo_mas_corto(red_metro, nombre_estacion):
    print(red_metro.ciclo_mas_corto(nombre_estacion))

def asegurar_ruta(nombre_estacion, destino, p_intermedias):
    print(red_metro.asegurar_ruta(nombre_estacion, destino, p_intermedias))

if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) != 3:
        print("Tienes que ingresar argumentos al llamar la funcion: 'python3 main.py <nombre de la red> <nombre de la estación>'")
    else:
        nombre_red = sys.argv[1]
        nombre_estacion = sys.argv[2]

        ruta = os.path.join("data", nombre_red + ".txt")
        if os.path.exists(ruta) == False:
            print("La red no existe.")
            sys.exit(1)
        lista_archivo = []
        with open (ruta, "r") as archivo:
            lineas = archivo.readlines()
            lista_archivo = []
            for linea in lineas:
                lista = linea.strip().split(",")
                lista_archivo.append(lista)
            lista_estaciones = []                               
            for i in lista_archivo[1:len(lista_archivo)-1]:
                lista_estaciones.append(i[0])
            if nombre_estacion not in lista_estaciones:
                print("La estación no existe.")
                sys.exit(1)
            lista_numeros = [] 
            cantidad = int(lista_archivo[0][0])
            for i in range(0, len(lista_archivo[-1]), cantidad):
                lista_numeros.append(lista_archivo[-1][i: i+cantidad])
            red = []
            for i in lista_numeros:
                sublista = []
                for j in i:
                    sublista.append(int(j))
                red.append(sublista)
        
        while True:
            print(f"¡Se cargó la red {nombre_red}.txt!")
            print(f"La estación elegida es {nombre_estacion}")
            print("*** Menú de Acciones ***")
            print("[1] Mostrar red")
            print("[2] Encontrar ciclo más corto")
            print("[3] Asegurar ruta")
            print("[4] Salir del programa")
            opcion = input("Indique su opción (1, 2, 3 o 4): ")

            red_metro = RedMetro(red, lista_estaciones)     # instancia de la clase RedMetro
            if opcion == "1":
                mostrar_red(red, lista_estaciones)
            elif opcion == "2":
                encontrar_ciclo_mas_corto(red_metro, nombre_estacion)
            elif opcion == "3":
                print("indique su lugar de destino")
                destino = input()
                print("indique la cantidad de estaciones intermedias")
                p_intermedias = input()
                asegurar_ruta(nombre_estacion, destino, p_intermedias)
            elif opcion == "4":
                break
            else:
                print("Por favor ingrese un número que si se encuentre en el menú")
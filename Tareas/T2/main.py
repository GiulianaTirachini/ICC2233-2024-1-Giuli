import parametros, os, sys
from abc import ABC, abstractmethod
from random import randint, choice
# herencia, clases abstractas, polimorfismo y properties

class Ejercito: #manejar las acciones a realizar dentro del campo de batalla
    def __init__(self) -> None:
        self.ejercito = [] # contiene los combatientes que posee el ejército
        self.oro = parametros.ORO_INICIAL # oro disponible a usar en el Menú de Tienda
    def __str__(self) -> str: # esta función es igual a presentarse
        mensaje = "*** Este es tu Ejército Actual ***\n"
        mensaje += "\n" 
        for person in self.ejercito:
            mensaje += f"¡Hola! Soy {person[0]}, un {person[1]} con {person[2]} / {person[3]} de vida"
            mensaje += f", {person[5]} de ataque y {person[4]} de defensa.\n"
        mensaje += f"\nTe quedan {len(self.ejercito)} combatientes. ¡Éxito, Guerrero!"
        return mensaje
    def agregar_combatiente(self, combatiente):
        self.ejercito.append(combatiente)
    def combatir(self, ejercito_enemigo): # manejar los enfrentamientos entre combatientes.
        num_ronda = 1
        while num_ronda < 4:
            if len(ejercito_enemigo) == 0:
                self.oro += parametros.ORO_GANADO
                print("¡Has ganado la batalla!")
                return True
            elif len(self.ejercito) == 0:
                num_ronda =1
                num_ronda +=1
                self.ejercito = []
                self.oro = parametros.ORO_INICIAL
                print("Has perdido la batalla.")
                return False
        
class Combatiente(ABC, Ejercito):
    def __init__(self, name, vida_max, poder, defensa, agility, resist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = name
        self.vida_max = vida_max # entre 0 y 100, cant máxi de puntos de vida que puede tener.
        self.vida = vida_max # No puede tener un valor <= 0 o >= self.vida_máx
        self.poder = poder # entre 1 y 10, cantidad de poder del peleador
        self.defensa = defensa # entre 1 y 20, resistencia del peleador
        self.agilidad = agility # entre 1 y 10, destreza del peleador
        self.resistencia = resist # entre 1 y 10, resistencia del peleador
        parte_de_vida = (2 * self.vida) / (self.vida_max)
        self.ataque = round((self.poder + self.agilidad + self.resistencia) * (parte_de_vida))
    
    def __str__(self) -> str:
        for person in self.ejercito: # esta función es igual a presentarse
            mensaje += f"¡Hola! Soy {person[0]}, un {person[1]} con {person[2]} / {person[2]} de vida"
            mensaje += f", {person[4]} de ataque y {person[3]} de defensa.\n"
        return mensaje

    @abstractmethod
    def atacar(self):
        pass
    
    @property
    def curarse(self) -> None:
        pass

    @curarse.setter
    def curarse(self, cura) -> None:
        if (self.vida + cura) <= self.vida_max and (self.vida + cura) >= 0:
            self.vida += cura
        elif (self.vida + cura) >= self.vida_max:
            self.vida = self.vida_max
        elif (self.vida + cura) <= 0:
            self.vida = 0
        return self.vida

    @abstractmethod
    def evolucionar(self):
        pass

    def presentarse(self) -> str:
        print(self)

class Guerrero(Combatiente):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def atacar(self, enemigo: "Guerrero"):
        self.agilidad -= parametros.CANSANCIO
        enemigo.vida -= round(self.ataque - enemigo.defensa)
    def evolucionar(self):
        pass

class Caballero(Combatiente):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def atacar(self, enemigo: "Guerrero"):
        if randint(0,1) >= parametros.PROB_CAB:
            porcentaje_poder = (enemigo.poder * parametros.RED_CAB) / 1
            enemigo.poder -= porcentaje_poder
            enemigo.vida -= round(self.ataque * (parametros.ATQ_CAB / 100) - enemigo.defensa)
        else:
            self.agilidad -= parametros.CANSANCIO
            enemigo.vida -= round(self.ataque - enemigo.defensa)
        self.defensa -= parametros.CANSANCIO
    def evolucionar(self):
        pass

class Mago(Combatiente):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def atacar(self, enemigo: "Guerrero"):
        if randint(0,1) >= parametros.PROB_MAG:
            ataque =self.ataque * (parametros.ATQ_MAG / 100)
            defensa = enemigo.defensa * ((100 - parametros.RED_MAG) / 100)
            enemigo.vida -= round( ataque - defensa)
    def evolucionar(self):
        pass

class Paladin(Guerrero, Caballero):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def atacar(self, enemigo: "Guerrero"):
        if randint(0,1) >= parametros.PROB_PAL:
            porcentaje_poder = (enemigo.poder * parametros.RED_CAB) / 1
            enemigo.poder -= porcentaje_poder
            enemigo.vida -= round(self.ataque * (parametros.ATQ_CAB / 100) - enemigo.defensa)
            self.resistencia += parametros.AUM_PAL
    def evolucionar(self):
        pass

class Mago_de_batalla(Guerrero, Mago):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def atacar(self, enemigo: "Guerrero"):
        if randint(0,1) >= parametros.PROB_MDB:
            ataque =self.ataque * (parametros.ATQ_MAG / 100)
            defensa = enemigo.defensa * ((100 - parametros.RED_MAG) / 100)
            enemigo.vida -= round( ataque - defensa)
            self.agilidad -= parametros.CANSANCIO
            self.defensa += parametros.DEF_MDB
    def evolucionar(self):
        pass

class Caballero_arcano(Caballero, Mago):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def atacar(self, enemigo: "Guerrero"):
        if randint(0,1) >= parametros.PROB_CAR:
            porcentaje_poder = (enemigo.poder * parametros.RED_CAB) / 1
            enemigo.poder -= porcentaje_poder
            enemigo.vida -= round(self.ataque * (parametros.ATQ_CAB / 100) - enemigo.defensa)  
        if randint(0,1) >= (100 - parametros.PROB_CAR):
            ataque =self.ataque * (parametros.ATQ_MAG / 100)
            defensa = enemigo.defensa * ((100 - parametros.RED_MAG) / 100)
            enemigo.vida -= round( ataque - defensa)
        self.poder += parametros.AUM_CAR
        self.agilidad += parametros.AUM_CAR
        self.resistencia -= parametros.CANSANCIO
    def evolucionar(self):
        pass

class Item(Combatiente):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    def pergamino(self): 
        self.evolucionar # hereda de evolucionar
    def lanza(self):
        self.evolucionar # hereda de evolucionar
    def armadura(self):
        self.evolucionar # hereda de evolucionar
          
tipos_gatos = ['MAG', 'CAB', 'GUE', 'CAR', 'PAL', 'MDB']
def cargar_ejercitos_enemigos(dificultad):
    ruta_archivo = os.path.join("data", f"{dificultad}.txt")
    ejercitos_enemigos = []
    with open(ruta_archivo, "r") as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            ronda = []
            combatientes = linea.strip().split(";")
            for combatiente in combatientes:
                caracteristicas = combatiente.split(",")
                if len(caracteristicas) != 7:
                    print("El formato del archivo es incorrecto.")
                    sys.exit(1)
                if caracteristicas[1] not in tipos_gatos:
                    print("Uno de los tipos de gato no es valido.")
                for caract in caracteristicas[2:]:
                    try:
                        int(caract)
                    except ValueError:
                        print(f"El campo '{caracteristicas[caract]}' no es un número entero.")
                        sys.exit(1)
                for caract in caracteristicas:
                    ronda.append(caract)
                ronda.append()
                
                ejercitos_enemigos.append(ronda)

ruta = os.path.join("data", "unidades.txt")
lista_unidades = []
ejercito_MAG = []
ejercito_GUE = []
ejercito_CAB = []
with open(ruta, "r") as archivo:
    lineas = archivo.readlines()
    for linea in lineas:
        caracteristicas = linea.strip().split(",")
        if len(caracteristicas) != 7:
            print("El formato del archivo es incorrecto.")
            sys.exit(1)
        if caracteristicas[1] not in tipos_gatos:
            print("Uno de los tipos de gato no es valido.")
        unidad = []
        for caract in caracteristicas[2:]:
            try:
                int_value = int(caract)
            except ValueError:
                print(f"El campo '{caract}' no es un número entero.")
                sys.exit(1)
        for indice, caract in enumerate(caracteristicas):
            if indice == 0 or indice == 1:
                unidad.append(caract)
            elif indice == 2:
                unidad.append(int(caract))
                unidad.append(int(caract))
            else:
                unidad.append(int(caract))
        lista_unidades.append(unidad)

for gato in lista_unidades:
    if gato[1] == "MAG":
        ejercito_MAG.append(gato)
    elif gato[1]  == "GUE":
        ejercito_GUE.append(gato)
    elif gato[1]  == "CAB":
        ejercito_CAB.append(gato)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Debes ingresar el nivel de dificultad siguiendo el formato:")
        print("python3 main.py <nivel de dificultad>")
        print("(puedes ser python, python3 o py seguún tu dispositivo)")
        sys.exit(1)
    nivel_dificultad = sys.argv[1]
    if nivel_dificultad not in ["facil", "intermedio", "dificil"]:
        print("Nivel de dificultad no válido. Debe ser 'facil', 'intermedio' o 'dificil'.")
        sys.exit(1)
    num_ronda = 1
    clase_ejercito = Ejercito()
    while True:
        print("*** Menú de Inicio ***")
        print(" ")
        print(f"Dinero disponible: {parametros.ORO_INICIAL}")
        print(f"Ronda actual: {num_ronda}") 
        print(" ")
        print("[1] Tienda")
        print("[2] Ejercito")
        print("[3] Combatir")
        print(" ")
        print("[0] Salir del programa")
        print(" ")
        opcion_inicio= input("Indique su opción: ")

        if opcion_inicio == "1":   #tienda
            while True:
                print("*** Tienda ***")
                print(" ")
                print(f"Dinero disponible: {parametros.ORO_INICIAL}") 
                print(" ")
                print("     Producto      Precio")
                print(f"[1] Gato Mago        {parametros.PRECIO_MAG}")
                print(f"[2] Gato Guerrero    {parametros.PRECIO_GUE}")
                print(f"[3] Gato Caballero   {parametros.PRECIO_CAB}")
                print(f"[4] Ítem Armadura     {parametros.PRECIO_ARMADURA}")
                print(f"[5] Ítem Pergamino    {parametros.PRECIO_PERGAMINO}")
                print(f"[6] Ítem Lanza        {parametros.PRECIO_LANZA}")
                print(f"[7] Curar Ejército    {parametros.PRECIO_CURA}")
                print(" ")
                print("[0] Volver al Menú de inicio")
                opcion_tienda = input("Indique su opción: ")
                if opcion_tienda in ["1", "2", "3"]:
                    if parametros.ORO_INICIAL >= parametros.PRECIO_MAG:
                        parametros.ORO_INICIAL -= parametros.PRECIO_MAG
                        if opcion_tienda == "1":
                            cualquier_gato = choice(ejercito_MAG)
                            clase_ejercito.agregar_combatiente(cualquier_gato)
                        elif opcion_tienda == "2":
                            cualquier_gato = choice(ejercito_GUE)
                            clase_ejercito.agregar_combatiente(cualquier_gato)
                        elif opcion_tienda == "3":   
                            cualquier_gato = choice(ejercito_CAB)
                            clase_ejercito.agregar_combatiente(cualquier_gato)
                        print("La compra ha sido un éxito")
                    elif parametros.ORO_INICIAL <= parametros.PRECIO_MAG:
                        print("No se puede realizar la compra porque no tiene suficiente dinero")
                elif opcion_tienda in["4", "5", "6"]:
                    if parametros.ORO_INICIAL >= parametros.PRECIO_ARMADURA:
                        print("*** Selecciona un gato ***")
                        print(" ")
                        print("       Clase          Nombre")
                        lista_opciones = []
                        if opcion_tienda == "4":
                            contador = 1
                            if len(clase_ejercito.ejercito) != 0:
                                for datos in clase_ejercito.ejercito:
                                    if datos[1] == "MAG":
                                        nombre = datos[0]
                                        print(f"[{contador}] Gato Mago        {nombre}")
                                        contador += 1
                                        lista_opciones.append(nombre)
                            if len(clase_ejercito.ejercito) != 0:
                                for datos in clase_ejercito.ejercito:
                                    if datos[1] == "GUE":
                                        nombre = datos[0]
                                        print(f"[{contador}] Gato Guerrero    {nombre}")
                                        lista_opciones.append(nombre)
                                        contador += 1
                        elif opcion_tienda == "5":
                            contador = 1
                            if len(clase_ejercito.ejercito) != 0:
                                for datos in clase_ejercito.ejercito:
                                    if datos[1] == "GUE":
                                        nombre = datos[0]
                                        print(f"[{contador}] Gato Guerrero    {nombre}")
                                        contador += 1
                                        lista_opciones.append(nombre)
                            if len(clase_ejercito.ejercito) != 0:
                                for datos in clase_ejercito.ejercito:
                                    if datos[1] == "CAB":
                                        nombre = datos[0]
                                        print(f"[{contador}] Gato Caballero   {nombre}")
                                        lista_opciones.append(nombre)
                                        contador += 1
                        elif opcion_tienda == "6":  
                            contador = 1
                            if len(clase_ejercito.ejercito) != 0:  
                                for datos in clase_ejercito.ejercito:
                                    if datos[1] == "MAG":
                                        nombre = datos[0]
                                        print(f"[{contador}] Gato Mago        {nombre}")
                                        contador += 1
                                        lista_opciones.append(nombre)
                            if len(clase_ejercito.ejercito) != 0: 
                                for datos in clase_ejercito.ejercito:
                                    if datos[1] == "CAB":
                                        nombre = datos[0]
                                        print(f"[{contador}] Gato Caballero   {nombre}")
                                        lista_opciones.append(nombre)
                                        contador += 1
                        print(" ")
                        opcion_gato = input("Indique su opción: ")
                        if opcion_tienda == "4":
                            for indice, nombre in enumerate(lista_opciones):
                                if opcion_gato == indice + 1:
                                    for antiguo in clase_ejercito.ejercito:
                                        if antiguo[1] == "MAG":
                                            antiguo[1] = "CAR"
                                        else:
                                            antiguo[1] = "PAL"
                        if opcion_tienda == "5":
                            for indice, nombre in enumerate(lista_opciones):
                                if opcion_gato == indice + 1:
                                    for antiguo in lista_unidades:
                                        if antiguo[1] == "MAG":
                                            antiguo[1] = "MDB"
                                        else:
                                            antiguo[1] = "CAR"
                        if opcion_tienda == "":
                            for indice, nombre in enumerate(lista_opciones):
                                if opcion_gato == indice + 1:
                                    for antiguo in lista_unidades:
                                        if antiguo[1] == "MAG":
                                            antiguo[1] = "MDB"
                                        else:
                                            antiguo[1] = "PAL"
                        parametros.ORO_INICIAL -= parametros.PRECIO_ARMADURA
                        if opcion_gato in lista_opciones:
                            print("La compra ha sido un éxito")
                        elif opcion_gato not in lista_opciones:
                                    print("Su opción ingresa es invalida")
                    elif parametros.ORO_INICIAL <= parametros.PRECIO_ARMADURA:
                        print("No se puede realizar la compra porque no tiene suficiente diero")
                elif opcion_tienda == "7":
                    if parametros.ORO_INICIAL >= parametros.PRECIO_CURA:
                        for per in lista_unidades:
                            instance = Combatiente(per[1], per[3], per[5], per[4], per[6], per[7])
                            m = instance.curarse(parametros.CURAR_VIDA)
                        parametros.ORO_INICIAL -= parametros.PRECIO_CURA
                        print("La compra ha sido un éxito")
                    elif parametros.ORO_INICIAL <= parametros.PRECIO_CURA:
                        print("No se puede realizar la compra porque no tiene suficiente dinero")
                elif opcion_tienda == "0":
                    break
                else: 
                    print("Ingresa una opción valida")
        elif opcion_inicio == "2":   #ejercito
            print(clase_ejercito)
        elif opcion_inicio == "3":   #combatir 
            pass
            #se deberá iniciar la simulación del combate (Podria se una clase)
            # if gana combate:
                # num_ronda+=1
                # if num_ronda >=4:
                    #terminan los duelos
            # elif pierde combate:
                # num_ronda = 1
        elif opcion_inicio == "0":
            print("El juego a concluido")
            print("Vuelve pronto!!")
            break
        else: 
            print("Ingresa una opción valida")
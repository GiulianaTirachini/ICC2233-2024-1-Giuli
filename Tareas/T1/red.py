import dcciudad, os 

class RedMetro:
    def __init__(self, red: list, estaciones: list) -> None:
        self.red = red
        self.estaciones = estaciones

    def informacion_red(self) -> list:
        lista_info_red = []
        cant_estaciones = len(self.estaciones)
        lista_info_red.append(cant_estaciones)
        lista_cant_estaciones = []
        cont_tuneles = 0
        for estacion in self.red:
            for tunel in estacion:
                if tunel == 1:
                    cont_tuneles+=1
            lista_cant_estaciones.append(cont_tuneles)
            cont_tuneles = 0
        lista_info_red.append(lista_cant_estaciones)
        return lista_info_red

    def agregar_tunel(self, inicio: str, destino: str) -> int:
        indice_inicio = 0
        indice_destino = 0
        for indice, estacion in enumerate(self.estaciones):
            if estacion == inicio:
                indice_inicio = indice
            if estacion == destino:
                indice_destino = indice
        for indice_de_red, estacion_de_red  in enumerate(self.red):
            if indice_de_red == indice_inicio:
                if estacion_de_red[indice_destino] == 0:
                    estacion_de_red[indice_destino] = 1
                    cant_tuneles = 0
                    for tunel in estacion_de_red:
                        if tunel == 1:
                            cant_tuneles += 1
                    return cant_tuneles
                elif estacion_de_red[indice_destino] == 1:
                    return -1

    def tapar_tunel(self, inicio: str, destino: str) -> int:
        indice_inicio = 0
        indice_destino = 0
        for indice, estacion in enumerate(self.estaciones):
            if estacion == inicio:
                indice_inicio = indice
            if estacion == destino:
                indice_destino = indice
        for indice_de_red, estacion_de_red  in enumerate(self.red):
            if indice_de_red == indice_inicio:
                if estacion_de_red[indice_destino] == 1:
                    estacion_de_red[indice_destino] = 0
                    cant_tuneles = 0
                    for tunel in estacion_de_red:
                        if tunel == 1:
                            cant_tuneles += 1
                    return cant_tuneles
                elif estacion_de_red[indice_destino] == 0:
                    return -1

    def invertir_tunel(self, estacion_1: str, estacion_2: str) -> bool:
        indice_e1 = self.estaciones.index(estacion_1)
        indice_e2 = self.estaciones.index(estacion_2)
        if self.red[indice_e1][indice_e2]==1 and self.red[indice_e2][indice_e1]==1:
            return True
        elif self.red[indice_e1][indice_e2]==1 and self.red[indice_e2][indice_e1]==0:
            self.red[indice_e1][indice_e2]=0 
            self.red[indice_e2][indice_e1]=1
            return True
        elif self.red[indice_e1][indice_e2]==0 and self.red[indice_e2][indice_e1]==1:
            self.red[indice_e1][indice_e2]=1 
            self.red[indice_e2][indice_e1]=0
            return True
        else:
            return False

    def nivel_conexiones(self, inicio: str, destino: str) -> str:
        indice_inicio = self.estaciones.index(inicio)
        indice_destino = self.estaciones.index(destino)
        estaciones_intermedias = 0
        estaciones = [indice_inicio]
        estacion_actual = indice_inicio
        ruta = dcciudad.alcanzable(self.red, indice_inicio, indice_destino)
        if ruta == False:
            return "no hay ruta"
        else:
            if self.red[indice_inicio][indice_destino] == 1:
               return "túnel directo"
            else:
                for i in range(2):
                    for indice, tuneles in enumerate(self.red[estacion_actual]):
                        if tuneles == 1 and indice != estacion_actual:
                            estaciones_intermedias += 1
                            estaciones.append(indice)
                            estacion_actual = indice
                if indice_destino in estaciones:
                    return "estación intermedia"
                else:
                    return "muy lejos"
    def rutas_posibles(self, inicio: str, destino: str, p_intermedias: int) -> int:
        indice_inicio = self.estaciones.index(inicio)
        indice_destino = self.estaciones.index(destino)
        estaciones_intermedias = 0
        estaciones = [indice_inicio]
        estacion_actual = indice_inicio
        for i in range(p_intermedias):
            for indice, tuneles in enumerate(self.red[estacion_actual]):
                if tuneles == 1 and indice != estacion_actual:
                    estaciones_intermedias += 1
                    estaciones.append(indice)
                    estacion_actual = indice
                    break
        if indice_destino in estaciones:
            return estaciones_intermedias
        else:
            return 0

    def ciclo_mas_corto(self, estacion: str) -> int:
        pass

    def estaciones_intermedias(self, inicio: str, destino: str) -> list:
        indice_inicio = self.estaciones.index(inicio)
        indice_destino = self.estaciones.index(destino)
        estaciones_intermedias = []
        for indice, tuneles in enumerate(self.red[indice_inicio]):
            if tuneles == 1 and self.red[indice][indice_destino] == 1:
                estaciones_intermedias.append(self.estaciones[indice])
        return estaciones_intermedias
            
    def estaciones_intermedias_avanzado(self, inicio: str, destino: str) -> list:
        indice_inicio = self.estaciones.index(inicio)
        indice_destino = self.estaciones.index(destino)
        estaciones_intermedias_avanzadas = []
        for indice, tuneles in enumerate(self.red[indice_inicio]):
            if tuneles == 1:
                for indice_intermedio, tuneles_intermedio in enumerate(self.red[indice]):
                    if indice_intermedio != indice_inicio and indice_intermedio != indice_destino:
                        if tuneles_intermedio == 1 and self.red[indice_intermedio][indice_destino] == 1:
                            estaciones_intermedias_avanzadas.append(self.estaciones[indice])
                            estaciones_intermedias_avanzadas.append(self.estaciones[indice_intermedio])
        if len(estaciones_intermedias_avanzadas) > 2:
            estaciones_avanzadas = []
            for i in range(0, len(estaciones_intermedias_avanzadas), 2):
                estaciones_avanzadas.append(estaciones_intermedias_avanzadas[i:i+2])
            return estaciones_avanzadas
        elif estaciones_intermedias_avanzadas == []:
            return []
        return [estaciones_intermedias_avanzadas]
            
    def cambiar_planos(self, nombre_archivo: str) -> bool:
        ruta = "data/" + nombre_archivo
        if os.path.isfile(ruta) == False:
            return False
        else:
            with open (ruta, "r") as archivo:
                lineas = archivo.readlines()
                lista_archivo = []
                for linea in lineas:
                    lista = linea.strip().split(",")
                    lista_archivo.append(lista)
            lista_nombres = []                               
            for i in lista_archivo[1:len(lista_archivo)-1]:
                lista_nombres.append(i[0])
            self.estaciones = lista_nombres      #aqui se cambia el antiguo self.estaciones por el nuevo
            lista_numeros = [] 
            cantidad = int(lista_archivo[0][0])
            for i in range(0, len(lista_archivo[-1]), cantidad):
                lista_numeros.append(lista_archivo[-1][i: i+cantidad])
            lista_final_numeros = []
            for i in lista_numeros:
                sublista = []
                for j in i:
                    sublista.append(int(j))
                lista_final_numeros.append(sublista)
            self.red = lista_final_numeros      #aqui se cambia en antguo self.red por el nuevo
            return True 

    def asegurar_ruta(self, inicio: str, destino: str, p_intermedias: int) -> list:
        pass 
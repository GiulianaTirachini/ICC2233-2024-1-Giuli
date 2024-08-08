from typing import Generator, Dict, List
import os 
from utilidades import (Animales, Candidatos, Distritos, Locales, Ponderador, Votos)
from itertools import combinations, tee, product
from collections import Counter
from functools import reduce

# ----------------------------------------------------------------------
# COMPLETAR
# ----------------------------------------------------------------------

# CARGA DE DATOS

def cargar_datos(tipo_generator: str, tamano: str) -> Generator:
    ruta = os.path.join('data', tamano, f'{tipo_generator}.csv')
    with open(ruta, 'r', encoding='latin-1') as archivo:
        next(archivo)
        for lineas in archivo:
            l = lineas.strip().split(",")
            if tipo_generator == "animales":
                yield Animales(int(l[0]), l[1], l[2], int(l[3]), float(l[4]), int(l[5]), l[6])
            elif tipo_generator == "candidatos":
               yield Candidatos(int(l[0]), l[1], int(l[2]), l[3])
            elif tipo_generator == "distritos":
                yield Distritos(int(l[0]), l[1], int(l[2]), l[3], l[4])
            elif tipo_generator == "locales":
                lista_locales = []
                lista_locales = lineas[lineas.find("[") + 1 : lineas.find("]")].split(", ") # find() indica el indice, +1 para quitarle "[]"
                nueva_lista_locales = []
                for x in lista_locales:
                    if x.strip().isdigit(): # strip() quita los espacios, isdigit() si todos son digitos
                        nueva_lista_locales.append(int(x))
                lista_locales = nueva_lista_locales
                yield Locales(int(l[0]), l[1], int(l[2]), lista_locales)
            elif tipo_generator == "ponderadores":
                yield Ponderador(l[0], float(l[1]))
            elif tipo_generator == "votos":
                yield Votos(int(l[0]), int(l[1]), int(l[2]), int(l[3]))

# 1 GENERADOR

def animales_segun_edad(generador_animales: Generator,
    comparador: str, edad: int) -> Generator: #comparador: "<", ">" o "="
    if comparador == "<":
        animal_filtrado = filter(lambda i: i.edad < edad, generador_animales)
    elif comparador == ">":
        animal_filtrado = filter(lambda i: i.edad > edad, generador_animales)
    elif comparador == "=":
        animal_filtrado = filter(lambda i: i.edad == edad, generador_animales)
    return (animal.nombre for animal in animal_filtrado)

def animales_que_votaron_por(generador_votos: Generator,
    id_candidato: int) -> Generator:    
    votos = filter(lambda i: i.id_candidato == id_candidato, generador_votos)
    return (voto.id_animal_votante for voto in votos)

def cantidad_votos_candidato(generador_votos: Generator,
    id_candidato: int) -> int:
    votos = filter(lambda i: i.id_candidato == id_candidato, generador_votos)
    return sum(1 for _ in votos)

def ciudades_distritos(generador_distritos: Generator) -> Generator:
    provincias = set()
    for distrito in generador_distritos:
        if distrito.provincia not in provincias:
            provincias.add(distrito.provincia)
            yield distrito.provincia

def especies_postulantes(generador_candidatos: Generator,
    postulantes: int) ->Generator:
    especies = set()
    candidatos = {}
    for candidato in generador_candidatos:
        especie = candidato.especie
        if especie in candidatos:
            candidatos[especie] += 1
        else:
            candidatos[especie] = 1
    for especie, num_candidatos in candidatos.items(): # items() lista que contiene key y value
        if num_candidatos >= postulantes:
            especies.add(especie)
    for especie in especies:
        yield especie

def pares_candidatos(generador_candidatos: Generator) -> Generator:
    for candidato1, candidato2 in combinations(generador_candidatos, 2): # combinaciones posibles
        yield (candidato1.nombre, candidato2.nombre)

def votos_alcalde_en_local(generador_votos: Generator, candidato: int,
    local: int) -> Generator:
    return filter(lambda v: v.id_local == local and v.id_candidato == candidato, generador_votos)

def locales_mas_votos_comuna (generador_locales: Generator,
    cantidad_minima_votantes: int, id_comuna: int) -> Generator:
    min_votantes = cantidad_minima_votantes
    labmda_f = lambda l: len(l.id_votantes) >= min_votantes and l.id_comuna == id_comuna
    locales_filtrados = filter(labmda_f, generador_locales)
    return (local.id_local for local in locales_filtrados) 

def votos_candidato_mas_votado(generador_votos: Generator) -> Generator:
    generador_votos, generador_votos_copia = tee(generador_votos) # copia del generador
    conteo_votos = Counter(voto.id_candidato for voto in generador_votos)  # cuenta los votos
    max_votos = max(conteo_votos.values())  # values() devuelve una lista
    mas_votados = [candi_id for candi_id, votos in conteo_votos.items() if votos == max_votos]
    mas_votado = max(mas_votados)
    for voto in generador_votos_copia:
        if voto.id_candidato == mas_votado:
            yield voto.id_voto
    
# 2 GENERADORES

def animales_segun_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator, comparador: str,
    edad: int) -> Generator:
    lista_animales = list(generador_animales) # transformar a lista para poder iterar mas de una vez
    lista_ponderadores = list(generador_ponderadores)
    generadores = product(lista_animales, lista_ponderadores) 
    if comparador == "<":
        l = lambda i: i[0].especie == i[1].especie and i[0].edad * i[1].ponderador < edad
    elif comparador == ">":
        l = lambda i: i[0].especie == i[1].especie and i[0].edad * i[1].ponderador > edad
    elif comparador == "=":
        l = lambda i: i[0].especie == i[1].especie and i[0].edad * i[1].ponderador == edad
    animal_filtrado = filter(l, generadores)
    for animal in animal_filtrado:
        yield animal[0].nombre

def animal_mas_viejo_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator) -> Generator:
    ponderadores = {p.especie: p.ponderador for p in generador_ponderadores}
    min_edad_humana = 0
    animales_mas_viejos = []
    for animal in generador_animales:
        ponderador = ponderadores.get(animal.especie, 1) 
        edad_humana = animal.edad * ponderador
        if edad_humana > min_edad_humana:
            min_edad_humana = edad_humana
            animales_mas_viejos = [animal.nombre]
        elif edad_humana == min_edad_humana:
            animales_mas_viejos.append(animal.nombre)
    for nombre in animales_mas_viejos:
        yield nombre

def votos_por_especie(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    generadores = product(generador_candidatos, generador_votos)
    votos = filter(lambda i: i[0].id_candidato == i[1].id_candidato, generadores)
    conteo_votos: Dict[str, int] = {}
    for candidato, voto in votos:
        especie = candidato.especie
        conteo_votos[especie] = conteo_votos.get(especie, 0) + 1
    for especie, numero_votos in conteo_votos.items():
        yield (especie, numero_votos)
        

def hallar_region(generador_distritos: Generator,
    generador_locales: Generator, id_animal: int) -> str:
    id_comuna = next(local.id_comuna for local in generador_locales if id_animal in local.id_votantes)
    region = next(distrito.region for distrito in generador_distritos if distrito.id_comuna == id_comuna)
    return region

def max_locales_distrito(generador_distritos: Generator,
    generador_locales: Generator) -> Generator:  
    """
    conteo_l_x_d = {} # locales por distrito
    for distrito, local in zip(generador_distritos, generador_locales):
        nombre_distrito = distrito.nombre
        conteo_l_x_d[nombre_distrito] = conteo_l_x_d.get(nombre_distrito, 0) + 1
    max_locales = max(conteo_l_x_d.values(), default=0)
    for nombre_distrito, cantidad in conteo_l_x_d.items():
        if cantidad == max_locales:
            yield nombre_distrito
            """
    
    conteo_locales = {}

    # Contar la cantidad de locales por distrito
    for local in generador_locales:
        distrito = next((dist for dist in generador_distritos if dist.id_distrito == local.id_comuna), None)
        if distrito:
            nombre_distrito = distrito.nombre
            conteo_locales[nombre_distrito] = conteo_locales.get(nombre_distrito, 0) + 1

    # Verificar si la lista de conteo de locales está vacía
    if not conteo_locales:
        return

    # Encontrar el máximo número de locales
    max_locales = max(conteo_locales.values())

    # Generar el resultado con los distritos que tienen el máximo número de locales
    for distrito, locales in conteo_locales.items():
        if locales == max_locales:
            yield distrito

def votaron_por_si_mismos(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    id_de_candi = {candidato.id_candidato: candidato.nombre for candidato in generador_candidatos}
    for voto in generador_votos:
        if voto.id_animal_votante in id_de_candi and voto.id_animal_votante == voto.id_candidato:
            yield id_de_candi[voto.id_animal_votante]

def ganadores_por_distrito(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    candidatos_x_distrito: Dict[int, List[Candidatos]] = {}
    for candidato in generador_candidatos:
        if candidato.id_distrito_postulacion not in candidatos_x_distrito:
            candidatos_x_distrito[candidato.id_distrito_postulacion] = []
        candidatos_x_distrito[candidato.id_distrito_postulacion].append(candidato)
    votos_x_candidato: Dict[int, int] = {}
    for voto in generador_votos:
        if voto.id_candidato not in votos_x_candidato:
            votos_x_candidato[voto.id_candidato] = 0
        votos_x_candidato[voto.id_candidato] += 1
    ganadores = []
    for distrito, candidatos in candidatos_x_distrito.items():
        if len(candidatos) > 1:
            for i in range(len(candidatos)):
                for j in range(i + 1, len(candidatos)):
                    candidato_1 = candidatos[i]
                    candidato_2 = candidatos[j]
                    votos1 = votos_x_candidato.get(candidato_1.id_candidato, 0)
                    votos2 = votos_x_candidato.get(candidato_2.id_candidato, 0)
                    if votos1 > votos2:
                        ganadores.append(candidato_1.nombre)
                    elif votos2 > votos1:
                        ganadores.append(candidato_2.nombre)
                    else:
                        ganadores.append(candidato_1.nombre)
                        ganadores.append(candidato_2.nombre)
    for ganador in ganadores:
        yield ganador
        

# 3 o MAS GENERADORES

def mismo_mes_candidato(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator,
    id_candidato: str) -> Generator:
    generador_animales, generador_animales_copia = tee(generador_animales)
    id_animales_votantes = set()
    for voto in generador_votos:
        if voto.id_candidato == id_candidato:
            id_animales_votantes.add(voto.id_animal_votante)
    for candi in generador_animales:
        if candi.id == id_candidato:
            ano_naci_candidato, mes_naci_candidato = map(int, candi.fecha_nacimiento.split('/'))
    for animal in generador_animales_copia:
        if animal.id in id_animales_votantes:
            ano_naci_animal, mes_naci_animal = map(int, animal.fecha_nacimiento.split('/'))
            if (mes_naci_animal == mes_naci_candidato or ano_naci_animal == ano_naci_candidato):
                yield animal.id

def edad_promedio_humana_voto_comuna(generador_animales: Generator,
    generador_ponderadores: Generator, generador_votos: Generator,
    id_candidato: int, id_comuna:int ) -> float:
    pond = {p.especie: p.ponderador for p in generador_ponderadores} # ponderadores
    votos_x_id = filter(lambda v: v.id_candidato == id_candidato, generador_votos)
    animales_id_comuna = filter(lambda a: a.id_comuna == id_comuna, generador_animales)
    id_anim = {a.id: a for a in animales_id_comuna} #id de animales
    edades_humanos = map(
        lambda v: id_anim[v.id_animal_votante].edad * pond[id_anim[v.id_animal_votante].especie]
        if v.id_animal_votante in id_anim and id_anim[v.id_animal_votante].especie in pond
        else None, votos_x_id)
    acumulador = reduce(lambda acumulado, edad: (acumulado[0] + (edad if edad is not None else 0),
        acumulado[1] + (1 if edad is not None else 0)), edades_humanos, (0, 0))
    if acumulador[1] == 0:
        return 0
    promedio_edad_humana = acumulador[0] / acumulador[1]
    return promedio_edad_humana

def votos_interespecie(generador_animales: Generator,
    generador_votos: Generator, generador_candidatos: Generator,
    misma_especie: bool = False,) -> Generator:
    esp_candidatos = {candid.id_candidato: candid.especie for candid in generador_candidatos}
    ani_votantes = {animal.id: animal for animal in generador_animales}
    for v in generador_votos:
        if v.id_animal_votante in ani_votantes and v.id_candidato in esp_candidatos:
            if misma_especie:
                if ani_votantes[v.id_animal_votante].especie == esp_candidatos[v.id_candidato]:
                    yield ani_votantes[v.id_animal_votante]
            else:
                if ani_votantes[v.id_animal_votante].especie != esp_candidatos[v.id_candidato]:
                    yield ani_votantes[v.id_animal_votante]

def porcentaje_apoyo_especie(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator) -> Generator:
    especie_x_animal = {}
    votos_x_especie = {}
    votos_candidato_x_especie = {}
    for animal in generador_animales:
        especie_x_animal[animal.id] = animal.especie
        if animal.especie not in votos_x_especie:
            votos_x_especie[animal.especie] = 0
            votos_candidato_x_especie[animal.especie] = {}
    for voto in generador_votos:
        especie = especie_x_animal[voto.id_animal_votante]
        votos_x_especie[especie] += 1
        if voto.id_candidato not in votos_candidato_x_especie[especie]:
            votos_candidato_x_especie[especie][voto.id_candidato] = 0
        votos_candidato_x_especie[especie][voto.id_candidato] += 1
    for candidato in generador_candidatos:
        especie_candidato = candidato.especie
        id_candidato = candidato.id_candidato
        if especie_candidato in votos_x_especie:
            total_votos_especie = votos_x_especie[especie_candidato]
            votos_candidato = votos_candidato_x_especie[especie_candidato].get(id_candidato, 0)            
            if total_votos_especie > 0:
                porcentaje = (votos_candidato / total_votos_especie) * 100
            else:
                porcentaje = 0
        else:
            porcentaje = 0
        yield (id_candidato, int(porcentaje))

def votos_validos(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores) -> int:
    p = {ponderador.especie: ponderador.ponderador for ponderador in generador_ponderadores} #ponderadores
    a = {animal.id: animal for animal in generador_animales} #animales
    v_filtrados = filter(lambda v: a.get(v.id_animal_votante) is not None, generador_votos)
    x = lambda v: a[v.id_animal_votante].edad * p.get(a[v.id_animal_votante].especie, 1)
    votos_validos = filter(x >= 18, v_filtrados)
    total_votos_validos = sum(1 for _ in votos_validos)
    return total_votos_validos

def cantidad_votos_especie_entre_edades(generador_animales: Generator,
    generador_votos: Generator, generador_ponderador: Generator,
    especie: str, edad_minima: int, edad_maxima: int) -> str:
    ponderadores = {p.especie: p.ponderador for p in generador_ponderador}
    if especie not in ponderadores:
        return (f"Hubo 0 votos emitidos por animales entre {edad_minima} "
               f"y {edad_maxima} años de la especie {especie}.")
    ponderador_especie = ponderadores[especie]
    edad_animales = filter(lambda a: a.especie == especie and
                    edad_minima < a.edad * ponderador_especie < edad_maxima, generador_animales)
    id_animales = map(lambda a: a.id, edad_animales)
    id_filtrados = {id_animal for id_animal in id_animales}
    votos_validos = filter(lambda v: v.id_animal_votante in id_filtrados, generador_votos)
    cantidad_votos = reduce(lambda cantidad, _: cantidad + 1, votos_validos, 0)
    return (f"Hubo {cantidad_votos} votos emitidos por animales entre {edad_minima} "
            f"y {edad_maxima} años de la especie {especie}.")

def distrito_mas_votos_especie_bisiesto(generador_animales: Generator,
    generador_votos: Generator, generador_distritos: Generator,
    especie: str) -> str:
    a_x_especie = filter(lambda e: e.especie == especie, generador_animales)
    a_bisiestos = filter(lambda e: (int(e.fecha_nacimiento.split('/')[0]) % 4 == 0 and
        int(e.fecha_nacimiento.split('/')[0]) % 100 != 0) or 
        (int(e.fecha_nacimiento.split('/')[0]) % 400 == 0), a_x_especie)
    id_anim = {animal.id: animal for animal in a_bisiestos} # id de animales
    comu_distri = {d.id_comuna: d.id_distrito for d in generador_distritos} # comunidad_distrito
    votos_x_distrito = reduce(lambda vs, v: # votos, voto
        (vs.update({comu_distri[id_anim[v.id_animal_votante].id_comuna]:
        vs.get(comu_distri[id_anim[v.id_animal_votante].id_comuna], 0) + 1}) or vs) # update : agregar elementos de un diccionario a otro
        if v.id_animal_votante in id_anim and id_anim[v.id_animal_votante].id_comuna in comu_distri
        else vs, generador_votos, {})
    if votos_x_distrito:
        nombre_distrito = max(votos_x_distrito, key=lambda d: (votos_x_distrito[d], -d)) # distrito
    else:
        nombre_distrito = min(comu_distri.values(), default=0)
    return (f"El distrito {nombre_distrito} fue el que tuvo más votos emitidos por "
            f"animales de la especie {especie} nacidos en año bisiesto.")

def votos_validos_local(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator,
    id_local: int) -> Generator:
    p = {ponderador.especie: ponderador.ponderador for ponderador in generador_ponderadores} # ponderadores
    a = {animal.id: animal for animal in generador_animales} # animales
    votos_local = filter(lambda voto: voto.id_local == id_local, generador_votos)
    votos_validos = filter(lambda v: a.get(v.id_animal_votante) is not None and 
        a[v.id_animal_votante].edad * p.get(a[v.id_animal_votante].especie, 1) >= 18, votos_local)
    for voto in votos_validos:
        yield voto.id_voto

def votantes_validos_por_distritos(generador_animales: Generator,
    generador_distritos: Generator, generador_locales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator) -> Generator:
    animales = {animal.id: animal for animal in generador_animales}
    ponderadores = {p.especie: p.ponderador for p in generador_ponderadores}
    comunas_a_distritos = {}
    for distrito in generador_distritos:
        if distrito.id_comuna not in comunas_a_distritos:
            comunas_a_distritos[distrito.id_comuna] = distrito.id_distrito
    locales = {local.id_local: local for local in generador_locales}
    votos_x_distrito = {}
    for voto in generador_votos:
        animal = animales.get(voto.id_animal_votante)
        if animal and animal.edad * ponderadores.get(animal.especie, 1) >= 18:
            local = locales.get(voto.id_local)
            if local:
                distrito = comunas_a_distritos.get(local.id_comuna)
                if distrito:
                    if distrito not in votos_x_distrito:
                        votos_x_distrito[distrito] = 0
                    votos_x_distrito[distrito] += 1
    max_votos = max(votos_x_distrito.values(), default=0)
    distrito_max_votos = min((distrito for distrito, votos in votos_x_distrito.items()
                              if votos == max_votos), default=None)
    if distrito_max_votos is not None:
        for animal in animales.values():
            if comunas_a_distritos.get(animal.id_comuna) == distrito_max_votos:
                yield animal
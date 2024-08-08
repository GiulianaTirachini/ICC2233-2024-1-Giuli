# Tarea 3: DCCerver

### Funciones implementadas y no implementadas:✅❌

Parte 1 - Carga de Datos:
- ✅ carga_datos
  
Parte 2 - Consultas que reciben un generador:
- ✅ animales_segun_edad
- ✅ animales_que votaron_por
- ✅ cantidad_votos_candidato
- ✅ ciudades_distritos
- ✅ especies_postulantes
- ✅ votos_alcalde_en_local
- ✅ votos_candidato_mas_votado

parte 3 - Consultas que reciben dos generador:
- ✅ animales_segun_edad_humana
- ✅ animal_mas_viejo_edad_humana
- 🟠 votos_por_especie (no pasa la mitad de los tests poblicos)
- ✅ hallar_region
- 🟠 max_locales_distrito (no pasa un test de los publicos)
- ✅ votaron_por_si_mismos
- ✅ ganadores_por_distrito 

parte 4 - Consultas que reciben tres o más generador:

- ✅ mismo_mes_candidato
- ✅ edad_promedio_humana_voto_comuna
- ✅ votos_interespecie
- ✅ porcentaje_apoyo_especie
- ✅ votos_validos
- ✅ cantidad_votos_especie_entre_edades
- ✅ distrito_mas_votos_especie_bisiesto
- ✅ votos_validos_local
- 🟠 votantes_validos_por_distritos (solo pasan tres de los tests piblicos)

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```typing```: ```Generator, Dict, List```
2. ```os```: ```path / join()```
3. ```intertools```: ```combinations, tee, product``` 
4. ```functools```: ```reduce```
5. ```collection```: ```Counter```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```utilidades.py```: Contiene a ```Animales, Candidatos, Distritos, Locales, Ponderador, Votos```
  
### Referencias :book:
Para realizar mi tarea saqué código de:
1. \< https://www.w3schools.com/python/ref_string_find.asp >: Este lo use para comprender que el método find() encuentra la primera aparición del valor especificado y está implementado en el archivo <cunsultas.py> en la línea < 28 > y hace < "indica el indice de "[" y de "]" >
2. \< https://www.w3schools.com/python/ref_string_isdigit.asp >: Este lo use para comprender si todos los caracteres del texto son dígitos, mediante el método isdigit() y está implementado en el archivo <cunsultas.py> en la línea < 31 > y hace < "comprueba si todos los caracteres de un texto son digitos o no, mediante True o False." >
3. \< https://www.w3schools.com/python/ref_dictionary_items.asp >: Este lo use para entender como obtener el valor y/o clave de algun diccionario, mediante el método items() y está implementado en el archivo <consultas.py> en las líneas < 79, 104, 152, 169, 193, 375 > y hace < "devuelve los pares clave-valor del diccionario usado." >
4. \< https://www.geeksforgeeks.org/itertools-combinations-module-python-print-possible-combinations/ >: Este lo use para comprender como se puede buscar las diferentes combinaciones entre distintos atributos, mediante el método combinations() y está implementado en el archivo <consultas.py> en las líneas < 86 > y hace < "devuelve tuplas de ordenadas sin elementos repetidos en una matríz." >
5. \< https://docs.python.org/es/dev/library/itertools.html >: Este lo use para comprender como hacer n iteradores independientes de un mismo iterador, mediante en método tee() y está implementado en el archivo <consultas.py> en las líneas < 101, 217 > y hace < "crea dos iteradores a partir de uno original (hace como una especie de copia)." >
6. \< https://python-para-impacientes.blogspot.com/2015/04/counter-el-contador-de-python.html >: Este lo use para comprender que mediante el método Counter() se puedes contar las veces que aparece un valor en una secuencia de caracteres y está implementado en el archivo <consultas.py> en las líneas < 102 > y hace < "cuanta la cantidad total de los votos que hay." >
7. \< https://ellibrodepython.com/diccionarios-en-python#:~:text='%2C%20'b'%5D-,values(),values%20o%20valores%20del%20diccionario. >: Este lo use para comprender  que el método values() devuelve una lista con todos los valores de un diccionario y está implementado en el archivo <consultas.py> en las líneas < 103, 168, 337, 374, 378 > y hace < "en contrar los valores en los diccionarios pedidos." >
8. \< https://www.w3schools.com/python/ref_dictionary_get.asp >: Este lo use para comprender que el método get() devuelve el valor del elemento con la clave especificada y está implementado en el archivo <consultas.py> en las líneas < 134, 151, 167, 199, 200, 284, 297, 298, 331, 347, 348, 365, 366, 367, 369, 379 > y hace < "encuentra el valor pedido a partir de la clave." >
9.  \< https://www.w3schools.com/python/ref_dictionary_update.asp >: Este lo use para comprender que el método update() inserta los elementos especificados en un diccionario y está implementado en el archivo <consultas.py> en las líneas < 330 > y hace < "colóca el atributo pedido en el lugar pedido." >
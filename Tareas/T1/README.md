# Tarea 1: DCCiudad 🚈🐈

## Consideraciones generales :octocat:

- Archivo red.py:
  - Este programa realiza correctamente las funciones basicas, algunos casos de una función un poco más compleja y no realiza la función mas dificil.
  - En este archivo el usuario debe ejecutar el código en la carpeta "T1".
- Archivo main.py: 
  - En este archivo el usuario debe ejecutar el código en la carpeta "T1".

### Cosas implementadas y no implementadas :white_check_mark: :x:

Parte 1 - Funcionalidades : Consola
- ✅ informacion_red
- ✅ agregar_tunel
- ✅ tapar_tunel
- ✅ invertir_tunel
- ✅ nivel_conecciones
- ✅ rutal_posible
- ❌ ciclo_mas_corto
- ✅ estaciones_intermedias
- 🟠 estaciones_intermedias_avanzado (falta programar el caso de que pasaria si el metro va y viene más de una vez para logras las dos estaciones intermedias)
- ✅ cambiar_plano
- ❌ asegurar_ruta

Parte 2 - Menú : Menú de Acciones
- ✅ Menú (se indica correctamente si la red o estación indicadas por el usuario existe o no, y abre el menú de acciones perfectamente)
- ✅ Menú de Acciones:
  1. ✅ Mostrar red
  2. ✅ Encontrar ciclo más corto
  3. ✅ Asegurar ruta (si bien no realiza la función asociada, en la consola imprime "None", lo que significa que no exite ningún tipo de error)
  4. ✅ Salir del programa
   
✅ Modularizacion  
✅ PEP8

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```path / isfile() /  join() / exists()```
2. ```sys```: ```argv``` 

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```red.py```: Contiene a ```RedMetro```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Por favor no ulvide que al momento de escribir el nombre de la red el nombre del archivo se escrive sin la estención ".txt" (ejemplo: ✅ ciudad_T, ❌ciudad_T.txt)

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \< https://www.eumus.edu.uy/eme/ensenanza/electivas/python/2020/clase_08a.html#:~:text=La%20funci%C3%B3n%20sys.,elemento%20de%20la%20lista%20(%20sys.) , https://docs.python.org/es/3/library/sys.html >: Este lo use para comprender como usar el sys.argv y está implementado en el archivo <main.py> en las líneas < 14, 18, 19, 35, 51, 63, 69 > y hace < "provee acceso a algunas variables usadas o mantenidas por el intérprete y a funciones que interactúan fuertemente con el intérprete." >
2. \< https://docs.python.org/3/library/os.path.html >: Este lo use para comprender como usar os.path.exists() implementado en el archivo <main.py> en la linea < 22 > y hace < retorna un booleano indicando si la ruta existe o no >, os.path.isfile() implementado en el archivo <red.py> en la linea < 154 > y hace < retorna un booleano indicando si la ruta existe o no >, os.path.join()  implementado en el archivo <main.py> en la linea < 21 > y hace < Combina partes de una ruta en una sola ruta >
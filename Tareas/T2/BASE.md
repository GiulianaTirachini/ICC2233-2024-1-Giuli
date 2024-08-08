# Tarea 2: DCCombatientes 🐈⚔️


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Programación Orientada a Objetos: 12 pts (10%)
##### 🟠 Definición de clases, herencia y *properties* (no se si se incluyó la property correctamente)

#### Preparación del programa: 10 pts (8%)
##### ✅ Inicio de la partida
- ✅ ejecito
- ✅ dinero
- ✅ dificuldad
- ✅ mensaje

#### Entidades: 56 pts (47%)
##### 🟠 Ejército (no todas las funciones estan completas)
##### 🟠 Combatientes (no todas las funciones estan completas)
##### ❌ Ítems

#### Flujo del programa: 30 pts (25%)
##### ✅ Menú de Inicio
##### ✅ Menú Tienda
##### ✅ Selección de gato 
##### ✅ Fin del Juego
##### ✅ Robustez

#### Archivos: 12 pts (10%)
##### ✅ Archivos .txt
##### ✅ parametros.py


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```parametros.py``` en ```/T2```
2. ```facil.txt``` en ```data/```
3. ```intermedio.txt``` en ```data/```
4. ```dificil.txt``` en ```data/```
5. ```unidades.txt``` en ```data/```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```randint / choice```
2. ```abc```: ```abstractmethod / ABC``` 
3. ```os```: ```path```
4. ```sys```: ```exit / argv``` 

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```librería_1```: Contiene a ```ClaseA```, ```ClaseB```, (ser general, tampoco es necesario especificar cada una)...
2. ```librería_2```: Hecha para <insertar descripción **breve** de lo que hace o qué contiene>
3. ...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. La tarea está excesivamente comentada por el simple hecho de no querer perder el hilo del programa: como las funciones, los combates, el flujo del menú, entre otras cosas, no porque se haya realizado con Chat GPT.
2. Los archivos "facil.txt", "intermedio.txt" y "dificil.txt" deben estar si o si dentro de la carpeta data.
3. <Descripción/consideración 2 y justificación del por qué es válido/a>
4. ...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).
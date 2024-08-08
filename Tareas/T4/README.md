# Tarea 3: DCCome Lechuga 🐢🍉🥬


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

#### Entidades: 18.5 pts (21%)
##### 🟠 Pepa (la tortuga no hace el click para comer la lechuga, ni para hacer poop)
##### 🟠 Sandías (Esta implementado, pero no funciona correctamente)

#### Interfaz gráfica: 27 pts (30%)
##### ✅ Ventana Inicio
##### ✅ Ventana Juego (eso si, la comprobación del puzzle no la hace el networing, si no que la hace el mismo fronted)
##### ✅ Fin del *puzzle*

#### Interacción: 13 pts (14%)
##### ❌ *Cheatcodes*
##### 🟠 Sonidos (falta implementar obtener_sandia.wav)

#### *Networking*: 20.5 pts (23%)
##### 🟠 Arquitectura (existe la separación funcional entre servidor y cliente, pero la la conección entre ambos no funciona del todo)
##### ❌ *Networking*
##### ❌ Codificación y decodifición 

#### Archivos: 11 pts (12%)
##### 🟠 *sprites* (falta implementar sandia.png)
##### ✅ *puzzle*
##### 🟠 JSON (Estan implementados, pero no funcionan correctamente)
##### ✅ parámetros.py


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` de la carpeta cliente. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```parametros.py``` en ```cliente/```
2. ```backend.py``` en ```backend/```
3. ```frontend.py``` en ```frontend/```
4. ```cliente.py``` en ```cliente/```
5. ```cliente.json``` en ```cliente/```
6. ```servidor.py``` en ```servidor/```
7. ```servidor.json``` en ```servidor/```
8. ```puntaje.txt``` en ```/T4```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt6.QtWidgets```: ```QApplication / instance()```, ```QVBoxLayout```, ```QPushButton```, ```QWidget```, ```QLabel()```, ```QLineEdit()```, ```QComboBox()```, ```QListWidget()```, ```QScrollArea()```, ```QMessageBox / warning() / information()```, ```argv```, ```QHBoxLayout()```, ```QStackedLayout()```, ```QGridLayout()```
2. ```PyQt6.QtGui```:  ```QPixmap()```, ```QKeyEvent```, ```QIcon```
3. ```PyQt6.QtCore```: ```QTimer()```, ```QObject```, ```pyqtSignal()```, ```QRandomGenerator / global_() / bounded()```, ```Qt / Key```, ```QUrl / fromLocalFile()```, ```QMutex()```
4. ```PyQt6.QtMultimedia```: ```QMediaPlayer / setAudioOutput() / setSource() / play() / setPosition()```, ```QAudioOutput() / setVolume()```, ```QSoundEffect() / setSource() / play()```
5. ```sys```: ```exit()```, ```argv```
6. ```os```: ```path / join() / listdir() / isfile()``` 
7. ```socket```: ```socket()```
8. ```threading```: ```Thread()```
9. ```json```: ```dumps() / loads() / load()```
10. ```struct```: ```pack() / unpack()```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```puzzle.py```: Contiene a ```TableroJuego```, ```Puzzle```.
2. ```leer_archivos.py```: Contiene a ```leer_base_puzzle```, ```dimencion_tablero```, ```leer_solucion_puzzle```.
   

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En terminos generales el juego funciona a la perfección:
   a. Verifica el resultado del puzzle, solo que no lo hace mediante la comunicación con el servidor, el cliente lo hace por si mismo.
   b. La tortuga pepa fue implementada, se mueve mediante las teclas a, w, s, d, pero no puede comer las lechugas ni hacer poop, estas accionces solo se pueden realizar mediante la flechas normales del teclado y el click.
   c. La funciòn de la sandia no funciona.
   d. Todos los botones del juego funcionan.


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

##listdir => investigar

1. \<https://www.pythonguis.com/tutorials/pyqt6-widgets/ , https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html>: este hace \<me explican todo acerca de los metodos de PyQt6.QtWidgets> y está implementado en el archivo <puzzle.py> en las líneas <9, 18, 66, 72, 85, 91, 95>, está implementado en el archivo <main.py> en la línea <7>, está implementado en el archivo <frontend.py> en las líneas <13, 26, 33, 34, 36, 37, 40, 41, 42, 47, 50, 53, 114, 144, 159, 161, 162, 167, 188, 208, 240, 241, 242, 244, 245, 250, 252, 276, 292, 298> y hace <Me ayudan a poder crear la interfaz y las ventanas de la forma en la que están, como los botones, las imagenes, entre otros.>
2. \<https://doc.qt.io/qtforpython-6.5/PySide6/QtGui/QKeyEvent.html , https://doc.qt.io/qt-6/qpixmap.html>: este hace \<me explican acerca de PyQt6.QtGui (QPixmap(), QIcon y KeyEvent)> y está implementado en el archivo <frontend.py> en las líneas <29, 169, 210>, y está implementado en el archivo <puzzle.py> en las líneas <26 - 41, 74, 75, 96, 110, 119, 120, 131, 132, 138> y hace <me ayudan a ver los pixeles de las imagenes y las teclas a usar en el teclado.>
3. \<https://doc.qt.io/qtforpython-6.6/PySide6/QtCore/index.html>: este hace \<me explican todo acerca de los metodos de PyQt6.QtCore> y está implementado en el archivo <puzzle.py> en las líneas <10, 11, 48, 52, 59, 61, 86, 92, 101, 125, 139, 141, 143, 145>,  y está implementado en el archivo <frontend.py> en las líneas <14, 15, 145, 146, 181, 217, 135, 197, 201, 219, 221, 223>,  y está implementado en el archivo <backend.py> en las líneas <6, 7, 20, 59, 60, 61, 66, 68, 75, 76, 84>,  y está implementado en el archivo <cliente.py> en las líneas <4, 5, 6> y hace <me ayudan a manejar las señales, los tiempo, entre otras cosas.> 
4. \<https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/index.html>: este hace \<PyQt6.QtMultimedia> y está implementado en el archivo <frontend.py> en las líneas <130, 131, 140, 195, 199>,  y está implementado en el archivo <puzzle.py> en las líneas <56, 57, 59, 61, 112, 123> y hace <me ayuda en la reprodución de los diferentes sonidos.>
5. \<https://docs.python.org/3/library/struct.html>: este hace \<convierte diferentes datos en bytes y viceversa> y está implementado en el archivo <cliente.py> en las líneas <54, 58,  66>,  y está implementado en el archivo <servidor.py> en las líneas <65, 69, 77> y hace <me ayudan a codificar y decodificar los diferentes mensaje,.> 


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).
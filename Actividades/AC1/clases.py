from abc import ABC, abstractmethod
import random


class Vehiculo(ABC):   #abstracta
    identificador = 0
    def __init__(self, rendimiento, marca, energia = 120, *args, **kwargs) -> None:
        self.rendimiento = rendimiento  #int
        self.marca = marca  #str
        self.energia = energia  #int - no baja de 0
        self.identificador = Vehiculo.identificador  #int
        Vehiculo.identificador += 1

    @abstractmethod
    def recorrer(self, kilometros) -> None:
        pass

    @property
    def autonomia(self) -> float:
        kilemetros_x_andar = self.energia * self.rendimiento
        return kilemetros_x_andar

    @property
    def energia(self) -> int:
        return self._energia
    @energia.setter
    def energia(self, energia) -> int:
        if energia < 0:
            self._energia = 0
        else:
            self._energia = energia


class AutoBencina(Vehiculo):
    def __init__(self, bencina_favorita, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bencina_favorita = bencina_favorita   #int

    def recorrer(self, kilometros) -> str:
        L = int(kilometros/self.rendimiento)
        autonomia = self.autonomia
        if autonomia >= kilometros:
            self.energia = self.energia - L
            return f"Anduve por {kilometros}Km y gaste {L}L de bencina"
        else:
            energia_gastada = self.energia
            self.energia = 0
            return f"Anduve por {autonomia}Km y gaste {energia_gastada}L de bencina"


class AutoElectrico(Vehiculo):
    def __init__(self, vida_util_bateria, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = vida_util_bateria  #int

    def recorrer(self, kilometros) -> str:
        L = int(kilometros/self.rendimiento)
        autonomia = self.autonomia
        if autonomia >= kilometros:
            self.energia = self.energia - L
            return f"Anduve por {kilometros}Km y gaste {L}W de energia electrica"
        else:
            energia_gastada = self.energia
            self.energia = 0
            return f"Anduve por {autonomia}Km y gaste {energia_gastada}W de energia electrica"


class Camioneta(AutoBencina):
    def __init__(self, capacidad_maleta, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.capacidad_maleta = capacidad_maleta  #int


class Telsa(AutoElectrico):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros) -> str:
        nuevo_recorrer = AutoElectrico.recorrer(self, kilometros)
        return nuevo_recorrer + " de forma inteligente"


class FaitHibrido(AutoBencina, AutoElectrico):  
    #vida útil de la batería de 5 años.
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(vida_util_bateria = 5, *args, **kwargs)

    def recorrer(self, kilometros) -> str:
        resultado = AutoElectrico.recorrer(self, kilometros/2) + " " + AutoBencina.recorrer(self, kilometros/2)
        return resultado

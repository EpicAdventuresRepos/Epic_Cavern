from epic_cavern.lexico import Comando
from epic_cavern.utilities import Eventos

#Asocia una dirección a un token de movimiento.
# N = 0, S = 1, etc.
movimiento = ("N", "S", "E", "O")
nombre_movimiento = ("Norte", "Sur", "Este", "Oeste")
movimiento_doble_sentido = (1, 0, 3, 2)


class Resultado:
    """
    """
    HECHO = "Éxito"
    NO_HECHO = "Fallo"
    REINICIA = "Reinicia"
    FIN_JUEGO = "Salir del juego"

###########################################

class Global:
    _instance = None

    @staticmethod
    def get_instance():
        """
        Devuelve la única instancia del Singleton.
        Si no existe, la crea.
        """
        if Global._instance is None:
            Global._instance = Global()
        return Global._instance

    def __init__(self):
        self.localizacion_actual = None
        self.inventario = {}
        # self._sve_dt = None - No sé qué hace
        self._output = None
        self._input = None
        self._locs = None
        self._events = Eventos()
        self._map = None

    def __str__(self):
        return f"Localización {self.localizacion_actual} / Inventario: {self.inventario}"

    def set_localizacion(self, localizacion_actual):
        """ Raises cambio_loc event igf there is an event manager. """
        self.localizacion_actual = localizacion_actual
        if self._events is not None:
            self._events.cambio_loc(localizacion_actual)

    def localizacion(self):
        return self.localizacion_actual

    def añade_inventario(self, token, objeto):
        self.inventario[token] = objeto

    def en_inventario(self, token):
        return token in self.inventario

    def saca_inventario(self, token):
        if not self.en_inventario(token):
            return None
        objeto = self.inventario[token]
        del self.inventario[token]
        return objeto

    def output(self):
        return self._output

    def input(self):
        return self._input

    def events_manager(self):
        return self._events

import unittest

from epic_cavern.datos import Global, ObjetoAventura, ObjetoGema
from epic_cavern.lexico import Comando
from epic_cavern.main import load_data


class LastLineOutput(object):

    def __init__(self):
        self._last_line = None

    def print(self, msg):
        self._last_line = msg

    def last_line(self):
        return self._last_line

#############

class AllLinesOutput(object):

    def __init__(self):
        self._lines = list()
        self._trace = False

    def print(self, msg):
        if self._trace:
            print(msg)
        self._lines.append(msg)

    def last_line(self, index =2):
        index *= -1
        return self._lines[index]

    def trace_on(self):
        self._trace = True

#############

class AutomaticInput(object):

    def __init__(self, trace=False):
        self._commands = None
        self._index = 0
        self._trace = trace

    def pulsa_intro(self):
        return

    def input(self, prompt=""):
        # print(self._commands)
        # print(self._index)
        command = self._commands[self._index]
        if self._trace:
            print(">> ", command)
        self._index += 1
        return command

    def set_commands(self, commands):
        self._commands = commands
        self._index = 0

    def trace_on(self):
        self._trace = True

####################################################

class BaseTest(unittest.TestCase):

    def setUp(self, loc_key = "loc3_Investigador"):
        Global._instance = None
        load_data()
        self.estado = Global.get_instance()
        self.test_output = LastLineOutput()
        self.estado._output = self.test_output
        self.estado.set_localizacion(self.estado._locs[loc_key])
        self.loc = self.estado._locs[loc_key]

    def comando(self, token_verbo, token_nombre):
        comando = Comando("no", "no", token_verbo, token_nombre)
        result = self.loc.run_command(comando)
        return self.test_output.last_line(), result

    def obj_idolo(self):
        return ObjetoAventura("IDOLO",
                               "Pequeña figura, toscamente tallada en piedra, que representa un ídolo.",
                              "IDOLO", "Un ídolo")
    def obj_vara(self):
        return ObjetoAventura("VARA", "Vara dorada. Frótala y emitirá luz durante un instante.", "VARA", "Una cara dorada")

    def obj_cuchillo(self):
        return ObjetoAventura("CUCHILLO", "descriopcion.", "CUCHILLO", "Una cuchillo")

    def obj_diapason(self):
        return ObjetoAventura("DIAPASON", "Un pequeño diapasón que emite un tono agudo si lo golpeas suavemente.", "DIAPASON", "Un diapasón")

    def obj_empanada(self):
        return ObjetoAventura("EMPANADA", "Aunque está recién horneada, no parece muy comestible.", "EMPANADA", "Una empanada")

    def add_rubi_inventario(self):
        obj = ObjetoGema("RUBI",
                           "Rubí rojo.",
                           "RUBI", "Un RUBI")
        self.estado.añade_inventario("RUBI", obj)
        return "RUBI", obj

    def add_inventario(self, objeto):
        self.estado.añade_inventario(objeto._token, objeto)

    def add_loc(self, objeto):
        self.loc.agregar_objeto(objeto._token, objeto)

    def _estoy_en(self):
        return self.estado.localizacion().nombre
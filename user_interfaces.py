from rich.panel import Panel


class ConsoleOutput(object):

    def print(self, msg):
        print(msg)

    # alguinas GUI les viene bien diferenciar.
    def print_salidas(self, msg):
        self.print(msg)

    def print_inventario(self, objetos):
        self.print("Llevas:")
        for objeto in objetos:
            self.print(objeto)

    def print_in_box(self, msg):
        self.print(msg)

    def start_two_columns(self, title):
        self.print(title)

    def row(self, column_1, column_2):
        self.print(column_1 + " - " + column_2)

    def end_two_columns(self):
        pass

    @staticmethod
    def _s_print(msg):
        print(msg)

##########################

class ConsoleInput(object):

        def pulsa_intro(self):
            ConsoleOutput._s_print("Pulsa Enter...")
            self.input()

        def input(self, prompt = ""):
            return input(prompt)

###########################

from rich.console import Console
from rich.table import Table
from rich import box

class ConsoleRichOutput(ConsoleOutput):

    def __init__(self):
        self.console = Console()
        # self.console.soft_wrap = True
        # print("Console size ", self.console.size)
        self._table = None

    def print(self, msg):
        self.console.print(msg)

    # alguinas GUI les viene bien diferenciar.
    def print_salidas(self, msg):
        self.console.print(msg)

    def print_inventario(self, objetos):
        self.start_two_columns("Objetos que llevas:")
        indice = 0
        while True and len(objetos) > 0:
            column_1 = objetos[indice]
            column_2 = ""
            indice += 1
            if indice < len(objetos):
                column_2 = objetos[indice]
            self.row(column_1, column_2)
            indice += 1
            if indice >= len(objetos):
                break
        self.end_two_columns()

    def print_in_box(self, msg):
        self.console.print(Panel(msg))

    def start_two_columns(self, title):
        self._table = Table( box=box.SIMPLE_HEAD)

        self._table.add_column(title)
        self._table.add_column("")

    def row(self, column_1, column_2):
        self._table.add_row(column_1, column_2)

    def end_two_columns(self):
        self.console.print(self._table)
        self._table = None
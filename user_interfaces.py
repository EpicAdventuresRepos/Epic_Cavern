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

    def print_map(self, map, current_loc):
        #table = Table(title="Automapa.")
        # self.print("")
        for row in map:
            linea_1 = str()
            linea_2 = str()
            for loc in row:
                if loc is not None and loc.is_discovered():
                    if loc == current_loc:
                        linea_1 += "X"
                    else:
                        linea_1 += "*"
                    if loc.has_east():
                        linea_1 += "--"
                    else:
                        linea_1 += "  "
                    if loc.has_south():
                        linea_2 += "|  "
                    else:
                        linea_2 += "   "
                else:
                    linea_1 += "   "
                    linea_2 += "   "
            if linea_1.strip() != "":
                self.print(linea_1)
            if linea_2.strip() != "":
                self.print(linea_2)

            #self.print("Automap no available in this interface.")


    def ready_to_save(self):
        pass

    def re_init(self):
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
        if self.console is None:
            self.console = Console()
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

    def ready_to_save(self):
        """
        Rich tiene clases que no son compatibles con pickle, así que hay que
        destruirlas antes de salvar.

        :return:
        """
        self.console = None
        self._table = None

    def re_init(self):
        self.console = Console()

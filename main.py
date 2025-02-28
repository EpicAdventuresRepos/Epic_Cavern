from epic_cavern.datos_aventura import load_data
from epic_cavern.datos import Resultado, Global
from epic_cavern.lexico import comando, crear_comando, AnaLex, vocabulario
from epic_cavern.user_interfaces import ConsoleOutput, ConsoleInput, ConsoleRichOutput

"""
el parser comprueba que la sgeunda palabra sea un nombre registrado, por eso no puedo usar save nombre_partida
ya que daría error.

"""


def load_interfaces():
    estado = Global.get_instance()
    #estado._output = ConsoleOutput()
    estado._output = ConsoleRichOutput()
    estado._input = ConsoleInput()


def mostrar_introducción(estado):
    estado.output().print("""Muchos han entrado en la caverna, pero muy pocos han salido. ¿Por qué iba a ser distinto contigo?
Estás a punto de descubrirlo.
Salir con vida ya es un éxito, pero para ti eso es poco. Encuentra las seis gemas ocultas en la caverna y serás rico y famoso durante el resto de tu vida. O muere intentándolo.
""")
    estado.input().pulsa_intro()
    # limpia la pantalla


def procesar_palabras(palabras, output):
    comando_jugador = crear_comando(palabras)
    es_valido = True

    # Ver si existen
    if comando_jugador.es_vacio():
        output.print("Verbo no encontrado.")
        es_valido = False

    if not comando_jugador.es_vacio() and comando_jugador.token_nombre is None:
        output.print("Nombre no encontrado.")
        es_valido = False

    return comando_jugador, es_valido


def notifica_reinicia(estado, loc_actual):
    eventos = estado.events_manager()
    eventos.reinicia(loc_actual)


def main_game():
    global output

    estado = Global.get_instance()
    output = estado.output()
    # print("main_game - output console", output.console)
    _input = estado.input()
    eventos = estado.events_manager()

    # print(estado._locs)
    # mostrar_introducción(estado)

    resultado = None
    while resultado != Resultado.FIN_JUEGO:
        resultado = None
        estado = Global.get_instance()
        loc_actual = estado.localizacion()
        #notifica_reinicia(estado, loc_actual)
        eventos.reinicia(loc_actual)

        output.print('\n'+loc_actual.mostrar_descripcion())
        output.print_salidas(loc_actual._mostrar_salidas())
        imprimir_objetos(loc_actual)

        while resultado != Resultado.REINICIA and resultado != Resultado.FIN_JUEGO:
            user_input = _input.input(">> ")

            # Hay GUIs que devuelven aquí un None si quieren terminar el juego
            if user_input is None:
                print("GUI insicates exit game.")
                resultado = Resultado.FIN_JUEGO
                break

            # aguien quiere porcesar la entrada
            if eventos.player_input_has_subs():
                eventos.player_input(user_input)
                # No se puede reiniciar ni terminar la partida
                # No cuenta para los eventos de contra los comandos.
                break

            # palabras = procesar_cadena(user_input)
            user_command, valido = procesar_palabras(user_input, output)
            # print(f"user_input: {user_input}, user_input {user_input}, user_command {user_command}, valido {valido}")
            if not valido:
                eventos.fin_comando(user_command)
                continue

            # Procesar comando en la loc en al que estoy
            loc_actual = estado.localizacion()
            resultado = loc_actual.run_command(user_command)
            if resultado != Resultado.NO_HECHO:
                eventos.fin_comando(user_command)
                continue

            # Procesar comando en los comandos por defecto.
            c_comunes = comandos_comunes()
            command_method = None
            if user_command.token_verbo in c_comunes:
                verbs = c_comunes[user_command.token_verbo]
                if user_command.token_nombre in verbs:
                    command_method = verbs[user_command.token_nombre]
                elif "*" in verbs:
                    command_method = verbs["*"]

            if command_method is not None:
                resultado = command_method(user_command)

            # Si no hay un HECHO es que no puedes hacerlo
            if resultado == Resultado.NO_HECHO or command_method is None:
                output.print("No puedes hacerlo.")
                resultado = Resultado.NO_HECHO

            eventos.fin_comando(user_command)

    # Fin del juego.
    # output.print("Bye.")


def imprimir_objetos(loc_actual):
    if loc_actual.hay_objetos_visibles():
        output.print("Aquí hay:")
        for obj in loc_actual.objetos.values():
            output.print(obj.breve_descripcion)


######

# Main screen

def mensaje_inicial(output):
    output.print(" Epic Caver v0.03 ")
    output.print("-------------------")
    output.print("Comandos de la pantalla de acceso:")
    output.print("")
    output.print("iniciar - comienza una nueva partida.")
    output.print("cargar  - carga una partida salvada.")
    output.print("ayuda   - cómo jugar y comandos principales.")
    output.print("salir   - cierra el juego.")
    output.print("")
    output.print("Escribe tu comando:")


def main_screen():
    """
    :return:
        True, empieza el juego.
        False, termina.
    """
    global output

    estado = Global.get_instance()
    output = estado.output()
    _input = estado.input()

    mensaje_inicial(output)

    v, n, i = vocabulario()
    ana_lex = AnaLex(v, n, i, output)
    allowed_tokens = ("INICIAR", "CARGAR_PARTIDA", "AYUDA", "FIN_JUEGO")
    exit_game = False
    #while not exit_game:
    while True:
        user_input = _input.input(">> ")
         # Completar
        comando, valido = ana_lex.procesar_palabras(user_input)
        if not valido:
            continue
        if comando.token_verbo not in allowed_tokens:
            output.print("Ese comando no se usa aquí.\n")
            continue
        if comando.token_verbo == "INICIAR":
            # main_game()
            # exit_game = True
            mostrar_introducción(estado)
            return True
        if comando.token_verbo == "CARGAR_PARTIDA":
            cmd_cargar(comando)
            #main_game()
            #exit_game = True
            return True
        if comando.token_verbo == "AYUDA":
            cmd_ayuda(comando)
            _input.pulsa_intro()
            mensaje_inicial(output)
        if comando.token_verbo == "FIN_JUEGO":
            #exit_game = True
            return False

    # Nunca se llega aquí
    output.print("Bye.")


# Verbos genéricos


def cmd_ver(comando):
    # borrar pantalla
    return Resultado.REINICIA


def cmd_inventario(comando):
    estado = Global.get_instance()
    objetos = [obj.breve_descripcion for obj in estado.inventario.values()]
    output.print_inventario(objetos)
    # for obj in estado.inventario.values():
    #    output.print(obj.breve_descripcion)
    return Resultado.HECHO


def cmd_fin(comando):
    return Resultado.FIN_JUEGO


def cmd_examinar_inventario(comando):
    # Mira si el objeto a examinar está en el inventario y muestra su descripción
    # Si no está en el inventario, es repsosabilidadd e la localización o de un objeto interactuable de la localización
    # dar repsuesta.
    estado = Global.get_instance()
    output = estado.output()
    if estado.en_inventario(comando.token_nombre) == False:
        output.print("No puedes examinar eso.")
    else:
        obj = estado.inventario[comando.token_nombre]
        output.print(obj.descripcion())
    return Resultado.HECHO


def cmd_guardar(comando):
    import pickle

    estado = Global.get_instance()

    # Tengo un cannot pickle '_thread.RLock' object
    # a ver si descubro cuál es
    # era rich
    #estado._output = None # Error
    #estado._input = None # Seguro
    #estado._events = None # Seguro
    #estado._map = None # Error
    #estado.localizacion_actual = None # Error
    #estado.inventario = None # Seguro
    #estado._locs = None # Error
    output.ready_to_save()

    #data = pickle.dumps(estado)
    with open("save_game.pck", "wb") as save_file:
        pickle.dump(estado, save_file)

    output.re_init()
    output.print("Guardado.")
    return Resultado.HECHO


def cmd_cargar(comando):
    import pickle
    with open("save_game.pck", "rb") as save_file:
        save_data = pickle.load(save_file)
    Global._instance = save_data

    output.re_init()
    output.print("Cargado.")
    # Pulsa una tecla.
    # _input.pulsa_intro()
    Global._instance._input.pulsa_intro()
    return Resultado.REINICIA


def cmd_ayuda(comando):
    output.print("El objetivo del juego es encontrar la salida de la caverna llevando en el inventario las 6 gemas, pero podrás salir con menos.")
    output.start_two_columns("Comandos básicos:")
    output.row("n, s, e, o", "movimiento.")
    output.row("i", "muestra los objetos que llevas.")
    output.row("m", "descripción de la localización dónde estás.")
    output.row("cargar, guardar", "carga o guarda tu partida en un fichero sobreescribiendo la anterior.")
    output.row("fin", "sales del juego (sin grabar partida).")
    output.end_two_columns()
    output.print("Si quiere pronunciar alguna palabra misteriosa, escríbela.")
    return Resultado.HECHO


def cmd_ayuda_backup(comando):
    output.print("""El objetivo del juego es encontrar la salida de la caverna llevando en el inventario las 6 gemas, pero podrás salir con menos.

Comandos básicos:
-------------------
 n, s, e, o
 i, inventario
 m, repite la localización
 cargar, guardar
 fin, sale del juego
 
 Si quiere pronunciar alguna palabra misteriosa, solo escríbela. 
""")
    return Resultado.HECHO


def cmd_debug(comando):
    estado = Global.get_instance()
    output.print(estado)
    return Resultado.HECHO


def cmd_no_pasa_nada(comando):
    output.print("No pasa nada.")
    return Resultado.HECHO

def cmd_mapa(comando):
    estado = Global.get_instance()
    output.print_map(estado._map, estado.localizacion())

def comandos_comunes():
    comandos = {
        "VER": {"*": cmd_ver},
        "INV": {"*": cmd_inventario},
        "EXAMINAR": {"*": cmd_examinar_inventario},
        "FIN_JUEGO": {"*": cmd_fin},
        "GUARDAR_PARTIDA": {"*": cmd_guardar},
        "CARGAR_PARTIDA": {"*": cmd_cargar},
        "DEBUG": {"*": cmd_debug},
        "NO_MALDICION": {"*": cmd_no_pasa_nada},
        "SI_MALDICION": {"*": cmd_no_pasa_nada},
        "AYUDA": {"*": cmd_ayuda},
        "MAP": {"*": cmd_mapa},
    }
    return comandos


def comandos_pantalla_principal():
    comandos = {
        "INICIA": {"*": cmd_ver},
        "FIN_JUEGO": {"*": cmd_fin},
        "CARGAR_PARTIDA": {"*": cmd_cargar},
        "DEBUG": {"*": cmd_debug},
        "AYUDA": {"*": cmd_ayuda},
    }
    return comandos


if __name__ == '__main__':
    load_data()
    load_interfaces()
    running = True
    while running:
        running = main_screen()
        if running:
            main_game()
            load_data()

#C:\Users\rince\AppData\Local\Programs\Python\Python312\Scripts\pyinstaller --onefile main.py
from epic_cavern.datos import Resultado, Global, Localizacion, ObjetoAventura, CofreAbreCierra, \
    CofreMimico, Puerta, LocalizacionIlusiones, Teletransporte, ObjetoGema, ExaminableEncuentra, LocalizacionGema, \
    LocalizacionOjos, Espejo, LocalizacionFinal, LocalizacionLosetas, LocalizacionBalanza
from epic_cavern.lexico import comando
from epic_cavern.user_interfaces import ConsoleOutput, ConsoleInput
from epic_cavern.datos import LocalizaciónVacía, Investigador

"""
el parser comprueba que la sgeunda palabra sea un nombre registrado, por eso no puedo usar save nombre_partida
ya que daría error.

"""


def load_data():

    # Localizaciones
    loc1_Caida = Localizacion("loc1_Caida", "Has entrado en la caverna y ya no hay marcha atrás. Escapa o muere.")
    loc2_Vacía = LocalizaciónVacía("loc2_Vacía")
    loc3_Investigador = Localizacion("loc3_Investigador", "Parte del suelo de está caverna está decorado con lineas talladas en la piedra que no parecen tener ningún sentido.")
    loc5_Vacía = LocalizaciónVacía("loc5_Vacía")
    loc7_Vacía = LocalizaciónVacía("loc7_Vacía")
    loc9_Balanza = LocalizacionBalanza("loc9_Balanza", "En esta caverna ves una gran estatua de una serpiente y, frente a ella dos platos de una balanza de piedra. Debajo de la balanza hay una placa grabada.")
    loc11_Vacía = LocalizaciónVacía("loc11_Vacía")
    loc13_Vacía = LocalizaciónVacía("loc13_Vacía")
    loc15_Ojos_rojos = LocalizacionOjos("loc15_Ojos_rojos", "Sin uso")
    loc17_Vacía = LocalizaciónVacía("loc17_Vacía")
    loc19_Vacía = LocalizaciónVacía("loc19_Vacía")
    loc21_Dibujos = Localizacion("loc21_Dibujos", "Esta caverna tiene las paredes cubiertas de dibujos de una época anterior.")
    loc22_Puerta = Localizacion("loc22_Puerta", "Incrustada en la pared de roca ves una gran y pesada puerta. Junto a ella, tallada en la roca, hay una vieja inscripción que aún parece legible")
    loc25_Vacía = LocalizaciónVacía("loc25_Vacía")
    loc27_Vacía = LocalizaciónVacía("loc27_Vacía")
    loc28_Cocina = Localizacion("loc28_Cocina", "Esta caverna se usa como cocina. En un extremo ves un pequeño fogón aún humeante con un tosco horno.")
    loc31_Inscripción = Localizacion("loc31_Inscripción", "En esta caverna hay una inscripción grabada en grandes letras en la pared de piedra.")
    loc33_Cofre_auténtico = Localizacion("loc33_Cofre_auténtico", "En una esquina de esta caverna ves un cofre.")
    loc35_Mímico = Localizacion("loc35_Mímico", "En una esquina de esta caverna ves un cofre.")
    loc37_Vacía = LocalizaciónVacía("loc37_Vacía")
    loc38_Llave = LocalizaciónVacía("loc38_Llave")
    loc41_Vacía = LocalizaciónVacía("loc41_Vacía")
    loc43_Oscura = LocalizacionGema("loc43_Oscura", "Oscura")
    loc46_Vacía = LocalizaciónVacía("loc46_Vacía")
    loc48_Sala_de_música = Localizacion("loc48_Sala_de_música", "En esta caverna hay varios instrumentos de música tirados y rotos. Los instrumentos parecen pensados para criaturas con manos más pequeñas que las de un humano.")
    loc49_Vacía = LocalizaciónVacía("loc49_Vacía")
    loc50_Teletransporte = Localizacion("loc50_Teletransporte", "Notas una extraña energía cuando entras en esta caverna. En la pared de roca hay tallada una inscripción.")
    loc54_Vacía = LocalizaciónVacía("loc54_Vacía")
    loc55_Ídolo = LocalizaciónVacía("loc55_Ídolo")
    loc58_Vacía = LocalizaciónVacía("loc58_Vacía")
    loc59_Cadáver_y_derrumbamiento = Localizacion("loc59_Cadáver_y_derrumbamiento", "En esta caverna ves un derrumbamiento que ha tapado la salida. Junto al derrumbamiento, hay un cadáver que debe llevar aquí muchos, muchos años.")
    loc62_Vacía = LocalizaciónVacía("loc62_Vacía")
    loc63_Charco = Localizacion("loc63_Charco", "El agua cae por estalactitas formando un charco apestoso y cenagoso en el centro. Por suerte no parece muy profundo.")
    loc64_Vacía = LocalizaciónVacía("loc64_Vacía")
    loc68_Bosque_de_setas_gigantes = Localizacion("loc68_Bosque_de_setas_gigantes", "Esta caverna está llena de setas tan grandes como árboles. Por suerte, todo parece tranquilo.")
    loc70_Vacía = LocalizaciónVacía("loc70_Vacía")
    loc71_Salida = LocalizacionFinal("loc71_Salida", "Has encontrado la salida. Está al sur, al otro lado de esta gran caverna.")
    loc74_Ilusiones = LocalizacionIlusiones("loc74_Ilusiones", "Llegas a una caverna vacía. Ves una inscripción en una de las paredes de esta caverna.")
    loc76_Zafiro = LocalizaciónVacía("loc76_Zafiro") # el zafiro ya no está aquí
    loc78_Vacía = LocalizaciónVacía("loc78_Vacía")
    loc80_Guardián_del_espejo = Localizacion("loc80_Guardián_del_espejo", "En la pared de roca de esta caverna ves un gran y tosco espejo. Junto él hay una inscripción grabada en la piedra.")
    loc82_Vacía = LocalizaciónVacía("loc82_Vacía")
    loc85_Vacía = LocalizaciónVacía("loc85_Vacía")
    loc87_Viaje_del_héroe = Localizacion("loc87_Viaje_del_héroe", "Esta caverna está decorada con imágenes de un héroe viajando a distintos lugares. También hay una inscripción.")
    loc89_Losetas = LocalizacionLosetas("loc89_Losetas", "Ante ti tienes tres losetas: la del este refulge con chispas mágicas, la del norte está llena de arena y la del oeste tiene una roca.\nTienes que pisar una de ellas.", 0)
    loc89_Losetas_2 = LocalizacionLosetas("loc89_Losetas_2", "Ante ti tienes tres losetas: la del este tiene una roca negra, la del norte tiene astillas de madera y la del oeste guijarros.\nTienes que pisar una de ellas.", 2)
    loc89_Losetas_3 = LocalizacionLosetas("loc89_Losetas_3", "Ante ti tienes tres losetas: la del este tiene charco de agua, la del norte tiene plumas de alas y la del oeste tienes arena negra.\nTienes que pisar una de ellas.", 2)
    loc90_Teletransporte = Localizacion("loc90_Teletransporte", "Notas una extraña energía cuando entras en esta caverna. En la pared de roca hay tallada una inscripción.")

    # Conexiones
    loc1_Caida.conectar(1, loc2_Vacía)
    loc2_Vacía.conectar(2, loc3_Investigador)
    loc2_Vacía.conectar(1, loc17_Vacía)
    loc3_Investigador.conectar(2, loc5_Vacía)
    loc7_Vacía.conectar(1, loc5_Vacía)
    loc7_Vacía.conectar(2, loc9_Balanza)
    loc5_Vacía.conectar(2, loc11_Vacía)
    loc11_Vacía.conectar(2, loc13_Vacía)
    loc11_Vacía.conectar(1, loc19_Vacía)
    loc13_Vacía.conectar(2, loc15_Ojos_rojos)
    loc22_Puerta.conectar(2, loc19_Vacía)
    loc19_Vacía.conectar(2, loc21_Dibujos)
    loc17_Vacía.conectar(2, loc25_Vacía)
    loc17_Vacía.conectar(1, loc27_Vacía)
    loc27_Vacía.conectar(3, loc28_Cocina)
    loc27_Vacía.conectar(1, loc31_Inscripción)
    loc33_Cofre_auténtico.conectar(2, loc31_Inscripción)
    loc31_Inscripción.conectar(1, loc35_Mímico)
    loc31_Inscripción.conectar(2, loc37_Vacía)
    loc38_Llave.conectar(1, loc37_Vacía)
    loc37_Vacía.conectar(2, loc41_Vacía)
    loc41_Vacía.conectar(0, loc43_Oscura)
    loc41_Vacía.conectar(1, loc46_Vacía)
    loc43_Oscura.conectar(0, loc25_Vacía)
    #loc50_Teletransporte.conectar(2, loc1_Caida)
    loc49_Vacía.conectar(2, loc48_Sala_de_música)
    loc49_Vacía.conectar(3, loc50_Teletransporte)
    loc46_Vacía.conectar(1, loc48_Sala_de_música)
    loc46_Vacía.conectar(2, loc54_Vacía)
    loc55_Ídolo.conectar(1, loc54_Vacía)
    loc54_Vacía.conectar(2, loc58_Vacía)
    loc58_Vacía.conectar(1, loc59_Cadáver_y_derrumbamiento)
    loc58_Vacía.conectar(2, loc62_Vacía)
    loc58_Vacía.conectar(0, loc76_Zafiro)
    loc62_Vacía.conectar(1, loc63_Charco)
    loc62_Vacía.conectar(2, loc68_Bosque_de_setas_gigantes)
    loc63_Charco.conectar(1, loc64_Vacía)
    loc68_Bosque_de_setas_gigantes.conectar(2, loc70_Vacía)
    loc68_Bosque_de_setas_gigantes.conectar(0, loc85_Vacía)
    loc70_Vacía.conectar(2, loc71_Salida)
    loc76_Zafiro.conectar(2, loc74_Ilusiones)
    loc78_Vacía.conectar(1, loc76_Zafiro)
    loc78_Vacía.conectar(2, loc80_Guardián_del_espejo)
    loc82_Vacía.conectar(0, loc19_Vacía)
    loc82_Vacía.conectar(2, loc78_Vacía)
    loc85_Vacía.conectar(0, loc87_Viaje_del_héroe)
    # conectar las localizaciones de losetas
    # comprobar que funcionan con el código que tengo.

    loc87_Viaje_del_héroe.conectar(3, loc89_Losetas)
    loc89_Losetas.conectar(0, loc89_Losetas_2, False)
    loc89_Losetas_2.conectar(2, loc89_Losetas_3, False)
    loc89_Losetas_3.conectar(2, loc90_Teletransporte, False)

    locs = {
        "loc1_Caida": loc1_Caida,
        "loc2_Vacía": loc2_Vacía,
        "loc3_Investigador": loc3_Investigador,
        "loc5_Vacía": loc5_Vacía,
        "loc7_Vacía": loc7_Vacía,
        "loc9_Balanza": loc9_Balanza,
        "loc11_Vacía": loc11_Vacía,
        "loc13_Vacía": loc13_Vacía,
        "loc15_Ojos_rojos": loc15_Ojos_rojos,
        "loc17_Vacía": loc17_Vacía,
        "loc19_Vacía": loc19_Vacía,
        "loc21_Dibujos": loc21_Dibujos,
        "loc22_Puerta": loc22_Puerta,
        "loc25_Vacía": loc25_Vacía,
        "loc27_Vacía": loc27_Vacía,
        "loc28_Cocina": loc28_Cocina,
        "loc31_Inscripción": loc31_Inscripción,
        "loc33_Cofre_auténtico": loc33_Cofre_auténtico,
        "loc35_Mímico": loc35_Mímico,
        "loc37_Vacía": loc37_Vacía,
        "loc38_Llave": loc38_Llave,
        "loc41_Vacía": loc41_Vacía,
        "loc43_Oscura": loc43_Oscura,
        "loc46_Vacía": loc46_Vacía,
        "loc48_Sala_de_música": loc48_Sala_de_música,
        "loc49_Vacía": loc49_Vacía,
        "loc50_Teletransporte": loc50_Teletransporte,
        "loc54_Vacía": loc54_Vacía,
        "loc55_Ídolo": loc55_Ídolo,
        "loc58_Vacía": loc58_Vacía,
        "loc59_Cadáver_y_derrumbamiento": loc59_Cadáver_y_derrumbamiento,
        "loc62_Vacía": loc62_Vacía,
        "loc63_Charco": loc63_Charco,
        "loc64_Vacía": loc64_Vacía,
        "loc68_Bosque_de_setas_gigantes": loc68_Bosque_de_setas_gigantes,
        "loc70_Vacía": loc70_Vacía,
        "loc71_Salida": loc71_Salida,
        "loc74_Ilusiones": loc74_Ilusiones,
        "loc76_Zafiro": loc76_Zafiro,
        "loc78_Vacía": loc78_Vacía,
        "loc80_Guardián_del_espejo": loc80_Guardián_del_espejo,
        "loc82_Vacía": loc82_Vacía,
        "loc85_Vacía": loc85_Vacía,
        "loc87_Viaje_del_héroe": loc87_Viaje_del_héroe,
        "loc89_Losetas": loc89_Losetas,
        "loc89_Losetas_2": loc89_Losetas_2,
        "loc89_Losetas_3": loc89_Losetas_3,
        "loc90_Teletransporte": loc90_Teletransporte,
    }

    # Examinables
    loc9_Balanza.agregar_examinable("PLACA", "Hay unas palabras grabadas en la placa: 'da antes de recibir'")
    loc21_Dibujos.agregar_examinable("DIBUJO", "Te llaman la atención tres dibujos, cada uno con una extraña palabra.\nUn dibujo de una persona con el nombre de ragul.\nUn dibujo de un disco amarillo con el nombre resid.\nUn dibujo de un disco negro con el nombre fosco.")
    loc22_Puerta.agregar_examinable("INSCRIPCION", "Está escrita en un idioma antiguo y no la entiendes.")
    # loc22_Puerta.agregar_examinable("PUERTA", "Cerrada y demasiado pesada para moverla. No tiene ninguna cerradura por lo que debe abrirse de otra manera.")
    loc31_Inscripción.agregar_examinable("INSCRIPCION", "No den de comer al cofre.")
    loc50_Teletransporte.agregar_examinable("INSCRIPCION", "Dijo edu y se marchó.")
    loc68_Bosque_de_setas_gigantes.agregar_examinable("SETAS", "Altas y de troncos gruesos como árboles.")
    loc74_Ilusiones.agregar_examinable("INSCRIPCION", "Tus ojos te engañan.")
    loc80_Guardián_del_espejo.agregar_examinable("INSCRIPCION", "Vence al guardián para conseguir su tesoro.")
    loc87_Viaje_del_héroe.agregar_examinable("INSCRIPCION", """Utur atravesó las tierras ardientes.
Utur cruzó la montaña de fuego.
Utur cruzó la gran serpiente azul.
""")
    loc90_Teletransporte.agregar_examinable("INSCRIPCION", "Dijo edu y se marchó.")

    estado = Global.get_instance()
    estado.set_localizacion(loc1_Caida)
    estado._locs = locs

    # Objetos
    loc38_Llave.agregar_objeto("LLAVE", ObjetoAventura("LLAVE", "Llave oxidada que nadie sabe qué abre.", "LLAVE", "Una llave"))
    loc48_Sala_de_música.agregar_objeto("DIAPASON", ObjetoAventura("DIAPASON", "Un pequeño diapasón que emite un tono agudo si lo golpeas suavemente.", "DIAPASON", "Un diapasón"))
    loc55_Ídolo.agregar_objeto("IDOLO", ObjetoAventura("IDOLO", "Pequeña figura, toscamente tallada en piedra, que representa un ídolo.", "IDOLO", "Un ídolo"))
    #loc76_Zafiro.agregar_objeto("ZAFIRO", ObjetoAventura("ZAFIRO", "Zafiro falso echo de cristal y sin ningún valor.", "ZAFIRO", "Un zafiro"))
    diamante = ObjetoGema("DIAMANTE", "Diamante tallado de gran valor.", "DIAMANTE", "Un diamante")
    loc43_Oscura.agregar_objeto("DIAMANTE", diamante)

    zafiro = ObjetoAventura("ZAFIRO", "Zafiro falso echo de cristal y sin ningún valor.", "ZAFIRO", "Un zafiro")
    aguamarina = ObjetoGema("AGUAMARINA", "Su color hace honor a su nombre y es de gran valor.", "AGUAMARINA", "Una aguamarina")
    esmeralda = ObjetoGema("ESMERALDA", "Esmeralda tan grande como tu mano y de gran valor.", "ESMERALDA", "Una esmeralda")
    jade = ObjetoGema("Jade", "De color verde intenso y superficie pulida, tan grande como tu mano y de gran valor.", "JADE", "Un jade")
    # Se crea dentro de la loc del espejo
    # opalo = ObjetoGema("OPALO", "Refleja todos los colores en su superficie y es de gran valor.", "OPALO", "Un ópalo")
    # Se crea dentro de la loc de los ojos
    # rubi = ObjetoGema("RUBI", "De color sangre y de gran valor.", "RUBI", "Un rubí")

    loc74_Ilusiones.agregar_objeto("AGUAMARINA", aguamarina)
    loc90_Teletransporte.agregar_objeto("JADE",jade)
    loc9_Balanza.init_objeto_primer_plato("ESMERALDA", esmeralda)


    #PNJ
    loc3_Investigador.pnj = Investigador("Investigador", "Pequeño y menudo, pero con una cabeza deproporcionadamente grande que le da un aspecto cómico a pesar de su edad.", "Un investigador de avanzada edad está de rodillas estudiando las extrañas líneas.")

    #Interactuables
    topacio = ObjetoGema("Topacio", "Azulado, translúcido. tan grande como tu mano y de gran valor.", "TOPACIO", "Un topacio")

    loc22_Puerta.interactivos.append(Puerta(obj_contenido=topacio))
    loc28_Cocina.interactivos.append(CofreAbreCierra(descripción="Un horno.", self_token="HORNO",
                                                     obj_contenido = ObjetoAventura("EMPANADA", "Aunque está recién horneada, no parece muy comestible.", "EMPANADA", "Una empanada")))
    loc33_Cofre_auténtico.interactivos.append(CofreAbreCierra(token_llave_abrir="LLAVE", obj_contenido = zafiro ))
    loc35_Mímico.interactivos.append(CofreMimico())
    loc50_Teletransporte.interactivos.append(Teletransporte(loc1_Caida))
    cadaver = ExaminableEncuentra("descripcion cadáver",
                                 ObjetoAventura("VARA", "Vara dorada. Frótala y emitirá luz durante un instante.", "VARA", "Una vara dorada"), "CADAVER")
    loc59_Cadáver_y_derrumbamiento.interactivos.append(cadaver)
    charco = ExaminableEncuentra("descripcion charco", ObjetoAventura("CUCHILLO", "descriopcion.", "CUCHILLO", "Un cuchillo"), "CHARCO")

    loc63_Charco.interactivos.append(charco)
    loc80_Guardián_del_espejo.interactivos.append(Espejo())
    loc90_Teletransporte.interactivos.append(Teletransporte(loc50_Teletransporte))


def load_interfaces():
    estado = Global.get_instance()
    estado._output = ConsoleOutput()
    estado._input = ConsoleInput()


def mostrar_introducción(estado):
    estado.output().print("""Muchos han entrado en la caverna, pero muy pocos han salido. ¿Por qué iba a ser distinto contigo?
Estás a punto de descubrirlo.
Salir con vida ya es un éxito, pero para ti eso es poco. Encuentra las seis gemas ocultas en la caverna y serás rico y famoso el resto de tu vida. O muere intentándolo.
""")
    estado.input().pulsa_intro()
    # limpia la pantalla

def procesar_cadena(cadena):
    """
    Divide una cadena en palabras y limita a 6 letras cualquier palabra que tenga más de 6 caracteres.

    Args:
        cadena (str): La cadena de entrada.

    Returns:
        str: Una nueva cadena con palabras procesadas.
    """
    CARACTERES = 7
    palabras = cadena.split()  # Divide la cadena en palabras
    palabras_procesadas = [palabra[:CARACTERES] if len(palabra) > CARACTERES else palabra for palabra in palabras]
    return palabras_procesadas


def procesar_palabras(palabras, output):
    es_valido = True
    es_vacio = False
    if len(palabras) == 0:
        es_vacio = True
        user_command = None
    elif len(palabras) == 1:
        user_command = comando(palabras[0])
    else:
        user_command = comando(palabras[0], palabras[1])

    # Ver si existen
    if es_vacio or user_command.token_verbo is None:
        output.print("Verbo no encontrado.")
        es_valido = False

    if not es_vacio and user_command.token_nombre is None:
        output.print("Nombre no encontrado.")
        es_valido = False

    return user_command, es_valido


def main_game():
    global output

    estado = Global.get_instance()
    output = estado.output()
    _input = estado.input()
    # print(estado._locs)

    mostrar_introducción(estado)

    resultado = None
    while resultado != Resultado.FIN_JUEGO:
        resultado = None
        estado = Global.get_instance()
        loc_actual = estado.localizacion()
        output.print('\n'+loc_actual.mostrar_descripcion())
        imprimir_objetos(loc_actual)

        while resultado != Resultado.REINICIA and resultado != Resultado.FIN_JUEGO:
            user_input = _input.input(">> ")
            palabras = procesar_cadena(user_input)
            user_command, valido = procesar_palabras(palabras, output)
            # print(user_input, palabras, user_command)
            if not valido:
                continue

            # Procesar comando en la loc en al que estoy
            loc_actual = estado.localizacion()
            resultado = loc_actual.run_command(user_command)
            if resultado != Resultado.NO_HECHO:
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

    # Fin del juego.
    output.print("Bye.")

def imprimir_objetos(loc_actual):
    if loc_actual.hay_objetos_visibles():
        output.print("Aquí hay:")
        for obj in loc_actual.objetos.values():
            output.print(obj.breve_descripcion)


# Verbos genéricos

def cmd_ver(comando):
    # borrar pantalla
    return Resultado.REINICIA


def cmd_inventario(comando):
    output.print("Llevas:")
    estado = Global.get_instance()
    for obj in estado.inventario.values():
        output.print(obj.breve_descripcion)
    return Resultado.HECHO


def cmd_fin(comando):
    return Resultado.FIN_JUEGO

def cmd_examinar_inventario(comando):
    # Mira si el objeto a examinar está en el inventario y muestra su descripción
    estado = Global.get_instance()
    output = estado.output()
    if estado.en_inventario(comando.token_nombre) == False:
        output.print("No puedes examinar eso.")
    else:
        obj = estado.inventario[comando.token_nombre]
        output.print(obj.descripcion)
    return Resultado.HECHO


def cmd_guardar(comando):
    import pickle
    with open("save_game.pck", "wb") as save_file:
        pickle.dump(Global.get_instance(), save_file)
    output.print("Guardado.")
    return Resultado.HECHO


def cmd_cargar(comando):
    import pickle
    with open("save_game.pck", "rb") as save_file:
        save_data = pickle.load(save_file)
    Global._instance = save_data
    output.print("Cargado.")
    # Pulsa una tecla.
    return Resultado.REINICIA


def cmd_debug(comando):
    estado = Global.get_instance()
    output.print(estado)
    return Resultado.HECHO

def comandos_comunes():
    comandos = {
        "VER": {"*": cmd_ver},
        "INV": {"*": cmd_inventario},
        "EXAMINAR": {"*": cmd_examinar_inventario},
        "FIN_JUEGO": {"*": cmd_fin},
        "GUARDAR_PARTIDA": {"*": cmd_guardar},
        "CARGAR_PARTIDA": {"*": cmd_cargar},
        "DEBUG": {"*": cmd_debug},
    }
    return comandos


if __name__ == '__main__':
    # Cargar datos iniciales
    load_data()
    load_interfaces()
    main_game()
#C:\Users\rince\AppData\Local\Programs\Python\Python312\Scripts\pyinstaller --onefile main.py
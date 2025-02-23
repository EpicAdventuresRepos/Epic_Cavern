from epic_cavern.datos import Global, movimiento, movimiento_doble_sentido
from epic_cavern.datos import Resultado
from epic_cavern.lexico import Comando


class Localizacion(object):
    def __init__(self, nombre, descripcion, oscura=False):
        """
        Constructor para la clase Localizacion.

        :param nombre: Nombre de la localización (str).
        :param descripcion: Descripción de la localización (str).
        :param oscura: Indica si la localización está a oscuras (bool).
        """
        self._nombre = nombre
        self.descripcion = descripcion
        self.oscura = oscura  # Estado de iluminación de la localización
        # Cambiar a mapa token: objeto
        self.objetos = {}  # Objetos visibles en la localización Token : Objeto
        self.conexiones = {}  # Diccionario para las conexiones con otras localizaciones {dirección: Localizacion}
        self.examinables = {}  # Cosas examinables que no son objetos.
        self.pnj = None
        self.interactivos = []
        self._estado = Global.get_instance()
        self._output = self._estado.output()

        self.comandos = {
            "N": {"*": self.mover_norte},
            "S": {"*": self.mover_sur},
            "E": {"*": self.mover_este},
            "O": {"*": self.mover_oeste},
            "COGER": {"TODO": self._coger_todo, "*": self.coger},
            "DEJAR": {"*": self.dejar},
            "EXAMINAR": {"*": self.examinar},
        }

    def __str__(self):
        return str(self._nombre) + " / Conexiones: " + str(self.conexiones)

    def nombre(self):
        return self._nombre

    def agregar_objeto(self, token, objeto):
        self.objetos[token] = objeto

    def hay_objetos_visibles(self):
        return len(self.objetos) > 0

    def conectar(self, direccion, otra_localizacion, doble_sentido=True):
        """
        Conecta esta localización con otra en una dirección específica.

        :param direccion: Dirección de la conexión (str, ej. "norte", "sur").
        :param otra_localizacion: Instancia de Localizacion a conectar.
        """
        self.conexiones[direccion] = otra_localizacion
        if not doble_sentido:
            return
        direccion_conraria = movimiento_doble_sentido[direccion]
        otra_localizacion.conectar(direccion_conraria, self, False)

    def agregar_examinable(self, token, descripción):
        self.examinables[token] = descripción

    def _cadena_descripción(self):
        if self.oscura:
            return f"Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\n"
        return f"{self.descripcion}\n"

    def mostrar_descripcion(self):
        """
        Devuelve una descripción detallada de la localización, incluyendo objetos visibles y direcciones.
        """
        descripcion = self._cadena_descripción()
        if self.pnj:
            descripcion += self.pnj.esta_aqui() + "\n"
        #if self.objetos:
        #    descripcion += f"Objetos visibles: {', '.join(self.objetos)}.\n"

        # algunas GUIs necesitan que se haga por separado
        #descripcion += self._mostrar_salidas()

        return descripcion

    def _mostrar_salidas(self):
        """
        Este método no debe llevar la _
        :return:
        """
        descripcion = f"Puedes ir hacia: "
        if len(self.conexiones) > 0:
            # print(self.conexiones)
            tmp_salidas = [movimiento[k] for k in self.conexiones.keys()]
            descripcion += f"{', '.join(tmp_salidas)}.\n"
        return descripcion

    def run_command(self, comando):
        #print(self.nombre, comando)
        self._output = self._estado.output()
        if self.pnj:
            val, res = self.pnj.run_command(self, comando)
            # print("PNJ ", comando, val, res)
            if val:
                return res

        if len(self.interactivos) > 0:
            # print("Interactivos ", self.interactivos)
            for objeto in self.interactivos:
                val, res = objeto.run_command(self, comando)
                #print("Interactivo: ", objeto, comando, val, res)
                if val:
                    #print(res)
                    return res
        #print("Sigue")
        if comando.token_verbo not in self.comandos:
            return Resultado.NO_HECHO
        verbs = self.comandos[comando.token_verbo]
        if comando.token_nombre not in verbs:
            if "*" not in verbs:
                return Resultado.NO_HECHO
            else:
                names = verbs["*"]
        else:
            names = verbs[comando.token_nombre]
        return names(comando)

    def _mover(self, direccion):
        #print(self.conexiones)
        if direccion not in self.conexiones:
            self._output.print("No hay salida.")
            return Resultado.HECHO
        estado = Global.get_instance()
        estado.set_localizacion(self.conexiones[direccion])
        return Resultado.REINICIA

    def mover_norte(self, command):
        return self._mover(0)

    def mover_sur(self, command):
        return self._mover(1)

    def mover_este(self, command):
        return self._mover(2)

    def mover_oeste(self, command):
        return self._mover(3)

    def _precondicones_coger(self, command):
        if command.token_nombre == "*":
            print("Indica qué coger.")
            return False
        if command.token_nombre not in self.objetos:
            #print(command.token_nombre)
            #print(self.objetos)
            self._output.print("No está aquí.")
            return False
        return True

    def coger(self, command):
        if not self._precondicones_coger(command):
            return Resultado.HECHO
        self._estado.añade_inventario(command.token_nombre, self.objetos[command.token_nombre])
        del self.objetos[command.token_nombre]
        self._output.print("Ok.")

        return Resultado.HECHO

    def _coger_todo(self, command):
        if not self.hay_objetos_visibles():
            self._output.print("No hay nada que coger.")
        objetos = list(self.objetos.keys())
        for obj_token in objetos:
            self.coger(Comando("no", "no", "no", obj_token))
        return Resultado.HECHO

    def _precondicion_dejar(self, token):
        if self._estado.en_inventario(token):
            return self._estado.saca_inventario(token)
        else:
            self._output.print(f"No tienes {token} en tu inventario")
        return None

    def dejar(self, command):
        objeto = self._precondicion_dejar(command.token_nombre)
        if objeto is not None:
            self.agregar_objeto(command.token_nombre, objeto)
            self._output.print(f"Dejaste el {command.token_nombre}")
        return Resultado.HECHO

    def examinar(self, command):
        # print("Examinar", command, self.examinables)
        if command.token_nombre in self.examinables:
            #print("A", self.examinables[command.token_nombre])
            self._output.print(self.examinables[command.token_nombre])
            return Resultado.HECHO
        if command.token_nombre in self.objetos:
            #print("B", self.objetos[command.token_nombre].descripcion)
            self._output.print(self.objetos[command.token_nombre].descripcion())
            return Resultado.HECHO
        #print("Fail")
        return Resultado.NO_HECHO


###

class LocalizaciónVacía(Localizacion):
    def __init__(self, nombre):
        super().__init__(nombre, "Estás en una caverna vacía.")


###
# sin uso
class LocalizacionPuertaLLave(Localizacion):
    def __init__(self, nombre, descripcion, oscura=False):
        super().__init__(nombre, descripcion, oscura)
        self.puerta_cerrada = True
        self.direccion_puerta = 3  # Oeste

        self.comandos["ABRIR"] = {"PUERTA": self.abrir_puerta}
        self.examinables["PUERTA"] = "Tiene una cerradura para una llave."

    def mover_oeste(self, command):
        # Asumo que hay salida
        if (self.puerta_cerrada):
            print("La puerta está cerrada")
            return Resultado.HECHO
        return self._mover(2)

    def abrir_puerta(self, comando):
        estado = Global.get_instance()
        if estado.en_inventario("LLAVE") and self.puerta_cerrada:
            print("Abres la puerta con la llave.")
            self.puerta_cerrada = True
        else:
            print("No puedes hacer eso")  # Mensajes más cocnretos.
        return Resultado.HECHO


##############

# To-Do. Falta poner el objeto
class LocalizacionIlusiones(Localizacion):
    def __init__(self, nombre, descripcion):
        super().__init__(nombre, descripcion)

    def _mostrar_salidas(self):
        inversa_salidas = list()
        for s in range(0, 3):
            if s not in self.conexiones.keys():
                inversa_salidas.append(s)
        # print(self.conexiones.keys())
        # print(inversa_salidas)
        descripcion = f"Puedes ir hacia: "
        if len(self.conexiones) > 0:
            # print(self.conexiones)
            tmp_salidas = [movimiento[k] for k in inversa_salidas]
            descripcion += f"{', '.join(tmp_salidas)}.\n"
        return descripcion

    def hay_objetos_visibles(self):
        return False


#######

class LocalizacionBalanza(Localizacion):
    def __init__(self, nombre, descripcion):
        super().__init__(nombre, descripcion)
        self._obj_primer_plato = None
        self._obj_segundo_plato = None
        # Verbos e interacción
        self.comandos["DEJAR"] = {"*": self._dejar}
        self.comandos["COGER"] = {"*": self._coger}
        self.comandos["EXAMINAR"]["BALANZA"] = self._ex_balanza

    def init_objeto_primer_plato(self, token, objeto):
        self.agregar_objeto(token, objeto)
        self._obj_primer_plato = objeto

    def _coger(self, command):
        msg = "Un potente chorro de ácido sale de la boca de la serpiente. Mueres rápido."
        if not self._precondicones_coger(command):
            return Resultado.HECHO
        objeto = self.objetos[command.token_nombre]
        self._estado.añade_inventario(command.token_nombre, objeto)
        del self.objetos[command.token_nombre]
        #print("Ok.")

        if objeto == self._obj_primer_plato:
            self._obj_primer_plato = None
            if self._obj_segundo_plato is None:
                self._output.print(msg)
                return Resultado.FIN_JUEGO
        if objeto == self._obj_segundo_plato:
            self._obj_segundo_plato = None
            if self._obj_primer_plato is None:
                self._output.print(msg)
                return Resultado.FIN_JUEGO

        self._output.print("Ok.")
        return Resultado.HECHO

    def _dejar(self, command):
        if self._obj_primer_plato is not None and self._obj_segundo_plato is not None:
            return self.dejar(command)
        objeto = self._precondicion_dejar(command.token_nombre)
        if objeto is None:
            return Resultado.HECHO

        self.agregar_objeto(command.token_nombre, objeto)
        if self._obj_primer_plato is None:
            self._output.print(f"Dejaste el {command.token_nombre} en el primer plato de la balanza de piedra.")
            self._obj_primer_plato = objeto
        elif self._obj_segundo_plato is None:
            self._output.print(f"Dejaste el {command.token_nombre} en el segundo plato de la balanza de piedra.")
            self._obj_segundo_plato = objeto
        return Resultado.HECHO

    def _ex_balanza(self, command):
        texto = "La balanza es parte de la estatua de la serpiente.\n"
        if self._obj_primer_plato is None:
            texto += "No hay nada en el primer plato.\n"
        else:
            texto += "En el primer plato hay " + self._obj_primer_plato.breve_descripcion.lower() + ".\n"
        if self._obj_segundo_plato is None:
            texto += "No hay nada en el segundo plato.\n"
        else:
            texto += "En el segundo plato hay " + self._obj_segundo_plato.breve_descripcion.lower() + ".\n"
        self._output.print(texto)
        return Resultado.HECHO


##############

class LocalizacionOscura(Localizacion):
    def __init__(self, nombre, descripcion):
        super().__init__(nombre, descripcion, oscura=True)
        self.comandos["FROTAR"] = {"VARA": self.frotar_vara}

    def frotar_vara(self, command):
        if self._estado.en_inventario(command.token_nombre):
            self._output.print("Frotas la vara hasta que esta comienza a emitir una tenue luz que no durará mucho.")
            self.oscura = False
        else:
            self._output.print("No llevas ninguna vara.")
        return Resultado.HECHO

    # Overload
    def _mover(self, direccion):
        resultado = super()._mover(direccion)
        if resultado == Resultado.REINICIA:
            self.oscura = True
        return resultado


##############

class LocalizacionGema(LocalizacionOscura):
    def __init__(self, nombre, descripcion="Sin uso", obj_token="DIAMANTE"):
        super().__init__(nombre, descripcion)
        self.comandos["COGER"] = {"*": self._coger}
        self._obj_token = obj_token
        self._tiene_objeto = False

    #Override
    def _cadena_descripción(self):
        if self.oscura and self._tiene_objeto:
            return f"Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\n"
        if self.oscura and not self._tiene_objeto:
            return f"La caverna está envuelta en la oscuridad. En el centro ves el débil resplandor de un diamante.\nA tu alrededor, en la oscuridad, escuchas ruidos de carreras y jadeos "
        if not self.oscura and not self._tiene_objeto:
            return f"La caverna está vacía.\n"
        if not self.oscura and self._tiene_objeto:
            return f"Las criaturas corren a esconderse de la luz. En el centro En el centro ves el débil resplandor de un diamante.\n"
        return f"{self.descripcion}\n"

    # Override
    def agregar_objeto(self, token, objeto):
        super().agregar_objeto(token, objeto)
        self._tiene_objeto = token == self._obj_token

    def _coger(self, command):
        if command.token_nombre == self._obj_token and self._tiene_objeto and self.oscura:
            self._output(
                f"Coges el {command.nombre} y la luz se ecxtingue. Las ciraturas se abalanzan sobre ti y desgarran tu cuerpo.\nHas muerto.")
            return Resultado.FIN_JUEGO
        return super().coger(command)


#########

class LocalizacionOjos(LocalizacionOscura):
    def __init__(self, nombre, descripcion="Sin uso"):
        super().__init__(nombre, descripcion)
        self.comandos["COGER"] = {"OJOS": self._caer_y_morir, "*": self.coger}
        self.comandos["EXAMINAR"] = {"OJOS": self._examinar_ojos}
        self.comandos["SACAR"] = {"OJOS": self._sacar_ojos}
        self._rubi_en_pared = True

    #Override
    def _cadena_descripción(self):
        if self.oscura and self._rubi_en_pared:
            return f"Está completamente a oscuras. Dos ojos rojos te miran fijamente desde el otro lado de la caverna.\n"
        if self.oscura and not self._rubi_en_pared:
            return f"Está completamente a oscuras."
        if not self.oscura and self._rubi_en_pared:
            return f"Hay un gran agujero sin fondo en el centro de la caverna. Al otro lado, ves una gran serpiente tallada en la pared. Tiene dos ojos rojos brillantes.\n"
        if not self.oscura and not self._rubi_en_pared:
            return f"Hay un gran agujero sin fondo en el centro de la caverna. Una gran serpiente está tallada en el otro lado de la caverna.\n"
        return f"{self.descripcion}\n"

    def _caer_y_morir(self, comando):
        if self.oscura:
            self._output.print(
                f"Avanzas por la caverna a oscuras. No ves el agujero que hay en el centro y caes en él a una muerte segura.\n")
            return Resultado.FIN_JUEGO
        if not self.oscura and self._rubi_en_pared:
            self._output.print(
                f"Uno de los ojos está suelto. Tal vez podrías sacarlo.\n")
            return Resultado.HECHO
        if not self.oscura and not self._rubi_en_pared:
            self._output.print(
                f"Es imposible sacar el ojo de la pared.\n")
        return Resultado.HECHO

    def _examinar_ojos(self, _examinar_ojos):
        if self.oscura:
            self._output.print(
                f"Avanzas por la caverna a oscuras. No ves el agujero que hay en el centro y caes en él a una muerte segura.\n")
            return Resultado.FIN_JUEGO
        if not self.oscura and self._rubi_en_pared:
            self._output.print(
                f"Los ojos son dos rubíes de gran valor. Uno de los ojos está suelto. Tal vez podrías sacarlo.\n")
            return Resultado.HECHO
        if not self.oscura and not self._rubi_en_pared:
            self._output.print(
                f"El otro ojo también es un rubí de gran valor, pero es imposible sacarlo de la pared.\n")
            return Resultado.HECHO
        # Nunca se ejecuta.
        return Resultado.NO_HECHO

    def _sacar_ojos(self, comando):
        if self.oscura:
            self._output.print(
                f"Avanzas por la caverna a oscuras. No ves el agujero que hay en el centro y caes en él a una muerte segura.\n")
            return Resultado.FIN_JUEGO
        if not self.oscura and not self._rubi_en_pared:
            self._output.print(
                f"Es imposible sacarlo de la pared.\n")
            return Resultado.HECHO
        if not self.oscura and self._rubi_en_pared:
            #print(self._estado.inventario)
            if self._estado.en_inventario("CUCHILLO"):
                self._rubi_en_pared = False
                self._output.print(f"Sacas el ojo de la pared. Es un rubí de gran valor.\n")
                self.agregar_objeto("RUBI", ObjetoGema("RUBI", "De color sangre y de gran valor.", "RUBI", "Un rubí"))
            else:
                self._output.print(f"No tienes nada con qué sacarlo.\n")
            return Resultado.HECHO
        return Resultado.NO_HECHO


##############

class LocalizacionLosetas(Localizacion):
    def __init__(self, nombre, descripcion, salida_correcta):
        super().__init__(nombre, descripcion)
        self._salida_correcta = salida_correcta
        self._losetas = {"N": 0, "E": 0, "O": 0}  # Esto es un poco absurdo.
        self.comandos["N"] = {"*": self._pisar_loseta}
        self.comandos["S"] = {"*": self._pisar_loseta}
        self.comandos["E"] = {"*": self._pisar_loseta}
        self.comandos["O"] = {"*": self._pisar_loseta}

        self.salidas = {"N": 0, "S": 1, "E": 2, "O": 3}

    def _pisar_loseta(self, comando):
        verbo = comando.token_verbo
        if verbo not in self._losetas:
            # print(verbo)
            # print(self._losetas)
            self._output.print("No hay salida.")
            return Resultado.HECHO
        salida = self.salidas[verbo]
        if salida != self._salida_correcta:
            self._output.print(
                "Cuando pisas la loseta, un antiguo mecanismo se pone en marcha y una trampa letal se activa. Mueres al instante.\n")
            return Resultado.FIN_JUEGO
        #print("Call mover: ", salida)
        result = self._mover(salida)
        #print("Resultado: ", result)
        return result

    # Override
    def _mostrar_salidas(self):
        return ""


##############

class LocalizacionFinal(Localizacion):
    """
    Ha un golem, si llvas todas las gemas el golem se arrodilla y te deja salir.
    si no llevas las gemas, si escrbes tres comandos dentro de la kocl te atrapa y te mata.
    """
    Limite_comandos = 3
    Gemas = 6

    def __init__(self, nombre, descripcion):
        super().__init__(nombre, descripcion)
        self._comandos_escritos = 0
        # self._todas_gemas = self._contar_gemas() == 6
        self.conexiones[1] = None  # Para que aparezca la salida en la descripción.

    def _contar_gemas(self):
        # Cuenta als gemas que lleva el fugador en su inventario
        gemas = [o for o in self._estado.inventario.values() if o.es_gema()]
        return len(gemas)

    #Override
    def _cadena_descripción(self):
        cadena = super()._cadena_descripción()
        cadena += "Aquí hay un gigante metálico. Cuando te ve, avanza pesadamente hacia ti.\n"
        #print(self._contar_gemas(), LocalizacionFinal.Gemas)
        if self._contar_gemas() == LocalizacionFinal.Gemas:
            cadena += "Has encontrado todas las gemas. El gigante se arrodilla ante ti y te permite pasar."
        else:
            cadena += "No has encontrado todas las gemas. El gigante te intentará matar, pero es lento y a lo mejor podrías esquivarle y salir."
        return cadena

    # Override
    def run_command(self, comando):
        if self._contar_gemas() != LocalizacionFinal.Gemas:
            self._comandos_escritos += 1
            if self._comandos_escritos == LocalizacionFinal.Limite_comandos:
                self._output.print("Mueres.\n")
                return Resultado.FIN_JUEGO
            else:
                self._output.print("Se acerca a ti.\n")
        return super().run_command(comando)

    def mover_sur(self, command):
        if self._contar_gemas() != LocalizacionFinal.Gemas:
            self._output.print("No has conseguido todas las gemas pero al menos has conservado tu vida.\n")
        else:
            self._output.print("Has conseguido todas las gemas. La fama y la fortuna te acompañará toda la vida.\n")
        return Resultado.FIN_JUEGO


##########

class LocalizacionObjetoMaldito(Localizacion):
    def __init__(self, nombre, descripcion, token_objeto_maldito, token_quitar_maldicion):
        super().__init__(nombre, descripcion)
        self._token_objeto_maldito = token_objeto_maldito
        self._token_palabra_quitar_maldicion = token_quitar_maldicion
        self.comandos["COGER"] = {token_objeto_maldito: self._coger_objeto_maldito}
        self.comandos[token_quitar_maldicion] = {"*": self._quitar_maldicion}

    def _quitar_maldicion(self, command):
        if self._token_objeto_maldito not in self.objetos \
                or self.objetos[self._token_objeto_maldito].esta_maldito() is False:
            self._output.print("No pasa nada")
            return Resultado.HECHO
        self._output.print("El aire de la habitación vibra. La maldición desaparece.")
        self.objetos[self._token_objeto_maldito].quitar_maldicion()
        return Resultado.HECHO

    def _coger_objeto_maldito(self, comando):
        if self._token_objeto_maldito not in self.objetos\
                or self.objetos[self._token_objeto_maldito].esta_maldito() is False:
            return self.coger(comando)
        self._output.print(f"El {comando.nombre} cobra vida y te atraviesa el cuello. Mueres en un instante.")
        return Resultado.FIN_JUEGO


#########################################

class ObjetoAventura:
    def __init__(self, nombre, descripcion, token, breve_descripcion):
        """
        Inicializa un objeto de aventura.

        Args:
            nombre (str): Nombre del objeto.
            descripcion (str): Descripción completa del objeto.
            token (str): Identificador único del objeto (obligatorio y de solo lectura).
            breve_descripcion (str): Una breve descripción del objeto.
        """
        self.nombre = nombre
        self._descripcion = descripcion
        self._token = token  # El atributo `token` es privado para hacer que sea de solo lectura
        self.breve_descripcion = breve_descripcion

    @property
    def token(self):
        return self._token

    def mostrar_breve_descripcion(self):
        return self.breve_descripcion or f"No hay descripción breve para el {self.nombre}."

    def descripcion(self):
        return self._descripcion

    def __repr__(self):
        return f"ObjetoAventura(nombre='{self.nombre}', token='{self.token}')"

    def es_gema(self):
        return False


########

class ObjetoGema(ObjetoAventura):
    def __init__(self, nombre, descripcion, token, breve_descripcion):
        super().__init__(nombre, descripcion, token, breve_descripcion)

    def es_gema(self):
        return True


########

class ObjetoMaldito(ObjetoAventura):
    def __init__(self, nombre, descripcion, token, breve_descripcion):
        super().__init__(nombre, descripcion, token, breve_descripcion)
        self._maldito = True
        self._descripción_maldito = None

    def descripción_maldito(self, descripcion):
        self._descripción_maldito = descripcion

    def esta_maldito(self):
        return self._maldito

    def quitar_maldicion(self):
        self._maldito = False

    def descripcion(self):
        if not self._maldito or self._descripción_maldito is None:
            return super().descripcion()
        return self._descripción_maldito



###########################################

class ObjetoIterable(object):
    def __init__(self, descripción=None, self_token=""):
        self._descripción = descripción
        self._estado = Global.get_instance()
        self._token = self_token
        self.comandos = {"EXAMINAR": {self._token: self.examinar_yo_mismo}}

    def run_command(self, loc, comando):
        self._out = self._estado._output
        # print(comando)
        if comando.token_verbo not in self.comandos:
            # print("A", comando.token_verbo, self.comandos)
            return False, Resultado.NO_HECHO
        verbs = self.comandos[comando.token_verbo]
        if comando.token_nombre not in verbs:
            #print("B ", comando.token_nombre, verbs)
            return False, Resultado.NO_HECHO
        #print(verbs)
        names = verbs[comando.token_nombre]
        #print("C")
        return True, names(loc, comando)

    def examinar_yo_mismo(self, loc, comando):
        self._out.print(self._descripción)
        return Resultado.HECHO


###########

class CofreAbreCierra(ObjetoIterable):

    def __init__(self, descripción=None, abierto=False, token_llave_abrir=None, obj_contenido=None, self_token="COFRE"):
        """

        :param descripción:
        :param abierto:
        :param llave_abrir: Si contiene un ojeto, el jugaor necesita llevar este objeto en su inventario para abrir el cocfre
        :param obj_contenido: Si contene un objeto, este se coloca en la loc al abrir el cocfre
        """
        super().__init__(descripción, self_token)
        self._token_llave_abrir = token_llave_abrir
        self._obj_contenido = obj_contenido
        if self._descripción is None:
            self._descripción = "Un cofre."
            # print(self._descripción)
        self._abierto = abierto
        self.comandos["ABRIR"] = {self._token: self.abrir_cofre}

    def examinar_yo_mismo(self, loc, comando):
        # print(self._descripción)
        status = " Está abierto." if self._abierto else " Está cerrado."
        self._out.print(self._descripción + status)
        return Resultado.HECHO

    def abrir_cofre(self, loc, comando):
        # print("Abrir. ", self._token_llave_abrir)
        if self._abierto:
            self._out.print("Ya está abierto.")
            return Resultado.HECHO
        if self._token_llave_abrir is None:
            self._out.print("Abres el cofre.")
        else:
            if self._estado.en_inventario(self._token_llave_abrir):
                self._out.print("Abres el cofre.")
            else:
                self._out.print("No tienes la llave.")
                return Resultado.HECHO

        self._mover_objeto(loc)
        return Resultado.HECHO

    def _mover_objeto(self, loc):
        self._abierto = True
        if self._obj_contenido is not None:
            loc.agregar_objeto(self._obj_contenido._token, self._obj_contenido)
            self._out.print("Encuentras " + self._obj_contenido.breve_descripcion + ".")
            self._obj_contenido = None
        else:
            # print("elf._obj_contenido is None")
            pass

    def __str__(self):
        return f"descripción = {self._descripción}, abierto = {self._abierto}, token_llave_abrir = {self._token_llave_abrir} \n"


###########

# Mejor que here de cofre.
class CofreMimico(CofreAbreCierra):

    def __init__(self):
        super().__init__("Un cofre.")
        self.comandos["DAR"] = {"EMPANADA": self.dar_empanada}

    def abrir_cofre(self, loc, comando):
        self._out.print("Cuando levantas la tapa, descubres una gran boca llena de afilados dientes.")
        self._out.print("No es un cofre, ¡es un mímico!.")
        self._out.print("La diabólica criatura salta sobre ti y te debora rápidamente.")
        self._out.print("Tu aventura termina aquí.")
        # To-Do. Pulsa una tecla.

        return Resultado.FIN_JUEGO

    def dar_empanada(self, loc, comando):
        # No en nventariio
        # Escribir ptrub unitaria
        if self._estado.en_inventario(comando.token_nombre) == False:
            self._out.print("No tienes una empanada.")
        else:
            self._out.print("Le das la empanada al cofre.")
            self._out.print(
                "La tapa se abre mostrando una boca de afilados dientes que engulle la empanada en un instante.")
            self._out.print("Saltas hacia atrás justo a tiempo de que no te arranque la mano.")
            self._estado.saca_inventario(comando.token_nombre)
        return Resultado.HECHO


########

# To-Do: descripción y objeto
class Puerta(CofreAbreCierra):

    def __init__(self, obj_contenido=None):
        super().__init__("Una pesada puerta de piedra sin cerradura.", obj_contenido=obj_contenido, self_token="PUERTA")
        self.comandos["RAGUL"] = {"*": self.muerte}
        self.comandos["FOSCO"] = {"*": self.muerte}
        self.comandos["RESID"] = {"*": self.abre_puerta}

    def examinar_yo_mismo(self, loc, comando):
        if self._abierto:
            self._out.print("Está abierta y nada hará que se cierre.")
        else:
            self._out.print("Está cerrada.")

        return Resultado.HECHO

    def muerte(self, loc, comando):
        self._out.print("Has invocado el nombre incorrecto.")
        self._out.print("La caverna se inunda de rayos de energía. Mueres al instante.")
        return Resultado.FIN_JUEGO

    def abre_puerta(self, loc, comando):
        if self._abierto:
            self._out.print("Nada sucede.")
            return Resultado.HECHO
        self._out.print(
            "La caverna tiembla cuando la puerta se abre ante el poder del nombre del sol.\nAl otro lado de la puerta ves un pequeño hueco.")
        self._mover_objeto(loc)
        return Resultado.HECHO


###########

class ExaminableEncuentra(CofreAbreCierra):

    def __init__(self, descripción, obj_contenido, self_token):
        """
        :param descripción:
        :param abierto:
        :param llave_abrir: Si contiene un ojeto, el jugaor necesita llevar este objeto en su inventario para abrir el cocfre
        :param obj_contenido: Si contene un objeto, este se coloca en la loc al abrir el cocfre
        """
        super().__init__(descripción=descripción, obj_contenido=obj_contenido, self_token=self_token)
        del self.comandos["ABRIR"]

    def examinar_yo_mismo(self, loc, comando):
        self._out.print(self._descripción)
        #print(self._abierto)
        if self._abierto is False:
            self._mover_objeto(loc)
        #print(self._abierto)
        return Resultado.HECHO


###########

class Espejo(ObjetoIterable):

    def __init__(self, descripción=None, self_token="ESPEJO"):
        super().__init__(descripción, self_token)
        self._descripción = descripción
        self._estado = Global.get_instance()
        self._out = self._estado._output
        self._token = self_token
        self.comandos["ATACAR"] = {"ESPEJO": self._atacar, "DIAPASON": self._romper_espejo}
        self._espejo_entero = True

    # Override
    def examinar_yo_mismo(self, loc, comando):
        if self._espejo_entero:
            self._out.print("Una terrible criatura se refleja en el espejo copiando todos tus movimientos.\n")
        else:
            self._out.print("El espejo está hecho pedazos y nada se refleja.\n")

        return Resultado.HECHO

    def _atacar(self, loc, comando):
        if self._espejo_entero:
            self._out.print(
                "Atacas al espejo. La criatura copia tus movimientos y te ataca a tui. su enorme fuerza te mata en el acto\n")
            return Resultado.FIN_JUEGO
        self._out.print("No pasa nada.\n")
        return Resultado.HECHO

    def _romper_espejo(self, loc, comando):
        #print("A")
        if self._espejo_entero:
            #print(self._estado.inventario)
            if self._estado.en_inventario(comando.token_nombre):
                self._out.print(
                    "El sonido agudo del diapasón hace tempblar al espejo hasta que se rompe. Entre sus trozos ves algo que brilla.\n")
                self._espejo_entero = False
                # Poner objeto
                loc.agregar_objeto("OPALO",
                                   ObjetoGema("OPALO", "Refleja todos los colores en su superficie y es de gran valor.",
                                              "OPALO", "Un ópalo"))
            else:
                self._out.print("No lo llevas.\n")
        else:
            self._out.print("No pasa nada.\n")
        return Resultado.HECHO


###########

# No lo uso.
class Teletransporte(ObjetoIterable):

    def __init__(self, loc_destino):
        super().__init__("No.", "No.")
        self._loc_destino = loc_destino
        self.comandos["EDU"] = {"*": self.teletransporte}

    def teletransporte(self, loc, comando):
        self._out.print("La energía mágica te desmonta y te vuelve a montar.")
        # To-Do. Pulsa una tecla.
        self._estado.set_localizacion(self._loc_destino)
        return Resultado.REINICIA


###########################################

class Investigador(ObjetoIterable):

    def __init__(self, nombre: str, descripcion: str, primera_vez=None, token="INVESTIGADOR"):
        """
        Constructor de la clase PNJ.

        :param nombre: Nombre del personaje.
        :param descripcion: Descripción del personaje.
        """
        super().__init__(descripcion, token)
        self.nombre = nombre
        self._primera_vez = primera_vez
        self._es_primera_vez = primera_vez is not True
        self.comandos["DAR"] = {"IDOLO": self.dar_idolo}
        self.comandos["EXAMINAR"]["INSCRIPCION"] = self.examinar_dibujos
        # print(self.comandos)

    def esta_aqui(self):
        if self._es_primera_vez:
            self._es_primera_vez = False
            return self._primera_vez
        return f"{self.nombre} está aquí."

    def dar_idolo(self, loc, comando):
        #print("dar_idolo")
        # estado = Global.get_instance()
        output = self._estado._output
        if not self._estado.en_inventario("IDOLO"):
            output.print("No tienes el ídolo.")
            return Resultado.HECHO
        self._estado.saca_inventario("IDOLO")
        #print("A")
        self._estado._locs["loc3_Investigador"].pnj = None
        self._estado._locs["loc22_Puerta"].pnj = self
        #print("B")

        # ¿Cómo sé la loc a la que tengo que ir?
        output.print(
            "Le das el ídolo.\n'Muy interesante, voy a estudiarlo. Puede que nos veamos pronto'\nEl investigador se marcha.")
        #print("C")

        return Resultado.HECHO

    def examinar_dibujos(self, loc, comando):
        estado = Global.get_instance()
        if estado.localizacion_actual.nombre() != "loc22_Puerta":
            estado._output.print("No hay nada que examinar")
            return Resultado.HECHO
        estado._output.print(
            "El investigador se acerca.\n'Interesante inscripción, déjame que te la traduzca:'\n'solo el nombre del sol abrirá la puerta'\n'También hay una advertencia de que algo terrible sucederá si te equivocas de nombre'")
        return Resultado.HECHO



###################################################################


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
    # loc38_Llave = LocalizaciónVacía("loc38_Llave")
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
    loc91_Círculo = Localizacion("loc91_Círculo", "En el suelo de roca de esta caverna ves dibujado un gran círculo ritual.")
    loc92_Cuchillo_maldito = LocalizacionObjetoMaldito("loc92_Cuchillo_maldito", "Un aura de maldad llena esta caverna.", "CUCHILLO", "SI_MALDICION")

    """
    Añadir dos descripciones al cuchillo
    """

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

    # loc38_Llave.conectar(1, loc37_Vacía)
    loc91_Círculo.conectar(1, loc37_Vacía)

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

    # loc91_Círculo
    # loc92_Cuchillo_maldito
    loc92_Cuchillo_maldito.conectar(0, loc82_Vacía)


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
        # "loc38_Llave": loc38_Llave,
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
        "loc91_Círculo": loc91_Círculo,
        "loc92_Cuchillo_maldito": loc92_Cuchillo_maldito
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
    loc91_Círculo.agregar_examinable("CIRCULO", "El círculo representa la eternidad ya que no tiene ni principio ni fin. Los símbolos de su interior parecen símbolos de protección. Alrededor del círculo ves las letras A R O L.")


    estado = Global.get_instance()
    estado.set_localizacion(loc1_Caida)
    estado._locs = locs

    # Objetos

    """ Llevar la llave al charco y aprovechar esta para poner unaltar diab´llico con el cuchillo """
    #loc38_Llave.agregar_objeto("LLAVE", ObjetoAventura("LLAVE", "Llave oxidada que nadie sabe qué abre.", "LLAVE", "Una llave"))

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
    cuchillo = ObjetoMaldito("CUCHILLO", "Un cuchillo con restos de sangre seca.", "CUCHILLO", "Un cuchillo")
    loc92_Cuchillo_maldito.agregar_objeto(cuchillo.token, cuchillo)

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

    llave = ObjetoAventura("LLAVE", "Llave oxidada que a saber que abrirá.", "LLAVE",
                           "Una llave oxidada")
    charco = ExaminableEncuentra("descripcion charco", llave, "CHARCO")
    loc63_Charco.interactivos.append(charco)

    loc80_Guardián_del_espejo.interactivos.append(Espejo())
    loc90_Teletransporte.interactivos.append(Teletransporte(loc50_Teletransporte))

    # De momento no hago nada con estos objetos
    # No están todos
    objetos = {
        "AGUAMARINA": aguamarina,
        "CUCHILLO": cuchillo,
        "DIAMANTE": diamante,
        "ESMERALDA": esmeralda,
        "Jade": jade,
        "LLAVE": llave,
        "Topacio": topacio,
        "ZAFIRO": zafiro,
    }

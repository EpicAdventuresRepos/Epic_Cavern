from dataclasses import dataclass

def vocabulario():
    verbos = {
        "abrir"  : "ABRIR",
        "arol"   : "NO_MALDICION",
        "atacar" : "ATACAR",
        "ayuda" : "AYUDA",
        "golpear": "ATACAR",
        "romper": "ATACAR",
        "coger"  : "COGER",
        "recoger": "COGER",
        "dar"    : "DAR",
        "ofrecer": "DAR",
        "dejar"  : "DEJAR",
        "edu": "EDU",
        "encende": "ENCENDER",
        "ex": "EXAMINAR",
        "examina": "EXAMINAR",
        "fosco": "FOSCO",
        "frotar": "FROTAR",
        "iniciar": "INICIAR",
        "nuevo"  : "INICIAR",
        "i"      : "INV",
        "inventa": "INV",
        "ver"    : "VER",
        "lee": "EXAMINAR",
        "leer": "EXAMINAR",
        "laro": "NO_MALDICION",
        "mapa"   : "MAP",
        "map"    : "MAP",
        "automap": "MAP",
        "mirar"  : "VER",
        "m"      : "VER",
        "n"      : "N",
        "s"      : "S",
        "e"      : "E",
        "o"      : "O",
        "olar": "SI_MALDICION",
        "poner": "DEJAR",
        "ragul": "RAGUL",
        "resid": "RESID",
        "rola": "NO_MALDICION",
        "sacar": "SACAR",
        "socorro": "AYUDA",
        "soltar": "SOLTAR",
        "salir"  : "FIN_JUEGO",
        "quit"  : "FIN_JUEGO",
        "exit"  : "FIN_JUEGO",
        "termina": "FIN_JUEGO",
        "fin": "FIN_JUEGO",
        "save": "GUARDAR_PARTIDA",
        "load": "CARGAR_PARTIDA",
        "cargar": "CARGAR_PARTIDA",
        "debug": "DEBUG",
    } # 38

    nombres = {
        "aguamar": "AGUAMARINA",
        "balanza": "BALANZA",
        "bosque" : "SETAS",
        "cadaver": "CADAVER",
        "cadáver": "CADAVER",
        "agua"   : "CHARCO",
        "charco" : "CHARCO",
        "circulo": "CIRCULO",
        "círculo": "CIRCULO",
        "cofre"  : "COFRE",
        "cuchill": "CUCHILLO",
        "diamant": "DIAMANTE",
        "diapaso": "DIAPASON",
        "dibujo" : "DIBUJO",
        "dibujos": "DIBUJO",
        # "edu"    : "EDU",
        "empanad": "EMPANADA",
        "esmeral": "ESMERALDA",
        "espejo" : "ESPEJO",
        "llave"  : "LLAVE",
        "figurit": "IDOLO",
        "fogon"  : "HORNO",
        "horno"  : "HORNO",
        "investi": "INVESTIGADOR",
        "inscrip": "INSCRIPCION",
        "ídolo": "IDOLO",
        "idolo": "IDOLO",
        "jade": "JADE",
        "lintern": "LINTERNA",
        "ojo"  : "OJOS",
        "ojos"  : "OJOS",
        "opalo"  : "OPALO",
        "ópalo"  : "OPALO",
        "placa" : "PLACA",
        "puerta" : "PUERTA",
        "pila"   : "PILA",
        "rubi"   : "RUBI",
        "rubí"   : "RUBI",
        "seta"   : "SETAS",
        "setas"  : "SETAS",
        "todo": "TODO",
        "topacio": "TOPACIO",
        "vara": "VARA",
        "zafiro" : "ZAFIRO",
    } # 36

    palabras_ignoradas = {
        "el", "la", "los", "las", "un", "una", "unos", "unas",  # Artículos
        "de", "del", "a", "al", "con", "sin", "por", "para", "en", "sobre", "entre", "tras",  # Preposiciones
        "y",  "u", "ni",  # Conjunciones # La "o", nos e puede ignorar
        "mi", "tu", "su", "sus", "mis", "tus", "nuestro", "nuestra", "vuestro", "vuestra",  # Posesivos
        "ese", "esa", "esos", "esas", "este", "esta", "estos", "estas", "aquel", "aquella", "aquellos", "aquellas",
        # Demostrativos
        "yo", "tú", "él", "ella", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas",
        # Pronombres personales
        "mío", "mía", "míos", "mías", "tuyo", "tuya", "suyo", "suya", "nuestro", "vuestra",  # Posesivos personales
        "lo", "cual", "quien", "cuyo", "cuyos", "cuyas",  # Pronombres relativos
        "que", "como", "cuando", "donde", "porque", "si", "aunque",  # Conectores
        "pero", "más", "menos", "también", "además", "aun", "todavía",  # Adverbios comunes
        "entonces", "después", "luego", "ahora", "antes", "mientras", "cuando",  # Términos temporales
        "muy", "poco", "mucho", "bastante", "demasiado", "casi", "solo", "tan", "tanto",  # Intensificadores
        "uno", "dos", "tres", "cuatro", "cinco", "muchos", "pocos", "varios", "algunos", "ninguno"
        # Cantidades generales
    }

    return verbos, nombres, palabras_ignoradas



# Esto aún no lo estoy usando
class Complemento:
    Vacio = 0 # No puede llevar una segunda palabra
    Nombre = 1 # La segunda palabra debe estar en la lista de nombres
    Cadena = 2 # Debe llegvar una palabra que nos e valida con la lista de nombres
    Cualquiera = 3 # No se valida si lleva algo o no

tokens = {
    "EXAMINAR": Complemento.Nombre,
    "N": Complemento.Vacio,
    "S": Complemento.Vacio,
    "E": Complemento.Vacio,
    "O": Complemento.Vacio,
    "GUARDAR_PARTIDA": Complemento.Cadena,
    "CARGAR_PARTIDA": Complemento.Cadena
}


### funciones ############################

def _procesar_cadena(cadena):
    CARACTERES = 7
    palabras = cadena.split()  # Divide la cadena en palabras
    palabras_procesadas = [palabra[:CARACTERES].lower() if len(palabra) > CARACTERES else palabra for palabra in palabras]
    return palabras_procesadas


def crear_comando(cadena):
    _, _, ignorar = vocabulario()
    palabras_bruto = _procesar_cadena(cadena)
    palabras = [p for p in palabras_bruto if p not in ignorar]
    if len(palabras) == 0:
        user_command = Comando.Vacio()
    elif len(palabras) == 1:
        user_command = comando(palabras[0])
    else:
        user_command = comando(palabras[0], palabras[1])

    return user_command


def comando(verbo, nombre="*"):
    verbos, nombres, _ = vocabulario()
    token_verbo = None

    for palabra, token in verbos.items():
        if palabra == verbo.lower():
            token_verbo = token
            break

    token_nombre = None
    if nombre == "*":
        token_nombre = nombre
    else:
        for palabra, token in nombres.items():
            if palabra == nombre.lower():
                token_nombre = token
                break
    return Comando(verbo = verbo, nombre = nombre, token_verbo=token_verbo, token_nombre=token_nombre)




@dataclass(frozen=True)
class Comando:

    @staticmethod
    def Vacio():
        return Comando(None, None, None, None)

    """
    Clase inmutable que representa una acción con un verbo, un nombre, y un token asociado.
    """
    verbo: str
    nombre: str
    token_verbo: str
    token_nombre: str

    def es_vacio(self):
        return self.token_verbo is None

    def __str__(self):
        """
        Devuelve una descripción completa de la acción.
        """
        return f"Acción: {self.verbo} {self.nombre} (Tokens: {self.token_verbo}, {self.token_nombre})"


###############################

class AnaLex(object):

    def __init__(self, verbs, names, ignores, output):
        self._verbs = verbs
        self._names = names
        self._output = output
        self._ignores = ignores

    def procesar_palabras(self, palabras):
        comando_jugador = self._crear_comando(palabras)
        es_valido = True

        # Ver si existen
        if comando_jugador.es_vacio():
            self._output.print("Verbo no encontrado.")
            es_valido = False

        if not comando_jugador.es_vacio() and comando_jugador.token_nombre is None:
            self._output.print("Nombre no encontrado.")
            es_valido = False

        return comando_jugador, es_valido

    def _crear_comando(self, cadena):
        palabras_bruto = self._procesar_cadena(cadena)
        palabras = [p for p in palabras_bruto if p not in self._ignores]
        if len(palabras) == 0:
            user_command = Comando.Vacio()
        elif len(palabras) == 1:
            user_command = self._comando(palabras[0])
        else:
            user_command = self._comando(palabras[0], palabras[1])

        return user_command

    def _comando(self,verbo, nombre="*"):
        token_verbo = None

        for palabra, token in self._verbs.items():
            if palabra == verbo.lower():
                token_verbo = token
                break

        token_nombre = None
        if nombre == "*":
            token_nombre = nombre
        else:
            for palabra, token in self._names.items():
                if palabra == nombre.lower():
                    token_nombre = token
                    break
        return Comando(verbo=verbo, nombre=nombre, token_verbo=token_verbo, token_nombre=token_nombre)

    def _procesar_cadena(self, cadena):
        CARACTERES = 7
        palabras = cadena.split()  # Divide la cadena en palabras
        palabras_procesadas = [palabra[:CARACTERES].lower() if len(palabra) > CARACTERES else palabra for palabra in palabras]
        return palabras_procesadas

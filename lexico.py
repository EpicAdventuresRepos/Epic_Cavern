
def vocabulario():
    verbos = {
        "encende": "ENCENDER",
        "abrir"  : "ABRIR",
        "atacar" : "ATACAR",
        "golpear": "ATACAR",
        "romper": "ATACAR",
        "coger"  : "COGER",
        "recoger": "COGER",
        "dar"    : "DAR",
        "ofrecer": "DAR",
        "dejar"  : "DEJAR",
        "poner"  : "DEJAR",
        "ragul": "RAGUL",
        "resid": "RESID",
        "sacar"  :"SACAR",
        "soltar" : "SOLTAR",
        "fosco": "FOSCO",
        "frotar" : "FROTAR",
        "i"      : "INV",
        "inventa": "INV",
        "ver"    : "VER",
        "mirar"  : "VER",
        "m"      : "VER",
        "ex"     : "EXAMINAR",
        "examina": "EXAMINAR",
        "lee": "EXAMINAR",
        "leer"   : "EXAMINAR",
        "n"      : "N",
        "s"      : "S",
        "e"      : "E",
        "o"      : "O",
        "edu"    : "EDU",
        "salir"  : "FIN_JUEGO",
        "quit"  : "FIN_JUEGO",
        "exit"  : "FIN_JUEGO",
        "termina": "FIN_JUEGO",
        "fin": "FIN_JUEGO",
        "save": "GUARDAR_PARTIDA",
        "load": "CARGAR_PARTIDA",
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

    return verbos, nombres



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

def comando(verbo, nombre="*"):
    verbos, nombres = vocabulario()
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


from dataclasses import dataclass

@dataclass(frozen=True)
class Comando:
    """
    Clase inmutable que representa una acción con un verbo, un nombre, y un token asociado.
    """
    verbo: str
    nombre: str
    token_verbo: str
    token_nombre: str

    def __str__(self):
        """
        Devuelve una descripción completa de la acción.
        """
        return f"Acción: {self.verbo} {self.nombre} (Tokens: {self.token_verbo}, {self.token_nombre})"
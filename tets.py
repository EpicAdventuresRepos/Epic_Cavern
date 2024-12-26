import unittest

from epic_cavern.datos import Localizacion, Resultado, Global
from epic_cavern.lexico import Comando, comando


def procesar_cadena(cadena):
    """
    Divide una cadena en palabras y limita a 6 letras cualquier palabra que tenga más de 6 caracteres.

    Args:
        cadena (str): La cadena de entrada.

    Returns:
        str: Una nueva cadena con palabras procesadas.
    """
    palabras = cadena.split()  # Divide la cadena en palabras
    palabras_procesadas = [palabra[:6] if len(palabra) > 6 else palabra for palabra in palabras]
    return palabras_procesadas


class TestLocalizacion(unittest.TestCase):

    def test_no_hay_metodo(self):
        loc = Localizacion("", "")
        c = Comando("verbo", "nombre", "AIR", "PUERTA")
        self.assertEqual(loc.run_command(c), Resultado.NO_HECHO)  # add assertion here

    def test_comando_norte(self):
        loc1 = Localizacion("1", "")
        loc2 = Localizacion("2", "")
        loc1.conectar(0, loc2)
        estado = Global.get_instance()
        estado.set_localizacion(loc1)
        c = Comando("verbo", "nombre", "N", "*")
        self.assertEqual(loc1.run_command(c), Resultado.REINICIA)  # add assertion here
        self.assertEqual(estado.localizacion().nombre, "2")  # add assertion here

    def test_direcciones_dos_sentidos(self):
        loc1 = Localizacion("1", "")
        loc2 = Localizacion("2", "")
        loc1.conectar(0, loc2)
        self.assertEqual(len(loc2.conexiones), 1)  # add assertion here
        self.assertTrue(1 in loc2.conexiones)

    def test_procesar_cadena(self):
        self.assertListEqual(procesar_cadena("hola caracola"), ["hola", "caraco"])

    def test_primera_vez(self):
        loc = Localizacion("", "")
        loc._primera_vez ="primera"
        expected = "Te encuentras en . \n"
        expected_primera = expected + "primera\n"
        self.assertEqual(loc._primera_vez, "primera")
        self.assertEqual(loc.mostrar_descripcion(), expected_primera)
        #self.assertEqual(loc.mostrar_descripcion(), expected)



class Test_Lexico(unittest.TestCase):

    def test_comando_2_PALABRAS(self):
        c = comando("recoger", "pila")
        self.assertEqual(c.verbo, "recoger")  # add assertion here
        self.assertEqual(c.token_verbo, "COGER")

    def test_comando_1_PALABRa(self):
        c = comando("recoger")

        self.assertEqual(c.token_verbo, "COGER")
        self.assertEqual(c.token_nombre, "*")


if __name__ == '__main__':
    unittest.main()

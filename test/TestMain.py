import unittest

from epic_cavern.lexico import Comando
from epic_cavern.main import procesar_cadena, procesar_palabras, load_data, cmd_examinar_inventario
from epic_cavern.test.test_helppers import BaseTest


class MyTestCase(BaseTest):

    def setUp(self):
        super().setUp("loc31_Inscripción")
        load_data()

    def test_examinar_inscripcion(self):
        palabras = procesar_cadena("ex inscripcion")
        self.assertEqual(["ex", "inscrip"], palabras)
        user_command, valido = procesar_palabras(palabras, self.test_output)
        self.assertEqual(True, valido)  # add assertion here

    def test_examinar_obj_en_inventario(self):
        self.add_rubi_inventario()
        comando = Comando("no", "no", "EXAMINAR", "RUBI")
        cmd_examinar_inventario(comando)
        self.assertEqual("Rubí rojo.",  self.test_output.last_line())

    def test_procesa_entrada_vacia(self):
        c, v = procesar_palabras(list(), self.test_output)
        self.assertFalse(v)
        self.assertIsNone(c)



if __name__ == '__main__':
    unittest.main()

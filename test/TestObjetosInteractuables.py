import unittest

from epic_cavern.datos import Global, Investigador, Resultado, ObjetoAventura, CofreAbreCierra, ExaminableEncuentra, \
    Espejo, CofreMimico
from epic_cavern.lexico import Comando
from epic_cavern.test.test_helppers import BaseTest



class TestPNJ(BaseTest):

    def setUp(self):
        super().setUp("loc3_Investigador")
        self.loc.pnj = Investigador("Investigador", "To-Do", "Primera", token="INVESTIGADOR")

    def test_primera_vez_pnj(self):
        desc = self.estado._locs["loc3_Investigador"].mostrar_descripcion()
        #print(desc)
        self.assertIn("Primera", desc)
        desc = self.estado._locs["loc3_Investigador"].mostrar_descripcion()
        #print(desc)
        self.assertIn("Investigador está aquí.", desc)

    def test_examinar_dibujos_otra_loc(self):
        comando = Comando("no", "no", "EXAMINAR", "INSCRIPCION")
        expected_msg = "No hay nada que examinar"
        result = self.estado._locs["loc3_Investigador"].run_command(comando)

        self.assertEqual(Resultado.HECHO, result)
        self.assertEqual(self.test_output.last_line(), expected_msg)

    def test_dar_idolo(self):
        self.estado.añade_inventario("IDOLO", self.obj_idolo())

        comando = Comando("no", "no", "DAR", "IDOLO")
        expected_msg = "Le das el ídolo.\n'Muy interesante, voy a estudiarlo. Puede que nos veamos pronto'\nEl investigador se marcha."

        self.assertIsNone(self.estado._locs["loc22_Puerta"].pnj)
        result = self.estado._locs["loc3_Investigador"].run_command(comando)
        # Se ha movido
        self.assertEqual(result, Resultado.HECHO)
        self.assertIsNone(self.estado._locs["loc3_Investigador"].pnj)
        self.assertIsNotNone(self.estado._locs["loc22_Puerta"].pnj)
        self.assertEqual(self.test_output.last_line(), expected_msg)

    def test_leer_inscripcion(self):
        self.estado.localizacion_actual = self.estado._locs["loc22_Puerta"]
        comando = Comando("no", "no", "EXAMINAR", "INSCRIPCION")
        self.estado.localizacion_actual.run_command(comando)
        last_line = self.test_output.last_line()
        # print(last_line)
        self.assertEqual(last_line, "Está escrita en un idioma antiguo y no la entiendes.")

        self.estado._locs["loc22_Puerta"].pnj = Investigador("Investigador", "To-Do", "Primera")
        self.estado.localizacion_actual.run_command(comando)
        last_line = self.test_output.last_line()
        # print(last_line)
        self.assertTrue(last_line.startswith("El investigador se acerca"))

    def test_examinar(self):
        expected_msg = "To-Do"
        last_line, resultado = self.comando("EXAMINAR", "INVESTIGADOR")
        self.assertEqual(resultado, Resultado.HECHO)
        print(last_line)
        self.assertEqual(expected_msg, last_line)


########################################

class TestCofre(BaseTest):

    def setUp(self):
        super().setUp("loc3_Investigador")
        self.cofre = CofreAbreCierra()
        self.loc.interactivos.append(self.cofre)

    def test_examinar_cofre(self):
        expected_msg = "Un cofre. Está cerrado."
        last_line, _ = self.comando("EXAMINAR", "COFRE")
        self.assertEqual(expected_msg, last_line)

        comando = Comando("no", "no", "ABRIR", "COFRE")
        expected_msg = "Un cofre. Está abierto."
        self.loc.run_command(comando)

        last_line, _ = self.comando("EXAMINAR", "COFRE")
        self.assertEqual(expected_msg, last_line)

    def test_abrir_cofre_vacio(self):
        last_line, _ = self.comando("ABRIR", "COFRE")
        expected_msg = "Abres el cofre."
        self.assertEqual(last_line, expected_msg)

        last_line, _ = self.comando("ABRIR", "COFRE")
        self.assertEqual(last_line, "Ya está abierto.")

    def test_abrir_cofre_con_objeto(self):
        self.assertEqual(len(self.loc.objetos), 0)
        self.cofre._obj_contenido = ObjetoAventura("TEST", "TEST", "TEST", "TEST")
        last_line, result = self.comando("ABRIR", "COFRE")
        self.assertIsNone(self.cofre._obj_contenido)
        self.assertEqual(len(self.loc.objetos), 1)
        self.assertEqual(result, Resultado.HECHO)
        # Mensaje "Encuentras TEST"

        last_line, _ = self.comando("ABRIR", "COFRE")
        self.assertIsNone(self.cofre._obj_contenido)
        self.assertEqual(len(self.loc.objetos), 1)

    def test_abrir_cofre_con_llave_no_inventario(self):
        llave = self.obj_cuchillo()
        self.cofre = CofreAbreCierra(token_llave_abrir=llave.token)
        self.loc.interactivos = (self.cofre,)
        #print(self.loc.interactivos)
        #print(self.cofre.comandos)
        last_line, result = self.comando("ABRIR", "COFRE")
        self.assertEqual(result, Resultado.HECHO)
        self.assertEqual(last_line, "No tienes la llave.")

    def test_abrir_cofre_con_llave_en_inventario(self):
        llave = self.obj_cuchillo()
        self.add_inventario(llave)
        self.cofre = CofreAbreCierra(token_llave_abrir=llave.token)
        self.loc.interactivos = (self.cofre,)

        last_line, result = self.comando("ABRIR", "COFRE")
        # print(last_line)
        #self.assertIsNone(self.cofre._obj_contenido)
        #self.assertEqual(len(self.loc.objetos), 1)
        self.assertEqual(result, Resultado.HECHO)
        self.assertTrue(self.cofre._abierto)
        self.assertEqual(len(self.estado.inventario), 1)

########################################

class TestCofreMimico(BaseTest):

    def setUp(self):
        super().setUp("loc3_Investigador")
        self.cofre = CofreMimico()
        self.loc.interactivos.append(self.cofre)

    def test_no_tienes_emmpanada(self):
        last_line, result = self.comando("DAR", "EMPANADA")
        self.assertEqual(result, Resultado.HECHO)
        self.assertEqual(last_line, "No tienes una empanada.")

    def test_tienes_emmpanada(self):
        self.add_inventario(self.obj_empanada())
        last_line, result = self.comando("DAR", "EMPANADA")
        self.assertEqual(result, Resultado.HECHO)
        self.assertFalse(self.estado.en_inventario("EMPANADA"))
        # self.assertEqual(last_line, "No tienes una empanada.")

################################

class TestExaminableEncontrar(BaseTest):

    def setUp(self):
        super().setUp("loc3_Investigador")
        self.examinable = ExaminableEncuentra("descripcion", self.obj_idolo(), "CHARCO")
        self.loc.interactivos.append(self.examinable)

    def test_examinar(self):
        # To-Do. Corregir la mayúscula.
        expected_msg = "Encuentras Un ídolo."
        last_line, _ = self.comando("EXAMINAR", "CHARCO")
        self.assertEqual(expected_msg, last_line)

        expected_msg = "descripcion"
        last_line, _ = self.comando("EXAMINAR", "CHARCO")
        self.assertEqual(expected_msg, last_line)

    def test_abrir(self):
        last_line, result = self.comando("ABRIR", "CHARCO")
        self.assertEqual(result, Resultado.NO_HECHO)

###################

class TestEspejo(BaseTest):

    def setUp(self):
        super().setUp("loc3_Investigador")
        self.examinable = Espejo()
        self.loc.interactivos.append(self.examinable)

    def test_morir(self):
        expected_msg = "Encuentras Un ídolo."
        last_line, resultado = self.comando("ATACAR", "ESPEJO")
        self.assertEqual(Resultado.FIN_JUEGO, resultado)


    def test_sin_dapason(self):
        expected_msg = "Una terrible criatura se refleja en el espejo copiando todos tus movimientos.\n"
        last_line, _ = self.comando("EXAMINAR", "ESPEJO")
        self.assertEqual(expected_msg, last_line)

        self.add_inventario(self.obj_vara())
        last_line, _ = self.comando("ATACAR", "DIAPASON")
        #print(last_line)
        self.assertTrue(self.examinable._espejo_entero)
        expected_msg = "No lo llevas.\n"
        self.assertEqual(expected_msg, last_line)

    def test_romper_espejo(self):
        self.add_inventario(self.obj_diapason())
        last_line, _ = self.comando("ATACAR", "DIAPASON")
        #print(last_line)
        self.assertFalse(self.examinable._espejo_entero)
        expected_msg = "El sonido agudo del diapasón hace tempblar al espejo hasta que se rompe. Entre sus trozos ves algo que brilla.\n"
        self.assertEqual(expected_msg, last_line)
        last_line, _ = self.comando("EXAMINAR", "ESPEJO")
        expected_msg = "El espejo está hecho pedazos y nada se refleja.\n"
        self.assertEqual(expected_msg, last_line)
        self.assertEqual(len(self.loc.objetos), 1)

        last_line, _ = self.comando("ATACAR", "DIAPASON")
        expected_msg = "No pasa nada.\n"
        self.assertEqual(expected_msg, last_line)


if __name__ == '__main__':
    unittest.main()

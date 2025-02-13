import unittest

from epic_cavern.datos import Global
from epic_cavern.main import main_game, load_data, load_interfaces
from epic_cavern.test.test_helppers import LastLineOutput, AutomaticInput, AllLinesOutput


class MyTestCase(unittest.TestCase):

    def _commands(self, commands):
        Global._instance._input.set_commands(commands)

    def _estoy_en(self):
        return self.estado.localizacion().nombre()

    def _run(self, commands, show=False):
        commands_fin = list(commands)
        commands_fin.append("FIN")
        self._commands(commands_fin)
        if show:
            print(commands_fin)
        main_game()

    def setUp(self):
        load_data()
        # load_interfaces()

        Global._instance = None
        Global.get_instance()
        self._out = AllLinesOutput()
        Global._instance._output = self._out
        Global._instance._input = AutomaticInput()
        self.estado = Global.get_instance()
        load_data()

    def test_empanada_al_mimico(self):
        self._run(("S", "S", "S", "O"))
        #print(self._out._lines[-3:])
        self.assertEqual("loc28_Cocina", self._estoy_en())  # add assertion here

        self._commands(( "ABRIR HORNO", "COGER EMPANADA", "I", "FIN"))
        main_game()
        #print(self._out._lines[-3:])
        self.assertEqual("Una empanada", self._out.last_line(2))

        self._commands(( "E", "S", "leer inscripcion", "FIN"))
        main_game()
        #print(self._out._lines[-3:])
        self.assertEqual("No den de comer al cofre.", self._out.last_line(2))

        #self._out.trace_on()
        self._run(( "S", "dar empanada", "I")) # "abrir cofre",
        #print(self._out._lines[-3:])
        #print(self._out._lines)
        self.assertEqual("Saltas hacia atrás justo a tiempo de que no te arranque la mano.", self._out.last_line(3))
        self.assertEqual("Llevas:", self._out.last_line(2))

    def test_abrir_cofre_con_llave_y_coger_esmeralda(self):
        # self._out.trace_on()
        #self._run(("S", "S", "S", "S", "E", "N", "coger llave", "I"))
        self.test_coger_llave_del_charco()
        # self.assertEqual("loc38_Llave", self._estoy_en())
        self.assertEqual("Una llave oxidada", self._out.last_line(2))
        #self._run(("S", "O", "O", "abrir cofre", "coger zafiro", "I"))
        self._run(("N", "O", "O", "O", "N", "O", "O", "O"))
        self.assertEqual("loc33_Cofre_auténtico", self._estoy_en())
        self._run(("abrir cofre", "coger zafiro", "I"))
        self.assertEqual("Llevas:", self._out.last_line(4))
        self.assertEqual("Una llave oxidada", self._out.last_line(3))
        self.assertEqual("Un zafiro", self._out.last_line(2))

    def test_diapason_y_teletransporte_1(self):
        # self._out.trace_on()
        self._run(("S", "S", "S", "S", "E", "E", "S", "S", "coger diapason", "I"))
        self.assertEqual("loc48_Sala_de_música", self._estoy_en())
        self.assertEqual("Un diapasón", self._out.last_line(2))
        self._run(("O", "O", "ex inscripción", "edu"))
        self.assertEqual("loc1_Caida", self._estoy_en())
        # self.assertEqual("", self._out.last_line(2))

    def test_dar_idolo_investigador(self):
        #self._out.trace_on()
        self._run(("S", "S", "S", "S", "E", "E", "S", "E", "N", "coger idolo", "I"))
        self.assertEqual("loc55_Ídolo", self._estoy_en())
        self.assertEqual("Un ídolo", self._out.last_line(2))
        self._run(("S", "O", "N", "O", "O", "N", "N", "N", "E", "ex investigador", "dar idolo", "I"))
        self.assertEqual("loc3_Investigador", self._estoy_en())
        #print(self._out._lines[-10:])
        exp = "Le das el ídolo.\n'Muy interesante, voy a estudiarlo. Puede que nos veamos pronto'\nEl investigador se marcha."
        self.assertEqual(exp, self._out.last_line(3))
        self.assertEqual("Llevas:", self._out.last_line())

    def test_abrir_puerta_investigador_y_Coger_diamante(self):
        self.test_dar_idolo_investigador()

        self._run(("E", "E", "S", "E", "ex dibujos"))
        # print(self._out._lines[-5:])
        self.assertTrue(self._out.last_line().startswith("Te llaman la atención tres dibujos"))
        self._run(("O", "O", "leer inscripción"))
        #print(self._out._lines[-5:])
        #print(self._out.last_line())
        self.assertTrue(self._out.last_line().startswith("El investigador se acerca."))
        # self._out.trace_on()
        self._run(("ex puerta", "resid", "m", "coger topacio", "I"))
        #print(self._out._lines[-6:])
        self.assertEqual("Un topacio", self._out.last_line())

    def test_derrotar_espejo(self):
        # self._out.trace_on()
        self.test_diapason_y_teletransporte_1()
        self._run(("S", "E", "E", "E", "S", "S", "E", "E", "ex dibujos"))
        self.assertEqual("loc80_Guardián_del_espejo", self._estoy_en())
        self._run(("golpear diapason", "coger opalo", "I"))
        #print(self._out._lines[-6:])
        self.assertEqual("Un ópalo", self._out.last_line())

    def test_coger_vara(self):
        self.test_coger_llave_del_charco()
        #self._out.trace_on()
        self._run(("N", "O", "S"))
        #print(self._out._lines[-6:])
        self.assertEqual("loc59_Cadáver_y_derrumbamiento", self._estoy_en())
        self._run(("ex cadaver", "coger vara", "i"))
        self.assertEqual("Una vara dorada", self._out.last_line())
        #self.fail()

    def test_coger_ojo_rojo(self):
        self.test_coger_vara()
        self.assertEqual("loc59_Cadáver_y_derrumbamiento", self._estoy_en())
        # self._out.trace_on()
        self._run(("N", "N", "N", "O", "S"))
        self.assertEqual("loc92_Cuchillo_maldito", self._estoy_en())
        self._run(("olar", "coger cuchillo", "i"))
        self._run(("N", "N", "N", "E", "E", "frotar vara", "ex ojos", "sacar ojo", "m", "coger rubi", "i"))
        #print(self._out._lines[-8:])
        self.assertEqual("loc15_Ojos_rojos", self._estoy_en())
        self.assertEqual("Un rubí", self._out.last_line())
        self.assertEqual("Un cuchillo", self._out.last_line(3))
        self.assertEqual("Una vara dorada", self._out.last_line(4))

    def test_coger_diamante(self):
        self.test_coger_vara()
        #self._out.trace_on()
        self._run(("N", "N", "N", "O", "N", "N", "O", "O", "O", "S", "S", "S", "E", "E", "N"))
        #print(self._out._lines[-6:])
        self._run(("frotar vara", "m", "coger diamante", "i"))
        self.assertEqual("loc43_Oscura", self._estoy_en())
        self.assertEqual("Un diamante", self._out.last_line())

    def test_balanza_y_coger_esmeralda(self):
        self.test_diapason_y_teletransporte_1()
        # self._out.trace_on()
        self._run(("S", "E", "E", "N", "E", "ex balanza", "ex balanza", "dejar diapason", "coger esmeralda", "m", "i"))
        # print(self._out._lines[-6:])
        self.assertEqual("loc9_Balanza", self._estoy_en())
        self.assertEqual("Llevas:", self._out.last_line(3))
        self.assertEqual("Una esmeralda", self._out.last_line())

    def test_camino_del_heroe_y_coger_jade(self):
        self.test_coger_llave_del_charco()
        self._run(("N", "E", "N", "N", "ex inscripcion"))
        self.assertEqual("loc87_Viaje_del_héroe", self._estoy_en())
        self.assertTrue(self._out.last_line().startswith("Utur atravesó"))
        self._run(("O", "N", "E", "E", "coger jade", "I"))
        self.assertEqual("loc90_Teletransporte", self._estoy_en())
        self.assertEqual("Un jade", self._out.last_line())
        # self._out.trace_on()
        # print(self._out._lines[-6:])
        self._run(("edu",))
        self.assertEqual("loc50_Teletransporte", self._estoy_en())

    def test_salida_sin_todas_gemas(self):
        self.test_coger_llave_del_charco()
        #self._out.trace_on()
        self._run(("N", "E", "E", "E", "S"))
        self.assertEqual("loc71_Salida", self._estoy_en())
        # print(self._out._lines[-6:])
        self.assertTrue(self._out.last_line().startswith("No has conseguido todas las gemas"))

    def test_coger_llave_del_charco(self):
        # self._out.trace_on()
        # self.test_diapason_y_teletransporte_1()
        self._run(("S", "E", "E", "E", "S", "S", "E", "S", "S", "E", "S", "ex charco", "coger llave", "i"))
        self.assertEqual("loc63_Charco", self._estoy_en())
        self.assertEqual("Una llave oxidada", self._out.last_line())

    def test_coger_cuchillo_y_morir(self):
        # self._out.trace_on()
        self._run(("S", "E", "E", "E", "S", "S", "S", "coger cuchillo", "i"))
        self.assertEqual("loc92_Cuchillo_maldito", self._estoy_en())
        self.assertIn("Mueres", self._out.last_line())

    def test_palabras_que_no_quitan_maldicion(self):
        # self._out.trace_on()
        self._run(("S", "E", "E", "E", "S", "S", "S", "rola", "laro", "arol", "coger cuchillo", "i"))
        self.assertEqual("loc92_Cuchillo_maldito", self._estoy_en())
        self.assertIn("Mueres", self._out.last_line())

    def test_coger_cuchillo(self):
        # self._out.trace_on()
        self._run(("S", "E", "E", "E", "S", "S", "S", "olar", "coger cuchillo", "i"))
        self.assertEqual("loc92_Cuchillo_maldito", self._estoy_en())
        self.assertEqual("Un cuchillo", self._out.last_line())

    def test_palabra_maldicion_otra_loc(self):
        #self._out.trace_on()
        self._run(("olar", "rola",), False)
        self.assertEqual("No pasa nada.", self._out.last_line())
        self.assertEqual("No pasa nada.", self._out.last_line(2))


if __name__ == '__main__':
    unittest.main()

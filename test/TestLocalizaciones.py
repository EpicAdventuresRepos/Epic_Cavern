import unittest

from epic_cavern.datos import Investigador, LocalizacionIlusiones, LocalizacionBalanza, Resultado, LocalizacionOscura, \
    LocalizacionOjos, LocalizacionLosetas, LocalizacionFinal, ObjetoGema, LocalizacionObjetoMaldito, ObjetoMaldito
from epic_cavern.test.test_helppers import BaseTest


class TestLocalizacion(BaseTest):
    def setUp(self):
        super().setUp("loc22_Puerta")

    def test_coger_objeto(self):
        self.loc.agregar_objeto("IDOLO", self.obj_idolo())
        self.assertEqual(len(self.loc.objetos), 1)
        #print(self.loc.objetos)
        last_line, resultado = self.comando("COGER", "IDOLO")
        #print(last_line)
        #print(self.estado.inventario)
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual(len(self.estado.inventario), 1)
        self.assertEqual(len(self.loc.objetos), 0)

    def test_dejar_objeto(self):
        self.estado.añade_inventario("IDOLO", self.obj_idolo())
        last_line, resultado = self.comando("DEJAR", "IDOLO")
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual(len(self.estado.inventario), 0)
        self.assertEqual(len(self.loc.objetos), 1)

    def test_coger_todo(self):
        self.add_loc(self.obj_cuchillo())
        self.add_loc(self.obj_diapason())
        last_line, resultado = self.comando("COGER", "TODO")
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual(len(self.estado.inventario), 2)

#######

class TestLoc22_Puerta(BaseTest):

    def setUp(self):
        super().setUp("loc22_Puerta")
        self.pnj = Investigador("Investigador", "To-Do", "Primera")

    def test_inscripcion_sin_investigador(self):
        expected_msg = "Está escrita en un idioma antiguo y no la entiendes."
        last_line, _ = self.comando("EXAMINAR", "INSCRIPCION")
        self.assertEqual(expected_msg, last_line)

    def test_inscripcion_con_investigador(self):
        self.loc.pnj = self.pnj
        expected_msg = "El investigador se acerca"
        last_line, _ = self.comando("EXAMINAR", "INSCRIPCION")
        self.assertTrue(last_line.startswith(expected_msg))

#########

class TestLocalizacionBalanza(BaseTest):
    def setUp(self):
        super().setUp("loc22_Puerta")
        self.loc = LocalizacionBalanza("xx", "xx")

    def test_poner_objeto(self):
        self.loc.init_objeto_primer_plato("IDOLO", self.obj_idolo())
        self.assertIsNotNone(self.loc._obj_primer_plato)
        self.assertEqual(len(self.loc.objetos), 1)

    def test_coger_unico_objeto(self):
        self.loc.init_objeto_primer_plato("IDOLO", self.obj_idolo())
        #print(self.loc.objetos)
        last_line, resultado = self.comando("COGER", "IDOLO")
        #print(last_line)
        self.assertEqual(Resultado.FIN_JUEGO, resultado)
        self.assertEqual("Un potente chorro de ácido sale de la boca de la serpiente. Mueres rápido.", last_line)

    def test_dejar_segundo_objeto(self):
        self.loc.init_objeto_primer_plato("IDOLO", self.obj_idolo())
        self.add_rubi_inventario()
        #print(self.loc.objetos)
        last_line, resultado = self.comando("DEJAR", "RUBI")
        #print(last_line)
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual("Dejaste el RUBI en el segundo plato de la balanza de piedra.", last_line)
        self.assertIsNotNone(self.loc._obj_segundo_plato)

    def test_dejar_objeto_que_no_llevo(self):
        self.loc.init_objeto_primer_plato("IDOLO", self.obj_idolo())
        last_line, resultado = self.comando("DEJAR", "RUBI")
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual("No tienes RUBI en tu inventario", last_line)
        self.assertIsNone(self.loc._obj_segundo_plato)

    def test_coger_objeto_despues_dejar_objeto(self):
        self.loc.init_objeto_primer_plato("IDOLO", self.obj_idolo())
        self.add_rubi_inventario()
        #print(self.loc.objetos)
        last_line, resultado = self.comando("DEJAR", "RUBI")
        #print(last_line)
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual("Dejaste el RUBI en el segundo plato de la balanza de piedra.", last_line)
        self.assertIsNotNone(self.loc._obj_segundo_plato)
        last_line, resultado = self.comando("COGER", "IDOLO")
        #print(last_line)
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual("Ok.", last_line)
        self.assertIsNotNone(self.loc._obj_segundo_plato)
        self.assertIsNone(self.loc._obj_primer_plato)

    def test_descripcion(self):
        self.loc.init_objeto_primer_plato("IDOLO", self.obj_idolo())
        self.add_rubi_inventario()
        # print(self.loc.objetos)
        last_line, resultado = self.comando("DEJAR", "RUBI")
        last_line, resultado = self.comando("EXAMINAR", "BALANZA")
        #print(last_line)
        self.assertEqual(resultado, Resultado.HECHO)
        self.assertIn("En el primer plato hay", last_line)
        self.assertIn("En el segundo plato hay", last_line)

######################

class TestLocalizacionOscura(BaseTest):
    def setUp(self):
        super().setUp("loc74_Ilusiones")
        loc74_Ilusiones = self.loc
        self.loc = LocalizacionOscura("xx", "Hay luz.")
        self.loc.conectar(0, loc74_Ilusiones)
        self.add_inventario(self.obj_vara())

    def test_descripción(self):
        expected = "Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\nPuedes ir hacia: N.\n"
        #expected = "Llegas a una caverna vacía. Ves una inscripción en una de las paredes de esta caverna."
        #print(self.loc.mostrar_descripcion())
        self.assertEqual(expected, self.loc.mostrar_descripcion())

    def test_frotar_barra(self):
        last_line, resultado = self.comando("FROTAR", "VARA")
        expected = "Hay luz.\nPuedes ir hacia: N.\n"
        # print(self.loc.mostrar_descripcion())
        self.assertEqual(expected, self.loc.mostrar_descripcion())

    def test_al_salir_se_apaga_luz(self):
        last_line, resultado = self.comando("FROTAR", "VARA")
        last_line, resultado = self.comando("N", "")
        self.assertEqual(resultado, Resultado.REINICIA)
        last_line, resultado = self.comando("S", "")
        expected = "Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\nPuedes ir hacia: N.\n"
        # print(self.loc.mostrar_descripcion())
        self.assertEqual(expected, self.loc.mostrar_descripcion())

######################

class TestLocalizacionOjos(BaseTest):
    def setUp(self):
        super().setUp("loc74_Ilusiones")
        self.loc = LocalizacionOjos("xx", "Hay luz.")
        self.add_inventario(self.obj_vara())

    def test_morir(self):
        #expected = "Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\nPuedes ir hacia: N.\n"
        # print(self.loc.mostrar_descripcion())
        last_line, resultado = self.comando("COGER", "OJOS")
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        last_line, resultado = self.comando("EXAMINAR", "OJOS")
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        last_line, resultado = self.comando("SACAR", "OJOS")
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        self.comando("FROTAR", "VARA")
        last_line, resultado = self.comando("COGER", "OJOS")
        self.assertEqual(resultado, Resultado.HECHO)
        last_line, resultado = self.comando("EXAMINAR", "OJOS")
        self.assertEqual(resultado, Resultado.HECHO)

    def test_sacar_ojo(self):
        #expected = "Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\nPuedes ir hacia: N.\n"
        # print(self.loc.mostrar_descripcion())
        self.comando("FROTAR", "VARA")
        last_line, resultado = self.comando("SACAR", "OJOS")
        expected = "No tienes nada con qué sacarlo.\n"
        self.assertEqual(last_line, expected)
        self.assertEqual(len(self.loc.objetos), 0)
        self.add_inventario(self.obj_cuchillo())

        last_line, resultado = self.comando("SACAR", "OJOS")
        # print(last_line)
        expected = "Sacas el ojo de la pared. Es un rubí de gran valor.\n"
        self.assertEqual(last_line, expected)
        self.assertEqual(len(self.loc.objetos), 1)

    def test_interactuar_despues_sacar_ojo(self):
        #expected = "Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\nPuedes ir hacia: N.\n"
        # print(self.loc.mostrar_descripcion())
        self.comando("FROTAR", "VARA")
        self.add_inventario(self.obj_cuchillo())
        last_line, resultado = self.comando("SACAR", "OJOS")

        last_line, resultado = self.comando("EXAMINAR", "OJOS")
        expected = "El otro ojo también es un rubí de gran valor, pero es imposible sacarlo de la pared.\n"
        self.assertEqual(last_line, expected)
        last_line, resultado = self.comando("SACAR", "OJOS")
        expected = "Es imposible sacarlo de la pared.\n"
        self.assertEqual(last_line, expected)


######################

class TestLocalizacionLosetas(BaseTest):
    def setUp(self):
        super().setUp("loc74_Ilusiones")
        otra_loc = self.loc
        self.loc = LocalizacionLosetas("Sin uso", "Sin uso", 0)
        # self.add_inventario(self.obj_vara())
        self.loc._losetas = {"E":"", "N":"", "O":""}
        self.loc.conectar(0, otra_loc, False)

    def test_descripción_loc(self):
        expected = "Sin uso\n"
        # print(self.loc.mostrar_descripcion())
        #last_line, resultado = self.comando("COGER", "OJOS")
        descripcion = self.loc.mostrar_descripcion()
        self.assertEqual(expected, descripcion)

    def test_No_hay_salida(self):
        expected = "No hay salida"
        # print(self.loc.mostrar_descripcion())
        last_line, resultado = self.comando("S", "")
        self.assertEqual(resultado, Resultado.HECHO)

    def test_pisas_losetA_y_mueres(self):
        expected = "Sin uso\nPuedes ir hacia: \n"
        # print(self.loc.mostrar_descripcion())
        last_line, resultado = self.comando("E", "")
        # print(last_line)
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        last_line, resultado = self.comando("O", "")
        self.assertEqual(resultado, Resultado.FIN_JUEGO)

    def test_pisas_losetA_correcta(self):
        expected = "Sin uso\nPuedes ir hacia: \n"
        # print(self.loc.mostrar_descripcion())
        last_line, resultado = self.comando("N", "")
        # print(last_line)
        self.assertEqual(resultado, Resultado.REINICIA)
        # Comprobar que vas a otra LOC
        self.assertEqual(self.estado.localizacion().nombre, "loc74_Ilusiones")

#######################

class TestMoverseLosetas(BaseTest):
    def setUp(self):
        super().setUp("loc89_Losetas")

    def test_descripción_loc(self):
        expected = "Ante ti tienes tres losetas: la del este refulge con chispas mágicas, la del norte está llena de arena y la del oeste tiene una roca.\nTienes que pisar una de ellas.\n"
        #last_line, resultado = self.comando("COGER", "OJOS")
        descripcion = self.loc.mostrar_descripcion()
        # print(descripcion)
        self.assertEqual(expected, descripcion)

    def test_de_la_1_a_la_2(self):
        self.assertEqual(self.loc._salida_correcta, 0)
        expected = "Ante ti tienes tres losetas: la del este llena de arena, la del norte refulge con chispas mágicas y la del oeste tiene una roca.\nTienes que pisar una de ellas.\n"
        #last_line, resultado = self.comando("COGER", "OJOS")
        last_line, resultado = self.comando("N", "")
        # print(descripcion)
        self.assertEqual(Resultado.REINICIA, resultado)
        self.assertEqual(self.estado.localizacion().nombre, "loc89_Losetas_2")


    def test_de_la_1_a_la_3(self):
        self.test_de_la_1_a_la_2()
        self.loc = self.estado.localizacion()
        last_line, resultado = self.comando("E", "")
        # print(descripcion)
        self.assertEqual(Resultado.REINICIA, resultado)
        self.assertEqual(self.estado.localizacion().nombre, "loc89_Losetas_3")


######################

class TestLocalizacionFinal(BaseTest):
    def setUp(self):
        super().setUp("loc74_Ilusiones")
        self.loc = LocalizacionFinal("Sin uso", "Sin uso")

    def _seis_gemas_a_inventario(self):
        self.estado.añade_inventario("G1", ObjetoGema("G1", "G1", "G1", "G1"))
        self.estado.añade_inventario("G2", ObjetoGema("G2", "Gema", "G2", "Gema"))
        self.estado.añade_inventario("G3", ObjetoGema("G2", "Gema", "G3", "Gema"))
        self.estado.añade_inventario("G4", ObjetoGema("G2", "Gema", "G4", "Gema"))
        self.estado.añade_inventario("G5", ObjetoGema("G2", "Gema", "G5", "Gema"))
        self.estado.añade_inventario("G6", ObjetoGema("G2", "Gema", "G6", "Gema"))

    def test_descripción_con_sin_gemas(self):
        expected = "No has encontrado todas las gemas"
        # print(self.loc.mostrar_descripcion())
        #last_line, resultado = self.comando("COGER", "OJOS")
        descripcion = self.loc.mostrar_descripcion()
        self.assertIn(expected, descripcion)

        self._seis_gemas_a_inventario()
        expected = "Has encontrado todas las gemas"
        descripcion = self.loc.mostrar_descripcion()
        self.assertIn(expected, descripcion)


    def test_contar_gemas(self):
        self.assertEqual(self.loc._contar_gemas(), 0)
        self.add_rubi_inventario()
        #print(self.estado.inventario)
        self.assertEqual(self.loc._contar_gemas(), 1)
        self.add_inventario(self.obj_cuchillo())
        self.add_inventario(self.obj_vara())
        self.assertEqual(self.loc._contar_gemas(), 1)

    def test_contar_6_gemas(self):
        self._seis_gemas_a_inventario()
        self.assertEqual(self.loc._contar_gemas(), 6)

    def test_se_acerca(self):
        expected = "Se acerca a ti.\n"
        # print(self.loc.mostrar_descripcion())
        last_line, resultado = self.comando("EDU", "")
        # print(last_line)
        self.assertEqual(resultado, Resultado.NO_HECHO)
        # Comprobar que vas a otra LOC
        self.assertEqual(last_line, expected)
        last_line, resultado = self.comando("EDU", "")
        self.assertEqual(last_line, expected)

    def test_mueres_al_tercer_comando(self):
        expected = "Mueres.\n"
        # print(self.loc.mostrar_descripcion())
        last_line, resultado = self.comando("EDU", "")
        last_line, resultado = self.comando("EDU", "")
        last_line, resultado = self.comando("EDU", "")
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        self.assertEqual(last_line, expected)

    def test_llevas_todas_gemas(self):
        self._seis_gemas_a_inventario()
        # print(self.loc.mostrar_descripcion())
        last_line, resultado = self.comando("EDU", "")
        # print(last_line)
        # Comprobar que vas a otra LOC
        last_line, resultado = self.comando("EDU", "")
        last_line, resultado = self.comando("EDU", "")
        self.assertEqual(resultado, Resultado.NO_HECHO)
        #self.assertEqual(last_line, expected)

    #def test_salir_con_las_gemas(self):
    def test_salir_sin_las_gemas(self):
        #self._seis_gemas_a_inventario()
        # print(self.loc.mostrar_descripcion())
        expected = "No has conseguido todas las gemas pero al menos has conservado tu vida.\n"
        last_line, resultado = self.comando("S", "")
        # print(last_line)
        # Comprobar que vas a otra LOC
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        self.assertEqual(last_line, expected)

    def test_salir_con_las_gemas(self):
        self._seis_gemas_a_inventario()
        # print(self.loc.mostrar_descripcion())
        expected = "Has conseguido todas las gemas. La fama y la fortuna te acompañará toda la vida.\n"
        last_line, resultado = self.comando("S", "")
        # print(last_line)
        # Comprobar que vas a otra LOC
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        self.assertEqual(last_line, expected)

#######################

class TestLocalizaciónEspejo(BaseTest):
    def setUp(self):
        super().setUp("loc80_Guardián_del_espejo")

    def test_descripción_loc(self):
        self.assertEqual("loc80_Guardián_del_espejo", self._estoy_en())
        expected = "Vence al guardián para conseguir su tesoro."
        last_line, resultado = self.comando("EXAMINAR", "INSCRIPCION")
        # descripcion = self.loc.mostrar_descripcion()
        #print(last_line)
        #print(self.loc.examinables)
        self.assertEqual(expected, last_line)

######################

class TestLocalizacionIlusion(BaseTest):
    def setUp(self):
        super().setUp("loc74_Ilusiones")

    def test_descripción(self):
        #expected = "Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\nPuedes ir hacia: N.\n"
        expected = "Llegas a una caverna vacía."
        # print(self.loc.mostrar_descripcion())
        self.assertTrue(self.loc.mostrar_descripcion().startswith(expected))

    def test_salidas(self):
        expected = "Puedes ir hacia: N, S, E.\n"
        self.assertEqual(expected, self.loc._mostrar_salidas())

    def test_objetos(self):
        expected = "aguamarina"
        #self.assertNotIn(expected, self.loc._mostrar_salidas())
        pass


#########

class TestLocalizacionObjetoMaldito(BaseTest):

    def setUp(self):
        super().setUp("loc22_Puerta")
        self.loc = LocalizacionObjetoMaldito("xx", "xx", token_objeto_maldito="PILA", token_quitar_maldicion="RESID")
        objeto_maldito = ObjetoMaldito("nombre PILA", "descripcion PILA", "PILA", "PILA")
        self.loc.agregar_objeto("PILA", objeto_maldito)

    def test_coger_objeto_maldito(self):
        # print(self.loc.mostrar_descripcion())
        expected = "El cuchillo cobra vida y te atraviesa el cuello. Mueres en un instante."
        last_line, resultado = self.comando("COGER", "PILA", nombre="cuchillo")
        # print(last_line)
        self.assertEqual(resultado, Resultado.FIN_JUEGO)
        self.assertEqual(last_line, expected)

    def test_quitar_maldicion(self):
        # print(self.loc.mostrar_descripcion())
        expected = "El aire de la habitación vibra. La maldición desaparece."
        last_line, resultado = self.comando("RESID", "")
        self.assertEqual(last_line, expected)
        self.assertEqual(resultado, Resultado.HECHO)
        last_line, resultado = self.comando("COGER", "PILA")
        self.assertEqual(Resultado.HECHO, resultado)
        self.assertEqual(last_line, "Ok.")

    def test_quitar_maldicion_dos_veces(self):
        # print(self.loc.mostrar_descripcion())
        expected = "No pasa nada"
        last_line, resultado = self.comando("RESID", "")
        last_line, resultado = self.comando("RESID", "")
        self.assertEqual(last_line, expected)
        self.assertEqual(resultado, Resultado.HECHO)


if __name__ == '__main__':
    unittest.main()

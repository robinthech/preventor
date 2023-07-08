# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _


class ProductProduct(models.Model):
	_inherit = "registro.monitoreo"

	ocra_ids = fields.One2many('ocra.ocra', 'registro_id', string=u'OCRA')
	puntos_ocra = fields.Integer(compute="_compute_puntos_ocra", string=u"OCRA")

	@api.depends("ocra_ids")
	def _compute_puntos_ocra(self):
		for record in self:
			record.puntos_ocra = len(record.ocra_ids)


class Ocra(models.Model):
	_name = 'ocra.ocra'
	_inherits = {'riesgo.disergonomico': 'riesgo_disergonomico_id'}

	riesgo_disergonomico_id = fields.Many2one('riesgo.disergonomico', required=True, ondelete='restrict',
											  auto_join=True, string='Riesgo Disergonomico')
	# Ficha 1
	duracion_oficial = fields.Integer(string='Duración del Turno (min) Oficial')
	duracion_efectivo = fields.Integer(string='Duración del Turno (min) Efectivo')
	pausa_contrato = fields.Integer(string='Pausas (min) de Contrato')
	pausa_efectivo = fields.Integer(string='Pausas (min) de Efectivo')
	comer_oficial = fields.Integer(string='Pausa para Comer (min) Oficial')
	comer_efectivo = fields.Integer(string='Pausa para Comer (min) Efectivo')
	no_repetitivo_oficial = fields.Integer(string='Tiempo total de trabajo no repetitivo (min) Oficial')
	no_repetitivo_efectivo = fields.Integer(string='Tiempo total de trabajo no repetitivo (min) Efectivo')
	ciclo_programado = fields.Integer(string='Nº de ciclos o unidades por turno Programados')
	ciclo_efectivo = fields.Integer(string='Nº de ciclos o unidades por turno Efectivos')
	ciclo_observado = fields.Integer(string='Tiempo del ciclo observado ó período de observación (seg.)')
	tiempo_neto = fields.Integer(compute="_compute_ocra_ficha_1", string="Tiempo neto de trabajo repetitivo (min)", store=True)
	tiempo_ciclo_neto = fields.Integer(compute="_compute_ocra_ficha_1", string="Tiempo neto del ciclo (seg.)", store=True)
	tiempo_ciclo = fields.Integer("Tiempo del ciclo observado ó período de observación (seg.)")
	tiempo_neto_observado = fields.Integer(compute="_compute_ocra_ficha_1", string="Tiempo neto de trabajo repetitivo según"
																				   " observado (min)", store=True)
	tiempo_instauracion_diferencia = fields.Char(compute="_compute_ocra_ficha_1", string="Tiempo de insaturación del turno que necesita"
																						 " justificación (% Diferencia)", store=True)
	tiempo_instauracion_min = fields.Integer(compute="_compute_ocra_ficha_1", string="Tiempo de insaturación del turno que necesita"
																					 " justificación (Minutos)", store=True)
	facto_dura = fields.Float(compute="_compute_ocra_ficha_1", string="Factor Duración", store=True)
	duracion_dere = fields.Float(compute="_compute_ocra_ficha_1", string="Factor Duración: ", store=True)
	duracion_izq = fields.Float(compute="_compute_ocra_ficha_1", string="Factor Duración: ", store=True)
	duracion_dere_res = fields.Float(compute="_compute_ocra_ficha_1", string="Factor Duración: ", store=True)
	duracion_izq_res = fields.Float(compute="_compute_ocra_ficha_1", string="Factor Duración: ", store=True)

	@api.depends("pausa_efectivo", "duracion_efectivo", "comer_efectivo", "no_repetitivo_efectivo",
				 "ciclo_programado", "ciclo_efectivo", "tiempo_ciclo")
	def _compute_ocra_ficha_1(self):
		for record in self:
			if (record.duracion_efectivo - record.pausa_efectivo - record.comer_efectivo - record.no_repetitivo_efectivo >= 0):
				record.tiempo_neto = record.duracion_efectivo - record.pausa_efectivo - record.comer_efectivo - record.no_repetitivo_efectivo
			else:
				record.tiempo_neto = 0
			if record.ciclo_programado == 0:
				record.tiempo_ciclo_neto = 0
			else:
				record.tiempo_ciclo_neto = (record.tiempo_neto * 60) / record.ciclo_programado
			record.tiempo_neto_observado = (record.ciclo_efectivo * record.tiempo_ciclo) / 60

			if record.tiempo_ciclo_neto == 0:
				record.tiempo_instauracion_diferencia = '0 %'
			else:
				record.tiempo_instauracion_diferencia = str((record.tiempo_ciclo_neto - record.tiempo_ciclo)*100 / record.tiempo_ciclo_neto) + '%'
			record.tiempo_instauracion_min = record.tiempo_neto

			if record.tiempo_neto < 120:
				record.facto_dura = 0.5
			elif record.tiempo_neto < 180:
				record.facto_dura = 0.65
			elif record.tiempo_neto < 240:
				record.facto_dura = 0.75
			elif record.tiempo_neto < 300:
				record.facto_dura = 0.85
			elif record.tiempo_neto < 360:
				record.facto_dura = 0.925
			elif record.tiempo_neto < 420:
				record.facto_dura = 0.95
			elif record.tiempo_neto <= 480:
				record.facto_dura = 1
			elif record.tiempo_neto > 480:
				record.facto_dura = 1.5

			record.duracion_dere = record.facto_dura
			record.duracion_izq = record.facto_dura
			record.duracion_dere_res = record.facto_dura
			record.duracion_izq_res = record.facto_dura

	# Regimen de Pausa
	regimen_1 = fields.Boolean(string='Existe una interrupción de al menos 8/10 minutos cada hora (incluyendo pausa para comer); o bien,'
									  ' el tiempo de recuperación está dentro del ciclo.')
	regimen_2 = fields.Boolean(string='Existen dos interrupciones en la mañana y dos por la tarde (más una pausa para comer) de una duración'
									  ' mínima de 8 – 10 minutos en el turno de 7 – 8 horas, ó como mínimo 4 interrupciones además de la'
									  ' pausa para comer, ó 4 interrupciones de 8 – 10 minutos en el turno de 6 horas.')
	regimen_3 = fields.Boolean(string='Existen 2 pausas de una duración mínima de 8 – 10 minutos cada una en el turno de 6 horas'
									  ' (sin pausa para comer); o bien, 3 pausas más una pausa para comer en el turno de 7 – 8 horas.')
	regimen_4 = fields.Boolean(string='Existen 2 interrupciones (más una pausa para comer) de una duración mínima de 8 – 10 minutos en el turno'
									  ' de 7 – 8 horas (o 3 pausas pero ninguna para comer); o bien, en el turno de 6 horas, una pausa de al'
									  ' menos 8-10 minutos.')
	regimen_5 = fields.Boolean(string='En el turno de 7 horas, sin pausa para comer, existe sólo una pausa de al menos 10 minutos; o bien, en el'
									  ' turno de 8 horas existe una única pausa para comer, la cuál no cuenta como horas de trabajo.')
	regimen_6 = fields.Boolean(string='No existen pausas reales, excepto algunos minutos (menos de 5) en el turno de 7 – 8 horas.')
	tiempo_recuperacion_dere = fields.Integer(compute="_compute_ocra_ficha_2", string="Tiempo de recuperación insuficiente:", store=True)
	tiempo_recuperacion_dere_1 = fields.Integer(compute="_compute_ocra_ficha_2", string="Tiempo de recuperación insuficiente:", store=True)
	tiempo_recuperacion_izq = fields.Integer(compute="_compute_ocra_ficha_2", string="Tiempo de recuperación insuficiente: ", store=True)
	tiempo_recuperacion_izq_1 = fields.Integer(compute="_compute_ocra_ficha_2", string="Tiempo de recuperación insuficiente: ", store=True)

	@api.depends("regimen_1", "regimen_2", "regimen_3", "regimen_4", "regimen_5", "regimen_6")
	def _compute_ocra_ficha_2(self):
		for record in self:
			cont = 0
			if record.regimen_1:
				cont = 0
			if record.regimen_2:
				cont = 2
			if record.regimen_3:
				cont = 3
			if record.regimen_4:
				cont = 4
			if record.regimen_5:
				cont = 6
			if record.regimen_6:
				cont = 10
			record.tiempo_recuperacion_dere = cont
			record.tiempo_recuperacion_izq = cont
			record.tiempo_recuperacion_dere_1 = cont
			record.tiempo_recuperacion_izq_1 = cont

	# Frecuencia de acciones técnicas dinámicas y estáticas
	accion_dere_1 = fields.Integer(string='Número de acciones técnicas contenidas en el ciclo')
	accion_izq_1 = fields.Integer(string='')
	accion_dere_2 = fields.Boolean(string='¿Existe la posibilidad de realizar breves interrupciones?')
	accion_izq_2 = fields.Boolean(string='')
	acciones_dere_1 = fields.Boolean("Los movimientos de los brazos son lentos con posibilidad de frecuentes interrupciones (20 acciones/minuto).")
	acciones_izq_1 = fields.Boolean("Los movimientos de los brazos son lentos con posibilidad de frecuentes interrupciones (20 acciones/minuto)"
									" Izquierda.")
	acciones_dere_2 = fields.Boolean("Los movimientos de los brazos no son demasiado rápidos (30 acciones/minuto ó una acción cada 2 segundos), con"
									 " posibilidad de breves interrupciones.")
	acciones_izq_2 = fields.Boolean("Los movimientos de los brazos no son demasiado rápidos (30 acciones/minuto ó una acción cada 2 segundos), con"
									" posibilidad de breves interrupciones Izquierda.")
	acciones_dere_3 = fields.Boolean("Los movimientos de los brazos son bastante rápidos (cerca de 40 acciones/min.) pero con posibilidad de breves"
									 " interrupciones.")
	acciones_izq_3 = fields.Boolean("Los movimientos de los brazos son bastante rápidos (cerca de 40 acciones/min.) pero con posibilidad de breves"
									" interrupciones Izquierda.")
	acciones_dere_4 = fields.Boolean("Los movimientos de los brazos son bastante rápidos (cerca de 40 acciones/min.) la posibilidad de interrupciones"
									 " es más escasa e irregular.")
	acciones_izq_4 = fields.Boolean("Los movimientos de los brazos son bastante rápidos (cerca de 40 acciones/min.) la posibilidad de interrupciones"
									" es más escasa e irregular Izquierda.")
	acciones_dere_5 = fields.Boolean("Los movimientos de los brazos son rápidos y constantes (cerca de 50 acciones/min.).")
	acciones_izq_5 = fields.Boolean("Los movimientos de los brazos son rápidos y constantes (cerca de 50 acciones/min.) Izquierda.")
	acciones_dere_6 = fields.Boolean("Los movimientos de los brazos son muy rápidos y constantes (60 acciones/min.).")
	acciones_izq_6 = fields.Boolean("Los movimientos de los brazos son muy rápidos y constantes (60 acciones/min.) Izquierda.")
	acciones_dere_7 = fields.Boolean("Frecuencia muy alta (70 acciones/min. o más).")
	acciones_izq_7 = fields.Boolean("Frecuencia muy alta (70 acciones/min. o más) Izquierda.")
	acciones_dere_8 = fields.Boolean("Un objeto es mantenido en presa estática por una duración de al menos 5 seg. consecutivos y esta acción dura 2/3"
									 " del tiempo ciclo o del período de observación.")
	acciones_izq_8 = fields.Boolean("Un objeto es mantenido en presa estática por una duración de al menos 5 seg. consecutivos y esta acción dura 2/3"
									" del tiempo ciclo o del período de observación Izquierda.")
	acciones_dere_9 = fields.Boolean("Un objeto es mantenido en presa estática por una duración de al menos 5 seg. consecutivos y esta acción dura TODO"
									 " el tiempo ciclo o el período de observación.")
	acciones_izq_9 = fields.Boolean("Un objeto es mantenido en presa estática por una duración de al menos 5 seg. consecutivos y esta acción dura TODO"
									" el tiempo ciclo o el período de observación Izquierda.")
	frecuencia_dere = fields.Float(compute="_compute_ocra_ficha_3_dere", string="Frecuencia (acciones/min) ", store=True)
	frecuencia_izq = fields.Float(compute="_compute_ocra_ficha_3_izq", string="Frecuencia (acciones/min) Izquierda", store=True)
	facto_frec_dere = fields.Float(compute="_compute_ocra_ficha_3_dere", string="Factor Frecuencia ", store=True)
	facto_frec_izq = fields.Float(compute="_compute_ocra_ficha_3_izq", string="Factor Frecuencia (Izquierda)", store=True)
	facto_frec_dere_1 = fields.Float(compute="_compute_ocra_ficha_3_dere", string="Factor Frecuencia ", store=True)
	facto_frec_izq_1 = fields.Float(compute="_compute_ocra_ficha_3_izq", string="Factor Frecuencia (Izquierda)", store=True)

	@api.depends("accion_dere_1", "tiempo_ciclo_neto", "acciones_dere_1", "acciones_dere_2", "acciones_dere_3", "acciones_dere_4", "acciones_dere_5",
				 "acciones_dere_6", "acciones_dere_7", "acciones_dere_8", "acciones_dere_9")
	def _compute_ocra_ficha_3_dere(self):
		for record in self:
			cont1 = 0
			cont2 = 0
			if record.acciones_dere_1:
				cont1 = 0
			if record.acciones_dere_2:
				cont1 = 1
			if record.acciones_dere_3:
				cont1 = 3
			if record.acciones_dere_4:
				cont1 = 4
			if record.acciones_dere_5:
				cont1 = 6
			if record.acciones_dere_6:
				cont1 = 8
			if record.acciones_dere_7:
				cont1 = 10
			if record.acciones_dere_8:
				cont2 = 2.5
			if record.acciones_dere_9:
				cont2 = 4.5
			if cont1 > cont2:
				record.facto_frec_dere = cont1
				record.facto_frec_dere_1 = cont1
			else:
				record.facto_frec_dere = cont2
				record.facto_frec_dere_1 = cont2

			if record.accion_dere_1 == 0:
				record.frecuencia_dere = 0
			else:
				if record.tiempo_ciclo_neto != 0:
					record.frecuencia_dere = (float(record.accion_dere_1*60) / float(record.tiempo_ciclo_neto))
				elif record.tiempo_ciclo_neto == 0:
					record.frecuencia_dere = 0

	@api.depends("accion_izq_1", "acciones_izq_1", "tiempo_ciclo_neto", "acciones_izq_2", "acciones_izq_3", "acciones_izq_4", "acciones_izq_5",
				 "acciones_izq_6", "acciones_izq_7", "acciones_izq_8", "acciones_izq_9")
	def _compute_ocra_ficha_3_izq(self):
		for record in self:
			cont3 = 0
			cont4 = 0
			if record.acciones_izq_1:
				cont3 = 0
			if record.acciones_izq_2:
				cont3 = 1
			if record.acciones_izq_3:
				cont3 = 3
			if record.acciones_izq_4:
				cont3 = 4
			if record.acciones_izq_5:
				cont3 = 6
			if record.acciones_izq_6:
				cont3 = 8
			if record.acciones_izq_7:
				cont3 = 10
			if record.acciones_izq_8:
				cont4 = 2.5
			if record.acciones_izq_9:
				cont4 = 4.5
			if cont3 > cont4:
				record.facto_frec_izq = cont3
				record.facto_frec_izq_1 = cont3
			else:
				record.facto_frec_izq = cont4
				record.facto_frec_izq_1 = cont4

			if record.accion_izq_1 == 0:
				record.frecuencia_izq == 0
			else:
				if record.tiempo_ciclo_neto != 0:
					record.frecuencia_izq = (float(record.accion_izq_1*60) / float(record.tiempo_ciclo_neto))
				elif record.tiempo_ciclo_neto == 0:
					record.frecuencia_izq = 0

	# Aplicación de fuerza
	tirar_1 = fields.Boolean("Tirar o empujar palancas.")
	tirar_2 = fields.Boolean("Tirar o empujar palancas.")
	tirar_3 = fields.Boolean("Tirar o empujar palancas.")
	cerrar_1 = fields.Boolean("Cerrar o abrir.")
	cerrar_2 = fields.Boolean("Cerrar o abrir.")
	cerrar_3 = fields.Boolean("Cerrar o abrir.")
	presionar_1 = fields.Boolean("Presionar o manipular componentes.")
	herramienta_1 = fields.Boolean("Utilizar herramientas.")
	herramienta_2 = fields.Boolean("Utilizar herramientas.")
	herramienta_3 = fields.Boolean("Utilizar herramientas.")
	peso_1 = fields.Boolean("Usar el peso del cuerpo para obtener fuerza necesaria.")
	manipular_comp_1 = fields.Boolean("Manipular componentes para levantar objetos")
	manipular_comp_2 = fields.Boolean("Manipular componentes para levantar objetos")
	manipular_comp_3 = fields.Boolean("Manipular componentes para levantar objetos")
	pulsar_2 = fields.Boolean("Pulsar botones.")
	pulsar_3 = fields.Boolean("Pulsar botones.")
	manipular_2 = fields.Boolean("Manipular o presionar objetos.")
	manipular_3 = fields.Boolean("Manipular o presionar objetos.")
	# Aplicación de fuerza ficha 1
	duracion_1_dere_1 = fields.Boolean("2 segundos cada 10 minutos")
	duracion_1_izq_1 = fields.Boolean("2 segundos cada 10 minutos")
	duracion_2_dere_1 = fields.Boolean("1 % del tiempo")
	duracion_2_izq_1 = fields.Boolean("1 % del tiempo")
	duracion_3_dere_1 = fields.Boolean("5 % del tiempo")
	duracion_3_izq_1 = fields.Boolean("5 % del tiempo")
	duracion_4_dere_1 = fields.Boolean("Más del 10% del tiempo")
	duracion_4_izq_1 = fields.Boolean("Más del 10% del tiempo")
	# Aplicación de fuerza ficha 2
	duracion_1_dere_2 = fields.Boolean("2 segundos cada 10 minutos")
	duracion_1_izq_2 = fields.Boolean("2 segundos cada 10 minutos")
	duracion_2_dere_2 = fields.Boolean("1 % del tiempo")
	duracion_2_izq_2 = fields.Boolean("1 % del tiempo")
	duracion_3_dere_2 = fields.Boolean("5 % del tiempo")
	duracion_3_izq_2 = fields.Boolean("5 % del tiempo")
	duracion_4_dere_2 = fields.Boolean("Más del 10% del tiempo")
	duracion_4_izq_2 = fields.Boolean("Más del 10% del tiempo")
	# Aplicación de fuerza ficha 3
	duracion_1_dere_3 = fields.Boolean("1/3 del tiempo")
	duracion_1_izq_3 = fields.Boolean("1/3 del tiempo")
	duracion_2_dere_3 = fields.Boolean("Aprox. la mitad del tiempo")
	duracion_2_izq_3 = fields.Boolean("Aprox. la mitad del tiempo")
	duracion_3_dere_3 = fields.Boolean("Más de la mitad del tiempo")
	duracion_3_izq_3 = fields.Boolean("Más de la mitad del tiempo")
	duracion_4_dere_3 = fields.Boolean("Casi todo el tiempo")
	duracion_4_izq_3 = fields.Boolean("Casi todo el tiempo")
	# Aplicación de fuerza calculado
	aplicacion_fuerza_dere = fields.Integer(compute="_compute_ocra_aplicacion_dere", string="Aplicación de fuerza: ", store=True)
	aplicacion_fuerza_izq = fields.Integer(compute="_compute_ocra_aplicacion_izq", string="Aplicación de fuerza: ", store=True)
	aplicacion_fuerza_dere_1 = fields.Integer(compute="_compute_ocra_aplicacion_dere", string="Aplicación de fuerza: ", store=True)
	aplicacion_fuerza_izq_1 = fields.Integer(compute="_compute_ocra_aplicacion_izq", string="Aplicación de fuerza: ", store=True)

	@api.depends("duracion_1_dere_1", "duracion_2_dere_1", "duracion_3_dere_1", "duracion_1_dere_2", "duracion_2_dere_2", "duracion_3_dere_2",
				 "duracion_1_dere_3", "duracion_2_dere_3", "duracion_3_dere_3", "duracion_4_dere_1", "duracion_4_dere_2", "duracion_4_dere_3")
	def _compute_ocra_aplicacion_dere(self):
		for record in self:
			cont = 0
			if record.duracion_1_dere_1:
				cont = 6
			if record.duracion_2_dere_1:
				cont = 12
			if record.duracion_3_dere_1:
				cont = 24
			if record.duracion_4_dere_1:
				cont = 32
			max1 = cont

			if record.duracion_1_dere_2:
				cont = 4
			if record.duracion_2_dere_2:
				cont = 8
			if record.duracion_3_dere_2:
				cont = 16
			if record.duracion_4_dere_2:
				cont = 24
			max2 = cont

			if record.duracion_1_dere_3:
				cont = 2
			if record.duracion_2_dere_3:
				cont = 4
			if record.duracion_3_dere_3:
				cont = 6
			if record.duracion_4_dere_3:
				cont = 8
			max3 = cont

			record.aplicacion_fuerza_dere = max1 + max2 + max3
			record.aplicacion_fuerza_dere_1 = max1 + max2 + max3

	@api.depends("duracion_1_izq_1", "duracion_2_izq_1", "duracion_3_izq_1", "duracion_1_izq_2", "duracion_2_izq_2", "duracion_3_izq_2",
				 "duracion_1_izq_3", "duracion_2_izq_3", "duracion_3_izq_3", "duracion_4_izq_1", "duracion_4_izq_2", "duracion_4_izq_3")
	def _compute_ocra_aplicacion_izq(self):
		for record in self:
			cont = 0
			if record.duracion_1_izq_1:
				cont = 6
			if record.duracion_2_izq_1:
				cont = 12
			if record.duracion_3_izq_1:
				cont = 24
			if record.duracion_4_izq_1:
				cont = 32
			max1 = cont

			if record.duracion_1_izq_2:
				cont = 4
			if record.duracion_2_izq_2:
				cont = 8
			if record.duracion_3_izq_2:
				cont = 16
			if record.duracion_4_izq_2:
				cont = 24
			max2 = cont

			if record.duracion_1_izq_3:
				cont = 2
			if record.duracion_2_izq_3:
				cont = 4
			if record.duracion_3_izq_3:
				cont = 6
			if record.duracion_4_izq_3:
				cont = 8
			max3 = cont

			record.aplicacion_fuerza_izq = max1 + max2 + max3
			record.aplicacion_fuerza_izq_1 = max1 + max2 + max3

	# Aplicación de postura
	postura_1_dere = fields.Boolean("El/los brazos no descansan sobre la superficie de trabajo sino que están ligeramente elevados durante algo más"
									" de la mitad del tiempo.")
	postura_1_izq = fields.Boolean("El/los brazos no descansan sobre la superficie de trabajo sino que están ligeramente elevados durante algo más"
								   " de la mitad del tiempo. (Izquierda)")
	postura_2_dere = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro (o en otra postura extrema) por casi un 10% del"
									" tiempo.")
	postura_2_izq = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro (o en otra postura extrema) por casi un 10% del"
								   " tiempo. (Izquierda)")
	postura_3_dere = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro (o en otra postura extrema) por casi 1/3 del"
									" tiempo.")
	postura_3_izq = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro (o en otra postura extrema) por casi 1/3 del"
								   " tiempo. (Izquierda)")
	postura_4_dere = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro (o en otra postura extrema) por más de la"
									" mitad del tiempo.")
	postura_4_izq = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro (o en otra postura extrema) por más de la mitad"
								   " del tiempo. (Izquierda)")
	postura_5_dere = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro ( o en otra postura extrema) por casi todo el"
									" tiempo.")
	postura_5_izq = fields.Boolean("Los brazos se mantienen sin apoyo casi a la altura del hombro ( o en otra postura extrema) por casi todo el"
								   " tiempo. (Izquierda)")
	postura_6_dere = fields.Boolean("Adicionalmente, las manos operan por encima de la cabeza por más del 50% del tiempo.)")
	postura_6_izq = fields.Boolean("Adicionalmente, las manos operan por encima de la cabeza por más del 50% del tiempo. (Izquierda)")
	postura_7_dere = fields.Boolean("El codo debe realizar amplios movimientos de flexo-extensión o prono-supinación, movimientos bruscos cerca de"
									" 1/3 del tiempo.")
	postura_7_izq = fields.Boolean("El codo debe realizar amplios movimientos de flexo-extensión o prono-supinación, movimientos bruscos cerca de"
								   " 1/3 del tiempo. (Izquierda)")
	postura_8_dere = fields.Boolean("El codo debe realizar amplios movimientos de flexo-extensión o prono-supinación, movimientos repentinos por"
									" más de la mitad del tiempo.")
	postura_8_izq = fields.Boolean("El codo debe realizar amplios movimientos de flexo-extensión o prono-supinación, movimientos repentinos por"
								   " más de la mitad del tiempo. (Izquierda)")
	postura_9_dere = fields.Boolean("El codo debe realizar amplios movimientos de flexo-extensión o prono-supinación, movimientos repentinos por"
									" casi todo el tiempo.")
	postura_9_izq = fields.Boolean("El codo debe realizar amplios movimientos de flexo-extensión o prono-supinación, movimientos repentinos por"
								   " casi todo el tiempo. (Izquierda)")
	postura_10_dere = fields.Boolean("La muñeca debe doblarse en una posición extrema o adoptar posturas molestas (amplias flexiones, extensiones"
									 " o desviaciones laterales) por lo menos 1/3 del tiempo.")
	postura_10_izq = fields.Boolean("La muñeca debe doblarse en una posición extrema o adoptar posturas molestas (amplias flexiones, extensiones"
									" o desviaciones laterales) por lo menos 1/3 del tiempo. (Izquierda)")
	postura_11_dere = fields.Boolean("La muñeca debe doblarse en una posición extrema o adoptar posturas molestas por más de la mitad del tiempo.")
	postura_11_izq = fields.Boolean("La muñeca debe doblarse en una posición extrema o adoptar posturas molestas por más de la mitad del tiempo."
									" (Izquierda)")
	postura_12_dere = fields.Boolean("La muñeca debe doblarse en una posición extrema por casi todo el tiempo.")
	postura_12_izq = fields.Boolean("La muñeca debe doblarse en una posición extrema por casi todo el tiempo. (Izquierda)")
	postura_13_dere = fields.Boolean("Por cada 1/3 del tiempo")
	postura_13_izq = fields.Boolean("Por cada 1/3 del tiempo (Izquierda)")
	postura_14_dere = fields.Boolean("Más de la mitad del tiempo.")
	postura_14_izq = fields.Boolean("Más de la mitad del tiempo. (Izquierda)")
	postura_15_dere = fields.Boolean("Casi todo el tiempo.")
	postura_15_izq = fields.Boolean("Casi todo el tiempo. (Izquierda)")
	postura_dere_1 = fields.Boolean("Con los dedos juntos (precisión)")
	postura_izq_1 = fields.Boolean("Con los dedos juntos (precisión) Izquierda")
	postura_dere_2 = fields.Boolean("Con la mano casi completamente abierta (presa palmar)")
	postura_izq_2 = fields.Boolean("Con la mano casi completamente abierta (presa palmar) Izquierda")
	postura_dere_3 = fields.Boolean("Con los dedos en forma de gancho.")
	postura_izq_3 = fields.Boolean("Con los dedos en forma de gancho. Izquierda")
	postura_dere_4 = fields.Boolean("Con otros tipos de toma o agarre similares a los indicados anteriormente.")
	postura_izq_4 = fields.Boolean("Con otros tipos de toma o agarre similares a los indicados anteriormente. Izquierda")
	postura_16_dere = fields.Boolean("Presencia del movimiento del hombro y/o codo y/o muñeca y/o mano idénticos, repetidos por más de la mitad"
									 " del tiempo (o tiempo de ciclo entre 8 y 15 segundos en que prevalecen las acciones técnicas, incluso"
									 " distintas entre ellas, de los miembros superiores).")
	postura_16_izq = fields.Boolean("Presencia del movimiento del hombro y/o codo y/o muñeca y/o mano idénticos, repetidos por más de la mitad"
									" del tiempo (o tiempo de ciclo entre 8 y 15 segundos en que prevalecen las acciones técnicas, incluso"
									" distintas entre ellas, de los miembros superiores). (Izquierda)")
	postura_17_dere = fields.Boolean("Presencia del movimiento del hombro y/o codo y/o muñeca y/o mano idénticos, repetidos casi todo el tiempo"
									 " (o tiempo de ciclo inferior a 8 segundos en que prevalecen las acciones técnicas, incluso distintas entre"
									 " ellas, de los miembros superiores).")
	postura_17_izq = fields.Boolean("Presencia del movimiento del hombro y/o codo y/o muñeca y/o mano idénticos, repetidos casi todo el tiempo"
									" (o tiempo de ciclo inferior a 8 segundos en que prevalecen las acciones técnicas, incluso distintas entre"
									" ellas, de los miembros superiores). (Izquierda)")
	postura_dere = fields.Integer(compute="_compute_ocra_ficha_5_dere", string="Posturas forzadas: ", store=True)
	postura_izq = fields.Integer(compute="_compute_ocra_ficha_5_izq", string="Posturas forzadas: ", store=True)
	hombro_dere = fields.Integer(compute="_compute_ocra_ficha_5_dere", string="Hombro:", store=True)
	hombro_izq = fields.Integer(compute="_compute_ocra_ficha_5_izq", string="Hombro: ", store=True)
	codo_dere = fields.Integer(compute="_compute_ocra_ficha_5_dere", string="Codo: ", store=True)
	codo_izq = fields.Integer(compute="_compute_ocra_ficha_5_izq", string="Codo: ", store=True)
	muneca_dere = fields.Integer(compute="_compute_ocra_ficha_5_dere", string="Muñeca: ", store=True)
	muneca_izq = fields.Integer(compute="_compute_ocra_ficha_5_izq", string="Muñeca: ", store=True)
	mano_dere = fields.Integer(compute="_compute_ocra_ficha_5_dere", string="Mano-dedos: ", store=True)
	mano_izq = fields.Integer(compute="_compute_ocra_ficha_5_izq", string="Mano-dedos: ", store=True)
	estereotipo_dere = fields.Integer(compute="_compute_ocra_ficha_5_dere", string="Estereotipo:", store=True)
	estereotipo_izq = fields.Integer(compute="_compute_ocra_ficha_5_izq", string="Estereotipo: ", store=True)
	postura_dere_res = fields.Integer(compute="_compute_ocra_ficha_5_dere", string="Posturas forzadas: ", store=True)
	postura_izq_res = fields.Integer(compute="_compute_ocra_ficha_5_izq", string="Posturas forzadas: ", store=True)

	@api.depends("postura_1_dere", "postura_2_dere", "postura_3_dere", "postura_dere_1", "postura_dere_2", "postura_dere_3", "postura_dere_4",
				 "postura_4_dere", "postura_5_dere", "postura_6_dere", "postura_7_dere", "postura_8_dere", "postura_9_dere", "postura_10_dere",
				 "postura_11_dere", "postura_12_dere", "postura_13_dere", "postura_14_dere", "postura_15_dere", "postura_16_dere", "postura_17_dere")
	def _compute_ocra_ficha_5_dere(self):
		for record in self:
			cont = 0
			max1 = 0
			max2 = 0
			max3 = 0
			max4 = 0
			max5 = 0
			if record.postura_1_dere:
				cont = 1
			if record.postura_2_dere:
				cont = 2
			if record.postura_3_dere:
				cont = 6
			if record.postura_4_dere:
				cont = 12
			if record.postura_5_dere:
				cont = 24
			record.hombro_dere = cont

			if record.postura_6_dere:
				max1 = cont*2
			else:
				max1 = cont

			if record.postura_7_dere:
				cont = 2
			if record.postura_8_dere:
				cont = 4
			if record.postura_9_dere:
				cont = 8
			max2 = cont
			record.codo_dere = cont

			if record.postura_10_dere:
				cont = 2
			if record.postura_11_dere:
				cont = 4
			if record.postura_12_dere:
				cont = 8
			max3 = cont
			record.muneca_dere = cont

			if record.postura_13_dere:
				cont = 2
			if record.postura_14_dere:
				cont = 4
			if record.postura_15_dere:
				cont = 8
			max4 = cont
			record.mano_dere = cont
			if record.postura_16_dere:
				cont = 2
			if record.postura_17_dere:
				cont = 4
			max5 = cont
			record.estereotipo_dere = cont
			record.postura_dere = max(max1, max2, max3, max4, max5)
			record.postura_dere_res = max(max1, max2, max3, max4, max5)

	@api.depends("postura_1_izq", "postura_2_izq", "postura_3_izq", "postura_4_izq", "postura_5_izq", "postura_6_izq", "postura_7_izq",
				 "postura_8_izq", "postura_9_izq", "postura_10_izq", "postura_11_izq", "postura_12_izq", "postura_13_izq", "postura_14_izq",
				 "postura_15_izq", "postura_16_izq", "postura_17_izq")
	def _compute_ocra_ficha_5_izq(self):
		for record in self:
			cont = 0
			max1 = 0
			max2 = 0
			max3 = 0
			max4 = 0
			max5 = 0
			if record.postura_1_izq:
				cont = 1
			if record.postura_2_izq:
				cont = 2
			if record.postura_3_izq:
				cont = 6
			if record.postura_4_izq:
				cont = 12
			if record.postura_5_izq:
				cont = 24
			record.hombro_izq = cont

			if record.postura_6_izq:
				max1 = cont*2
			else:
				max1 = cont

			if record.postura_7_izq:
				cont = 2
			if record.postura_8_izq:
				cont = 4
			if record.postura_9_izq:
				cont = 8
			max2 = cont
			record.codo_izq = cont
			if record.postura_10_izq:
				cont = 2
			if record.postura_11_izq:
				cont = 4
			if record.postura_12_izq:
				cont = 8
			max3 = cont
			record.muneca_izq = cont
			if record.postura_13_izq:
				cont = 2
			if record.postura_14_izq:
				cont = 4
			if record.postura_15_izq:
				cont = 8
			max4 = cont
			record.mano_izq = cont
			if record.postura_16_izq:
				cont = 2
			if record.postura_17_izq:
				cont = 4
			max5 = cont
			record.estereotipo_izq = cont

			record.postura_izq = max(max1, max2, max3, max4, max5)
			record.postura_izq_res = max(max1, max2, max3, max4, max5)

	fisico_dere_1 = fields.Boolean(string='Se emplean por más de la mitad del tiempo guantes inadecuados para la tarea, (incómodos, demasiado'
										  ' gruesos, talla incorrecta).')
	fisico_izq_1 = fields.Boolean(string='')
	fisico_dere_2 = fields.Boolean(string='Presencia de movimientos repentinos, bruscos con frecuencia de 2 o más por minuto.')
	fisico_izq_2 = fields.Boolean(string='')
	fisico_dere_3 = fields.Boolean(string='Presencia de impactos repetidos (uso de las manos para dar golpes) con frecuencia de al menos'
										  ' 10 veces por hora.')
	fisico_izq_3 = fields.Boolean(string='')
	fisico_dere_4 = fields.Boolean(string='Contacto con superficies frías (inferior a 0 grados) o desarrollo de labores en cámaras frigoríficas'
										  ' por más de la mitad del tiempo.')
	fisico_izq_4 = fields.Boolean(string='')
	fisico_dere_5 = fields.Boolean(string='Se emplean herramientas vibradoras por al menos un tercio del tiempo. Atribuir un valor de 4 en caso'
										  ' de uso de instrumentos con elevado contenido de vibración (ej. Martillo neumático, etc.) Utilizados'
										  ' en al menos 1/3 del tiempo.')
	fisico_izq_5 = fields.Boolean(string='')
	fisico_dere_6 = fields.Boolean(string='Se emplean herramientas que provocan compresión sobre las estructuras musculosas y tendinosas'
										  ' (verificar la presencia de enrojecimiento, callos, heridas, etc. Sobre la piel).')
	fisico_izq_6 = fields.Boolean(string='')
	fisico_dere_7 = fields.Boolean(string='Se realizan tareas de presición durante más de la mitad del tiempo (tareas en áreas menores a 2 o'
										  ' 3mm) que requieren distancia visual de acercamiento.')
	fisico_izq_7 = fields.Boolean(string='')
	fisico_dere_8 = fields.Boolean(string='Existen más factores adicionales al mismo tiempo que ocupan más de la mitad del tiempo.')
	fisico_izq_8 = fields.Boolean(string='')
	fisico_dere_9 = fields.Boolean(string='Existen uno o más factores complementarios que ocupan casi todo el tiempo.')
	fisico_izq_9 = fields.Boolean(string='')
	socio_dere_1 = fields.Boolean(string='El ritmo de trabajo está determinado por la máquina, pero existen “espacios de recuperación” por'
										 ' lo que el ritmo puede acelerarse o desacelerar. Derecha')
	socio_izq_1 = fields.Boolean(string='')
	socio_dere_2 = fields.Boolean(string='El ritmo de trabajo está completamente determinado por la máquina. Derecha')
	socio_izq_2 = fields.Boolean(string='')
	comple_dere = fields.Integer(compute="_compute_ocra_complemento_dere", string="Factores de riesgo complementarios: ", store=True)
	comple_izq = fields.Integer(compute="_compute_ocra_complemento_izq", string="Factores de riesgo complementarios: ", store=True)
	comple_dere_res = fields.Integer(compute="_compute_ocra_complemento_dere", string="Factores de riesgo complementarios: ", store=True)
	comple_izq_res = fields.Integer(compute="_compute_ocra_complemento_izq", string="Factores de riesgo complementarios: ", store=True)

	@api.depends("fisico_dere_1", "fisico_dere_2", "fisico_dere_3", "fisico_dere_4", "fisico_dere_5", "fisico_dere_6", "fisico_dere_7",
				 "fisico_dere_8", "fisico_dere_9", "socio_dere_1", "socio_dere_2")
	def _compute_ocra_complemento_dere(self):
		for record in self:
			cont = 0
			max1 = 0
			max2 = 0
			if record.fisico_dere_1:
				cont = 2
			if record.fisico_dere_2:
				cont = 2
			if record.fisico_dere_3:
				cont = 2
			if record.fisico_dere_4:
				cont = 2
			if record.fisico_dere_5:
				cont = 2
			if record.fisico_dere_6:
				cont = 2
			if record.fisico_dere_7:
				cont = 2
			if record.fisico_dere_8:
				cont = 2
			if record.fisico_dere_9:
				cont = 3
			max1 = cont
			if record.socio_dere_1:
				cont = 1
			if record.socio_dere_2:
				cont = 2
			max2 = cont
			record.comple_dere = max(max1, max2)
			record.comple_dere_res = max(max1, max2)

	@api.depends("fisico_izq_1", "fisico_izq_2", "fisico_izq_3", "fisico_izq_4", "fisico_izq_5", "fisico_izq_6", "fisico_izq_7", "fisico_izq_8",
				 "fisico_izq_9", "socio_izq_1", "socio_izq_2")
	def _compute_ocra_complemento_izq(self):
		for record in self:
			cont = 0
			max1 = 0
			max2 = 0
			if record.fisico_izq_1:
				cont = 2
			if record.fisico_izq_2:
				cont = 2
			if record.fisico_izq_3:
				cont = 2
			if record.fisico_izq_4:
				cont = 2
			if record.fisico_izq_5:
				cont = 2
			if record.fisico_izq_6:
				cont = 2
			if record.fisico_izq_7:
				cont = 2
			if record.fisico_izq_8:
				cont = 2
			if record.fisico_izq_9:
				cont = 3
			max1 = cont
			if record.socio_izq_1:
				cont = 1
			if record.socio_izq_2:
				cont = 2
			max2 = cont
			record.comple_izq = max(max1, max2)
			record.comple_izq_res = max(max1, max2)

		# Resultados
	indice_riesgo_dere = fields.Float(compute="_compute_ocra", string="Indice de Riesgo", store=True)
	indice_riesgo_izq = fields.Float(compute="_compute_ocra", string="Indice de Riesgo ", store=True)
	nivel_riesgo_dere = fields.Char(compute="_compute_ocra", string="Nivel de Riesgo", store=True)
	nivel_riesgo_izq = fields.Char(compute="_compute_ocra", string="Nivel de Riesgo ", store=True)
	cumple_dere = fields.Char(compute="_compute_ocra", string="¿Cumple? (derecha)", store=True)
	cumple_izq = fields.Char(compute="_compute_ocra", string="¿Cumple? (izquierda)", store=True)
	cumple = fields.Char(compute="_compute_ocra", string="¿Cumple?", store=True)
	nivel_riesgo_total = fields.Char(compute="_compute_ocra", string="Nivel de Riesgo Total", store=True)

	@api.depends("tiempo_recuperacion_dere", "tiempo_recuperacion_izq", "facto_frec_izq", "facto_frec_dere", "aplicacion_fuerza_dere",
				 "aplicacion_fuerza_izq", "postura_dere", "postura_izq", "comple_dere", "comple_izq", "duracion_dere", "duracion_izq")
	def _compute_ocra(self):
		for record in self:
			cont_dere = 0
			cont_izq = 0

			record.indice_riesgo_dere = (record.tiempo_recuperacion_dere + record.facto_frec_dere + record.aplicacion_fuerza_dere +
										 record.postura_dere + record.comple_dere)*record.duracion_dere
			record.indice_riesgo_izq = (record.tiempo_recuperacion_izq + record.facto_frec_izq + record.aplicacion_fuerza_izq +
										record.postura_izq + record.comple_izq)*record.duracion_izq

			if record.indice_riesgo_dere <= 7.5:
				cont_dere = 1
				record.nivel_riesgo_dere = 'ACEPTABLE'
				record.cumple_dere = "SÍ CUMPLE"
			elif record.indice_riesgo_dere <= 11:
				cont_dere = 2
				record.nivel_riesgo_dere = 'MUY LEVE'
				record.cumple_dere = "SÍ CUMPLE"
			elif record.indice_riesgo_dere <= 14:
				cont_dere = 3
				record.nivel_riesgo_dere = 'NO ACEPTABLE NIVEL LEVE'
				record.cumple_dere = "NO CUMPLE"
			elif record.indice_riesgo_dere <= 22.5:
				cont_dere = 4
				record.nivel_riesgo_dere = 'NO ACEPTABLE NIVEL MEDIO'
				record.cumple_dere = "NO CUMPLE"
			elif record.indice_riesgo_dere > 22.5:
				cont_dere = 5
				record.nivel_riesgo_dere = 'NO ACEPTABLE NIVEL ALTO'
				record.cumple_dere = "NO CUMPLE"

			if record.indice_riesgo_izq <= 7.5:
				cont_izq = 1
				record.nivel_riesgo_izq = 'ACEPTABLE'
				record.cumple_izq = "SÍ CUMPLE"
			elif record.indice_riesgo_izq <= 11:
				cont_izq = 2
				record.nivel_riesgo_izq = 'MUY LEVE'
				record.cumple_izq = "SÍ CUMPLE"
			elif record.indice_riesgo_izq <= 14:
				cont_izq = 3
				record.nivel_riesgo_izq = 'NO ACEPTABLE NIVEL LEVE'
				record.cumple_izq = "NO CUMPLE"
			elif record.indice_riesgo_izq <= 22.5:
				cont_izq = 4
				record.nivel_riesgo_izq = 'NO ACEPTABLE NIVEL MEDIO'
				record.cumple_izq = "NO CUMPLE"
			elif record.indice_riesgo_izq > 22.5:
				cont_izq = 5
				record.nivel_riesgo_izq = 'NO ACEPTABLE NIVEL ALTO'
				record.cumple_izq = "NO CUMPLE"

			if cont_dere <= cont_izq:
				record.nivel_riesgo_total = record.nivel_riesgo_izq
			elif cont_izq <= cont_dere:
				record.nivel_riesgo_total = record.nivel_riesgo_dere

			if record.cumple_dere == "SÍ CUMPLE" and record.cumple_izq == "SÍ CUMPLE":
				record.cumple = "SÍ CUMPLE"

			elif record.cumple_dere == "NO CUMPLE" or record.cumple_izq == "NO CUMPLE":
				record.cumple = "NO CUMPLE"

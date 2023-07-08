# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _

tabla_a = [[1,	2,	3,	4,	1,	2,	3,	4,	3,	3,	5,	6],
		   [2,	3,	4,	5,	3,	4,	5,	6,	4,	5,	6,	7],
		   [2,	4,	5,	6,	4,	5,	6,	7,	5,	6,	7,	8],
		   [3,	5,	6,	7,	5,	6,	7,	8,	6,	7,	8,	9],
		   [4,	6,	7,	8,	6,	7,	8,	9,	7,	8,	9,	9]]

tabla_b = [[1,	2,	2,	1,	2,	3],
		   [1,	2,	3,	2,	3,	4],
		   [3,	4,	5,	4,	5,	5],
		   [4,	5,	5,	5,	6,	7],
		   [6,	7,	8,	7,	8,	8],
		   [7,	8,	8,	8,	9,	9]]
tabla_c = [[1,	1,	1,	2,	3,	3,	4,	5,	6,	7,	7,	7],
		   [1,	2,	2,	3,	4,	4,	5,	6,	6,	7,	7,	8],
		   [2,	3,	3,	3,	4,	5,	6,	7,	7,	8,	8,	8],
		   [3,	4,	4,	4,	5,	6,	7,	8,	8,	9,	9,	9],
		   [4,	4,	4,	5,	6,	7,	8,	8,	9,	9,	9,	9],
		   [6,	6,	6,	7,	8,	8,	9,	9,	10,	10,	10,	10],
		   [7,	7,	7,	8,	9,	9,	9,	10,	10,	11,	11,	11],
		   [8,	8,	8,	9,	10,	10,	10,	10,	10,	11,	11,	11],
		   [9,	9,	9,	10,	10,	10,	11,	11,	11,	12,	12,	12],
		   [10, 10,	10,	11,	11,	11,	11,	12,	12,	12,	12,	12],
		   [11, 11,	11,	11,	12,	12,	12,	12,	12,	12,	12,	12],
		   [12, 12,	12,	12,	12,	12,	12,	12,	12,	12,	12,	12]]

class ProductProduct(models.Model):
	_inherit = "res.users"

	registro_ids = fields.One2many('registro.monitoreo.disergonomico', 'create_uid', string=u'Iluminación')

class RegistroMonitoreo(models.Model):
	_name = 'registro.monitoreo.disergonomico'

	name = fields.Char("Codigo", index=True, default=lambda self: _('New'))
	ruc = fields.Char(string="RUC")
	cliente = fields.Char(string="Razon Social")
	sede = fields.Char(string=u'Sede')
	fecha_monitoreo = fields.Date("Fecha Inicio de Monitoreo")
	fecha_monitoreo_fin = fields.Date("Fecha Fin de Monitoreo")
	puntos = fields.Integer("Puntos Máximos por Agente")
	sequence = fields.Char(compute='_compute_sequence', string="Codigo")

	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('registro.monitoreo.disergonomico') or _('New')
		res = super(RegistroMonitoreo, self).create(vals)
		return res

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "RD-000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "RD-00{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "RD-0{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "RD-{}".format(i)

class AgenteGeneral(models.Model):
	_name = 'agente.general.disergonomico'

	registro_id = fields.Many2one('registro.monitoreo.disergonomico', string=u'Registro')
	area = fields.Char(string=u'Área')
	puesto_trabajo = fields.Char(string=u'Puesto de Trabajo')
	empleado = fields.Char(string=u'Empleado')
	ubicacion = fields.Char(string=u'Ubicación del Punto')
	actividades = fields.Char(string='Actividades')
	fuentes_peligro = fields.Char(string=u'Fuentes de Peligro')
	controles = fields.Char(string=u'Controles Existentes')
	active = fields.Boolean(string=u'Activo', default=True)
	capacitacion = fields.Boolean("Capacitaciones", default=False)
	imagen = fields.Binary(string=u'Imagen')


class RiesgoDisergonomico(models.Model):
	_name = 's3.riesgo.disergonomico'
	_inherits = {'agente.general.disergonomico': 'agente_general_id'}

	agente_general_id = fields.Many2one('agente.general.disergonomico', required=True, ondelete='restrict',
										string='Agente General')
	postura_1 = fields.Boolean(string='Las manos por encima de la cabeza')
	postura_2 = fields.Boolean(string='Las codos por encima del hombro')
	postura_3 = fields.Boolean(string='Espalda inclinada hacia adelante más de 30 grados')
	postura_4 = fields.Boolean(string='Espalda en extensión más de 30 grados')
	postura_5 = fields.Boolean(string='Cuello doblado / girado más de 30 grados')
	postura_6 = fields.Boolean(string='Estando sentado, espalda inclinada hacia adelante más de 30 grados')
	postura_7 = fields.Boolean(string='Estando sentado, espalda girada o lateralizada más de 30 grados')
	postura_8 = fields.Boolean(string='De cuclillas')
	postura_9 = fields.Boolean(string='De rodillas')
	postura_10 = fields.Boolean(string='Más de 2 horas en total por día')
	levantamiento_1 = fields.Boolean(string='40 KG. Una vez/ día')
	levantamiento_2 = fields.Boolean(string='25 KG. Más de doce veces / hora')
	levantamiento_3 = fields.Boolean(string='5 KG. Más de doce veces / minuto')
	levantamiento_4 = fields.Boolean(string='Menos de 3 Kg. Más de cuatro veces / min')
	levantamiento_5 = fields.Boolean(string='Durante más de 2 horas por día')
	esfuerzo_1 = fields.Boolean(string='Si se manipula y sujeta en pinza un objeto de más de 1kg')
	esfuerzo_2 = fields.Boolean(
		string='Si las muñecas están flexionadas en extensión, giradas o lateralizadas haciendo un agarre con fuerza')
	esfuerzo_3 = fields.Boolean(string='Si se ejecuta la acción de atornillar de forma intensa')
	esfuerzo_4 = fields.Boolean(string='Durante más de 2 horas por día')
	movimiento_1 = fields.Boolean(
		string='El trabajador repite el mismo movimiento muscular más de 4 veces/min. durante más de 2 horas por día')
	impacto_1 = fields.Boolean(
		string='Usando manos o rodillas como un martillo más de 10 veces por hora, más de 2 horas por día')
	vibracion_1 = fields.Boolean(string='Nivel moderado: más de 30 min/día')
	vibracion_2 = fields.Boolean(string='Nivel alto: 2horas/día')

class ProductRegistro(models.Model):
	_inherit = "registro.monitoreo.disergonomico"

	reba_ids = fields.One2many('reba.reba.disergonomico', 'registro_id', string=u'REBA')
	# puntos_reba = fields.Integer(compute="_compute_puntos_reba", string=u"REBA")
	#
	# @api.depends("reba_ids")
	# def _compute_puntos_reba(self):
	# 	for record in self:
	# 		record.puntos_reba = len(record.reba_ids)

class Reba(models.Model):
	_name = 'reba.reba.disergonomico'
	_inherits = {'s3.riesgo.disergonomico': 'riesgo_disergonomico_id'}

	riesgo_disergonomico_id = fields.Many2one('s3.riesgo.disergonomico', required=True, ondelete='restrict',
											  auto_join=True, string='Riesgo Disergonomico')

	peso = fields.Float(string='Peso de Carga')
	puntuacion_a = fields.Integer(compute="_compute_reba", string="Puntuación del Grupo A", store=True)
	tronco = fields.Integer(compute="_compute_reba", string="Tronco", store=True)
	cuello = fields.Integer(compute="_compute_reba", string="Cuello", store=True)
	piernas = fields.Integer(compute="_compute_reba", string="Piernas", store=True)
	flexion_tronco = fields.Integer(string="Flexion o Extención de Tronco", default=1, store=True)
	flexion_tronco_texto = fields.Char(compute="_compute_reba", string="Flexion o Extención de Tronco", store=True)
	extension_tronco = fields.Integer(string=u"Torsión o Inclinación Lateral", default=0, store=True)
	extension_tronco_texto = fields.Char(compute="_compute_reba", string="Torsión o Inclinación Lateral", store=True)
	flexion_cuello = fields.Integer(string=u"Flexión o Extensión de Cuello", default=1, store=True)
	flexion_cuello_texto = fields.Char(compute="_compute_reba", string="Flexión o Extensión de Cuello", store=True)
	extension_cuello = fields.Integer(string="Cabeza Rotada o con Inclinación Lateral", default=0, store=True)
	extension_cuello_texto = fields.Char(compute="_compute_reba", string="Cabeza Rotada o con Inclinación Lateral", store=True)
	soporte_pie = fields.Integer(string="Soporte de Pies", default=1, store=True)
	soporte_pie_texto = fields.Char(compute="_compute_reba", string="Soporte de Pies", store=True)
	flexion_rodilla = fields.Integer(string="Flexión en Rodillas", default=0, store=True)
	flexion_rodilla_texto = fields.Char(compute="_compute_reba", string="Flexión en Rodillas", store=True)

	@api.onchange("flexion_tronco", "extension_tronco", "flexion_cuello", "extension_cuello", "soporte_pie", "flexion_rodilla")
	def cambio_puntos_a(self):
		for record in self:
			if record.flexion_tronco < 1 or record.flexion_tronco > 4:
				record.flexion_tronco = 1
			if record.extension_tronco < 0 or record.extension_tronco > 2:
				record.extension_tronco = 0
			if record.flexion_cuello < 1 or record.flexion_cuello > 2:
				record.flexion_cuello = 1
			if record.extension_cuello < 0 or record.extension_cuello > 2:
				record.extension_cuello = 0
			if record.soporte_pie < 1 or record.soporte_pie > 2:
				record.soporte_pie = 1
			if record.flexion_rodilla < 0 or record.flexion_rodilla > 2:
				record.flexion_rodilla = 0

	# B
	puntuacion_b = fields.Integer(compute="_compute_reba", string="Puntuación del Grupo B", store=True)
	brazo = fields.Integer(compute="_compute_reba", string="Brazo", store=True)
	antebrazo = fields.Integer(compute="_compute_reba", string="Antebrazo", store=True)
	muneca = fields.Integer(compute="_compute_reba", string="Muñeca", store=True)
	extension_brazo = fields.Integer(string="Extensión o Flexión de Brazo", default=1, store=True)
	extension_brazo_texto = fields.Char(compute="_compute_reba", string="Extensión o Flexión de Brazo", store=True)
	correccion_brazo = fields.Integer(string="Correcciones del Brazo", default=0, store=True)
	correccion_brazo_texto = fields.Char(compute="_compute_reba", string="Correcciones del Brazo", store=True)
	extension_antebrazo = fields.Integer(string="Extensión o Flexión de Antebrazo", default=1, store=True)
	extension_antebrazo_texto = fields.Char(compute="_compute_reba", string="Extensión o Flexión de Antebrazo", store=True)
	extension_muneca = fields.Integer(string="Extensión o Flexión de Muñeca", default=1, store=True)
	extension_muneca_texto = fields.Char(compute="_compute_reba", string="Extensión o Flexión de Muñeca", store=True)
	torsion_muneca = fields.Integer(string="Presenta Torsión o Desviación Radial o Cubital", default=0, store=True)
	torsion_muneca_texto = fields.Char(compute="_compute_reba", string="Presenta Torsión o Desviación Radial o Cubital", store=True)

	@api.onchange("extension_brazo", "correccion_brazo", "extension_antebrazo", "extension_muneca", "torsion_muneca")
	def cambio_puntos_b(self):
		for record in self:
			if record.extension_brazo < 1 or record.extension_brazo > 4:
				record.extension_brazo = 1
			if record.correccion_brazo < -1 or record.correccion_brazo > 1:
				record.correccion_brazo = 0
			if record.extension_antebrazo < 1 or record.extension_antebrazo > 2:
				record.extension_antebrazo = 1
			if record.extension_muneca < 0 or record.extension_muneca > 2:
				record.extension_muneca = 0
			if record.torsion_muneca < 0 or record.torsion_muneca > 2:
				record.torsion_muneca = 0

	# C
	puntuacion_c = fields.Integer(compute="_compute_reba", string="Puntuación del Grupo C", store=True)
	fuerza_carga = fields.Integer(compute="_compute_reba", string="Fuerzas de Cargas", store=True)
	cantidad_carga = fields.Integer(string="Carga o Fuerza", default=0, store=True)
	cantidad_carga_texto = fields.Char(compute="_compute_reba", string="Carga o Fuerza", store=True)
	fuerza_brusca = fields.Integer(string="Existen Fuerzas o Cargas Aplicadas Bruscamente", default=0, store=True)
	fuerza_brusca_texto = fields.Char(compute="_compute_reba", string="Existen Fuerzas o Cargas Aplicadas Bruscamente", store=True)
	agarre = fields.Integer(compute="_compute_reba", string="Calidad de Agarre", store=True)
	agarre_tipo = fields.Integer(string="Tipo de Agarre", default=0, store=True)
	agarre_tipo_texto = fields.Char(compute="_compute_reba", string="Tipo de Agarre", store=True)
	agarre_tipo_texto_1 = fields.Char(compute="_compute_reba", string="Tipo de Agarre", store=True)
	acti_muscular = fields.Integer(compute="_compute_reba", string="Tipo de Actividad Muscular", store=True)
	tip_muscu = fields.Boolean(string="Una o más partes del cuerpo permanecen estáticas soportadas durante más de 1 minuto", default=False, store=True)
	tip_muscu_1 = fields.Boolean(string="Se producen movimientos repetitivos, por ejemplo repetidos más de 4 veces por minuto (excluyendo caminar)", default=False, store=True)
	tip_muscu_2 = fields.Boolean(string="Se producen cambios de postura importantes o se adoptan posturas inestables", default=False, store=True)

	@api.onchange("cantidad_carga", "fuerza_brusca", "agarre_tipo")
	def cambio_puntos_c(self):
		for record in self:
			if record.cantidad_carga < 0 or record.cantidad_carga > 2:
				record.cantidad_carga = 0
			if record.fuerza_brusca < 0 or record.fuerza_brusca > 2:
				record.fuerza_brusca = 0
			if record.agarre_tipo < 0 or record.agarre_tipo > 3:
				record.agarre_tipo = 0
	# Final
	puntuacion = fields.Integer(compute="_compute_reba", string="Puntuación Final", store=True)
	nivel_riesgo = fields.Char(compute="_compute_reba", string="Nivel de Riesgo", store=True)
	nivel_actuacion = fields.Integer(compute="_compute_reba", string="Nivel de Actuación", store=True)
	cumple = fields.Char(compute="_compute_reba", string="¿Cumple?", store=True)

	@api.depends("flexion_tronco", "extension_tronco", "flexion_cuello", "extension_cuello", "soporte_pie", "flexion_rodilla", "extension_brazo",
				 "correccion_brazo", "extension_antebrazo", "extension_muneca", "torsion_muneca", "tip_muscu", "tip_muscu_1", "tip_muscu_2",
				 "cantidad_carga", "fuerza_brusca", "agarre_tipo", "nivel_riesgo")
	def _compute_reba(self):
		for record in self:
			if record.flexion_tronco == 0:
				record.flexion_tronco_texto = ""

			if record.flexion_tronco >= 1 and record.extension_tronco >= 0:

				if record.flexion_tronco == 1:
					record.flexion_tronco_texto = "Tronco Erguido"
				elif record.flexion_tronco == 2:
					record.flexion_tronco_texto = "Flexión o Extensión entre 0° y 20°"
				elif record.flexion_tronco == 3:
					record.flexion_tronco_texto = "Flexión  >20° y ≤60° o Extensión >20°"
				elif record.flexion_tronco == 4:
					record.flexion_tronco_texto = "Flexión >60°"

				if record.extension_tronco == 0:
					record.extension_tronco_texto = u"No"
				elif record.extension_tronco > 0:
					record.extension_tronco_texto = u"Sí"

				record.tronco = record.flexion_tronco + record.extension_tronco

			if record.flexion_cuello == 0:
				record.flexion_cuello_texto = ""
			if record.flexion_cuello >= 1 and record.extension_cuello >= 0:

				if record.flexion_cuello == 1:
					record.flexion_cuello_texto = "Flexión entre 0° y 20°"
				elif record.flexion_cuello == 2:
					record.flexion_cuello_texto = "Flexión  >20° o Extensión"

				if record.extension_cuello == 0:
					record.extension_cuello_texto = "No"
				elif record.extension_cuello > 0:
					record.extension_cuello_texto = "Sí"

				record.cuello = record.extension_cuello + record.flexion_cuello

			if record.soporte_pie == 0:
				record.soporte_pie_texto = "Sentado, Andando o de Pie con Soporte Bilateral Simétrico"

			if record.soporte_pie >= 1 and record.flexion_rodilla >= 0:
				if record.soporte_pie == 1:
					record.soporte_pie_texto = "Sentado, Andando o de Pie con Soporte Bilateral Simétrico"
				elif record.soporte_pie == 2:
					record.soporte_pie_texto = "De Pie con Soporte Unilateral, Soporte Ligero o Postura Inestable"

				if record.flexion_rodilla == 0:
					record.flexion_rodilla_texto = "No Presenta Flexión de Rodillas"
				elif record.flexion_rodilla == 1:
					record.flexion_rodilla_texto = "Flexión de una o ambas Rodillas entre 30 y 60°"
				elif record.flexion_rodilla == 2:
					record.flexion_rodilla_texto = "Flexión de una o ambas rodillas de más de 60° (salvo postura sedente)"

				record.piernas = record.soporte_pie + record.flexion_rodilla

			if record.cantidad_carga >= 0 and record.fuerza_brusca >= 0:
				record.fuerza_carga = record.cantidad_carga + record.fuerza_brusca

				if record.cantidad_carga == 0:
					record.cantidad_carga_texto = "Carga o fuerza menor de 5 Kg."
				elif record.cantidad_carga == 1:
					record.cantidad_carga_texto = "Carga o fuerza entre 5 y 10 Kg."
				elif record.cantidad_carga == 2:
					record.cantidad_carga_texto = "Carga o fuerza mayor de  10 Kg."

				if record.fuerza_brusca == 0:
					record.fuerza_brusca_texto = "No"
				elif record.fuerza_brusca > 0:
					record.fuerza_brusca_texto = "Sí"

			# puntuacion A
			if record.tronco == 1:
				if record.cuello == 1 or record.cuello == 2:
					if record.piernas == 1:
						record.puntuacion_a = 1 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 2 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 3 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 4 + record.fuerza_carga
				elif record.cuello == 3:
					if record.piernas == 1:
						record.puntuacion_a = 3 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 3 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 6 + record.fuerza_carga
			if record.tronco == 2:
				if record.cuello == 1:
					if record.piernas == 1:
						record.puntuacion_a = 2 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 3 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 4 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 5 + record.fuerza_carga
				elif record.cuello == 2:
					if record.piernas == 1:
						record.puntuacion_a = 3 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 4 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 6 + record.fuerza_carga
				elif record.cuello == 3:
					if record.piernas == 1:
						record.puntuacion_a = 4 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 7 + record.fuerza_carga
			if record.tronco == 3:
				if record.cuello == 1:
					if record.piernas == 1:
						record.puntuacion_a = 2 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 4 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 6 + record.fuerza_carga
				elif record.cuello == 2:
					if record.piernas == 1:
						record.puntuacion_a = 4 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 7 + record.fuerza_carga
				elif record.cuello == 3:
					if record.piernas == 1:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 7 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 8 + record.fuerza_carga
			if record.tronco == 4:
				if record.cuello == 1:
					if record.piernas == 1:
						record.puntuacion_a = 3 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 7 + record.fuerza_carga
				elif record.cuello == 2:
					if record.piernas == 1:
						record.puntuacion_a = 5 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 7 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 8 + record.fuerza_carga
				elif record.cuello == 3:
					if record.piernas == 1:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 7 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 8 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 9 + record.fuerza_carga
			if record.tronco == 5:
				if record.cuello == 1:
					if record.piernas == 1:
						record.puntuacion_a = 4 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 7 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 8 + record.fuerza_carga
				elif record.cuello == 2:
					if record.piernas == 1:
						record.puntuacion_a = 6 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 7 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 8 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 9 + record.fuerza_carga
				elif record.cuello == 3:
					if record.piernas == 1:
						record.puntuacion_a = 7 + record.fuerza_carga
					elif record.piernas == 2:
						record.puntuacion_a = 8 + record.fuerza_carga
					elif record.piernas == 3:
						record.puntuacion_a = 9 + record.fuerza_carga
					elif record.piernas == 4:
						record.puntuacion_a = 9 + record.fuerza_carga

			if record.agarre_tipo >= 0:
				record.agarre = record.agarre_tipo
				if record.agarre_tipo == 0:
					record.agarre_tipo_texto = "Bueno"
					record.agarre_tipo_texto_1 = "El agarre es bueno y la fuerza de agarre de rango medio"
				elif record.agarre_tipo == 1:
					record.agarre_tipo_texto = "Regular"
					record.agarre_tipo_texto_1 = "El agarre es aceptable pero no ideal o el agarre es aceptable utilizando otras partes del cuerpo"
				elif record.agarre_tipo == 2:
					record.agarre_tipo_texto = "Malo"
					record.agarre_tipo_texto_1 = "El agarre es posible pero no aceptable"
				elif record.agarre_tipo == 3:
					record.agarre_tipo_texto = "Inaceptable"
					record.agarre_tipo_texto_1 = "El agarre es torpe e inseguro, no es posible el agarre manual o el agarre es inaceptable utilizando" \
												 " otras partes del cuerpo"

			if record.extension_brazo == 0:
				record.extension_brazo_texto = ""
			if record.extension_brazo >= 1 and record.correccion_brazo >= 0:
				record.brazo = record.extension_brazo + record.correccion_brazo
				if record.extension_brazo == 1:
					record.extension_brazo_texto = "Desde 20° de Extensión a 20° de Flexión"
				elif record.extension_brazo == 2:
					record.extension_brazo_texto = "Extensión >20° o Flexión >20° y <45°"
				elif record.extension_brazo == 3:
					record.extension_brazo_texto = "Flexión >45° y 90°"
				elif record.extension_brazo == 4:
					record.extension_brazo_texto = "Flexión >90°"

				if record.correccion_brazo == 0:
					record.correccion_brazo_texto = "No Presenta Correcciones"
				elif record.correccion_brazo == 1:
					record.correccion_brazo_texto = "Brazo Abducido, Brazo Rotado u Hombro Elevado"
				elif record.correccion_brazo == -1:
					record.correccion_brazo_texto = "Existe un Punto de Apoyo o la Postura a Favor de la Gravedad"

			if record.extension_antebrazo == 0:
				record.extension_antebrazo_texto = ""

			if record.extension_antebrazo >= 1:
				record.antebrazo = record.extension_antebrazo
				if record.extension_antebrazo == 1:
					record.extension_antebrazo_texto = "Flexión entre 60° y 100°"
				elif record.extension_antebrazo == 2:
					record.extension_antebrazo_texto = "Flexión <60° o >100°"
			if record.extension_muneca == 0:
				record.extension_muneca_texto = "Posición neutra"
			if record.extension_muneca >= 1 and record.torsion_muneca >= 0:
				record.muneca = record.extension_muneca + record.torsion_muneca

				if record.extension_muneca == 1:
					record.extension_muneca_texto = "Flexión o extensión > 0° y <15°"
				elif record.extension_muneca == 2:
					record.extension_muneca_texto = "Flexión o extensión >15°"

				if record.torsion_muneca == 0:
					record.torsion_muneca_texto = "No"
				elif record.torsion_muneca > 0:
					record.torsion_muneca_texto = "Sí"

			# puntuacion B
			if record.brazo == 1:
				if record.antebrazo == 1:
					if record.muneca == 1:
						record.puntuacion_b = 1 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 2 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 2 + record.agarre
				elif record.antebrazo == 2:
					if record.muneca == 1:
						record.puntuacion_b = 1 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 2 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 3 + record.agarre
			elif record.brazo == 2:
				if record.antebrazo == 1:
					if record.muneca == 1:
						record.puntuacion_b = 1 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 2 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 3 + record.agarre
				elif record.antebrazo == 2:
					if record.muneca == 1:
						record.puntuacion_b = 2 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 3 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 4 + record.agarre
			if record.brazo == 3:
				if record.antebrazo == 1:
					if record.muneca == 1:
						record.puntuacion_b = 3 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 4 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 5 + record.agarre
				elif record.antebrazo == 2:
					if record.muneca == 1:
						record.puntuacion_b = 4 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 5 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 5 + record.agarre
			if record.brazo == 4:
				if record.antebrazo == 1:
					if record.muneca == 1:
						record.puntuacion_b = 4 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 5 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 5 + record.agarre
				elif record.antebrazo == 2:
					if record.muneca == 1:
						record.puntuacion_b = 5 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 6 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 7 + record.agarre
			if record.brazo == 5:
				if record.antebrazo == 1:
					if record.muneca == 1:
						record.puntuacion_b = 6 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 7 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 8 + record.agarre
				elif record.antebrazo == 2:
					if record.muneca == 1:
						record.puntuacion_b = 7 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 8 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 8 + record.agarre
			if record.brazo == 6:
				if record.antebrazo == 1:
					if record.muneca == 1:
						record.puntuacion_b = 7 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 8 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 8 + record.agarre
				elif record.antebrazo == 2:
					if record.muneca == 1:
						record.puntuacion_b = 8 + record.agarre
					elif record.muneca == 2:
						record.puntuacion_b = 9 + record.agarre
					elif record.muneca == 3:
						record.puntuacion_b = 9 + record.agarre

			cont = 0
			if record.tip_muscu:
				cont = cont + 1
			if record.tip_muscu_1:
				cont = cont + 1
			if record.tip_muscu_2:
				cont = cont + 1

			record.acti_muscular = cont
			record.puntuacion = 1
			if record.puntuacion_a == 1:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 1
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 1
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 1
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 2
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 3
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 3
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 5
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 7
			elif record.puntuacion_a == 2:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 1
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 2
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 2
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 3
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 5
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 8
			if record.puntuacion_a == 3:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 2
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 3
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 3
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 3
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 5
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 8
			if record.puntuacion_a == 4:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 3
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 5
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 9
			if record.puntuacion_a == 5:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 4
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 5
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 9
			if record.puntuacion_a == 6:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 6
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 10
			if record.puntuacion_a == 7:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 7
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 11
			if record.puntuacion_a == 8:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 8
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 11
			if record.puntuacion_a == 9:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 9
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 12
			if record.puntuacion_a == 10:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 10
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 12
			if record.puntuacion_a == 11:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 11
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 12
			if record.puntuacion_a == 12:
				if record.puntuacion_b == 1:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 2:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 3:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 4:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 5:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 6:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 7:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 8:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 9:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 10:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 11:
					record.puntuacion_c = 12
				elif record.puntuacion_b == 12:
					record.puntuacion_c = 12
			record.puntuacion = record.puntuacion_c + record.acti_muscular

			if record.puntuacion == 1:
				record.nivel_riesgo = "INAPRECIABLE"
				record.nivel_actuacion = 0
				record.cumple = "SI CUMPLE"
			elif record.puntuacion == 2:
				record.nivel_riesgo = "BAJO"
				record.nivel_actuacion = 1
				record.cumple = "SI CUMPLE"
			elif record.puntuacion == 3:
				record.nivel_riesgo = "BAJO"
				record.nivel_actuacion = 1
				record.cumple = "SI CUMPLE"
			elif record.puntuacion == 4:
				record.nivel_riesgo = "MEDIO"
				record.nivel_actuacion = 2
				record.cumple = "SI CUMPLE"
			elif record.puntuacion == 5:
				record.nivel_riesgo = "MEDIO"
				record.nivel_actuacion = 2
				record.cumple = "SI CUMPLE"
			elif record.puntuacion == 6:
				record.nivel_riesgo = "MEDIO"
				record.nivel_actuacion = 2
				record.cumple = "SI CUMPLE"
			elif record.puntuacion == 7:
				record.nivel_riesgo = "MEDIO"
				record.nivel_actuacion = 2
				record.cumple = "SI CUMPLE"
			elif record.puntuacion == 8:
				record.nivel_riesgo = "ALTO"
				record.nivel_actuacion = 3
				record.cumple = "NO CUMPLE"
			elif record.puntuacion == 9:
				record.nivel_riesgo = "ALTO"
				record.nivel_actuacion = 3
				record.cumple = "NO CUMPLE"
			elif record.puntuacion == 10:
				record.nivel_riesgo = "ALTO"
				record.nivel_actuacion = 3
				record.cumple = "NO CUMPLE"
			elif record.puntuacion == 11:
				record.nivel_riesgo = "MUY ALTO"
				record.nivel_actuacion = 4
				record.cumple = "NO CUMPLE"
			elif record.puntuacion == 12:
				record.nivel_riesgo = "MUY ALTO"
				record.nivel_actuacion = 4
				record.cumple = "NO CUMPLE"
			elif record.puntuacion == 13:
				record.nivel_riesgo = "MUY ALTO"
				record.nivel_actuacion = 4
				record.cumple = "NO CUMPLE"
			elif record.puntuacion == 14:
				record.nivel_riesgo = "MUY ALTO"
				record.nivel_actuacion = 4
				record.cumple = "NO CUMPLE"
			elif record.puntuacion == 15:
				record.nivel_riesgo = "MUY ALTO"
				record.nivel_actuacion = 4
				record.cumple = "NO CUMPLE"

# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
import math

class ProductProduct(models.Model):
	_inherit = "registro.monitoreo"

	polvo_inhalable_ids = fields.One2many('polvo.inhalable', 'registro_id', string=u'Polvo Inhalable')
	puntos_inha = fields.Integer(compute="_compute_puntos_inha", string=u"Polvo Inhalable")

	@api.depends("polvo_inhalable_ids")
	def _compute_puntos_inha(self):
		for record in self:
			record.puntos_inha = len(record.polvo_inhalable_ids)


class PolvoInhalable(models.Model):
	_name = "polvo.inhalable"
	_inherits = {'agente.general': 'agente_general_id'}

	agente_general_id = fields.Many2one('agente.general', required=True, ondelete='restrict', auto_join=True,
										string='Agente General')
	codigo = fields.Char("Código de Muestra", required=True)
	hora_inicio = fields.Float("Hora de Inicio", required=True)
	hora_fin = fields.Float("Hora Final", required=True)
	jornada = fields.Float("Jornada Laboral (horas)", required=True)
	tiempo_expo = fields.Float("Tiempo de Exposición (horas)", required=True)
	tiempo_medio = fields.Float(compute="_compute_polvo", digits=(16, 0), string="Tiempo Medido (min)", required=True)
	flujo_promedio = fields.Float("Flujo Promedio (L/min)", required=True)
	volumen = fields.Float(compute="_compute_polvo", string="Volumen (m³)", digits=(16, 3), store=True)
	peso_inicial = fields.Float("Peso Inicial (g)", digits=(16, 6), required=True)
	peso_final = fields.Float("Peso Final (g)", digits=(16, 6), required=True)
	muestra = fields.Float(compute="_compute_polvo", string="Δ Muestra (mg)", digits=(16, 3), store=True)
	concentracion = fields.Float(compute="_compute_polvo", string="Concentración (mg/m³)", digits=(16, 3), store=True)
	concentracion_real = fields.Float(compute="_compute_polvo", string="Concentración Real (mg/m³)", digits=(16, 3), store=True)
	tlv = fields.Float(compute="_compute_polvo", string="TLV-TWAc (mg/m³)", digits=(16, 2), store=True)
	indice = fields.Float(compute="_compute_polvo", string="Indice de Exposición (%)", digits=(16, 2), store=True)
	cumple = fields.Char(compute="_compute_polvo", string="¿Cumple el D.S. N° 015-2005 S.A?", store=True)

	@api.depends("hora_inicio", "hora_fin", "jornada", "tiempo_expo", "flujo_promedio", "peso_inicial", "peso_final")
	def _compute_polvo(self):
		for record in self:
			if record.hora_inicio:
				inicio_min = (record.hora_inicio - math.trunc(record.hora_inicio))*60
				inicio_hor = math.trunc(record.hora_inicio)
				inicio_minuto = inicio_min + inicio_hor*60
				if record.hora_fin:
					fin_min = (record.hora_fin - math.trunc(record.hora_fin))*60
					fin_hor = math.trunc(record.hora_fin)
					fin_minuto = fin_min + fin_hor*60
					record.tiempo_medio = fin_minuto - inicio_minuto
				else:
					record.tiempo_medio = 0.00
			else:
				record.tiempo_medio = 0.00

			if record.flujo_promedio:
				record.volumen = (record.tiempo_medio*record.flujo_promedio)/1000
			else:
				record.volumen = 0.00

			if record.peso_final:
				if record.peso_inicial:
					record.muestra = (record.peso_final - record.peso_inicial)*1000
				else:
					record.muestra = record.peso_final*1000
			else:
				record.muestra = 0.00

			if record.volumen != 0.00:
				if record.muestra:
					record.concentracion = record.muestra/record.volumen
				else:
					record.concentracion = 0.00

			if record.jornada != 0.00:
				if record.tiempo_expo:
					record.concentracion_real = (record.concentracion*record.tiempo_expo)/record.jornada
					record.tlv = ((8/record.jornada)*((24-record.jornada)/16))*10
				else:
					record.concentracion_real = 0.00
					record.tlv = 0.00

			if record.tlv != 0.00:
				if record.concentracion_real:
					record.indice = (record.concentracion_real*100.00 / record.tlv)
				else:
					record.indice = 0.00

			if record.tlv >= record.concentracion_real:
				record.cumple = "SI CUMPLE"
			else:
				record.cumple = "NO CUMPLE"

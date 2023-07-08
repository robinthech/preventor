# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
import math  # noqa
import base64  # noqa
import io  # noqa
from xlwt import easyxf, Workbook  # noqa
from xlwt import Formula  # noqa
from PIL import Image  # noqa
import xlsxwriter
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import os
import pytz


class Registroaccidente(models.Model):
	_name = 'registro.incidente'

	# Datos del empleador principal
	name = fields.Char("name",default="RI")
	sequence = fields.Char(compute='_compute_sequence', string="Codigo")
	razon = fields.Char("Razon Social")
	ruc = fields.Char("RUC")
	primeros_auxilios = fields.Char("Primeros Auxilios")
	domicilio = fields.Char("Domicilio")
	actividad = fields.Char("Actividad Economica")
	trabajadores = fields.Integer("Nº de Trabajadores")
	trabajadores_afiliados = fields.Integer("Nº de Trabajadores Afiliados")
	trabajadores_no_afiliados = fields.Integer("Nº de Trabajadores no Afiliados")
	aseguradora = fields.Char("Aseguradora")

	# Datos del empleador de intermediacion
	razon_terciario = fields.Char("Razon Social")
	ruc_terciario = fields.Char("RUC")
	domicilio_terciario = fields.Char("Domicilio")
	actividad_terciario = fields.Char("Actividad Economica")
	trabajadores_terciario = fields.Integer("Nº de Trabajadores")
	trabajadores_afiliados_terciario = fields.Integer("Nº de Trabajadores Afiliados")
	trabajadores_no_afiliados_terciario = fields.Integer("Nº de Trabajadores no Afiliados")
	aseguradora_terciario = fields.Char("Aseguradora")

	# Datos del trabajador
	trabajador = fields.Char("Trabajador")
	dni = fields.Char("DNI")
	edad = fields.Integer("Edad")
	area = fields.Char("Area")
	puesto = fields.Char("Puesto de trabajo")
	antiguedad = fields.Char("Antiguedad")
	sexo = fields.Selection(selection=[('F', 'Femenino'), ('M', 'Masculino')], string='Sexo', default='M')
	turno = fields.Selection(selection=[('D', 'Dia'), ('T', 'Tarde'), ('N', 'Noche')], string='Turno', default='D')
	tipo_incidente = fields.Selection(selection=[('P', 'Peligroso'), ('I', 'Incidente')], string='Tipo de incidente')
	contrato = fields.Char("Tipo de contrato")
	tiempo = fields.Char("Tiempo de experiencia")
	hora = fields.Integer("Nº de Horas trabajadas")

	# investigacion del accidente
	fecha_accidente = fields.Datetime(u"Fecha de Accidente")
	fecha_investigacion = fields.Date(u"Fecha de Investigacion")
	lugar_accidente = fields.Char("Lugar de accidente")
	gravedad_accidente = fields.Selection(selection=[('L', 'Accidente leve'), ('I', 'Accidente Incapacitante'), ('M', 'Mortal')], string='Gravedad accidente')
	gravedad_accidente_incapacitante = fields.Selection(selection=[('TT', 'Total temporal'), ('PT', 'Parcial temporal'), ('PP', 'Parcial permanente'), ('TP', 'Total permanente')], string='Gravedad accidente')
	dias_descanso = fields.Integer("Nº de dias de descanso")
	trabajadores_afectados = fields.Integer("Nº de trabajadores afectados")
	potencialmente_afectados = fields.Integer("Nº de trabajadores potencialmente afectados")
	pobladores_afectados = fields.Integer("Nº de pobladores potencialmente afectados")
	cuerpo = fields.Char("Parte del cuerpo")

	# Descripcion del accidente
	descripcion = fields.Text("Descripcion del accidente")
	descripcion_causas = fields.Text("Descripcion de las causas accidente")

	# medidas correcticas
	def default_medidas(self):
		medida_ids = self.env["medida.incidente.default"].search([])
		return [(0, 0, {'name': i.name, 'fecha_ejecucion': i.fecha_ejecucion }) for i in medida_ids]

	medida_ids = fields.One2many("medida.incidente", "accidente_id", "Medidas correctivas",default=default_medidas)


	def default_responsables(self):
		responsable_ids = self.env["incidente.responsable.final.default"].search([])
		return [(0, 0, {'name': i.name, 'fecha': i.fecha, 'cargo': i.cargo }) for i in responsable_ids]


	responsable_ids = fields.One2many("incidente.responsable.final", "responsable_id", "Responsable",default=default_responsables)

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "RI-000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "RI-00{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "RI-0{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "RI-{}".format(i)

class RegistroIncidenteTransient(models.TransientModel):
	_name = 'registro.incidente.transient'

	def guardar_linea(self,accidente_id,field,value):
		lineaedit = self.env["registro.incidente"].search([('id','=',accidente_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class MedidaIncidenteTransient(models.TransientModel):
	_name = 'medida.incidente.transient'

	def guardar_linea(self,medida_id,field,value):
		lineaedit = self.env["medida.incidente"].search([('id','=',medida_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class RegistroIncidente(models.Model):
	_name = 'medida.incidente'

	accidente_id = fields.Many2one("registro.incidente", string=u"Registro de accidente")
	name = fields.Char("Descripcion")
	responsable = fields.Many2one("incidente.responsable",string=u"Responsable")
	fecha_ejecucion = fields.Date("Fecha de ejecucion")
	estado = fields.Selection(selection=[('R', 'Realizado'), ('P', 'Pendiente'), ('E', 'En ejecucion')], string='Estado',default='P')

class MedidaIncidenteDefault(models.Model):
	_name = 'medida.incidente.default'

	name = fields.Char("Descripcion")
	fecha_ejecucion = fields.Date("Fecha de ejecucion")

class IncidenteResponsable(models.Model):
	_name = "incidente.responsable"

	name = fields.Char("Nombre Completo", store=True)

class IncidenteResponsableFinal(models.Model):
	_name = "incidente.responsable.final"

	responsable_id = fields.Many2one("registro.incidente", string=u"Registro de accidente")
	name = fields.Char("Nombre Completo", store=True)
	fecha = fields.Date("Fecha")
	cargo = fields.Char("Cargo")

class IncidenteResponsableFinalDefault(models.Model):
	_name = "incidente.responsable.final.default"

	name = fields.Char("Nombre Completo")
	fecha = fields.Date("Fecha")
	cargo = fields.Char("Cargo")

class IncidenteResponsableFinalTransient(models.TransientModel):
	_name = 'incidente.responsable.final.transient'

	def guardar_linea(self,medida_id,field,value):
		lineaedit = self.env["incidente.responsable.final"].search([('id','=',medida_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

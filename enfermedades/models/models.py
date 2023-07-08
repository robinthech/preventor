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


class EnfermedadesOcupacionales(models.Model):
	_name = 'enfermedades.ocupacionales'

	# Datos del empleador principal
	name = fields.Char("name",default="RI")
	sequence = fields.Char(compute='_compute_sequence', string="Codigo")
	razon = fields.Char("Razon Social")
	ruc = fields.Char("RUC")
	domicilio = fields.Char("Domicilio")
	actividad = fields.Char("Actividad Economica")
	trabajadores = fields.Integer("Nº de Trabajadores")
	trabajadores_afiliados = fields.Integer("Nº de Trabajadores Afiliados")
	trabajadores_no_afiliados = fields.Integer("Nº de Trabajadores no Afiliados")
	aseguradora = fields.Char("Aseguradora")
	año = fields.Integer("Año de inicio de la actividad",default=2021)
	servicios = fields.Text("Servicios")

	# Datos del empleador de intermediacion
	razon_terciario = fields.Char("Razon Social")
	ruc_terciario = fields.Char("RUC")
	domicilio_terciario = fields.Char("Domicilio")
	actividad_terciario = fields.Char("Actividad Economica")
	trabajadores_terciario = fields.Integer("Nº de Trabajadores")
	trabajadores_afiliados_terciario = fields.Integer("Nº de Trabajadores Afiliados")
	trabajadores_no_afiliados_terciario = fields.Integer("Nº de Trabajadores no Afiliados")
	aseguradora_terciario = fields.Char("Aseguradora")
	año_terciario = fields.Integer("Año de inicio de la actividad",default=2021)
	servicios_terciario = fields.Text("Servicios")

	# Datos del trabajador
	trabajador = fields.Char("Trabajador")
	dni = fields.Char("DNI")
	edad = fields.Integer("Edad")
	area = fields.Char("Area")
	puesto = fields.Char("Puesto de trabajo")
	antiguedad = fields.Char("Antiguedad")
	sexo = fields.Selection(selection=[('F', 'Femenino'), ('M', 'Masculino')], string='Sexo', default='M')
	turno = fields.Selection(selection=[('D', 'Dia'), ('T', 'Tarde'), ('N', 'Noche')], string='Turno', default='D')
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
		medida_ids = self.env["medida.enfermedades.default"].search([])
		return [(0, 0, {'name': i.name, 'fecha_ejecucion': i.fecha_ejecucion }) for i in medida_ids]

	medida_ids = fields.One2many("medida.enfermedades", "accidente_id", "Medidas correctivas",default=default_medidas)

	def default_relacion(self):
		sustancias_ids = self.env["relacion.sustancias.default"].search([])
		return [(0, 0, {'name': i.name, 'monitoreo': i.monitoreo }) for i in sustancias_ids]

	relacion_ids = fields.One2many("relacion.sustancias", "relacion_id", "Relacion de sustancias",default=default_relacion)


	def default_responsables(self):
		responsable_ids = self.env["enfermedades.responsable.final.default"].search([])
		return [(0, 0, {'name': i.name, 'fecha': i.fecha, 'cargo': i.cargo }) for i in responsable_ids]


	responsable_ids = fields.One2many("enfermedades.responsable.final", "responsable_id", "Responsable",default=default_responsables)
	enfermedad_ids = fields.One2many("datos.enfermedad", "enfermedad_id", "Enfermedad")

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "EO-000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "EO-00{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "EO-0{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "EO-{}".format(i)

class RegistroIncidenteTransient(models.TransientModel):
	_name = 'registro.enfermedades.transient'

	def guardar_linea(self,accidente_id,field,value):
		lineaedit = self.env["enfermedades.ocupacionales"].search([('id','=',accidente_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class MedidaIncidenteTransient(models.TransientModel):
	_name = 'medida.enfermedades.transient'

	def guardar_linea(self,medida_id,field,value):
		lineaedit = self.env["medida.enfermedades"].search([('id','=',medida_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class RegistroIncidente(models.Model):
	_name = 'medida.enfermedades'

	accidente_id = fields.Many2one("enfermedades.ocupacionales", string=u"Registro de accidente")
	name = fields.Char("Descripcion")
	responsable = fields.Many2one("enfermedades.responsable",string=u"Responsable")
	fecha_ejecucion = fields.Date("Fecha de ejecucion")
	estado = fields.Selection(selection=[('R', 'Realizado'), ('P', 'Pendiente'), ('E', 'En ejecucion')], string='Estado',default='P')

class RelacionSustanciaDefault(models.Model):
	_name = 'relacion.sustancias.default'

	name = fields.Char("Descripcion")
	monitoreo = fields.Boolean(string=u"Monitoreo")

class RelacionSustancia(models.Model):
	_name = 'relacion.sustancias'

	relacion_id = fields.Many2one("enfermedades.ocupacionales", string=u"Registro de accidente")
	name = fields.Char("Descripcion")
	monitoreo = fields.Boolean(string=u"Monitoreo",default=False)

class RelacionSustanciaTransient(models.TransientModel):
	_name = 'relacion.sustancias.transient'

	def guardar_linea(self,medida_id,field,value):
		lineaedit = self.env["relacion.sustancias"].search([('id','=',medida_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class DatosdeEnfermedad(models.Model):
	_name = 'datos.enfermedad'

	name = fields.Char("Descripcion")
	enfermedad_id = fields.Many2one("enfermedades.ocupacionales", string=u"Enfermedad Ocupacional")
	agente = fields.Many2one("tipo.agente",string=u"Agente")
	cuerpo = fields.Char("Parte del cuerpo")
	trabajadores = fields.Integer("Nº de Trabajadores")
	areas = fields.Char("Areas")

	enero_p = fields.Boolean("Enero (P)")
	enero_e = fields.Boolean("Enero (E)")
	enero_value = fields.Integer("Enero valor")
	febrero_p = fields.Boolean("Febrero (P)")
	febrero_e = fields.Boolean("Febrero (E)")
	febrero_value = fields.Integer("Febrero valor")
	marzo_p = fields.Boolean("Marzo (P)")
	marzo_e = fields.Boolean("Marzo (E)")
	marzo_value = fields.Integer("Marzo valor")
	abril_p = fields.Boolean("Abril (P)")
	abril_e = fields.Boolean("Abril (E)")
	abril_value = fields.Integer("Abril valor")
	mayo_p = fields.Boolean("Mayo (P)")
	mayo_e = fields.Boolean("Mayo (E)")
	mayo_value = fields.Integer("Mayo valor")
	junio_p = fields.Boolean("Junio (P)")
	junio_e = fields.Boolean("Junio (E)")
	junio_value = fields.Integer("Junio valor")
	julio_p = fields.Boolean("Julio (P)")
	julio_e = fields.Boolean("Julio (E)")
	julio_value = fields.Integer("Julio valor")
	agosto_p = fields.Boolean("Agosto (P)")
	agosto_e = fields.Boolean("Agosto (E)")
	agosto_value = fields.Integer("Agosto valor")
	septiembre_p = fields.Boolean("Septiembre (P)")
	septiembre_e = fields.Boolean("Septiembre (E)")
	septiembre_value = fields.Integer("septiembre valor")
	octubre_p = fields.Boolean("Octubre (P)")
	octubre_e = fields.Boolean("Octubre (E)")
	octubre_value = fields.Integer("octubre valor")
	noviembre_p = fields.Boolean("Noviembre (P)")
	noviembre_e = fields.Boolean("Noviembre (E)")
	noviembre_value = fields.Integer("noviembre valor")
	diciembre_p = fields.Boolean("Diciembre (P)")
	diciembre_e = fields.Boolean("Diciembre (E)")
	diciembre_value = fields.Integer("diciembre valor")

class DatosEnfermedadTransient(models.TransientModel):
	_name = 'datos.enfermedad.transient'

	def guardar_linea(self,medida_id,field,value):
		lineaedit = self.env["datos.enfermedad"].search([('id','=',medida_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class TipoAgente(models.Model):
	_name = 'tipo.agente'

	name = fields.Char("Descripcion")
	codigo = fields.Char("Codigo")
	agente = fields.Selection(selection=[('F', 'Fisico'), ('Q', 'Quimico'), ('B', 'Biologico'), ('D', 'Disergonomico'), ('P', 'Psicosociales')], string='Agente',default='F')

class TipoAgenteTransient(models.TransientModel):
	_name = 'tipo.agente.transient'

	def guardar_linea(self,medida_id,field,value):
		lineaedit = self.env["tipo.agente"].search([('id','=',medida_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class MedidaIncidenteDefault(models.Model):
	_name = 'medida.enfermedades.default'

	name = fields.Char("Descripcion")
	fecha_ejecucion = fields.Date("Fecha de ejecucion")

class IncidenteResponsable(models.Model):
	_name = "enfermedades.responsable"

	name = fields.Char("Nombre Completo", store=True)

class IncidenteResponsableFinal(models.Model):
	_name = "enfermedades.responsable.final"

	responsable_id = fields.Many2one("enfermedades.ocupacionales", string=u"Registro de accidente")
	name = fields.Char("Nombre Completo", store=True)
	fecha = fields.Date("Fecha")
	cargo = fields.Char("Cargo")

class IncidenteResponsableFinalDefault(models.Model):
	_name = "enfermedades.responsable.final.default"

	name = fields.Char("Nombre Completo")
	fecha = fields.Date("Fecha")
	cargo = fields.Char("Cargo")

class IncidenteResponsableFinalTransient(models.TransientModel):
	_name = 'enfermedades.responsable.final.transient'

	def guardar_linea(self,medida_id,field,value):
		lineaedit = self.env["enfermedades.responsable.final"].search([('id','=',medida_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

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

class EquiposSeguridad(models.Model):
	_name = 'equipos.seguridad'


	name = fields.Char("name",default="RI")
	sequence = fields.Char(compute='_compute_sequence', string="Codigo")
	razon = fields.Char("Razon Social")
	ruc = fields.Char("RUC")
	domicilio = fields.Char("Domicilio")
	actividad = fields.Char("Actividad Economica")
	trabajadores = fields.Integer("Nº de Trabajadores")

	tipo_personal = fields.Boolean(string="Equipo de protección personal",default=True)
	tipo_emergencia = fields.Boolean(string="Equipo de emergencia",default=True)

	fecha_accidente = fields.Datetime(u"Fecha de Accidente")
	firma = fields.Text("Firma")

	def default_proteccion(self):
		proteccion_ids = self.env["equipo.proteccion.default"].search([])
		return [(0, 0, {'name': i.name}) for i in proteccion_ids]

	proteccion_ids = fields.One2many("equipo.proteccion", "equipo_id", "Equipo proteccion",default=default_proteccion)

	def default_emergencia(self):
		emergencia_ids = self.env["equipo.emergencia.default"].search([])
		return [(0, 0, {'name': i.name}) for i in emergencia_ids]

	emergencia_ids = fields.One2many("equipo.emergencia", "emergencia_id", "Equipo emergencia",default=default_emergencia)

	def default_responsables(self):
		responsable_ids = self.env["seguridad.responsable.default"].search([])
		return [(0, 0, {'name': i.name, 'fecha': i.fecha, 'cargo': i.cargo }) for i in responsable_ids]

	responsable_ids = fields.One2many("seguridad.responsable", "responsable_id", "Responsable",default=default_responsables)

	def default_trabajadores(self):
		default_trabajadores = self.env["equipo.trabajadores.default"].search([])
		return [(0, 0, {'equipo_id': i.equipo_id, 'dni': i.dni, 'area': i.area, 'fecha_entrega': i.fecha_entrega, 'fecha_renovacion': i.fecha_renovacion }) for i in default_trabajadores]

	trabajador_ids = fields.One2many("equipo.trabajadores", "trabajador_id", "Trabajador",default=default_trabajadores)

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "ES-000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "ES-00{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "ES-0{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "ES-{}".format(i)

class EquipoSeguridadTransient(models.TransientModel):
	_name = 'equipos.seguridad.transient'

	def guardar_linea(self,accidente_id,field,value):
		lineaedit = self.env["equipos.seguridad"].search([('id','=',accidente_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class EquipoTrabajadores(models.Model):
	_name = 'equipo.trabajadores'

	trabajador_id = fields.Many2one("equipos.seguridad", string=u"Registro de seguridad")
	equipo_id = fields.Many2one('equipo.trabajadores.trabajadores',string='Nombre')
	dni = fields.Char(string='dni',related="equipo_id.dni")
	area = fields.Char(string='area')
	fecha_entrega = fields.Date(string='Fecha de entrega')
	fecha_renovacion = fields.Date(string='Fecha de renovacion')

class EquipoTrabajadoresDefault(models.Model):
	_name = 'equipo.trabajadores.default'

	equipo_id = fields.Many2one('equipo.trabajadores.trabajadores',string='Nombre')
	dni = fields.Char(string='dni')
	area = fields.Char(string='area')
	fecha_entrega = fields.Date(string='Fecha de entrega')
	fecha_renovacion = fields.Date(string='Fecha de renovacion')

class EquipoTrabajadoresFinal(models.Model):
	_name = 'equipo.trabajadores.trabajadores'

	trabajador_id = fields.One2many("equipo.trabajadores","equipo_id", string=u"Registro de trabajadores")
	name = fields.Char(string='Name')
	dni = fields.Char(string='dni')

class EquipoTrabajadoresTransient(models.TransientModel):
	_name = 'equipo.trabajadores.transient'

	def guardar_linea(self,accidente_id,field,value):
		lineaedit = self.env["equipo.trabajadores"].search([('id','=',accidente_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class EquipoProteccionDefault(models.Model):
	_name = 'equipo.proteccion.default'

	name = fields.Char("Descripcion")

class EquipoEmergenciaDefault(models.Model):
	_name = 'equipo.emergencia.default'

	name = fields.Char("Descripcion")

class EquipoProteccion(models.Model):
	_name = 'equipo.proteccion'

	equipo_id = fields.Many2one("equipos.seguridad", string=u"Registro de equipo de seguridad")
	name = fields.Char("Descripcion")
	equipo = fields.Boolean("Es un equipo de proteccion?")

class EquipoProteccionTransient(models.TransientModel):
	_name = 'equipo.proteccion.transient'

	def guardar_linea(self,accidente_id,field,value):
		lineaedit = self.env["equipo.proteccion"].search([('id','=',accidente_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class EquipoEmergencia(models.Model):
	_name = 'equipo.emergencia'

	emergencia_id = fields.Many2one("equipos.seguridad", string=u"Registro de equipo de seguridad")
	name = fields.Char("Descripcion")
	equipo = fields.Boolean("Es un equipo de proteccion?")

class EquipoEmergenciaTransient(models.TransientModel):
	_name = 'equipo.emergencia.transient'

	def guardar_linea(self,accidente_id,field,value):
		lineaedit = self.env["equipo.emergencia"].search([('id','=',accidente_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class EquipoResponsableFinal(models.Model):
	_name = "seguridad.responsable"

	responsable_id = fields.Many2one("equipos.seguridad", string=u"Registro de seguridad")
	name = fields.Char("Nombre Completo", store=True)
	fecha = fields.Date("Fecha")
	cargo = fields.Char("Cargo")

class EquipoResponsableFinalTransient(models.TransientModel):
	_name = 'seguridad.responsable.transient'

	def guardar_linea(self,accidente_id,field,value):
		lineaedit = self.env["seguridad.responsable"].search([('id','=',accidente_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class EquipoResponsableFinalDefault(models.Model):
	_name = "seguridad.responsable.default"

	name = fields.Char("Nombre Completo")
	fecha = fields.Date("Fecha")
	cargo = fields.Char("Cargo")

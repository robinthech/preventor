# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.http import request, content_disposition
import re
import logging

_logger = logging.getLogger(__name__)


class IpercContinuo(models.Model):
	_name = 'iperc.continuo'

	name = fields.Char("Codigo", index=True, default=lambda self: _('New'))
	ruc = fields.Char(string="RUC")
	cliente = fields.Char(string="Razon Social")
	sede = fields.Char(string=u'Sede')
	# sequence = fields.Char(compute='_compute_sequence', string="Codigo")


	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('iperc.continuo') or _('New')
		res = super(IpercContinuo, self).create(vals)
		return res

	def default_supervisor(self):
		supervisor_ids = self.env["supervisor.iperc.default"].search([])
		return [(0, 0, {'name': i.name, 'fecha': i.fecha }) for i in supervisor_ids]

	def default_control(self):
		control_ids = self.env["control.iperc.default"].search([])
		return [(0, 0, {'name': i.name }) for i in control_ids]

	def default_evaluacion(self):
		evaluacion_ids = self.env["evaluacion.iperc.default"].search([])
		return [(0, 0, {'name': i.name,'riesgo': i.riesgo}) for i in evaluacion_ids]

	def default_trabajador(self):
		trabajador_ids = self.env["trabajador.iperc.default"].search([])
		return [(0, 0, {'name': i.name,'fecha': i.fecha }) for i in trabajador_ids]

	@api.model
	def print_report(self):
		_logger.info('entramodelo')
		_logger.info(self.id)
		return self.env.ref('iperc_continuo.action_report_saleorder').report_action(self.id)

	trabajador_ids = fields.One2many("trabajador.iperc","iperc_id",string="Trabajadores",default=default_trabajador)
	evaluacion_ids = fields.One2many("evaluacion.iperc","iperc_id",string="Evaluacion",default=default_evaluacion)
	control_ids = fields.One2many("control.iperc","iperc_id",string="Control",default=default_control)
	supervisor_ids = fields.One2many("supervisor.iperc","iperc_id",string="Supervisor",default=default_supervisor)


class IpercContinuoTransient(models.TransientModel):
	_name = 'continuo.transient'

	def limites_permisos(self,plan_id):
		permiso_line = self.env['iperc.continuo'].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			return True
		else:
			return False

class TrabajadorIperc(models.Model):
	_name = 'trabajador.iperc'

	name = fields.Char("Trabajador")
	iperc_id = fields.Many2one("iperc.continuo",string=u'Iperc')
	fecha = fields.Date("Fecha")
	area = fields.Char(string=u'Nivel/Area')
	dni = fields.Char("DNI")
	#firma = fields.Char(string=u'Firma') Un Binario por en momento no ira

class TrabajadorIpercDefault(models.Model):
	_name = 'trabajador.iperc.default'

	name = fields.Char("Trabajador")
	fecha = fields.Date("Fecha")
	area = fields.Char(string=u'Nivel/Area')
	dni = fields.Char("DNI")

class TrabajadorIpercTransient(models.TransientModel):
	_name = 'trabajador.iperc.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["trabajador.iperc"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class TypeIperc(models.Model):
	_name = 'type.iperc'

	name = fields.Char("Tipo de riesgo")
	evaluacion_ids = fields.One2many("evaluacion.iperc","type_id",string="Riesgos")
	descripcion_ids = fields.One2many("descripcion.iperc","descripcion_id",string="Descripcion")

class EvaluacionIperc(models.Model):
	_name = 'descripcion.iperc'

	descripcion_id = fields.Many2one("type.iperc",string="Tipo de riesgo")
	name = fields.Char("Descripción")

class EvaluacionIperc(models.Model):
	_name = 'evaluacion.iperc'

	type_id = fields.Many2one("type.iperc",string="Tipo de riesgo")
	name = fields.Char("Descripción del Peligro")
	riesgo = fields.Char("Riesgo")
	iperc_id = fields.Many2one("iperc.continuo",string=u'Iperc')
	evaluacion = fields.Char("Evaluacion Iperc") # A, M, B
	riesgo_residual = fields.Char("Evaluacion Riesgo Residual") # A, M, B
	medidas = fields.Char("Medidas de Control")

class EvaluacionIpercDefault(models.Model):
	_name = 'evaluacion.iperc.default'

	name = fields.Char("Descripción del Peligro")
	riesgo = fields.Char("Riesgo")
	evaluacion = fields.Char("Evaluacion Iperc") # A, M, B
	riesgo_residual = fields.Char("Evaluacion Riesgo Residual") # A, M, B
	medidas = fields.Char("Medidas de Control")

class EvaluacionIpercTransient(models.TransientModel):
	_name = 'evaluacion.iperc.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["evaluacion.iperc"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class ControlIperc(models.Model):
	_name = 'control.iperc'

	name = fields.Char("Secuencia para el Control")
	iperc_id = fields.Many2one("iperc.continuo",string=u'Iperc')
	active = fields.Boolean("Activo",default=True)

class ControlIpercTransient(models.TransientModel):
	_name = 'control.iperc.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["control.iperc"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class ControlIpercDefault(models.Model):
	_name = 'control.iperc.default'

	name = fields.Char("Secuencia para el Control")
	active = fields.Boolean("Activo",default=True)

class SupervisorIperc(models.Model):
	_name = 'supervisor.iperc'

	name = fields.Char("Nombre del Supervisor")
	fecha = fields.Datetime("Fecha y Hora")
	iperc_id = fields.Many2one("iperc.continuo", string="Iperc")
	active = fields.Boolean("Activo",default=True)

class SupervisorIpercTransient(models.TransientModel):
	_name = 'supervisor.iperc.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["supervisor.iperc"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class SupervisorIpercDefault(models.Model):
	_name = 'supervisor.iperc.default'

	name = fields.Char("Nombre del Supervisor")
	fecha = fields.Datetime("Fecha y Hora")
	active = fields.Boolean("Activo",default=True)

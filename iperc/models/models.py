# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.http import request, content_disposition
import re
import logging

_logger = logging.getLogger(__name__)


class IperCompleto(models.Model):
	_name = 'iper.completo'

	name = fields.Char("Codigo", index=True, default=lambda self: _('New'))
	fecha = fields.Date(string="Fecha")
	cliente = fields.Char(string="Razon Social")
	responsable = fields.Char(string="Responsable")
	dni = fields.Char(string="DNI")
	direccion = fields.Char(string="Direccion")
	telefono = fields.Char(string="Telefono")
	email = fields.Char(string="Email")
	distrito = fields.Char(string="Distrito")
	provincia = fields.Char(string="Provincia")
	region = fields.Char(string="Region")
	actividad = fields.Char(string="Actividad economica")
	ciiu = fields.Char(string="ciiu")
	ruc = fields.Char(string="RUC")
	sede = fields.Many2one('sede.sede', string=u'Sede')
	# sequence = fields.Char(compute='_compute_sequence', string="Codigo")


	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('iper.completo') or _('New')
		res = super(IperCompleto, self).create(vals)
		return res

	def default_supervisor(self):
		supervisor_ids = self.env["supervisor.iper.default"].search([])
		return [(0, 0, {'name': i.name, 'fecha': i.fecha }) for i in supervisor_ids]


	def default_evaluacion(self):
		evaluacion_ids = self.env["evaluacion.iper.default"].search([])
		return [(0, 0, {'name': i.name,'riesgo': i.riesgo}) for i in evaluacion_ids]

	evaluacion_ids = fields.One2many("evaluacion.iper","iperc_id",string="Evaluacion",default=default_evaluacion)
	supervisor_ids = fields.One2many("supervisor.iper","iperc_id",string="Supervisor",default=default_supervisor)


class IperCompletoTransient(models.TransientModel):
	_name = 'iper.completo.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["iper.completo"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class TypeIperCompleto(models.Model):
	_name = 'type.iper'

	name = fields.Char("Tipo de riesgo")
	evaluacion_ids = fields.One2many("evaluacion.iper","type_id",string="Riesgos")
	descripcion_ids = fields.One2many("descripcion.iper","descripcion_id",string="Descripcion")

class DescripcionIperCompleto(models.Model):
	_name = 'descripcion.iper'

	descripcion_id = fields.Many2one("type.iper",string="Tipo de riesgo")
	name = fields.Char("Descripción")

class EvaluacionIperCompleto(models.Model):
	_name = 'evaluacion.iper'

	type_id = fields.Many2one("type.iper",string="Tipo de riesgo")
	name = fields.Char("Descripción del Peligro")
	area = fields.Char("Area")
	puesto = fields.Char("Puesto")
	riesgo = fields.Char("Riesgo")
	consecuencia = fields.Char("Consecuencia")
	causas = fields.Char("Causas")
	cumplimiento = fields.Char("Cumplimiento")
	iperc_id = fields.Many2one("iper.completo",string=u'Iper Completo')
	evaluacion = fields.Char("Evaluacion Iper") # A, M, B
	riesgo_residual = fields.Char("Evaluacion Riesgo Residual") # A, M, B
	medidas = fields.Char("Medidas de Control")

class EvaluacionIpercDefault(models.Model):
	_name = 'evaluacion.iper.default'

	name = fields.Char("Descripción del Peligro")
	riesgo = fields.Char("Riesgo")
	evaluacion = fields.Char("Evaluacion Iperc") # A, M, B
	riesgo_residual = fields.Char("Evaluacion Riesgo Residual") # A, M, B
	medidas = fields.Char("Medidas de Control")

class EvaluacionIpercTransient(models.TransientModel):
	_name = 'evaluacion.iper.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["evaluacion.iper"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

# class ControlIperc(models.Model):
# 	_name = 'control.iperc'
#
# 	name = fields.Char("Secuencia para el Control")
# 	iperc_id = fields.Many2one("iperc.continuo",string=u'Iperc')
# 	active = fields.Boolean("Activo",default=True)
#
# class ControlIpercTransient(models.TransientModel):
# 	_name = 'control.iperc.transient'
#
# 	def guardar_linea(self,linea_id,field,value):
# 		lineaedit = self.env["control.iperc"].search([('id','=',linea_id)],limit=1)
# 		lineaedit.write({'{}'.format(field):value})
# 		return True
#
# class ControlIpercDefault(models.Model):
# 	_name = 'control.iperc.default'
#
# 	name = fields.Char("Secuencia para el Control")
# 	active = fields.Boolean("Activo",default=True)
#
class SupervisorIper(models.Model):
	_name = 'supervisor.iper'

	responsable = fields.Many2one("res.users",string=u"Responsable")
	iperc_id = fields.Many2one("iper.completo",string=u'Iper Completo')
	active = fields.Boolean("Activo",default=True)

class SupervisorIperTransient(models.TransientModel):
	_name = 'supervisor.iper.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["supervisor.iper"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

	def guardar_firma(self, supervisor_id, usuario_id):
		supervisor_line = self.env["supervisor.iper"].search(
			[('id', '=', supervisor_id)], limit=1)
		supervisor_line.write({'responsable': usuario_id})
		usuario = self.env["res.users"].search(
			[('id', '=', usuario_id)], limit=1)
		src = ""
		if usuario.signature_binary:
			src = "data:image/png;base64, "+str(usuario.signature_binary)[2:-1]
		return src


class SupervisorIperDefault(models.Model):
	_name = 'supervisor.iper.default'

	name = fields.Char("Nombre del Supervisor")
	active = fields.Boolean("Activo",default=True)

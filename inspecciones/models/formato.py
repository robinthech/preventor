# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)
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
from odoo.tools.misc import profile


#plantilla de formato de inspecciones

class FormatoInspeccion(models.Model):
	_name= "formato.inspeccion"

	name = fields.Char(string="Nombre")
	area = fields.Char(string=u'Área')
	codigo = fields.Char(string=u'Código')
	fecha = fields.Date("Fecha Inicio de Monitoreo")
	origen = fields.Selection(selection=[('1', 'BASE'), ('2', 'GENERADO')], string="Origen", default="1")
	tipo = fields.Selection(selection=[('1', 'GENERAL'), ('2', 'SUB ESTANDARES'), ('3', 'ITEMS CRITICOS'), ('4', 'MONTACARGAS')], string="Estado", default="1")
	sub_total_max = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	sub_total_log = fields.Integer(compute="_compute_total",string="Puntaje Logrado")

	formato_id = fields.Many2one("formato.inspeccion",string="Formato de Inspeccion")
	condiciones_ids = fields.One2many("formato.condicion","inspeccion_id",string="Condiciones")
	inspectores_ids = fields.One2many("inspector.inspeccion","inspeccion_id",string="Inspector")

	@api.depends("condiciones_ids")
	def _compute_total(self):
		for rec in self:
			total_max = 0
			total_log = 0
			for line in rec.condiciones_ids:
				total_max += line.sub_total_max
				total_log += line.sub_total_log
			rec.sub_total_max = total_max
			rec.sub_total_log = total_log

	@api.model
	def create(self, vals):
		rec = super(FormatoInspeccion, self).create(vals)
		if "formato_id" in vals:
			formato = self.env["formato.inspeccion"].sudo().search([('id','=',int(vals["formato_id"]) )],limit=1)
			rec.tipo = formato.tipo
			for cond in formato.condiciones_ids:
				condicion = rec.condiciones_ids.create({"name":cond.name ,"is_comentario":cond.is_comentario ,"inspeccion_id":rec.id})
				for sub_cond in cond.sub_condiciones_ids:
					sub_condicion = condicion.sub_condiciones_ids.create({"name":sub_cond.name ,"puntaje_maximo":sub_cond.puntaje_maximo ,"condicion_id":condicion.id})
		return rec

class FormatoCondicion(models.Model):
	_name= "formato.condicion"

	name = fields.Char(string="Nombre")
	comentario = fields.Char(string="Comentarios")
	accion_correctiva = fields.Char(string="Comentarios")
	is_comentario = fields.Boolean(string="Comentarios")
	sub_total_max = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	sub_total_log = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	responsable_id = fields.Many2one("trabajador.trabajador",string="Responsble")
	fecha_cierre = fields.Date(string="Fecha Limite")
	fecha_limite = fields.Date(string="Fecha Cierre")
	rango_peligro = fields.Selection(selection=[('A', 'A'), ('B', 'B'), ('C', 'C')], string="Peligro Rango A,B,C", default="A")
	estado = fields.Selection(selection=[('1', 'PENDIENTE'), ('2', 'PROCESO'), ('3', 'PROCESO')], string="Estado", default="1")

	inspeccion_id = fields.Many2one("formato.inspeccion",string="Formato de Inspeccion")

	sub_condiciones_ids = fields.One2many("formato.sub.condicion","condicion_id",string="Sub Condiciones")

	@api.depends("sub_condiciones_ids")
	def _compute_total(self):
		for rec in self:
			total_max = 0
			total_log = 0
			for line in rec.sub_condiciones_ids:
				total_max += line.puntaje_maximo
				total_log += line.puntaje_logrado
			rec.sub_total_max = total_max
			rec.sub_total_log = total_log

class FormatoSubCondiciones(models.Model):
	_name= "formato.sub.condicion"

	name = fields.Char(string="Nombre")
	puntaje_maximo = fields.Integer(string="Puntaje Máximo")
	puntaje_logrado = fields.Integer(string="Puntaje Logrado")
	rango_peligro = fields.Selection(selection=[('A', 'A'), ('B', 'B'), ('C', 'C')], string="Peligro Rango A,B,C", default="A")
	nivel_riesgo = fields.Selection(selection=[('B', 'Bajo(B)'), ('M', 'Medio(M) '), ('A', 'Alto(A)'), ('E', 'Extremo(E)')], string="Nivel de Riesgo", default="A")
	responsable_id = fields.Many2one("trabajador.trabajador",string="Responsble")
	condicion_id = fields.Many2one("formato.condicion",string="Condicion")
	fecha_cierre = fields.Date(string="Fecha Limite")
	fecha_limite = fields.Date(string="Fecha Cierre")
	estado = fields.Selection(selection=[('1', 'PENDIENTE'), ('2', 'PROCESO'), ('3', 'PROCESO')], string="Estado", default="1")

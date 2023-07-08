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

class Inspecciones(models.Model):
	_name= "inspeccion"

	name = fields.Char(string="Nombre")
	area = fields.Char(string=u'Área')
	codigo = fields.Char(string=u'Código')
	fecha = fields.Date("Fecha Inicio de Monitoreo")
	sub_total_max = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	sub_total_log = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	tipo = fields.Selection(selection=[('1', 'GENERAL'), ('2', 'SUB ESTANDARES'), ('3', 'ITEMS CRITICOS'), ('4', 'MONTACARGAS')], string="Estado", default="1",related="formato_id.tipo")

	total_pendiente = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	total_proceso = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	total_cerrado = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	sede_id = fields.Many2one("sede.sede", string="Sede")

	formato_id = fields.Many2one("formato.inspeccion",string="Formato")

	condiciones_ids = fields.One2many("condicion.inspeccion","inspeccion_id",string="Condiciones")
	inspectores_ids = fields.One2many("inspector.inspeccion","inspeccion_id",string="Inspector")

	@api.model
	def create(self, vals):
		rec = super(Inspecciones, self).create(vals)
		if vals["formato_id"]:
			formato = self.env["formato.inspeccion"].sudo().search([('id','=',int(vals["formato_id"]) )],limit=1)
			for cond in formato.condiciones_ids:
				condicion = rec.condiciones_ids.create({"name":cond.name ,"is_comentario":cond.is_comentario ,"inspeccion_id":rec.id})
				for sub_cond in cond.sub_condiciones_ids:
					sub_condicion = condicion.sub_condiciones_ids.create({"name":sub_cond.name ,"puntaje_maximo":sub_cond.puntaje_maximo ,"condicion_id":condicion.id})
		return rec

	@api.depends("condiciones_ids")
	def _compute_total(self):
		for rec in self:
			total_max = 0
			total_log = 0
			total_pendiente = 0
			total_proceso = 0
			total_cerrado = 0
			for line in rec.condiciones_ids:
				total_max += line.sub_total_max
				total_log += line.sub_total_log
				if rec.tipo == '2':
					for line_sub in line.sub_condiciones_ids:
						if line_sub.estado and (line_sub.estado == '1'):
							total_pendiente += 1
						if line_sub.estado and (line_sub.estado == '2'):
							total_proceso += 1
						if line_sub.estado and (line_sub.estado == '3'):
							total_cerrado += 1
				elif rec.tipo == '3':
					if line.estado and (line.estado == '1'):
						total_pendiente += 1
					if line.estado and (line.estado == '2'):
						total_proceso += 1
					if line.estado and (line.estado == '3'):
						total_cerrado += 1
			rec.sub_total_max = total_max
			rec.sub_total_log = total_log
			rec.total_pendiente = total_pendiente
			rec.total_proceso = total_proceso
			rec.total_cerrado = total_cerrado


class CondicionInspeccion(models.Model):
	_name= "condicion.inspeccion"

	name = fields.Char(string="Nombre")
	comentario = fields.Char(string="Comentarios")
	is_comentario = fields.Boolean(string="Comentarios")
	sub_total_max = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	sub_total_log = fields.Integer(compute="_compute_total",string="Puntaje Logrado")
	responsable_id = fields.Many2one("trabajador.trabajador",string="Responsble")
	fecha_cierre = fields.Date(string="Fecha Limite")
	fecha_limite = fields.Date(string="Fecha Cierre")
	estado = fields.Selection(selection=[('1', 'PENDIENTE'), ('2', 'PROCESO'), ('3', 'CERRADO')], string="Estado", default="1")
	rango_peligro = fields.Selection(selection=[('A', 'A'), ('B', 'B'), ('C', 'C')], string="Peligro Rango A,B,C", default="A")
	accion_correctiva = fields.Char(string="Acción Correctiva")
	sede_id = fields.Many2one("area.area", string="Area")

	inspeccion_id = fields.Many2one("inspeccion",string="Inspeccion")

	sub_condiciones_ids = fields.One2many("sub.condicion","condicion_id",string="Sub Condiciones")


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



class SubCondicion(models.Model):
	_name= "sub.condicion"

	name = fields.Char(string="Nombre")
	puntaje_maximo = fields.Integer(string="Puntaje Máximo")
	puntaje_logrado = fields.Integer(string="Puntaje Logrado")
	rango_peligro = fields.Selection(selection=[('A', 'A'), ('B', 'B'), ('C', 'C')], string="Peligro Rango A,B,C", default="A")
	nivel_riesgo = fields.Selection(selection=[('B', 'Bajo(B)'), ('M', 'Medio(M) '), ('A', 'Alto(A)'), ('E', 'Extremo(E)')], string="Nivel de Riesgo", default="A")
	responsable_id = fields.Many2one("trabajador.trabajador",string="Responsble")
	fecha_cierre = fields.Date(string="Fecha Limite")
	fecha_limite = fields.Date(string="Fecha Cierre")
	estado = fields.Selection(selection=[('1', 'PENDIENTE'), ('2', 'PROCESO'), ('3', 'CERRADO')], string="Estado", default="1")

	condicion_id = fields.Many2one("condicion.inspeccion",string="Condicion")

	# @api.depends("fecha_cierre","fecha_limite")
	# def _compute_estado_condicion(self):
	# 	for record in self:

#editar info de website

class EditInspecciones(models.TransientModel):
	_name = 'edit.inspecciones'

	def limites_permisos(self,plan_id):
		permiso_line = self.env["inspecciones"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			return True
		else:
			return False

	def funcion_matriz_reporte(self,responsable_id):
		registros = self.env["inspeccion"].sudo().search([('create_uid','=', self.env.uid),('tipo','in', ['2','3'])])
		matriz_consolidado = []
		_logger.info("responsable_id")
		_logger.info(responsable_id)
		# header_consolidado = ["INSPECIONES","PENDIENTE","PROCESO","CERRADO"]
		# matriz_consolidado.append(header_consolidado)
		for line in registros:
			line_consolidado = []
			total_pendiente = 0
			total_proceso = 0
			total_cerrado = 0
			for condicion in line.condiciones_ids:
				if line.tipo == '2':
					for sub_condicion in condicion.sub_condiciones_ids:
						if int(sub_condicion.responsable_id.id)  ==int(responsable_id) :
							if sub_condicion.estado and (sub_condicion.estado == '1'):
								total_pendiente +=1
							if sub_condicion.estado and (sub_condicion.estado == '2'):
								total_proceso +=1
							if sub_condicion.estado and (sub_condicion.estado == '3'):
								total_cerrado +=1
				elif line.tipo == '3':
					if int(condicion.responsable_id.id)  ==int(responsable_id) :
						if condicion.estado and (condicion.estado == '1'):
							total_pendiente += 1
						if condicion.estado and (condicion.estado == '2'):
							total_proceso += 1
						if condicion.estado and (condicion.estado == '3'):
							total_cerrado += 1
			if total_pendiente>0 or total_proceso>0 or total_cerrado>0:
				line_consolidado.append(line.name)
				line_consolidado.append(total_pendiente)
				line_consolidado.append(total_proceso)
				line_consolidado.append(total_cerrado)
				matriz_consolidado.append(line_consolidado)
		return matriz_consolidado

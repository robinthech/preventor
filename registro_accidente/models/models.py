# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import pytz
import threading
import logging
import hmac
from email.utils import formataddr
from collections import defaultdict
from datetime import datetime, timedelta
import odoo.addons.decimal_precision as dp
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource

import math  # noqa
import base64  # noqa
import io  # noqa
from xlwt import easyxf, Workbook  # noqa
from xlwt import Formula  # noqa
from PIL import Image  # noqa
_logger = logging.getLogger(__name__)


class RegistroAccidente(models.Model):
	_name = "registro.accidente"

	name = fields.Char("N° Permiso", index=True,
					   default=lambda self: _('Borrador'))
	fecha = fields.Date("Fechas")
	razon_social = fields.Char("Razón Social")
	lugar = fields.Char("AREA / SEDE")
	responsable_id = fields.Many2one("res.users", string="Solicitante")
	empresa_id = fields.Many2one("empresa.empresa", string="Empresa")
	txt_excel_cal = fields.Char()
	txt_binary_excel_cal = fields.Binary(string=u'Informe Calor')
	sequence = fields.Char(compute='_compute_sequence', string="Codigo")

	@api.model
	def create(self, vals):
		if vals.get('name', _('Borrador')) == _('Borrador'):
			vals['name'] = self.env['ir.sequence'].next_by_code(
				'registro.accidente') or _('Borrador')
		res = super(RegistroAccidente, self).create(vals)
		return res

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "AC-0000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "AC-000{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "AC-00{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "AC-0{}".format(i)

	@api.model
	def default_line_accidente(self):
		return [(0, 0, {'name': "ENERO"}),(0, 0, { 'name': "FEBRERO"}),(0, 0, {'name': "MARZO"}),(0, 0, { 'name': "ABRIL"}),(0, 0, { 'name': "MAYO"}),(0, 0, { 'name': "JUNIO"}),(0, 0, { 'name': "JULIO"}),(0, 0, { 'name': "AGOSTO"}),(0, 0, { 'name': "SEPTIEMBRE"}),(0, 0, { 'name': "OCTUBRE"}),(0, 0, { 'name': "NOVIEMBRE"}),(0, 0, { 'name': "DICIEMBRE"})]

	accidentes_ids = fields.One2many("line.accidente", "registro_id", string="Preparación", default=default_line_accidente)

	def open_word_frio(self):
		biologico = Workbook()
		style1_0 = easyxf('font: height 210, name Arial Narrow, colour_index black; align:wrap on, horiz center, vertical center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;')
		style1_2 = easyxf('font: bold on, height 210, name Arial Narrow, colour_index white; pattern: pattern solid, fore_colour light_blue; align:wrap on, horiz center, vertical center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;')

		ws = biologico.add_sheet(u'REGISTRO ACCIDENTE')
		ws.col(0).width = 4000
		ws.col(1).width = 4000
		ws.col(2).width = 4000
		ws.col(3).width = 4000
		ws.col(4).width = 4000
		ws.col(5).width = 4000
		ws.col(6).width = 4000
		ws.col(7).width = 4000
		ws.col(8).width = 4000
		ws.col(9).width = 4000
		ws.col(10).width = 4000
		ws.col(11).width = 4000
		ws.col(12).width = 4000
		ws.col(13).width = 4000
		ws.col(14).width = 4000
		ws.col(15).width = 4000
		ws.col(16).width = 4000
		ws.col(17).width = 4000
		ws.col(18).width = 4000
		ws.col(19).width = 4000
		ws.col(20).width = 4000

		ws.row(0).height = 600
		ws.row(1).height = 600
		ws.row(2).height = 600
		ws.row(3).height = 1086
		ws.row(4).height = 600
		ws.row(5).height = 600
		ws.row(6).height = 600
		ws.row(7).height = 600
		ws.row(8).height = 600
		ws.row(9).height = 600
		ws.row(10).height = 600
		ws.row(11).height = 600
		ws.row(12).height = 600
		ws.row(13).height = 600
		ws.row(14).height = 600
		ws.row(15).height = 600
		ws.row(16).height = 600
		ws.row(17).height = 600
		ws.row(18).height = 600
		ws.row(19).height = 600
		ws.row(20).height = 600


		ws.write_merge(0, 0, 0, 1, u"N° REGISTRO:", style1_2)
		ws.write_merge(0, 0, 2, 4, u"{}".format(self.name if self.name else ""), style1_0)
		ws.write_merge(0, 0, 5, 20, u"FORMATO DE DATOS PARA REGISTRO DE ESTADÍSTICAS DE SEGURIDAD Y SALUD EN EL TRABAJO", style1_2)

		ws.write_merge(1, 1, 0, 2, u"FECHA:", style1_2)
		ws.write_merge(1, 1, 3, 7, u"{}".format(self.fecha if self.fecha else ""), style1_0)
		ws.write_merge(1, 1, 8, 10, u"RAZÓN SOCIAL O DENOMINACIÓN SOCIAL::", style1_2)
		ws.write_merge(1, 1, 11, 15, u"{}".format(self.razon_social if self.razon_social else ""), style1_0)
		ws.write_merge(1, 1, 16, 18, u"RAZÓN SOCIAL O DENOMINACIÓN SOCIAL::", style1_2)
		ws.write_merge(1, 1, 19, 20, u"{}".format(self.lugar if self.lugar else ""), style1_0)

		ws.write_merge(2, 3, 0, 0, u"MES:", style1_2)
		ws.write_merge(2, 3, 1, 2, u"N° ACCIDENTE MORTAL", style1_2)
		ws.write_merge(2, 3, 3, 4, u"N° ACCIDENTE DE TRABAJO LEVE", style1_2)
		ws.write_merge(2, 2, 5, 11, u"SÓLO PARA ACCIDENTES INCAPACITANTES", style1_2)
		ws.write_merge(3, 3, 5, 6, u"N° ACCIDENTES DE TRABAJO INCAPACITANTES", style1_2)
		ws.write_merge(3, 3, 7, 7, u"TOTAL DE HORAS HOMBRES TRABAJADAS", style1_2)
		ws.write_merge(3, 3, 8, 8, u"ÍNDICE DE FRECUENCIA", style1_2)
		ws.write_merge(3, 3, 9, 9, u"N° DÍAS PERDIDOS", style1_2)
		ws.write_merge(3, 3, 10, 10, u"ÍNDICE DE GRAVEDAD", style1_2)
		ws.write_merge(3, 3, 11, 11, u"ÍNDICE DE ACCIDENTABILIDAD", style1_2)
		ws.write_merge(2, 2, 12, 16, u"ENFERMEDAD OCUPACIONAL", style1_2)
		ws.write_merge(3, 3, 12, 13, u"N° ENFERMEDAD OCUPACIONAL", style1_2)
		ws.write_merge(3, 3, 14, 14, u"N° TRABAJADORES EXPUESTOS AL AGENTE", style1_2)
		ws.write_merge(3, 3, 15, 15, u"TASA DE INCIDENCIA", style1_2)
		ws.write_merge(3, 3, 16, 16, u"N° TRABAJADORES CON CÁNCER PROFESIONAL", style1_2)
		ws.write_merge(2, 3, 17, 18, u"N° INCIDENTES PELIGROSOS", style1_2)
		ws.write_merge(2, 3, 19, 20, u"N° INCIDENTES", style1_2)

		s = 4
		for line_obj in self.accidentes_ids:
			ws.write_merge(s, s, 0, 0, u"{}".format(line_obj.name if line_obj.name else ""), style1_0)
			ws.write_merge(s, s, 1, 2, u"{}".format(line_obj.n_mortal if line_obj.n_mortal else ""), style1_0)
			ws.write_merge(s, s, 3, 4, u"{}".format(line_obj.n_leve if line_obj.n_leve else ""), style1_0)
			ws.write_merge(s, s, 5, 6, u"{}".format(line_obj.n_inca if line_obj.n_inca else ""), style1_0)
			ws.write_merge(s, s, 7, 7, u"{}".format(line_obj.horas_trabajadas if line_obj.horas_trabajadas else ""), style1_0)
			ws.write_merge(s, s, 8, 8, u"{}".format(line_obj.indice_frecuencia if line_obj.indice_frecuencia else ""), style1_0)
			ws.write_merge(s, s, 9, 9, u"{}".format(line_obj.dias_perdidos if line_obj.dias_perdidos else ""), style1_0)
			ws.write_merge(s, s, 10, 10, u"{}".format(line_obj.indice_gravedad if line_obj.indice_gravedad else ""), style1_0)
			ws.write_merge(s, s, 11, 11, u"{}".format(line_obj.indice_accidentabilidad if line_obj.indice_accidentabilidad else ""), style1_0)
			ws.write_merge(s, s, 12, 13, u"{}".format(line_obj.n_ocupacional if line_obj.n_ocupacional else ""), style1_0)
			ws.write_merge(s, s, 14, 14, u"{}".format(line_obj.trabajador_expuesto if line_obj.trabajador_expuesto else ""), style1_0)
			ws.write_merge(s, s, 15, 15, u"{}".format(line_obj.tasa_incidencia if line_obj.tasa_incidencia else ""), style1_0)
			ws.write_merge(s, s, 16, 16, u"{}".format(line_obj.trabajador_cancer if line_obj.trabajador_cancer else ""), style1_0)
			ws.write_merge(s, s, 17, 18, u"{}".format(line_obj.n_peligroso if line_obj.n_peligroso else ""), style1_0)
			ws.write_merge(s, s, 19, 20, u"{}".format(line_obj.n_incidentes if line_obj.n_incidentes else ""), style1_0)
			s = s + 1

		file_name = io.BytesIO()
		biologico.save(file_name)

		self.write({
			'txt_excel_cal': u'REGISTRO DE ACCIDENTE - {}.xls'.format(self.name),
			'txt_binary_excel_cal': base64.encodestring(file_name.getvalue())
		})


class LneAccidente(models.Model):
	_name = "line.accidente"

	name = fields.Char("MES")
	n_mortal = fields.Integer("N° ACCIDENTE MORAL")
	lugar_mortal = fields.Char("AREA / SEDE")
	n_leve = fields.Integer("N° ACCIDENTE DE TRABAJO LEVE")
	lugar_leve = fields.Char("AREA / SEDE")
	n_inca = fields.Integer("N° ACCIDENTES DE TRABAJO INCAPACITANTES")
	lugar_inca = fields.Char("AREA / SEDE")
	horas_trabajadas = fields.Integer("TOTAL HORAS HOMBRE TRABAJADAS")
	indice_frecuencia = fields.Float(compute="_compute_indice",string="Indice de Frecuencia",store=True)
	dias_perdidos = fields.Integer("Nº DIAS PERDIDOS")
	indice_gravedad = fields.Float(compute="_compute_indice",string="Indice de Gravedad", store=True)
	indice_accidentabilidad = fields.Float(compute="_compute_indice",string="Indice de Accidentabilidad",store=True)
	n_ocupacional= fields.Integer("N° ACCIDENTE MORAL")
	lugar_ocupacional = fields.Char("AREA / SEDE")
	trabajador_expuesto = fields.Integer("Trabajadores Expuesto al Agente")
	tasa_incidencia = fields.Float("Tasa de Incidencia")
	trabajador_cancer = fields.Float("N° TRABAJADORES CON CÁNCER PROFESIONAL ")
	n_peligroso = fields.Integer("N° INCIDENTES PELIGROSOS")
	lugar_peligroso = fields.Char("AREA / SEDE")
	n_incidentes = fields.Integer("N° INCIDENTES PELIGROSOS")
	lugar_incidentes = fields.Char("AREA / SEDE")

	@api.depends("n_inca","horas_trabajadas","dias_perdidos")
	def _compute_indice(self):
		for record in self:
			if record.horas_trabajadas > 0:
				record.indice_frecuencia = (record.n_inca*1000000)/record.horas_trabajadas
				record.indice_gravedad = (record.dias_perdidos*1000000)/record.horas_trabajadas
				record.indice_accidentabilidad = (record.indice_gravedad*record.indice_frecuencia) /1000




	registro_id = fields.Many2one("registro.accidente", string="Registro")

class EditlineAccidente(models.TransientModel):
	_name = 'edit.linea.accidente'

	def gruardar_linea(self, linea_id, field,value):
		lineaedit = self.env["line.accidente"].search([('id', '=', linea_id)], limit=1)
		lineaedit.write({'{}'.format(field): value})
		if lineaedit.horas_trabajadas> 0:
			lineaedit.indice_frecuencia =  round((lineaedit.n_inca*1000000)/lineaedit.horas_trabajadas,2)
			lineaedit.indice_gravedad = round( (lineaedit.dias_perdidos*1000000)/lineaedit.horas_trabajadas,2)
			lineaedit.indice_accidentabilidad = round((lineaedit.indice_gravedad*lineaedit.indice_frecuencia) /1000,2)

		return [lineaedit.indice_frecuencia,lineaedit.indice_gravedad,lineaedit.indice_accidentabilidad]

	def limites_permisos(self,plan_id):
		permiso_line = self.env["registro.accidente"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			_logger.info(plan.limite_registro)
			return True
		else:
			return False

	def get_data(self,empresa):
		registros = self.env["registro.accidente"].search([('empresa_id', '=', empresa)])
		accidentes = self.env["line.accidente"].search([('registro_id', 'in', [(rec.id) for rec in registros])])
		suma_enero = 0
		suma_febrero = 0
		suma_marzo = 0
		suma_abril = 0
		suma_mayo = 0
		suma_junio = 0
		suma_julio = 0
		suma_agosto = 0
		suma_septiembre = 0
		suma_octubre = 0
		suma_noviembre = 0
		suma_diciembre = 0
		for line in accidentes:
			if line.name =="ENERO":
				suma_enero = suma_enero + line.n_mortal
			if line.name =="FEBRERO":
				suma_febrero = suma_febrero + line.n_mortal
			if line.name =="MARZO":
				suma_marzo = suma_marzo + line.n_mortal
			if line.name =="ABRIL":
				suma_abril = suma_abril + line.n_mortal
			if line.name =="MAYO":
				suma_mayo = suma_mayo + line.n_mortal
			if line.name =="JUNIO":
				suma_junio = suma_junio + line.n_mortal
			if line.name =="JULIO":
				suma_julio = suma_julio + line.n_mortal
			if line.name =="AGOSTO":
				suma_agosto = suma_agosto + line.n_mortal
			if line.name =="SEPTIEMBRE":
				suma_septiembre = suma_septiembre + line.n_mortal
			if line.name =="OCTUBRE":
				suma_octubre = suma_octubre + line.n_mortal
			if line.name =="NOVIEMBRE":
				suma_noviembre = suma_noviembre + line.n_mortal
			if line.name =="DICIEMBRE":
				suma_diciembre = suma_diciembre + line.n_mortal
		data_graph = [suma_enero,suma_febrero,suma_marzo,suma_abril,suma_mayo,suma_junio,suma_julio,suma_agosto,suma_septiembre,suma_octubre,suma_noviembre,suma_diciembre]
		return data_graph


	def get_data_1(self,empresa):
		registros = self.env["registro.accidente"].search([('empresa_id', '=', empresa)])
		accidentes = self.env["line.accidente"].search([('registro_id', 'in', [(rec.id) for rec in registros])])
		suma_enero = 0
		suma_febrero = 0
		suma_marzo = 0
		suma_abril = 0
		suma_mayo = 0
		suma_junio = 0
		suma_julio = 0
		suma_agosto = 0
		suma_septiembre = 0
		suma_octubre = 0
		suma_noviembre = 0
		suma_diciembre = 0
		for line in accidentes:
			if line.name =="ENERO":
				suma_enero = suma_enero + line.n_leve
			if line.name =="FEBRERO":
				suma_febrero = suma_febrero + line.n_leve
			if line.name =="MARZO":
				suma_marzo = suma_marzo + line.n_leve
			if line.name =="ABRIL":
				suma_abril = suma_abril + line.n_leve
			if line.name =="MAYO":
				suma_mayo = suma_mayo + line.n_leve
			if line.name =="JUNIO":
				suma_junio = suma_junio + line.n_leve
			if line.name =="JULIO":
				suma_julio = suma_julio + line.n_leve
			if line.name =="AGOSTO":
				suma_agosto = suma_agosto + line.n_leve
			if line.name =="SEPTIEMBRE":
				suma_septiembre = suma_septiembre + line.n_leve
			if line.name =="OCTUBRE":
				suma_octubre = suma_octubre + line.n_leve
			if line.name =="NOVIEMBRE":
				suma_noviembre = suma_noviembre + line.n_leve
			if line.name =="DICIEMBRE":
				suma_diciembre = suma_diciembre + line.n_leve
		data_graph = [suma_enero,suma_febrero,suma_marzo,suma_abril,suma_mayo,suma_junio,suma_julio,suma_agosto,suma_septiembre,suma_octubre,suma_noviembre,suma_diciembre]
		return data_graph

	def get_data_2(self,empresa):
		registros = self.env["registro.accidente"].search([('empresa_id', '=', empresa)])
		accidentes = self.env["line.accidente"].search([('registro_id', 'in', [(rec.id) for rec in registros])])
		suma_enero = 0
		suma_febrero = 0
		suma_marzo = 0
		suma_abril = 0
		suma_mayo = 0
		suma_junio = 0
		suma_julio = 0
		suma_agosto = 0
		suma_septiembre = 0
		suma_octubre = 0
		suma_noviembre = 0
		suma_diciembre = 0
		for line in accidentes:
			if line.name =="ENERO":
				suma_enero = suma_enero + line.n_inca
			if line.name =="FEBRERO":
				suma_febrero = suma_febrero + line.n_inca
			if line.name =="MARZO":
				suma_marzo = suma_marzo + line.n_inca
			if line.name =="ABRIL":
				suma_abril = suma_abril + line.n_inca
			if line.name =="MAYO":
				suma_mayo = suma_mayo + line.n_inca
			if line.name =="JUNIO":
				suma_junio = suma_junio + line.n_inca
			if line.name =="JULIO":
				suma_julio = suma_julio + line.n_inca
			if line.name =="AGOSTO":
				suma_agosto = suma_agosto + line.n_inca
			if line.name =="SEPTIEMBRE":
				suma_septiembre = suma_septiembre + line.n_inca
			if line.name =="OCTUBRE":
				suma_octubre = suma_octubre + line.n_inca
			if line.name =="NOVIEMBRE":
				suma_noviembre = suma_noviembre + line.n_inca
			if line.name =="DICIEMBRE":
				suma_diciembre = suma_diciembre + line.n_inca
		data_graph = [suma_enero,suma_febrero,suma_marzo,suma_abril,suma_mayo,suma_junio,suma_julio,suma_agosto,suma_septiembre,suma_octubre,suma_noviembre,suma_diciembre]
		return data_graph

	def get_data_3(self,empresa):
		registros = self.env["registro.accidente"].search([('empresa_id', '=', empresa)])
		accidentes = self.env["line.accidente"].search([('registro_id', 'in', [(rec.id) for rec in registros])])
		suma_enero = 0
		suma_febrero = 0
		suma_marzo = 0
		suma_abril = 0
		suma_mayo = 0
		suma_junio = 0
		suma_julio = 0
		suma_agosto = 0
		suma_septiembre = 0
		suma_octubre = 0
		suma_noviembre = 0
		suma_diciembre = 0
		for line in accidentes:
			if line.name =="ENERO":
				suma_enero = suma_enero + line.n_ocupacional
			if line.name =="FEBRERO":
				suma_febrero = suma_febrero + line.n_ocupacional
			if line.name =="MARZO":
				suma_marzo = suma_marzo + line.n_ocupacional
			if line.name =="ABRIL":
				suma_abril = suma_abril + line.n_ocupacional
			if line.name =="MAYO":
				suma_mayo = suma_mayo + line.n_ocupacional
			if line.name =="JUNIO":
				suma_junio = suma_junio + line.n_ocupacional
			if line.name =="JULIO":
				suma_julio = suma_julio + line.n_ocupacional
			if line.name =="AGOSTO":
				suma_agosto = suma_agosto + line.n_ocupacional
			if line.name =="SEPTIEMBRE":
				suma_septiembre = suma_septiembre + line.n_ocupacional
			if line.name =="OCTUBRE":
				suma_octubre = suma_octubre + line.n_ocupacional
			if line.name =="NOVIEMBRE":
				suma_noviembre = suma_noviembre + line.n_ocupacional
			if line.name =="DICIEMBRE":
				suma_diciembre = suma_diciembre + line.n_ocupacional
		data_graph = [suma_enero,suma_febrero,suma_marzo,suma_abril,suma_mayo,suma_junio,suma_julio,suma_agosto,suma_septiembre,suma_octubre,suma_noviembre,suma_diciembre]
		return data_graph


	def get_data_4(self,empresa):
		registros = self.env["registro.accidente"].search([('empresa_id', '=', empresa)])
		accidentes = self.env["line.accidente"].search([('registro_id', 'in', [(rec.id) for rec in registros])])
		suma_enero = 0
		suma_febrero = 0
		suma_marzo = 0
		suma_abril = 0
		suma_mayo = 0
		suma_junio = 0
		suma_julio = 0
		suma_agosto = 0
		suma_septiembre = 0
		suma_octubre = 0
		suma_noviembre = 0
		suma_diciembre = 0
		for line in accidentes:
			if line.name =="ENERO":
				suma_enero = suma_enero + line.n_peligroso
			if line.name =="FEBRERO":
				suma_febrero = suma_febrero + line.n_peligroso
			if line.name =="MARZO":
				suma_marzo = suma_marzo + line.n_peligroso
			if line.name =="ABRIL":
				suma_abril = suma_abril + line.n_peligroso
			if line.name =="MAYO":
				suma_mayo = suma_mayo + line.n_peligroso
			if line.name =="JUNIO":
				suma_junio = suma_junio + line.n_peligroso
			if line.name =="JULIO":
				suma_julio = suma_julio + line.n_peligroso
			if line.name =="AGOSTO":
				suma_agosto = suma_agosto + line.n_peligroso
			if line.name =="SEPTIEMBRE":
				suma_septiembre = suma_septiembre + line.n_peligroso
			if line.name =="OCTUBRE":
				suma_octubre = suma_octubre + line.n_peligroso
			if line.name =="NOVIEMBRE":
				suma_noviembre = suma_noviembre + line.n_peligroso
			if line.name =="DICIEMBRE":
				suma_diciembre = suma_diciembre + line.n_peligroso
		data_graph = [suma_enero,suma_febrero,suma_marzo,suma_abril,suma_mayo,suma_junio,suma_julio,suma_agosto,suma_septiembre,suma_octubre,suma_noviembre,suma_diciembre]
		return data_graph

	def get_data_5(self,empresa):
		registros = self.env["registro.accidente"].search([('empresa_id', '=', empresa)])
		accidentes = self.env["line.accidente"].search([('registro_id', 'in', [(rec.id) for rec in registros])])
		suma_enero = 0
		suma_febrero = 0
		suma_marzo = 0
		suma_abril = 0
		suma_mayo = 0
		suma_junio = 0
		suma_julio = 0
		suma_agosto = 0
		suma_septiembre = 0
		suma_octubre = 0
		suma_noviembre = 0
		suma_diciembre = 0
		for line in accidentes:
			if line.name =="ENERO":
				suma_enero = suma_enero + line.n_incidentes
			if line.name =="FEBRERO":
				suma_febrero = suma_febrero + line.n_incidentes
			if line.name =="MARZO":
				suma_marzo = suma_marzo + line.n_incidentes
			if line.name =="ABRIL":
				suma_abril = suma_abril + line.n_incidentes
			if line.name =="MAYO":
				suma_mayo = suma_mayo + line.n_incidentes
			if line.name =="JUNIO":
				suma_junio = suma_junio + line.n_incidentes
			if line.name =="JULIO":
				suma_julio = suma_julio + line.n_incidentes
			if line.name =="AGOSTO":
				suma_agosto = suma_agosto + line.n_incidentes
			if line.name =="SEPTIEMBRE":
				suma_septiembre = suma_septiembre + line.n_incidentes
			if line.name =="OCTUBRE":
				suma_octubre = suma_octubre + line.n_incidentes
			if line.name =="NOVIEMBRE":
				suma_noviembre = suma_noviembre + line.n_incidentes
			if line.name =="DICIEMBRE":
				suma_diciembre = suma_diciembre + line.n_incidentes
		data_graph = [suma_enero,suma_febrero,suma_marzo,suma_abril,suma_mayo,suma_junio,suma_julio,suma_agosto,suma_septiembre,suma_octubre,suma_noviembre,suma_diciembre]
		return data_graph

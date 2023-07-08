# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.http import request, content_disposition
import re
import logging
import math  # noqa
import base64  # noqa
import io  # noqa
from xlwt import easyxf, Workbook  # noqa
from xlwt import Formula  # noqa
from PIL import Image  # noqa
import xlsxwriter
import odoo.addons.decimal_precision as dp
import os
import pytz

_logger = logging.getLogger(__name__)


class Psicosocial(models.Model):
	_name = 'psicosocial.psicosocial'

	name = fields.Char("Codigo", index=True, default=lambda self: _('New'))
	ruc = fields.Char(string="RUC")
	cliente = fields.Char(string="Razon Social")
	txt_excel_psicosocial = fields.Char()
	txt_binary_excel_psicosocial = fields.Binary(string=u'Reporte Psicosocial')
	# sequence = fields.Char(compute='_compute_sequence', string="Codigo")


	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('psicosocial.psicosocial') or _('New')
		res = super(Psicosocial, self).create(vals)
		return res

	@api.model
	def print_report(self):
		_logger.info('entramodelo')
		_logger.info(self.id)
		return self.env.ref('iperc_continuo.action_report_saleorder').report_action(self.id)

	evaluacion_ids = fields.One2many("evaluacion.psicosocial","psicosocial_id",string="Evaluacion")

	def get_data_riesgo_trabajo(self,psicosocial_id):
		evaluaciones = self.env["evaluacion.psicosocial"].search([('psicosocial_id', '=', psicosocial_id)])
		suma_bajo_trabajo = 0
		suma_medio_trabajo = 0
		suma_alto_trabajo = 0
		suma_bajo_psicologicas = 0
		suma_medio_psicologicas = 0
		suma_alto_psicologicas = 0
		suma_baja_apoyo = 0
		suma_medio_apoyo = 0
		suma_alto_apoyo = 0
		suma_baja_compensaciones = 0
		suma_medio_compensaciones = 0
		suma_alto_compensaciones = 0
		suma_baja_presencia = 0
		suma_medio_presencia = 0
		suma_alto_presencia = 0
		for line in evaluaciones:
			if line.riesgo_trabajo =="BAJO":
				suma_bajo_trabajo += 1
			if line.riesgo_trabajo =="MEDIO":
				suma_medio_trabajo += 1
			if line.riesgo_trabajo =="ALTO":
				suma_alto_trabajo += 1
			if line.riesgo_psicologicas =="BAJO":
				suma_bajo_psicologicas += 1
			if line.riesgo_psicologicas =="MEDIO":
				suma_medio_psicologicas += 1
			if line.riesgo_psicologicas =="ALTO":
				suma_alto_psicologicas += 1
			if line.riesgo_apoyo == "BAJO":
				suma_baja_apoyo += 1
			if line.riesgo_apoyo == "MEDIO":
				suma_medio_apoyo += 1
			if line.riesgo_apoyo == "ALTO":
				suma_alto_apoyo += 1
			if line.riesgo_compensaciones == "BAJO":
				suma_baja_compensaciones += 1
			if line.riesgo_compensaciones == "MEDIO":
				suma_medio_compensaciones += 1
			if line.riesgo_compensaciones == "ALTO":
				suma_alto_compensaciones += 1
			if line.riesgo_presencia == "BAJO":
				suma_baja_presencia += 1
			if line.riesgo_presencia == "MEDIO":
				suma_medio_presencia += 1
			if line.riesgo_presencia == "ALTO":
				suma_alto_presencia += 1


		return [suma_bajo_trabajo,suma_medio_trabajo,suma_alto_trabajo,suma_bajo_psicologicas,suma_medio_psicologicas,suma_alto_psicologicas,
		suma_baja_apoyo,suma_medio_apoyo,suma_alto_apoyo,suma_baja_compensaciones,suma_medio_compensaciones,suma_alto_compensaciones,
		suma_baja_presencia,suma_medio_presencia,suma_alto_presencia]


	def genera_excel(self):
		if self.evaluacion_ids:
			self.ensure_one()
			workbook = xlsxwriter.Workbook(u'/odoo/custom/excel.xlsx')
			worksheet = workbook.add_worksheet(u"ReportePsicosocial")
			head = workbook.add_format()
			head.set_bold()
			head.set_font_color("white")
			head.set_font_name('Arial')
			head.set_font_size(10)
			head.set_align('center')

			head.set_align('vcenter')
			head.set_text_wrap()
			head.set_fg_color('#7da7d8')
			head.set_border(1)


			worksheet.set_column('A:A', 50)
			worksheet.write(2, 0, u"TRABAJO ACTIVO Y DESARROLLO DE HABILIDADES", head)
			worksheet.write(3, 0, u"EXIGENCIAS PSICOLÓGICAS", head)
			worksheet.write(4, 0, u"APOYO SOCIAL EN LA EMPRESA Y CALIDAD DE LIDERAZGO", head)
			worksheet.write(5, 0, u"COMPENSACIONES", head)
			worksheet.write(6, 0, u"DOBLE PRESENCIA", head)

			workbook.close()

			f = open('/odoo/custom/excel.xlsx', 'rb')
			# f = open('C:\\Program Files (x86)\\Odoo 13.0\\server\\addons\\excel.xlsx', 'rb')
			file_name = io.BytesIO(f.read())
			# workbook.save(file_name)
			self.write({
				'txt_excel_psicosocial': u'ReportePsicosocial.xlsx',
				'txt_binary_excel_psicosocial': base64.encodestring(file_name.getvalue())
			})
			# for evaluacion in self.evaluacion_ids:
			# 	eva


class EvaluacionPsicosocial(models.Model):
	_name = 'evaluacion.psicosocial'

	name = fields.Char("Codigo", index=True, default=lambda self: _('New'))
	psicosocial_id = fields.Many2one("psicosocial.psicosocial",string=u'Evaluación psicosocial')
	fecha = fields.Date("Fecha")
	empresa = fields.Char("Empresa")
	area = fields.Char("Area")
	puesto = fields.Char("Puesto")
	sexo = fields.Selection(selection=[('femenino', 'femenino'), ('masculino', 'masculino')], string="Sexo", default="femenino")
	edad = fields.Selection(selection=[('menosde26', 'menosde26'), ('26y35', '26y35'), ('36y45', '36y45'), ('46y55', '46y55'), ('Masde55', 'Masde55')], string="Edad")
	tiempo = fields.Selection(selection=[('hasta6meses', 'hasta6meses'), ('6y2', '6y2'), ('2y5', '2y5'), ('5y10', '5y10'), ('Masde10', 'Masde10')], string="Tiempo")
	jornada = fields.Selection(selection=[('parcial', 'parcial'), ('completo', 'completo'), ('nojornada', 'nojornada')], string="Jornada")
	horario = fields.Selection(selection=[('mananaytarde', 'mananaytarde'), ('manana', 'manana'), ('tarde', 'tarde'), ('noche', 'noche'), ('rotativo', 'rotativo')], string="Horario")
	riesgo_trabajo = fields.Char(string="Riesgo de trabajo activo",compute="_compute_riesgo_trabajo")
	riesgo_psicologicas = fields.Char(string="Riesgo de exigencias psicologicas",compute="_compute_psicologicas")
	riesgo_apoyo = fields.Char(string="Riesgo de apoyo social",compute="_compute_riesgo_apoyo")
	riesgo_compensaciones = fields.Char(string="Riesgo de compensaciones",compute="_compute_riesgo_compensaciones")
	riesgo_presencia = fields.Char(string="Riesgo de doble presencia",compute="_compute_riesgo_presencia")
	# DIMENSIÓN: TRABAJO ACTIVO Y DESARROLLO DE HABILIDADES
	psicosocial71 = fields.Char("psicosocial71")
	psicosocial72 = fields.Char("psicosocial72")
	psicosocial73 = fields.Char("psicosocial73")
	psicosocial74 = fields.Char("psicosocial74")
	psicosocial75 = fields.Char("psicosocial75")

	# DIMENSIÓN: EXIGENCIAS PSICOLÓGICAS
	psicosocial81 = fields.Char("psicosocial81")
	psicosocial82 = fields.Char("psicosocial82")
	psicosocial83 = fields.Char("psicosocial83")
	psicosocial84 = fields.Char("psicosocial84")
	psicosocial85 = fields.Char("psicosocial85")

	# DIMENSIÓN: APOYO SOCIAL EN LA EMPRESA Y CALIDAD DE LIDERAZGO
	psicosocial91 = fields.Char("psicosocial91")
	psicosocial92 = fields.Char("psicosocial92")
	psicosocial93 = fields.Char("psicosocial93")
	psicosocial94 = fields.Char("psicosocial94")
	psicosocial95 = fields.Char("psicosocial95")

	# DIMENSIÓN: COMPENSACIONES
	psicosocial101 = fields.Char("psicosocial101")
	psicosocial102 = fields.Char("psicosocial102")
	psicosocial103 = fields.Char("psicosocial103")

	# DIMENSIÓN: DOBLE PRESENCIA
	psicosocial111 = fields.Char("psicosocial111")
	psicosocial112 = fields.Char("psicosocial112")

	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('evaluacion.psicosocial') or _('New')
		res = super(EvaluacionPsicosocial, self).create(vals)
		return res

	@api.depends("psicosocial71","psicosocial72","psicosocial73","psicosocial74","psicosocial75")
	def _compute_riesgo_trabajo(self):
		# SI(AE16="","",SI(AE16<6,"BAJO",SI(Y(AE16>=6,AE16<9),"MEDIO","ALTO")))
		for record in self:
			suma = int(record.psicosocial71) + int(record.psicosocial72) + int(record.psicosocial73) + int(record.psicosocial74) + int(record.psicosocial75)
			if suma < 6:
				record.riesgo_trabajo = 'BAJO'
			elif 6 <= suma < 9:
				record.riesgo_trabajo = 'MEDIO'
			else:
				record.riesgo_trabajo = 'ALTO'

	@api.depends("psicosocial81","psicosocial82","psicosocial83","psicosocial84","psicosocial85")
	def _compute_psicologicas(self):
		# SI(AD16<9,"BAJO",SI(Y(AD16>=9,AD16<12),"MEDIO","ALTO")))
		for record in self:
			suma = int(record.psicosocial81) + int(record.psicosocial82) + int(record.psicosocial83) + int(record.psicosocial84) + int(record.psicosocial85)
			if suma < 9:
				record.riesgo_psicologicas = 'BAJO'
			elif 9 <= suma < 12:
				record.riesgo_psicologicas = 'MEDIO'
			else:
				record.riesgo_psicologicas = 'ALTO'

	@api.depends("psicosocial91","psicosocial92","psicosocial93","psicosocial94","psicosocial95")
	def _compute_riesgo_apoyo(self):
		# SI(AD16<9,"BAJO",SI(Y(AD16>=9,AD16<12),"MEDIO","ALTO")))
		for record in self:
			suma = int(record.psicosocial91) + int(record.psicosocial92) + int(record.psicosocial93) + int(record.psicosocial94) + int(record.psicosocial95)
			if suma < 9:
				record.riesgo_apoyo = 'BAJO'
			elif 9 <= suma < 12:
				record.riesgo_apoyo = 'MEDIO'
			else:
				record.riesgo_apoyo = 'ALTO'

	@api.depends("psicosocial101","psicosocial102","psicosocial103")
	def _compute_riesgo_compensaciones(self):
		# SI(AD16<9,"BAJO",SI(Y(AD16>=9,AD16<12),"MEDIO","ALTO")))
		for record in self:
			suma = int(record.psicosocial101) + int(record.psicosocial102) + int(record.psicosocial103)
			if suma < 9:
				record.riesgo_compensaciones = 'BAJO'
			elif 9 <= suma < 12:
				record.riesgo_compensaciones = 'MEDIO'
			else:
				record.riesgo_compensaciones = 'ALTO'

	@api.depends("psicosocial111","psicosocial112")
	def _compute_riesgo_presencia(self):
		# SI(AD16<9,"BAJO",SI(Y(AD16>=9,AD16<12),"MEDIO","ALTO")))
		for record in self:
			suma = int(record.psicosocial111) + int(record.psicosocial112)
			if suma < 9:
				record.riesgo_presencia = 'BAJO'
			elif 9 <= suma < 12:
				record.riesgo_presencia = 'MEDIO'
			else:
				record.riesgo_presencia = 'ALTO'

class EvaluacionPsicosocialTransient(models.TransientModel):
	_name = 'evaluacion.psicosocial.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["evaluacion.psicosocial"].sudo().search([('id','=',linea_id)],limit=1)
		_logger.info('lineaedit')
		_logger.info(lineaedit)
		lineaedit.sudo().write({'{}'.format(field):value})
		return True

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


class EvaluacionPsicosocialMulti(models.Model):
	_name = 'evaluacion.psicosocial.multi'

	name = fields.Char("Codigo", index=True, default=lambda self: _('New'))
	fecha = fields.Date("Fecha")
	area = fields.Char("Area")
	puesto = fields.Char("Puesto")
	user_id = fields.Many2one("res.users")
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
	empresa = fields.Many2one('empresa.multicompania', string='Empresa')
	tipo = fields.Char("Tipo")
	sede = fields.Selection(selection=[('ENCARNACION', 'ENCARNACION'), ('ATE', 'ATE'), ('RIMAC', 'RIMAC')], string="Sede")
	estado = fields.Boolean(string='Estado',default=False)

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
			vals['name'] = self.env['ir.sequence'].next_by_code('evaluacion.psicosocial.multi') or _('New')
		res = super(EvaluacionPsicosocialMulti, self).create(vals)
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

class EvaluacionPsicosocialMultiTransient(models.TransientModel):
	_name = 'evaluacion.psicosocial.multi.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["evaluacion.psicosocial.multi"].sudo().search([('id','=',linea_id)],limit=1)
		lineaedit.sudo().write({'{}'.format(field):value})
		return True

class EmpresaMulticompania(models.Model):
	_name = 'empresa.multicompania'

	name = fields.Char("Empresa")
	evaluacion_ids = fields.One2many("evaluacion.psicosocial.multi","empresa",string="Evaluaciones")

class SurveyInherit(models.Model):
	_inherit = 'survey.survey'

	deadline = fields.Datetime(string="Tiempo de finalizacion", help="Datetime until customer can open the survey and submit answers")

class SurveyUserInputInherit(models.Model):
    _inherit = "survey.user_input"

    deadline = fields.Datetime('Deadline', help="Datetime until customer can open the survey and submit answers",related="survey_id.deadline")

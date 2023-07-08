# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import math
import base64
import io
import xlsxwriter
import os

TAREA_EQUIVALENCE = {'1': u'Administrativo',
					 '2': u'Operativo'}

class ProductProduct(models.Model):
	_inherit = "registro.monitoreo"

	sonometria_ids = fields.One2many('ruido.sonometria', 'registro_id', string=u'Ruido por Sonometria')
	puntos_sono = fields.Integer(compute="_compute_puntos_sono", string=u"Ruido por Sonometria")
	excel_sono = fields.Char()
	excel_sono_binary = fields.Binary(string=u'R. Dosimetria')

	def datos_sono(self):
		s = 0
		tarea_visual = {'1':'Administrativo', '2':'Operativo'}

		if self.sonometria_ids:
			self.ensure_one()
			# workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')
			workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')

			head = workbook.add_format()
			head.set_bold()
			head.set_font_color("white")
			head.set_font_name('Arial')
			head.set_font_size(10)
			head.set_align('center')
			head.set_align('vcenter')
			head.set_text_wrap()
			head.set_fg_color('#000066')
			head.set_border(1)

			formato = workbook.add_format()
			formato.set_font_color("black")
			formato.set_font_name('Arial')
			formato.set_font_size(8)
			formato.set_align('center')
			formato.set_align('vcenter')
			formato.set_text_wrap()
			formato.set_border(1)

			formatos = workbook.add_format()
			formatos.set_font_color("black")
			formatos.set_font_name('Arial')
			formatos.set_font_size(8)
			formatos.set_align('center')
			formatos.set_align('vcenter')
			formatos.set_text_wrap()
			formatos.set_fg_color('#36C716')
			formatos.set_border(1)

			formaton = workbook.add_format()
			formaton.set_font_color("black")
			formaton.set_font_name('Arial')
			formaton.set_font_size(8)
			formaton.set_align('center')
			formaton.set_align('vcenter')
			formaton.set_text_wrap()
			formaton.set_fg_color('#F73434')
			formaton.set_border(1)

			worksheet = workbook.add_worksheet(u"R. Dosimetria")
			worksheet.set_column('A:K', 20)
			worksheet.set_row(0, 40)
			worksheet.write(s, 0, u"N°", head)
			worksheet.write(s, 1, u"Área", head)
			worksheet.write(s, 2, u"Puesto de Trabajo", head)
			worksheet.write(s, 3, u"Tipo de Actividad", head)
			worksheet.write(s, 4, u"Jornada Laboral (Horas)", head)
			worksheet.write(s, 5, u"Leq (dBA)", head)
			worksheet.write(s, 6, u"LMPc (dBA)", head)
			# worksheet.write(s, 7, u"Dosis (%)", head)
			worksheet.write(s, 7, u"¿Cumple con la R.M. N°375-2008-TR?", head)

			s = 1
			for o in self.sonometria_ids:
				worksheet.set_row(s, 30)
				worksheet.write(s, 0, u"{}".format(s if s else ""), formato)
				worksheet.write(s, 1, u"{}".format(o.area if o.area else ""), formato)
				worksheet.write(s, 2, u"{}".format(o.puesto_trabajo if o.puesto_trabajo else ""), formato)
				worksheet.write(s, 3, u"{}".format(tarea_visual[o.tipo_actividad] if o.tipo_actividad else ""), formato)
				worksheet.write(s, 4, u"{}".format(round(o.jornada,2) if o.jornada else ""), formato)
				worksheet.write(s, 5, u"{}".format(round(o.leq,2) if o.leq else ""), formato)
				worksheet.write(s, 6, u"{}".format(round(o.val_max,1) if o.val_max else ""), formato)
				# worksheet.write(s, 7, u"{}".format(round(o.dosis,2) if o.dosis else ""), formato)
				if o.cumple == "SÍ CUMPLE":
					worksheet.write(s, 7, u"{}".format(o.cumple if o.cumple else ""), formatos)
				else:
					worksheet.write(s, 7, u"{}".format(o.cumple if o.cumple else ""), formaton)
				s += 1

			workbook.close()
			f = open('/odoopreventor/custom/excel.xlsx', 'rb')
			file_name = io.BytesIO(f.read())
			self.write({
				'excel_sono': u'{} - R Sonometria.xlsx'.format(self.sequence if self.sequence else ""),
				'excel_sono_binary': base64.encodestring(file_name.getvalue())
			})

	@api.depends("sonometria_ids")
	def _compute_puntos_sono(self):
		for record in self:
			record.puntos_sono = len(record.sonometria_ids)

class RuidoSonometria(models.Model):
	_name = 'ruido.sonometria'
	_inherits = {'agente.general': 'agente_general_id'}

	agente_general_id = fields.Many2one('agente.general', required=True, ondelete='restrict', auto_join=True,
										string='Agente General')
	tipo_actividad = fields.Selection(selection=[('1', 'Administrativo'), ('2', 'Operativo')],
									  string='Tipo de Actividad', default="1")
	jornada = fields.Float(string='Jornada Laboral (horas)')
	leq = fields.Float(string='Leq (dBA)')
	l_max = fields.Float("L max")
	l_min = fields.Float("L min")
	val_max = fields.Float(compute="_compute_calculo", string=u"LMPc (dBA)", store=True)
	cumple = fields.Char(compute="_compute_dosimetria", string="¿Cumple con la R.M. N°375-2008-TR?", store=True)

	@api.depends("tipo_actividad","jornada")
	def _compute_calculo(self):
		for record in self:
			if record.jornada:
				if record.tipo_actividad:
					if record.tipo_actividad == "1":
						record.val_max = 65
					else:
						if record.jornada == 1.00:
							record.val_max = 94
						elif record.jornada == 2.00:
							record.val_max = 91
						elif record.jornada == 4.00:
							record.val_max = 88
						elif record.jornada == 8.00:
							record.val_max = 85
						elif record.jornada == 12.00:
							record.val_max = 83
						elif record.jornada == 16.00:
							record.val_max = 82
						elif record.jornada == 24.00:
							record.val_max = 80
						else:
							record.val_max = round((85 + 10*math.log((8/record.jornada), 10)) ,1)

	@api.depends("leq")
	def _compute_dosimetria(self):
		for record in self:
			if record.leq:
				if record.leq <= record.val_max:
					record.cumple = u"SÍ CUMPLE"
				else:
					record.cumple = u"NO CUMPLE"

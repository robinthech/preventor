from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import math
import base64
import io
import xlsxwriter
import os

TAREA_EQUIVALENCE = {'1': u'En Exteriores',
					 '2': u'En Interiores',
					 '3': u'Requerimiento Visual Simple',
					 '4': u'Distinción Moderada de Detalles',
					 '5': u'Distinción Clara de Detalles',
					 '6': u'Distinción Fina de Detalles',
					 '7': u'Alta Exactitud en la Distinción de Delta',
					 '8': u'Alta Exactitud de Especialización'}

class ProductProduct(models.Model):
	_inherit = "registro.monitoreo"

	iluminacion_ids = fields.One2many('iluminacion.iluminacion', 'registro_id', string=u'Iluminación')
	puntos_ilu = fields.Integer(compute="_compute_puntos_ilu", string=u"Puntos de Iluminación")
	excel_ilu = fields.Char()
	excel_ilu_binary = fields.Binary(string=u'Iluminación')

	def datos_ilu(self):
		s = 0
		tarea_visual = {'1':'En exteriores', '2':'En interiores', '3':'Requerimiento visual simple',
						'4':'Distinción moderada de detalles', '5':'Distinción clara de detalles',
						'6':'Distinción fina de detalles','7':'Alta exactitud en la distinción de delta',
						'8':'Alta exactitud de especialización'}

		turno = {'9':'Diurno', '0':'Nocturno'}

		if self.iluminacion_ids:
			self.ensure_one()
			workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')
			# workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')
			# workbook = xlsxwriter.Workbook(u'/odoo/custom/excel.xlsx')

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

			worksheet = workbook.add_worksheet(u"Iluminación")
			worksheet.set_column('A:K', 20)
			worksheet.set_row(0, 40)
			worksheet.write(s, 0, u"N°", head)
			worksheet.write(s, 1, u"Área", head)
			worksheet.write(s, 2, u"Puesto de Trabajo", head)
			worksheet.write(s, 3, u"Turno", head)
			worksheet.write(s, 4, u"Tarea Visual", head)
			worksheet.write(s, 5, u"Nivel de Iluminación (lux)", head)
			worksheet.write(s, 6, u"Nivel Mínimo Recomendado (lux)", head)
			worksheet.write(s, 7, u"¿Cumple con la R.M. N°375-2008-TR?", head)

			s = 1
			for o in self.iluminacion_ids:
				worksheet.set_row(s, 30)
				worksheet.write(s, 0, u"{}".format(s if s else ""), formato)
				worksheet.write(s, 1, u"{}".format(o.area if o.area else ""), formato)
				worksheet.write(s, 2, u"{}".format(o.puesto_trabajo if o.puesto_trabajo else ""), formato)
				worksheet.write(s, 3, u"{}".format(turno[o.horario] if o.horario else ""), formato)
				worksheet.write(s, 4, u"{}".format(tarea_visual[o.tarea] if o.tarea else ""), formato)
				worksheet.write(s, 5, u"{}".format(round(o.lux,2) if o.lux else ""), formato)
				worksheet.write(s, 6, u"{}".format(o.val_min if o.val_min else ""), formato)
				if o.cumple == "SÍ CUMPLE":
					worksheet.write(s, 7, u"{}".format(o.cumple if o.cumple else ""), formatos)
				else:
					worksheet.write(s, 7, u"{}".format(o.cumple if o.cumple else ""), formaton)
				s += 1

			workbook.close()
			f = open('/odoopreventor/custom/excel.xlsx', 'rb')
			# f = open('/odoo/custom/excel.xlsx', 'rb')
			file_name = io.BytesIO(f.read())
			self.write({
				'excel_ilu': u'{} - Iluminación.xlsx'.format(self.sequence if self.sequence else ""),
				'excel_ilu_binary': base64.encodestring(file_name.getvalue())
			})

		else:
			self.ensure_one()
			workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')
			# workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')
			# workbook = xlsxwriter.Workbook(u'/odoo/custom/excel.xlsx')

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

			worksheet = workbook.add_worksheet(u"Iluminación")
			worksheet.set_column('A:K', 20)
			worksheet.set_row(0, 40)
			worksheet.write(s, 0, u"N°", head)
			worksheet.write(s, 1, u"Área", head)
			worksheet.write(s, 2, u"Puesto de Trabajo", head)
			worksheet.write(s, 3, u"Turno", head)
			worksheet.write(s, 4, u"Tarea Visual", head)
			worksheet.write(s, 5, u"Nivel de Iluminación (lux)", head)
			worksheet.write(s, 6, u"Nivel Mínimo Recomendado (lux)", head)
			worksheet.write(s, 7, u"¿Cumple con la R.M. N°375-2008-TR?", head)

			workbook.close()
			f = open('/odoopreventor/custom/excel.xlsx', 'rb')
			# f = open('/odoo/custom/excel.xlsx', 'rb')
			file_name = io.BytesIO(f.read())
			self.write({
				'excel_ilu': u'{} - Iluminación.xlsx'.format(self.sequence if self.sequence else ""),
				'excel_ilu_binary': base64.encodestring(file_name.getvalue())
			})

	@api.depends("iluminacion_ids")
	def _compute_puntos_ilu(self):
		for record in self:
			record.puntos_ilu = len(record.iluminacion_ids)

class Iluminacion(models.Model):
	_name = 'iluminacion.iluminacion'
	_inherits = {'agente.general': 'agente_general_id'}

	agente_general_id = fields.Many2one('agente.general', required=True, ondelete='restrict', auto_join=True,
										string='Agente General')
	tarea = fields.Selection(selection=[('1', 'En Exteriores'),
										('2', 'En Interiores'),
										('3', 'Requerimiento Visual Simple'),
										('4', 'Distinción Moderada de Detalles'),
										('5', 'Distinción Clara de Detalles'),
										('6', 'Distinción Fina de Detalles'),
										('7', 'Alta Exactitud en la Distinción de Delta'),
										('8', 'Alta Exactitud de Especialización')], string='Tarea Visual', default="1")
	lux = fields.Float(string='Nivel de Iluminación (lux)')
	horario = fields.Selection(selection=[('9', 'Diurno'), ('0', 'Nocturno')], string='Turno', default="9")

	cumple = fields.Char(compute="_compute_iluminacion", string="¿Cumple con la R.M. N°375-2008-TR?", store=True)
	val_min = fields.Integer(compute="_compute_iluminacion", string="Nivel Mínimo Recomendado (lux)", store=True)


	@api.depends("tarea", "lux")
	def _compute_iluminacion(self):
		for record in self:

			if record.tarea:
				if record.tarea == "1":
					record.val_min = 20
				if record.tarea == "2":
					record.val_min = 50
				if record.tarea == "3":
					record.val_min = 200
				if record.tarea == "4":
					record.val_min = 300
				if record.tarea == "5":
					record.val_min = 500
				if record.tarea == "6":
					record.val_min = 750
				if record.tarea == "7":
					record.val_min = 1000
				if record.tarea == "8":
					record.val_min = 2000

			if record.lux:
				if record.lux < record.val_min:
					record.cumple = "NO CUMPLE"
				else:
					record.cumple = u"SÍ CUMPLE"
			else:
				record.cumple = "NO CUMPLE"

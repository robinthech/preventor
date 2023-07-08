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

class CovidAnexo4(models.Model):
	_name= "covid.anexo"

	name = fields.Char("Nombre")
	fecha = fields.Date('Fecha de Evaluación')
	evaluado = fields.Char('Evaluado por')
	empresa = fields.Char('Empresa Evaluada')
	ruc = fields.Char('RUC')
	puntaje = fields.Float('PUNTAJE',store=True)
	count_si = fields.Float('PUNTAJE',store=True)
	count_no = fields.Float('PUNTAJE',store=True)
	puntaje_2 = fields.Float('PUNTAJE',compute="_compute_puntaje",store=True)
	sequence = fields.Char("Codigo",compute="_compute_sequence",store=True)

	def default_covid(self):
		lista_ids = self.env["tipo.elemento.covid"].search([])
		return [(0, 0, {'name': i.name, 'cumplimiento': False,'sublista_ids':[(0, 0, {'name': j.name, 'cumplimiento': False,}) for j in i.elementos_ids] }) for i in lista_ids]

	lista_ids = fields.One2many("covid.anexo.lista","covid_id",string="Lista",default=default_covid, copy=True, store=True)


	txt_excel_cal = fields.Char()
	txt_binary_excel_cal = fields.Binary(string=u'Excel ANEXO 4')



	def fuction_compute_puntaje(self):
		puntaje = 0
		total = 0
		suma = 0
		for record in self:
			for line in record.lista_ids:
				total += 1
				if line.cumplimiento:
					suma += 1
				for sub_line in line.sublista_ids:
					total += 1
					if sub_line.cumplimiento:
						suma += 1

			if total ==0:
				record.puntaje = 0.0
				record.count_si = suma
				record.count_no = total-suma
			else:
				record.puntaje = round(suma/total,2)
				record.count_si = suma
				record.count_no = total-suma
		return round(suma/total,2)


	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "A4-00000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "A4-0000{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "A4-000{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "A4-00{}".format(i)

	def file_excel(self):
		self.ensure_one()
		workbook = xlsxwriter.Workbook(u'/odoo/custom/excel.xlsx')
		reporte = workbook.add_format()
		head = workbook.add_format()
		tbody = workbook.add_format()
		codigo = workbook.add_format()
		cabecera = workbook.add_format()
		titulo = workbook.add_format()
		texto = workbook.add_format()

		head.set_bold()


		reporte.set_bold()
		reporte.set_align('vcenter')
		reporte.set_font_size(16)
		reporte.set_fg_color('#FFFF00')
		reporte.set_align('center')


		head.set_font_color("white")
		head.set_font_name('Arial')
		head.set_font_size(10)
		head.set_align('center')
		codigo.set_align('right')
		codigo.set_border(1)
		head.set_align('vcenter')
		head.set_text_wrap()
		head.set_fg_color('#7da7d8')
		head.set_border(1)
		tbody.set_border(1)
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
		formatos.set_fg_color('#7da7d8')
		formatos.set_border(1)
		formaton = workbook.add_format()
		formaton.set_font_color("black")
		formaton.set_font_name('Arial')
		formaton.set_font_size(8)
		formaton.set_align('center')
		formaton.set_align('vcenter')
		formaton.set_text_wrap()
		formaton.set_fg_color('#7da7d8')
		formaton.set_border(1)
		cabecera.set_align('vcenter')
		cabecera.set_align('center')
		cabecera.set_text_wrap()
		cabecera.set_bold()
		cabecera.set_border(2)
		cabecera.set_fg_color('#000080')
		cabecera.set_font_color("white")
		cabecera.set_font_name('Arial')
		cabecera.set_font_size(10)
		titulo.set_align('vcenter')
		titulo.set_align('left')
		titulo.set_text_wrap()
		titulo.set_bold()
		titulo.set_border(2)
		titulo.set_font_name('Arial')
		titulo.set_font_size(8)
		texto.set_align('vcenter')
		texto.set_align('left')
		texto.set_text_wrap()
		texto.set_border(2)
		texto.set_font_name('Arial')
		texto.set_font_size(10)






		# worksheet.set_row(0, 40)
		today = date.today()
		my_date = datetime.now(pytz.timezone('America/Lima'))
		now = datetime.now()
		fecha_actual = today.strftime("%d/%m/%Y")
		hora_actual = my_date.strftime('%H:%M:%S')

		worksheet = workbook.add_worksheet(u"Reporte")
		worksheet.set_column('A:A', 20)
		worksheet.set_column('B:B', 0.1)
		worksheet.set_column('C:D', 20)
		worksheet.set_column('E:E', 5)
		worksheet.set_column('F:G', 0.1)
		worksheet.set_column('H:H', 12)
		worksheet.set_column('I:I', 0.1)
		worksheet.set_column('J:K', 8)
		worksheet.set_column('L:M', 12)
		worksheet.write(2, 0, u"CÓDIGO", head)
		worksheet.write(3, 0, u"FECHA", head)
		worksheet.write(4, 0, u"HORA", head)
		worksheet.write(5, 0, u"EVALUADO POR", head)
		worksheet.write(6, 0, u"EMPRESA", head)
		worksheet.write(7, 0, u"PUNTAJE OBTENIDO", head)
		worksheet.merge_range('A1:M1', u"REPORTE LISTA DE CHEQUEO", reporte)



		worksheet.write(10, 0, u"ELEMENTOS", head)
		worksheet.merge_range('B11:C11', u"Nº", head)
		worksheet.write(11, 0, u"ELEMENTO CUMPLIDAS", head)
		worksheet.write(12, 0, u"ELEMENTO SIN CUMPLIR", head)
		worksheet.write(13, 0, u"% CUMPLIMIENTO", head)
		worksheet.merge_range('B3:C3', self.sequence, codigo)
		worksheet.merge_range('B4:C4', fecha_actual, codigo)
		worksheet.merge_range('B5:C5', hora_actual, codigo)
		worksheet.merge_range('B6:C6', self.evaluado, codigo)
		worksheet.merge_range('B7:C7', self.empresa, codigo)
		worksheet.merge_range('B8:C8', self.puntaje, codigo)
		worksheet.merge_range('B12:C12', self.count_si, tbody)
		worksheet.merge_range('B13:C13', self.count_no, tbody)
		worksheet.merge_range('B14:C14', self.puntaje, tbody)

		chart = workbook.add_chart({
			'type': 'column'
			})
		chart.add_series({
			'name': 'Actividades',
			'categories': '=ReporteCovid!$A$12:$A$13',
			'values': '=ReporteCovid!$B$12:$B$13',
			'fill':   {'color': '#FF9900'}
		})


		chart.set_legend({'none': True})
		chart.set_size({'width': 435})
		worksheet.insert_chart('E2', chart)

		worksheet.merge_range('A17:G17', u"ELEMENTOS", cabecera)
		worksheet.merge_range('H17:J17', u"CUMPLE (SI/NO)", cabecera)
		worksheet.merge_range('K17:M17', u"Detalles / Pendientes / Por Mejorar", cabecera)

		s = 18

		for line in self.lista_ids:
			worksheet.merge_range('A{}:G{}'.format(s,s), line.name if line.name else "", head)
			if line.cumplimiento:
				worksheet.merge_range('H{}:J{}'.format(s,s), "X", texto)
			else:
				worksheet.merge_range('H{}:J{}'.format(s,s), "", texto)
			worksheet.merge_range('K{}:M{}'.format(s,s), line.detalles if line.detalles else "", texto)
			s +=1
			for sub_line in line.sublista_ids:
				worksheet.merge_range('A{}:G{}'.format(s,s), sub_line.name if sub_line.name else "", texto)
				if sub_line.cumplimiento:
					worksheet.merge_range('H{}:J{}'.format(s,s), "X", texto)
				else:
					worksheet.merge_range('H{}:J{}'.format(s,s), "", texto)
				worksheet.merge_range('K{}:M{}'.format(s,s), sub_line.detalles if sub_line.detalles else "", texto)
				s +=1

		workbook.close()

		f = open('/odoopreventor/custom/excel.xlsx', 'rb')

		file_name = io.BytesIO(f.read())
		
		self.write({
			'txt_excel_cal': u'LISTA DE CHEQUEO.xlsx',
			'txt_binary_excel_cal': base64.encodestring(file_name.getvalue())
		})



class ElementoCovid(models.Model):
	_name = "elemento.covid"

	name = fields.Char("Elemento")
	cumplimiento = fields.Boolean("Cumple (Si/No)")
	detalles = fields.Char("Detalles / Pendientes / Por Mejorar")
	tipo_elemento_id = fields.Many2one("tipo.elemento.covid",string="Tipo de Elemento")

class TipoElementoCovid(models.Model):
	_name = "tipo.elemento.covid"

	name = fields.Char("Elemento")
	cumplimiento = fields.Boolean("Cumple (Si/No)")
	detalles = fields.Char("Detalles / Pendientes / Por Mejorar")
	elementos_ids = fields.One2many("elemento.covid","tipo_elemento_id",string="Sub Elementos", copy=True, store=True)


class CovidAnexo4Lista(models.Model):
	_name= "covid.anexo.lista"

	name = fields.Char("Elemento")
	cumplimiento = fields.Boolean("Cumple (Si/No)")
	detalles = fields.Char("Detalles / Pendientes / Por Mejorar")
	covid_id = fields.Many2one("covid.anexo",string="Covid 4")
	sublista_ids = fields.One2many("covid.anexo.sublista","lista_id",string="Sub Elementos", copy=True, store=True)


class CovidAnexo4Subista(models.Model):
	_name= "covid.anexo.sublista"

	name = fields.Char("Elemento")
	cumplimiento = fields.Boolean("Cumple (Si/No)")
	detalles = fields.Char("Detalles / Pendientes / Por Mejorar")
	lista_id = fields.Many2one("covid.anexo.lista",string="lista Covid 4")



class EditlineCovid(models.TransientModel):
	_name = 'edit.linea.covid'


	def limites_permisos(self,plan_id):
		permiso_line = self.env["covid.anexo"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			_logger.info(plan.limite_registro)
			return True
		else:
			return False

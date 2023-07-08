# -*- coding: utf-8 -*-

import base64
import datetime
import os
import time
from datetime import datetime, timedelta, date
import os
import pytz
import xlsxwriter
import math
import base64
import io

from odoo import api, fields, models, _
from odoo.exceptions import UserError



class ProgramaAnual(models.Model):
	_name = 'programa.anual'

	name = fields.Char("name",default="PA")
	sequence = fields.Char(compute='_compute_sequence', string="Codigo")
	cliente = fields.Char("Razon Social")
	ruc = fields.Char("RUC")
	domicilio = fields.Char("Domicilio")
	actividad = fields.Char("Actividad Economica")
	trabajadores = fields.Integer("Nº de Trabajadores")
	objetivo_ids = fields.One2many("objetivo.general", "programa_id", "Objetivos Generales")
	excel_pa = fields.Char()
	excel_pa_binary = fields.Binary(string=u'Programa Anual')

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "PA-000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "PA-00{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "PA-0{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "PA-{}".format(i)

	def datos_sst(self):
		s = 0

		if self.objetivo_ids:
			self.ensure_one()
			# workbook = xlsxwriter.Workbook(u'C:\\Program Files (x86)\\Odoo 13.0\\server\\addons\\excel.xlsx')
			workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')

			head = workbook.add_format()
			head.set_bold()
			head.set_font_name('Frutiger-Light')
			head.set_font_size(28)
			head.set_align('center')
			head.set_align('vcenter')
			head.set_text_wrap()

			titulo = workbook.add_format()
			titulo.set_font_name('Frutiger-Light')
			titulo.set_font_size(16)
			titulo.set_bold()
			titulo.set_align('center')
			titulo.set_align('vcenter')
			titulo.set_fg_color('#8DB4E2')
			titulo.set_text_wrap()
			titulo.set_border(2)

			datos = workbook.add_format()
			datos.set_font_name('Frutiger-Light')
			datos.set_font_size(11)
			datos.set_bold()
			datos.set_align('left')
			datos.set_align('vcenter')
			datos.set_text_wrap()
			datos.set_border(2)

			titulo1 = workbook.add_format()
			titulo1.set_font_name('Frutiger-Light')
			titulo1.set_font_size(11)
			titulo1.set_bold()
			titulo1.set_align('center')
			titulo1.set_align('vcenter')
			titulo1.set_fg_color('#D9D9D9')
			titulo1.set_text_wrap()
			titulo1.set_border(2)

			titulo2 = workbook.add_format()
			titulo2.set_font_name('Frutiger-Light')
			titulo2.set_font_size(11)
			titulo2.set_bold()
			titulo2.set_align('left')
			titulo2.set_align('vcenter')
			titulo2.set_fg_color('#D9D9D9')
			titulo2.set_text_wrap()
			titulo2.set_border(2)

			datos1 = workbook.add_format()
			datos1.set_font_name('Frutiger-Light')
			datos1.set_font_size(11)
			datos1.set_align('center')
			datos1.set_align('vcenter')
			datos1.set_text_wrap()
			datos1.set_border(2)

			datos2 = workbook.add_format()
			datos2.set_font_name('Frutiger-Light')
			datos2.set_font_size(11)
			datos2.set_align('left')
			datos2.set_align('vcenter')
			datos2.set_text_wrap()
			datos2.set_border(2)

			actividad = workbook.add_format()
			actividad.set_font_name('Frutiger-Light')
			actividad.set_font_size(11)
			actividad.set_align('center')
			actividad.set_align('vcenter')
			actividad.set_text_wrap()
			actividad.set_border(2)

			mes = workbook.add_format()
			mes.set_font_name('Frutiger-Light')
			mes.set_font_size(11)
			mes.set_align('center')
			mes.set_align('vcenter')
			mes.set_fg_color('#646464')
			mes.set_text_wrap()
			mes.set_border(2)

			mes1 = workbook.add_format()
			mes1.set_font_name('Frutiger-Light')
			mes1.set_font_size(11)
			mes1.set_align('center')
			mes1.set_align('vcenter')
			mes1.set_fg_color('#FFFFFF')
			mes1.set_text_wrap()
			mes1.set_border(2)



			worksheet = workbook.add_worksheet(u"Programa Anual de SST")
			worksheet.set_column('A:A', 0.92)
			worksheet.set_column('B:B', 4)
			worksheet.set_column('C:C', 16)
			worksheet.set_column('D:D', 34.5)
			worksheet.set_column('E:E', 16.38)
			worksheet.set_column('F:F', 13)
			worksheet.set_column('G:G', 40.38)
			worksheet.set_column('H:I', 6.88)
			worksheet.set_column('J:J', 8.88)
			worksheet.set_column('K:W', 3.5)
			worksheet.set_column('X:X', 25.63)
			worksheet.set_column('Y:Y', 13.38)
			worksheet.set_column('Z:Z', 43.25)

			worksheet.merge_range('B3:Z3', u'PROGRAMA ANUAL DE SEGURIDAD Y SALUD EN EL TRABAJO', head)
			worksheet.merge_range('B7:Z7', u'PROGRAMA ANUAL DE SEGURIDAD Y SALUD EN EL TRABAJO', titulo)
			worksheet.merge_range('B8:Z8', u'DATOS DEL EMPLEADOR:', datos)
			worksheet.merge_range('B9:D9', u'RAZÓN SOCIAL O DENOMINACIÓN SOCIAL', titulo1)
			worksheet.write('E9', u"RUC", titulo1)
			worksheet.merge_range('F9:T9', u'DOMICILIO\n(Dirección, distrito,departamento,provincia)', titulo1)
			worksheet.merge_range('U9:X9', u'ACTIVIDAD ECONÓMICA', titulo1)
			worksheet.merge_range('Y9:Z9', u'N° TRABAJADORES', titulo1)

			worksheet.merge_range('B10:D10', u'{}'.format(self.cliente if self.cliente else ""), datos1)
			worksheet.write('E10', u'{}'.format(self.ruc if self.ruc else ""), datos1)
			worksheet.merge_range('E10:E10', u'{}'.format(self.ruc if self.ruc else ""), datos1)
			worksheet.merge_range('F10:T10', u'{}'.format(self.domicilio if self.domicilio else ""), datos1)
			worksheet.merge_range('U10:X10', u'{}'.format(self.actividad if self.actividad else ""), datos1)
			worksheet.merge_range('Y10:Z10', u'{}'.format(self.trabajadores if self.trabajadores else ""), datos1)

			my_date = datetime.now(pytz.timezone('America/Lima'))

			i = 10
			j = 1
			l = 0
			k = 0
			m = 0
			p = 0
			n = 0
			for o in self.objetivo_ids:
				worksheet.merge_range(i, 1, i, 2, u"Objetivo General {}".format(j), titulo2)
				worksheet.merge_range(i, 3, i, 25, u"{}".format(o.name if o.name else ""), datos)
				k = 1
				if o.especifico_ids:
					for a in o.especifico_ids:
						l = i + k
						worksheet.merge_range(l, 3, l, 25, u"{}".format(a.name if a.name else ""), datos2)
						k += 1
						j += 1
				else:
					l = 1
				worksheet.merge_range(i+1, 1, l, 2, u"Objetivos Especificos", titulo2)
				i = i + k
				worksheet.merge_range(i, 1, i, 2, u"Meta", titulo2)
				worksheet.merge_range(i, 3, i, 25, u"{}".format(o.meta if o.meta else ""), datos2)
				worksheet.merge_range(i+1, 1, i+1, 2, u"Presupuesto", titulo2)
				worksheet.merge_range(i+1, 3, i+1, 25, u"{}".format(o.presupuesto if o.presupuesto else ""), datos2)
				worksheet.merge_range(i+2, 1, i+2, 2, u"Recursos", titulo2)
				worksheet.merge_range(i+2, 3, i+2, 25, u"{}".format(o.recurso if o.recurso else ""), datos2)

				worksheet.merge_range(i+3, 1, i+4, 1, u"N°", titulo1)
				worksheet.merge_range(i+3, 2, i+4, 3, u"Descripción de la Actividad", titulo1)
				worksheet.merge_range(i+3, 4, i+4, 4, u"Responsable de la Ejecución", titulo1)
				worksheet.merge_range(i+3, 5, i+4, 5, u"Área", titulo1)
				worksheet.merge_range(i+3, 6, i+4, 6, u"Indicador", titulo1)
				worksheet.merge_range(i+3, 7, i+4, 7, u"Meta", titulo1)
				worksheet.merge_range(i+3, 8, i+4, 9, u"Avance", titulo1)
				worksheet.merge_range(i+3, 10, i+3, 21, u"AÑO {}".format(my_date.strftime('%Y')), titulo1)
				worksheet.write(i+4, 10, u"E", titulo1)
				worksheet.write(i+4, 11, u"F", titulo1)
				worksheet.write(i+4, 12, u"M", titulo1)
				worksheet.write(i+4, 13, u"A", titulo1)
				worksheet.write(i+4, 14, u"M", titulo1)
				worksheet.write(i+4, 15, u"J", titulo1)
				worksheet.write(i+4, 16, u"J", titulo1)
				worksheet.write(i+4, 17, u"A", titulo1)
				worksheet.write(i+4, 18, u"S", titulo1)
				worksheet.write(i+4, 19, u"O", titulo1)
				worksheet.write(i+4, 20, u"N", titulo1)
				worksheet.write(i+4, 21, u"D", titulo1)
				worksheet.merge_range(i+3, 22, i+4, 23, u"Estado (Realizado - Pendiente - En Proceso", titulo1)
				worksheet.merge_range(i+3, 24, i+4, 25, u"Observaciones", titulo1)
				m = 1
				p = 1
				i = i + 2
				for b in o.actividad_ids:
					n = i + m

					worksheet.merge_range(n+2, 1, n+3, 1, u"{}".format(p), actividad)
					worksheet.merge_range(n+2, 2, n+3, 3, u"{}".format(b.name if b.name else ""), actividad)
					worksheet.merge_range(n+2, 4, n+3, 4, u"{}".format(b.responsable if b.responsable else ""), actividad)
					worksheet.merge_range(n+2, 5, n+3, 5, u"{}".format(b.area if b.area else ""), actividad)
					worksheet.merge_range(n+2, 6, n+3, 6, u"{}".format(b.indicador if b.indicador else ""), actividad)
					worksheet.merge_range(n+2, 7, n+3, 7, u"{}".format(o.meta if o.meta else ""), actividad)
					worksheet.write(n+2, 8, u"P", actividad)
					worksheet.write(n+2, 9, u"{}".format(b.avance_p if b.avance_p else ""), actividad)
					worksheet.write(n+3, 8, u"E", actividad)
					worksheet.write(n+3, 9, u"{}".format(b.avance_e if b.avance_e else ""), actividad)
					#meses
					if b.enero_p == True:
						worksheet.write(n+2, 10, u"", mes)
					else:
						worksheet.write(n+2, 10, u"", mes1)
					if b.febrero_p == True:
						worksheet.write(n+2, 11, u"", mes)
					else:
						worksheet.write(n+2, 11, u"", mes1)
					if b.marzo_p == True:
						worksheet.write(n+2, 12, u"", mes)
					else:
						worksheet.write(n+2, 12, u"", mes1)
					if b.abril_p == True:
						worksheet.write(n+2, 13, u"", mes)
					else:
						worksheet.write(n+2, 13, u"", mes1)
					if b.mayo_p == True:
						worksheet.write(n+2, 14, u"", mes)
					else:
						worksheet.write(n+2, 14, u"", mes1)
					if b.junio_p == True:
						worksheet.write(n+2, 15, u"", mes)
					else:
						worksheet.write(n+2, 15, u"", mes1)
					if b.julio_p == True:
						worksheet.write(n+2, 16, u"", mes)
					else:
						worksheet.write(n+2, 16, u"", mes1)
					if b.agosto_p == True:
						worksheet.write(n+2, 17, u"", mes)
					else:
						worksheet.write(n+2, 17, u"", mes1)
					if b.septiembre_p == True:
						worksheet.write(n+2, 18, u"", mes)
					else:
						worksheet.write(n+2, 18, u"", mes1)
					if b.octubre_p == True:
						worksheet.write(n+2, 19, u"", mes)
					else:
						worksheet.write(n+2, 19, u"", mes1)
					if b.noviembre_p == True:
						worksheet.write(n+2, 20, u"", mes)
					else:
						worksheet.write(n+2, 20, u"", mes1)
					if b.diciembre_p == True:
						worksheet.write(n+2, 21, u"", mes)
					else:
						worksheet.write(n+2, 21, u"", mes1)
					if b.enero_e == True:
						worksheet.write(n+3, 10, u"", mes)
					else:
						worksheet.write(n+3, 10, u"", mes1)
					if b.febrero_e == True:
						worksheet.write(n+3, 11, u"", mes)
					else:
						worksheet.write(n+3, 11, u"", mes1)
					if b.marzo_e == True:
						worksheet.write(n+3, 12, u"", mes)
					else:
						worksheet.write(n+3, 12, u"", mes1)
					if b.abril_e == True:
						worksheet.write(n+3, 13, u"", mes)
					else:
						worksheet.write(n+3, 13, u"", mes1)
					if b.mayo_e == True:
						worksheet.write(n+3, 14, u"", mes)
					else:
						worksheet.write(n+3, 14, u"", mes1)
					if b.junio_e == True:
						worksheet.write(n+3, 15, u"", mes)
					else:
						worksheet.write(n+3, 15, u"", mes1)
					if b.julio_e == True:
						worksheet.write(n+3, 16, u"", mes)
					else:
						worksheet.write(n+3, 16, u"", mes1)
					if b.agosto_e == True:
						worksheet.write(n+3, 17, u"", mes)
					else:
						worksheet.write(n+3, 17, u"", mes1)
					if b.septiembre_e == True:
						worksheet.write(n+3, 18, u"", mes)
					else:
						worksheet.write(n+3, 18, u"", mes1)
					if b.octubre_e == True:
						worksheet.write(n+3, 19, u"", mes)
					else:
						worksheet.write(n+3, 19, u"", mes1)
					if b.noviembre_e == True:
						worksheet.write(n+3, 20, u"", mes)
					else:
						worksheet.write(n+3, 20, u"", mes1)
					if b.diciembre_e == True:
						worksheet.write(n+3, 21, u"", mes)
					else:
						worksheet.write(n+3, 21, u"", mes1)
					worksheet.merge_range(n+2, 22, n+3, 23, u"{}".format(b.estado if b.estado else ""), actividad)
					worksheet.merge_range(n+2, 24, n+3, 25, u"{}".format(b.observaciones if b.observaciones else ""), actividad)
					m += 2
					p += 1
				i += m + 2

			workbook.close()

			# f = open('C:\\Program Files (x86)\\Odoo 13.0\\server\\addons\\excel.xlsx', 'rb')
			f = open('/odoopreventor/custom/excel.xlsx', 'rb')
			file_name = io.BytesIO(f.read())

			self.write({
				'excel_pa': u'{} - Programa Anual de SST - {}.xlsx'.format(self.sequence if self.sequence else "", my_date.strftime('%Y-%m-%d %H:%M')),
				'excel_pa_binary': base64.encodestring(file_name.getvalue())
			})

class ProgramaAnualTransient(models.TransientModel):
	_name = 'programaanual.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["programa.anual"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class ObjetivoGeneral(models.Model):
	_name = 'objetivo.general'

	name = fields.Char("Objetivo General")
	programa_id = fields.Many2one("programa.anual", string="Programa Anual de Seguridad")
	especifico_ids = fields.One2many("objetivo.especifico", "objetivo_id", string="Objetivos Especificos")
	meta = fields.Char("Meta")
	indicador = fields.Char("Indicador")
	presupuesto = fields.Char("Presupuesto")
	recurso = fields.Char("Recurso")
	actividad_ids = fields.One2many("actividad.actividad", "objetivo_id", string="Actividades")

class ObjetivoGeneralTransient(models.TransientModel):
	_name = 'objetivogeneral.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["objetivo.general"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class ObjetivoEspecifico(models.Model):
	_name = 'objetivo.especifico'

	name = fields.Char("Objetivo Especifico")
	objetivo_id = fields.Many2one("objetivo.general", string="Objetivo General", required=True)
	active = fields.Boolean("Archivado", default=True)

class ObjetivoEspecificoTransient(models.TransientModel):
	_name = 'objetivoespecifico.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["objetivo.especifico"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

	def nuevo_especifico(self,name,id_general):
		general = self.env["objetivo.general"].search([('id','=',id_general)],limit=1)
		especifico = self.env["objetivo.especifico"].create({'name':name, 'objetivo_id':general.id})

class Actividades(models.Model):
	_name = 'actividad.actividad'

	name = fields.Char("Descripcion de la Actividad")
	responsable = fields.Char("Responsable de Ejecucion")
	area = fields.Char("Area")
	indicador = fields.Char("Indicador")
	meta = fields.Char("Meta")
	objetivo_id = fields.Many2one("objetivo.general", string="Objetivo General")
	avance_p = fields.Integer("Avance Programado (P)")
	avance_e = fields.Char("Avance Ejecutado (E)")
	enero_p = fields.Boolean("Enero (P)")
	enero_e = fields.Boolean("Enero (E)")
	febrero_p = fields.Boolean("Febrero (P)")
	febrero_e = fields.Boolean("Febrero (E)")
	marzo_p = fields.Boolean("Marzo (P)")
	marzo_e = fields.Boolean("Marzo (E)")
	abril_p = fields.Boolean("Abril (P)")
	abril_e = fields.Boolean("Abril (E)")
	mayo_p = fields.Boolean("Mayo (P)")
	mayo_e = fields.Boolean("Mayo (E)")
	junio_p = fields.Boolean("Junio (P)")
	junio_e = fields.Boolean("Junio (E)")
	julio_p = fields.Boolean("Julio (P)")
	julio_e = fields.Boolean("Julio (E)")
	agosto_p = fields.Boolean("Agosto (P)")
	agosto_e = fields.Boolean("Agosto (E)")
	septiembre_p = fields.Boolean("Septiembre (P)")
	septiembre_e = fields.Boolean("Septiembre (E)")
	octubre_p = fields.Boolean("Octubre (P)")
	octubre_e = fields.Boolean("Octubre (E)")
	noviembre_p = fields.Boolean("Noviembre (P)")
	noviembre_e = fields.Boolean("Noviembre (E)")
	diciembre_p = fields.Boolean("Diciembre (P)")
	diciembre_e = fields.Boolean("Diciembre (E)")
	estado = fields.Char(string="Finalizado", default="Pendiente")
	observaciones = fields.Text("Observaciones")

	# @api.onchange("avance_e")
	# def cambio_estado(self):
	#     for record in self:
	#         if record.avance_e:
	#             if record.avance_e == "100.00%":
	#                 record.estado = "Finalizado"
	#             else:
	#                 record.estado = "En Proceso"
	#         else:
	#             record.estado = "Pendiente"

class ActividadesTransient(models.TransientModel):
	_name = 'actividad.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["actividad.actividad"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

	def write_linea(self,actividad_id,estado,avance_p,final):
		lineaedit = self.env["actividad.actividad"].sudo().browse(actividad_id)
		lineaedit.write({'estado': estado,'avance_p': avance_p,'avance_e': final})
		return [lineaedit.estado,lineaedit.avance_p,lineaedit.avance_e]

	def limites_permisos(self,plan_id):
		permiso_line = self.env["programa.anual"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			return True
		else:
			return False

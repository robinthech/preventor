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


class PermisoTrabajo(models.Model):
	_name = "permiso.trabajo"
	_inherit = ['mail.thread']

	name = fields.Char("N° Permiso", index=True,
					   default=lambda self: _('Borrador'))
	ubicacion_exacta = fields.Char("Ubicación")
	area = fields.Char("Ubicación")
	sub_area = fields.Char("Ubicación")
	descripcion = fields.Char("Descripción del Trabajo")
	fecha_inicio = fields.Datetime("Fecha y Hora Inicio")
	hora_inicio = fields.Date("Hora Inicio")
	fecha_fin = fields.Datetime("Fecha y Hora Fin")
	hora_fin = fields.Date("Hora Fin")
	fecha_inicio_1 = fields.Date("Fecha y Hora Inicio")
	fecha_fin_1 = fields.Date("Fecha y Hora Fin")
	contratista_id = fields.Many2one(
		"empresa.empresa", string="Empresa", store=True)
	solicitante_id = fields.Many2one(
		"res.users", string="Solicitante")
	autorizador_id = fields.Many2one(
		"res.users", string="Autorizador")
	aprobador_id = fields.Many2one(
		"res.users", string="Aprobador")
	empleados_ids = fields.One2many(
		"permiso.trabajador", "permiso_id", string="Empleados", copy=True)
	area_id = fields.Many2one(
		"area.area", string="Área", store=True)
	sub_area_id = fields.Many2one("sub.area", string="Sub Área")
	observacion_auto = fields.Char("Observaciones del Autorizador")
	observacion_apro = fields.Char("Observaciones del Aprobador")
	estado = fields.Selection(selection=[('1', 'Draft'), ('2', 'Requested'), ('3', 'Authorized'), ('4', 'Approved'), ('5', 'Closed'), (
		'6', 'Observed'), ('7', 'Canceled')], index=True, track_visibility='onchange', string="Estado", default="1", readonly=True)

	txt_excel_cal = fields.Char()
	txt_binary_excel_cal = fields.Binary(string=u'Informe Calor')
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)
	sequence = fields.Char(compute='_compute_sequence', string="Codigo", store=True)
	plantilla = fields.Many2one("tipo.permiso", string="Plantilla", store=True)
	empresa_id = fields.Many2one("empresa.empresa", string="Empresa", store=True)

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "PTR-0000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "PTR-000{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "PTR-00{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "PTR-0{}".format(i)
	# renovacion
	def open_word_frio(self):
		biologico = Workbook()
		style1_0 = easyxf('font: height 210, name Arial Narrow, colour_index black; align:wrap on, horiz center, vertical center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;')
		style1_2 = easyxf('font: bold on, height 210, name Arial Narrow, colour_index white; pattern: pattern solid, fore_colour blue; align:wrap on, horiz center, vertical center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;')

		ws = biologico.add_sheet(u'PERMISO TRABAJO')
		ws.write_merge(0, 0, 0, 2, u"{}".format(self.name if self.name else ""), style1_2)
		ws.write_merge(0, 0, 3, 8, u"PERMISO DE TRABAJO", style1_2)
		ws.write_merge(0, 0, 9, 11, u"{}".format(self.estado if self.estado else ""), style1_2)
		ws.write_merge(1, 1, 0, 11, u"TIPO DE TRABAJO", style1_2)
		ws.write_merge(2, 2, 0, 2, u"Trabajo en Altura", style1_0)
		ws.write_merge(2, 2, 4, 6, u"Trabajo en Espacios Confinados", style1_0)
		ws.write_merge(2, 2, 8, 10, u"Trabajo en Caliente", style1_0)
		if self.altura:
			ws.write(2, 3, u"X", style1_0)
		else:
			ws.write(2, 3, u"", style1_0)
		if self.confinado:
			ws.write(2, 7, u"X", style1_0)
		else:
			ws.write(2, 7, u"", style1_0)
		if self.calor:
			ws.write(2, 11, u"X", style1_0)
		else:
			ws.write(2, 11, u"", style1_0)
		ws.write_merge(3, 3, 0, 2, u"Trabajo en Frío", style1_0)
		ws.write_merge(3, 3, 4, 6, u"Trabajo Eléctricos", style1_0)
		if self.frio:
			ws.write(3, 3, u"X")
		else:
			ws.write(3, 3, u"")
		if self.electrico:
			ws.write(3, 7, u"X")
		else:
			ws.write(3, 7, u"")
		ws.write_merge(4, 4, 0, 11, u"DATOS GENERALES", style1_2)
		ws.write_merge(5, 5, 0, 5, u"AREA", style1_0)
		ws.write_merge(5, 5, 6, 11, u"CONTRATISTA", style1_0)
		ws.write_merge(6, 6, 0, 5, u"{}".format(self.area if self.area else ""), style1_0)
		ws.write_merge(6, 6, 6, 11, u"{}".format(
			self.contratista_id.name if self.contratista_id else ""), style1_0)
		ws.write_merge(7, 7, 0, 5, u"SUB AREA", style1_0)
		ws.write_merge(7, 7, 6, 11, u"Fecha de Inicio", style1_0)
		ws.write_merge(8, 8, 0, 5, u"{}".format(
			self.sub_area if self.sub_area else ""), style1_0)
		ws.write_merge(8, 8, 6, 11, u"{}".format(self.fecha_inicio if self.fecha_inicio else ""), style1_0)
		ws.write_merge(9, 9, 0, 5, u"UBICACION", style1_0)
		ws.write_merge(9, 9, 6, 11, u"Fecha de Fin", style1_0)
		ws.write_merge(10, 10, 0, 5, u"{}".format(
			self.ubicacion_exacta if self.ubicacion_exacta else ""), style1_0)
		ws.write_merge(10, 10, 6, 11, u"{}".format(self.fecha_fin if self.fecha_fin else ""), style1_0)
		ws.write_merge(11, 11, 0, 11, u"DESCRIPCIÓN DEL TRABAJO", style1_2)
		ws.write_merge(12, 12, 0, 11, u"{}".format(
			self.descripcion if self.descripcion else ""), style1_0)
		s = 13
		if self.altura:
			ws.write_merge(s, s, 0, 11, u"Trabajo en Altura", style1_2)
			s = s + 1
			unir_numero = len(self.epp_altura_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2, u"EPP", style1_2)
				for line in self.epp_altura_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name ), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.herramienta_altura_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0,
							   2, u"HERRAMIENTAS", style1_2)
				for line in self.herramienta_altura_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.preparacion_altura_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"REQUISITOS DE PREPARACIÓN", style1_2)
				for line in self.preparacion_altura_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.cerramiento_altura_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CERRAMIENTO DE ABERTURAS", style1_2)
				for line in self.cerramiento_altura_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)

					s = s + 1
			unir_numero = len(self.seguridad_altura_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CONDICIONES DE SEGURIDAD", style1_2)
				for line in self.seguridad_altura_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.otras_altura_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"OTRAS CONDICIONES", style1_2)
				for line in self.otras_altura_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
		if self.confinado:
			ws.write_merge(
				s, s, 0, 11, u"Trabajo en Espacios Confinados", style1_2)
			s = s + 1
			unir_numero = len(self.epp_confinado_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2, u"EPP", style1_2)
				for line in self.epp_confinado_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.herramienta_confinado_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0,
							   2, u"HERRAMIENTAS", style1_2)
				for line in self.herramienta_confinado_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.preparacion_confinado_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"REQUISITOS DE PREPARACIÓN", style1_2)
				for line in self.preparacion_confinado_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.cerramiento_confinado_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CERRAMIENTO DE ABERTURAS", style1_2)
				for line in self.cerramiento_confinado_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.seguridad_confinado_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CONDICIONES DE SEGURIDAD", style1_2)
				for line in self.seguridad_confinado_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
		if self.calor:
			ws.write_merge(s, s, 0, 11, u"Trabajo en Caliente", style1_2)
			s = s + 1
			unir_numero = len(self.epp_calor_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2, u"EPP", style1_2)
				for line in self.epp_calor_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.herramienta_calor_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0,
							   2, u"HERRAMIENTAS", style1_2)
				for line in self.herramienta_calor_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.preparacion_calor_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"REQUISITOS DE PREPARACIÓN", style1_2)
				for line in self.preparacion_calor_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.cerramiento_calor_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CERRAMIENTO DE ABERTURAS", style1_2)
				for line in self.cerramiento_calor_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.seguridad_calor_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CONDICIONES DE SEGURIDAD", style1_2)
				for line in self.seguridad_calor_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.otras_calor_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"OTRAS CONDICIONES", style1_2)
				for line in self.otras_calor_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1

		if self.frio:
			ws.write_merge(s, s, 0, 11, u"Trabajo en Frio", style1_2)
			s = s + 1
			unir_numero = len(self.epp_frio_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2, u"EPP", style1_2)
				for line in self.epp_frio_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.herramienta_frio_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0,
							   2, u"HERRAMIENTAS", style1_2)
				for line in self.herramienta_frio_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.preparacion_frio_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"REQUISITOS DE PREPARACIÓN", style1_2)
				for line in self.preparacion_frio_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.cerramiento_frio_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CERRAMIENTO DE ABERTURAS", style1_2)
				for line in self.cerramiento_frio_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.seguridad_frio_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CONDICIONES DE SEGURIDAD", style1_2)
				for line in self.seguridad_frio_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_2)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.otras_frio_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"OTRAS CONDICIONES", style1_2)
				for line in self.otras_frio_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_2)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
		if self.electrico:
			ws.write_merge(s, s, 0, 11, u"Trabajo Eléctrico", style1_2)
			s = s + 1
			unir_numero = len(self.epp_electrico_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2, u"EPP", style1_2)
				for line in self.epp_electrico_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.herramienta_electrico_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0,
							   2, u"HERRAMIENTAS", style1_2)
				for line in self.herramienta_electrico_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.preparacion_electrico_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"REQUISITOS DE PREPARACIÓN", style1_2)
				for line in self.preparacion_electrico_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.cerramiento_electrico_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CERRAMIENTO DE ABERTURAS", style1_2)
				for line in self.cerramiento_electrico_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.seguridad_electrico_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"CONDICIONES DE SEGURIDAD", style1_2)
				for line in self.seguridad_electrico_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
			unir_numero = len(self.otras_electrico_ids)
			if unir_numero > 0:
				ws.write_merge(s, s + unir_numero - 1, 0, 2,
							   u"OTRAS CONDICIONES", style1_2)
				for line in self.otras_electrico_ids:
					ws.write_merge(s, s, 3, 10, u"{}".format(
						line.name), style1_0)
					if line.check:
						ws.write(s, 11, u"X", style1_0)
					else:
						ws.write(s, 11, u"", style1_0)
					s = s + 1
		ws.write_merge(s, s, 0, 11, u"TRABAJADORES", style1_2)
		s = s + 1
		for line in self.empleados_ids:
			ws.write_merge(s, s, 0, 11, u"{}".format(
				line.trabajador_id.name if line.trabajador_id else ""), style1_0)
			s = s + 1
		ws.write_merge(s, s, 0, 11, u"COMENTARIOS", style1_2)
		s = s + 1

		ws.write_merge(s, s, 0, 5, u"AUTORIZADOR", style1_2)
		ws.write_merge(s, s, 6, 11, u"APROBADOR", style1_2)
		s = s + 1
		ws.write_merge(s, s, 0, 5, u"{}".format(
			self.observacion_auto if self.observacion_auto else ""), style1_0)
		ws.write_merge(s, s, 6, 11, u"{}".format(
			self.observacion_apro if self.observacion_apro else ""), style1_0)
		s = s + 1
		ws.write_merge(s, s, 0, 3, u"SOLICITANTE", style1_2)
		ws.write_merge(s, s, 4, 7, u"AUTORIZADOR", style1_2)
		ws.write_merge(s, s, 8, 11, u"APROBADOR", style1_2)
		s = s + 1
		ws.write_merge(s, s, 0, 3, u"{}".format(
			self.solicitante_id.name if self.solicitante_id else ""), style1_0)
		ws.write_merge(s, s, 4, 7, u"{}".format(
			self.autorizador_id.name if self.autorizador_id else ""), style1_0)
		ws.write_merge(s, s, 8, 11, u"{}".format(
			self.aprobador_id.name if self.aprobador_id else ""), style1_0)

		file_name = io.BytesIO()
		biologico.save(file_name)

		self.write({
			'txt_excel_cal': u'PermisosTrabajo.xls',
			'txt_binary_excel_cal': base64.encodestring(file_name.getvalue())
		})

	@api.model
	def create(self, vals):
		if vals.get('name', _('Borrador')) == _('Borrador'):
			vals['name'] = self.env['ir.sequence'].next_by_code(
				'permiso.trabajo') or _('Borrador')
		res = super(PermisoTrabajo, self).create(vals)
		return res

	def set_solicitado(self):
		return self.write({'estado': '2'})

	def set_autorizado(self):
		return self.write({'estado': '3'})

	def set_aprobado(self):
		return self.write({'estado': '4'})

	def set_cerrado(self):
		return self.write({'estado': '5'})


	def default_epp_1(self):
		epps_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'EPP'), ('altura', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'altura': True}) for i in epps_ids]

	def default_epp_2(self):
		epps_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'EPP'), ('confinado', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'confinado': True, 'image': i.image}) for i in epps_ids]

	@api.model
	def default_epp_3(self):
		epps_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'EPP'), ('calor', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'calor': True, 'image': i.image}) for i in epps_ids]

	@api.model
	def default_epp_4(self):
		epps_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'EPP'), ('frio', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'frio': True, 'image': i.image}) for i in epps_ids]

	@api.model
	def default_epp_5(self):
		epps_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'EPP'), ('electrico', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'electrico': True, 'image': i.image}) for i in epps_ids]

	@api.model
	def default_herramienta_1(self):
		herramientas_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Herramientas'), ('altura', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'altura': True, 'image': i.image}) for i in herramientas_ids]

	@api.model
	def default_herramienta_2(self):
		herramientas_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Herramientas'), ('confinado', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'confinado': True, 'image': i.image}) for i in herramientas_ids]

	@api.model
	def default_herramienta_3(self):
		herramientas_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Herramientas'), ('calor', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'calor': True, 'image': i.image}) for i in herramientas_ids]

	@api.model
	def default_herramienta_4(self):
		herramientas_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Herramientas'), ('frio', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'frio': True, 'image': i.image}) for i in herramientas_ids]

	@api.model
	def default_herramienta_5(self):
		herramientas_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Herramientas'), ('electrico', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'electrico': True, 'image': i.image}) for i in herramientas_ids]

	@api.model
	def default_preparacion_1(self):
		preparacions_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Preparación'), ('altura', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'altura': True}) for i in preparacions_ids]

	@api.model
	def default_preparacion_2(self):
		preparacions_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Preparación'), ('confinado', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'confinado': True}) for i in preparacions_ids]

	@api.model
	def default_preparacion_3(self):
		preparacions_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Preparación'), ('calor', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'calor': True}) for i in preparacions_ids]

	@api.model
	def default_preparacion_4(self):
		preparacions_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Preparación'), ('frio', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'frio': True}) for i in preparacions_ids]

	@api.model
	def default_preparacion_5(self):
		preparacions_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Preparación'), ('electrico', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'electrico': True}) for i in preparacions_ids]

	@api.model
	def default_cerramiento_1(self):
		cerramientos_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('altura', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'altura': True}) for i in cerramientos_ids]

	@api.model
	def default_cerramiento_2(self):
		cerramientos_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('confinado', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'confinado': True}) for i in cerramientos_ids]

	@api.model
	def default_cerramiento_3(self):
		cerramientos_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('calor', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'calor': True}) for i in cerramientos_ids]

	@api.model
	def default_cerramiento_4(self):
		cerramientos_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('frio', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'frio': True}) for i in cerramientos_ids]

	@api.model
	def default_cerramiento_5(self):
		cerramientos_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('electrico', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'electrico': True}) for i in cerramientos_ids]

	@api.model
	def default_seguridad_1(self):
		seguridads_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('altura', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'altura': True}) for i in seguridads_ids]

	@api.model
	def default_seguridad_2(self):
		seguridads_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('confinado', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'confinado': True}) for i in seguridads_ids]

	@api.model
	def default_seguridad_3(self):
		seguridads_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('calor', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'calor': True}) for i in seguridads_ids]

	@api.model
	def default_seguridad_4(self):
		seguridads_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('frio', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'frio': True}) for i in seguridads_ids]

	@api.model
	def default_seguridad_5(self):
		seguridads_ids = self.env["requisito.requisito"].search(
			['&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('electrico', '=', True)])
		return [(0, 0, {'name': i.name,'requisito_id': i.id, 'tipo_requi_id': i.tipo_requi_id.id, 'check': False, 'electrico': True}) for i in seguridads_ids]

	epp_altura_ids = fields.One2many("requisito.permiso", "permiso_id", string="EPPs", domain=[
		'&', ('tipo_requi_id.name', '=', 'EPP'), ('altura', '=', True)], default=default_epp_1, copy=True, store=True)
	epp_confinado_ids = fields.One2many("requisito.permiso", "permiso_id", string="EPPs", domain=[
		'&', ('tipo_requi_id.name', '=', 'EPP'), ('confinado', '=', True)], default=default_epp_2, copy=True, store=True)
	epp_calor_ids = fields.One2many("requisito.permiso", "permiso_id", string="EPPs", domain=[
		'&', ('tipo_requi_id.name', '=', 'EPP'), ('calor', '=', True)], default=default_epp_3, copy=True, store=True)
	epp_frio_ids = fields.One2many("requisito.permiso", "permiso_id", string="EPPs", domain=[
		'&', ('tipo_requi_id.name', '=', 'EPP'), ('frio', '=', True)], default=default_epp_4, copy=True, store=True)
	epp_electrico_ids = fields.One2many("requisito.permiso", "permiso_id", string="EPPs", domain=[
		'&', ('tipo_requi_id.name', '=', 'EPP'), ('electrico', '=', True)], default=default_epp_5, copy=True, store=True)

	herramienta_altura_ids = fields.One2many("requisito.permiso", "permiso_id", string="Herraminetas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Herramientas'), ('altura', '=', True)], default=default_herramienta_1, copy=True, store=True)
	herramienta_confinado_ids = fields.One2many("requisito.permiso", "permiso_id", string="Herraminetas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Herramientas'), ('confinado', '=', True)], default=default_herramienta_2, copy=True, store=True)
	herramienta_calor_ids = fields.One2many("requisito.permiso", "permiso_id", string="Herraminetas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Herramientas'), ('calor', '=', True)], default=default_herramienta_3, copy=True, store=True)
	herramienta_frio_ids = fields.One2many("requisito.permiso", "permiso_id", string="Herraminetas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Herramientas'), ('frio', '=', True)], default=default_herramienta_4, copy=True, store=True)
	herramienta_electrico_ids = fields.One2many("requisito.permiso", "permiso_id", string="Herraminetas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Herramientas'), ('electrico', '=', True)], default=default_herramienta_5, copy=True, store=True)

	cerramiento_altura_ids = fields.One2many("requisito.permiso", "permiso_id", string="Cerramiento de Aberturas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('altura', '=', True)], default=default_cerramiento_1, copy=True, store=True)
	cerramiento_confinado_ids = fields.One2many("requisito.permiso", "permiso_id", string="Cerramiento de Aberturas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('confinado', '=', True)], default=default_cerramiento_2, copy=True, store=True)
	cerramiento_calor_ids = fields.One2many("requisito.permiso", "permiso_id", string="Cerramiento de Aberturas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('calor', '=', True)], default=default_cerramiento_3, copy=True, store=True)
	cerramiento_frio_ids = fields.One2many("requisito.permiso", "permiso_id", string="Cerramiento de Aberturas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('frio', '=', True)], default=default_cerramiento_4, copy=True, store=True)
	cerramiento_electrico_ids = fields.One2many("requisito.permiso", "permiso_id", string="Cerramiento de Aberturas", domain=[
		'&', ('tipo_requi_id.name', '=', 'Cerramiento de Aberturas'), ('electrico', '=', True)], default=default_cerramiento_5, copy=True, store=True)

	seguridad_altura_ids = fields.One2many("requisito.permiso", "permiso_id", string="Condiciones de Seguridad", domain=[
		'&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('altura', '=', True)], default=default_seguridad_1, copy=True, store=True)
	seguridad_confinado_ids = fields.One2many("requisito.permiso", "permiso_id", string="Condiciones de Seguridad", domain=[
		'&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('confinado', '=', True)], default=default_seguridad_2, copy=True, store=True)
	seguridad_calor_ids = fields.One2many("requisito.permiso", "permiso_id", string="Condiciones de Seguridad", domain=[
		'&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('calor', '=', True)], default=default_seguridad_3, copy=True, store=True)
	seguridad_frio_ids = fields.One2many("requisito.permiso", "permiso_id", string="Condiciones de Seguridad", domain=[
		'&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('frio', '=', True)], default=default_seguridad_4, copy=True, store=True)
	seguridad_electrico_ids = fields.One2many("requisito.permiso", "permiso_id", string="Condiciones de Seguridad", domain=[
		'&', ('tipo_requi_id.name', '=', 'Condiciones de Seguridad'), ('electrico', '=', True)], default=default_seguridad_5, copy=True, store=True)

	preparacion_altura_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Preparación'), ('altura', '=', True)], default=default_preparacion_1, copy=True)
	preparacion_confinado_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Preparación'), ('confinado', '=', True)], default=default_preparacion_2, copy=True)
	preparacion_calor_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Preparación'), ('calor', '=', True)], default=default_preparacion_3, copy=True)
	preparacion_frio_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Preparación'), ('frio', '=', True)], default=default_preparacion_4, copy=True)
	preparacion_electrico_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Preparación'), ('electrico', '=', True)], default=default_preparacion_5, copy=True)

	otras_altura_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Otras Condiciones'), ('altura', '=', True)],copy=True)
	otras_confinado_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Otras Condiciones'), ('confinado', '=', True)], copy=True)
	otras_calor_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Otras Condiciones'), ('calor', '=', True)], copy=True)
	otras_frio_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Otras Condiciones'), ('frio', '=', True)], copy=True)
	otras_electrico_ids = fields.One2many("requisito.permiso", "permiso_id", string="Preparación", domain=[
		'&', ('tipo_requi_id.name', '=', 'Otras Condiciones'), ('electrico', '=', True)], copy=True)

	altura = fields.Boolean("Altura")
	confinado = fields.Boolean("Confinado")
	calor = fields.Boolean("Calor")
	frio = fields.Boolean("Frío")
	electrico = fields.Boolean("Eléctrico")
	sede = fields.Many2one('sede.sede', string=u'Sede')


class TipoPermiso(models.Model):
	_name = "tipo.permiso"

	name = fields.Char("Tipo de Permiso")
	descripcion = fields.Char("Descripción")
	active = fields.Boolean("Estado", default=True)
	icono = fields.Binary("Icono")
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)
	tipos = fields.One2many("requisito.requisito", "tipo_permiso_id", string="Tipo permiso", copy=True)


	altura = fields.Boolean("Altura", default=False)
	confinado = fields.Boolean("Confinado", default=False)
	calor = fields.Boolean("Calor", default=False)
	frio = fields.Boolean("Frío", default=False)
	electrico = fields.Boolean("Eléctrico", default=False)


class Area(models.Model):
	_name = "area.area"

	name = fields.Char("Área")
	descripcion = fields.Char("Descripción")
	sub_area_ids = fields.One2many("sub.area", "area_id", string="Sub Áreas")
	active = fields.Boolean("Estado", default=True)
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)
	sede_id = fields.Many2one("sede.sede", string="Sede")


class SubArea(models.Model):
	_name = "sub.area"

	name = fields.Char("Sub Área")
	descripcion = fields.Char("Descripción")
	area_id = fields.Many2one("area.area", string="Área")
	active = fields.Boolean("Estado", default=True)
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)


class Empresa(models.Model):
	_name = "empresa.empresa"

	name = fields.Char("Empresa")
	logo = fields.Binary("Logo")
	razon_social = fields.Char("Razón Social")
	ruc = fields.Char("RUC")
	correo = fields.Char("Correo Principal")
	telefono = fields.Char("Telefono")
	active = fields.Boolean("Estado", default=True)
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)


class PermisoTrabajador(models.Model):
	_name = "permiso.trabajador"

	name = fields.Char("Nombre")
	permiso_id = fields.Many2one("permiso.trabajo", string="Permiso")
	dni = fields.Char("DNI", compute="_compute_trabajador", store=True)
	trabajador_id = fields.Many2one(
		"trabajador.trabajador", string="Trabajador")
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)


class Trabajador(models.Model):
	_name = "trabajador.trabajador"

	foto = fields.Binary("Foto")
	name = fields.Char("Nombres")
	dni = fields.Char("DNI")
	correo = fields.Char("Correo")
	telefono = fields.Char("Telefono")
	codigo = fields.Char("Codigo")
	puesto = fields.Char("Puesto")
	tipo = fields.Selection(selection=[('1', 'Planilla'), ('2', 'Locacion de Servicios')], index=True, string="Tipo de trabajador")
	active = fields.Boolean("Estado", default=True)
	empresa_id = fields.Many2one("empresa.empresa", string="Empresa")
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)

	@api.model
	def default_requisitos(self):
		seguridads_ids = self.env["requisito.estandar"].search([])
		return [(0, 0, {'name': i.name}) for i in seguridads_ids]

	requisito_ids = fields.One2many("requisito.trabajador", "trabajador_id", string="Requisitos",default=default_requisitos)
	aptitud = fields.Selection(selection=[('1', 'Apto'), ('2', 'No Apto')], index=True, string="Aptitud",compute="_compute_aptitud",store=True)

	@api.depends("requisito_ids")
	def _compute_aptitud(self):
		for record in self:
			record.aptitud = '1'
			for line in record.requisito_ids:
				if not line.cumple:
					record.aptitud = '2'

class Contratista(models.Model):
	_name = "contratista.contratista"

	name = fields.Char("Nombre")
	empresa_id = fields.Many2one("empresa.empresa", string="Empresa")
	empleados_ids = fields.One2many("trabajador.contratista", "contratisa_id", string="Empresas")

class TrabajadorConstratista(models.Model):
	_name = "trabajador.contratista"

	name = fields.Char("Nombres y Apellido")
	dni = fields.Char("DNI")
	correo = fields.Char("Correo")
	telefono = fields.Char("Telefono")
	puesto = fields.Char("Puesto")
	contratisa_id = fields.Many2one("contratista.contratista", string="Constratista")

class Requisitos(models.Model):
	_name = "requisito.requisito"

	name = fields.Char("Requisito",translate=True)
	descripcion = fields.Char("Descripción")
	image = fields.Binary("Icono")
	active = fields.Boolean("Estado", default=True)
	check = fields.Boolean("Check")
	permiso_id = fields.Many2one("permiso.trabajo", string="Permiso")
	tipo_permiso_id = fields.Many2one("tipo.permiso", string="Tipo de Permiso")
	tipo_requi_id = fields.Many2one(
		"tipo.requisito", string="Tipo de Requisito")

	altura = fields.Boolean("Altura")
	confinado = fields.Boolean("Confinado")
	calor = fields.Boolean("Calor")
	frio = fields.Boolean("Frío")
	electrico = fields.Boolean("Eléctrico")
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)

	@api.onchange("tipo_permiso_id")
	def cambio_modificacion(self):
		for line in self:
			value = dict()
			value.update({'altura': False})
			value.update({'confinado': False})
			value.update({'calor': False})
			value.update({'frio': False})
			value.update({'electrico': False})
			if line.name == u'Trabajo en Altura':
				value['altura'] = True
			if line.name == u'Trabajo en Espacios Confinados':
				value['confinado'] = True
			if line.name == u'Trabajo en Caliente':
				value['calor'] = True
			if line.name == u'Trabajo en Frío':
				value['frio'] = True
			if line.name == u'Trabajo Eléctricos':
				value['electrico'] = True
		return {'value': value}

class RequisitosTransient(models.TransientModel):
	_name = 'requisito.requisito.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["requisito.requisito"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class TipoRequisito(models.Model):
	_name = "tipo.requisito"

	name = fields.Char("Tipo de Requisito")
	descripcion = fields.Char("Descripción")
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)


class RequsitoPermiso(models.Model):
	_name = "requisito.permiso"

	name = fields.Char("Nombre")
	permiso_id = fields.Many2one("permiso.trabajo", string="Permiso")
	requisito_id = fields.Many2one("requisito.requisito", string="Requisito")
	tipo_requi_id = fields.Many2one(
		"tipo.requisito", string="Tipo de Requisito")
	image = fields.Binary("Icono", related="requisito_id.image")
	check = fields.Boolean("Check")
	tipo_permiso_id = fields.Many2one("tipo.permiso", string="Tipo de Permiso")

	altura = fields.Boolean("Altura")
	confinado = fields.Boolean("Confinado")
	calor = fields.Boolean("Calor")
	frio = fields.Boolean("Frío")
	electrico = fields.Boolean("Eléctrico")
	company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)


class User(models.Model):
	_inherit = "res.users"

	empresa_id = fields.Many2one("empresa.empresa", string="Empresa")


class PermisoCreateLine(models.TransientModel):
	_name = 'permiso.create.line'

	def crear_empresa_usuario(self,nombre, ruc,correo, telefono):
		permiso_line = self.env["empresa.empresa"].create({'name':nombre,'ruc':ruc,'correo':correo,'telefono':telefono})
		usuario =  self.env.user
		usuario.empresa_id = permiso_line.id

	def limites_permisos(self,plan_id):
		permiso_line = self.env["permiso.trabajo"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			return True
		else:
			return False

	def gruardar_permiso(self, value, permiso_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.altura = True

	def solicitar_permiso(self, permiso_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'estado': '2'})

	def cancelar_permiso(self, permiso_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'estado': '7'})

	def autorizar_permiso(self, permiso_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'estado': '3'})

	def aprobar_permiso(self, permiso_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'estado': '4'})

	def guardar_area(self, permiso_id, area_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'area': area_id})
		return "listo"

	def guardar_contratista(self, permiso_id, contratista_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'contratista_id': contratista_id})
		return "listo"

	def guardar_sub_area(self, permiso_id, sub_area_id):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'sub_area': sub_area_id})
		return "listo"

	def guardar_solicitante(self, permiso_id, usuario_id):
		permiso_line = self.env["permiso.trabajo"].sudo().search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.sudo().write({'solicitante_id': usuario_id})
		usuario = self.env["res.users"].sudo().search(
			[('id', '=', usuario_id)], limit=1)
		src = ""
		if usuario.signature_binary:
			src = "data:image/png;base64, "+str(usuario.signature_binary)[2:-1]
		return src

	def guardar_autorizador(self, permiso_id, usuario_id):
		permiso_line = self.env["permiso.trabajo"].sudo().search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.sudo().write({'autorizador_id': usuario_id})
		usuario = self.env["res.users"].sudo().search(
			[('id', '=', usuario_id)], limit=1)
		src = ""
		if usuario.signature_binary:
			src = "data:image/png;base64, "+str(usuario.signature_binary)[2:-1]
		return src

	def guardar_aprobador(self, permiso_id, usuario_id):
		permiso_line = self.env["permiso.trabajo"].sudo().search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.sudo().write({'aprobador_id': usuario_id})
		usuario = self.env["res.users"].sudo().search(
			[('id', '=', usuario_id)], limit=1)
		src = ""
		if usuario.signature_binary:
			src = "data:image/png;base64, "+str(usuario.signature_binary)[2:-1]
		return src

	def guardar_ubicacion(self, permiso_id, ubicacion):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'ubicacion_exacta': ubicacion})
		return "listo"

	def nuevo_trabajador(self, permiso_id, nuevo_trabajador):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		trabajador_id = self.env["trabajador.trabajador"].search(
			[('id', '=', nuevo_trabajador)], limit=1)
		permiso_line.empleados_ids.create(
			{'trabajador_id': trabajador_id.id, 'permiso_id': permiso_id})

		return "listo"

	def funcion_observacion_aprobar(self, permiso_id, value):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'estado': '6'})
		permiso_line.write({'observacion_apro': value})

		return "listo"

	def funcion_observacion_autorizar(self, permiso_id, value):
		permiso_line = self.env["permiso.trabajo"].search(
			[('id', '=', permiso_id)], limit=1)
		permiso_line.write({'estado': '6'})
		permiso_line.write({'observacion_auto': value})

		return "listo"

	def nuevo_requisito(self, permiso_id, tipo_requi_id,tipo_permiso_id,name):
		obj_tipo_requi_id = self.env["tipo.requisito"].search(
			[('name', '=', tipo_requi_id)], limit=1)
		lineaedit = self.env["requisito.permiso"].create({"permiso_id":permiso_id,"{}".format(tipo_permiso_id):True,"tipo_requi_id":obj_tipo_requi_id.id,"name":name})

	def get_data(self,fecha_desde=False,fecha_hasta=False):
		domain = [('empresa_id',  '=', self.env.user.empresa_id.id)]
		domain += [('create_date', '>', fecha_desde), ('create_date', '<=', fecha_hasta)]
		permisos = self.env["permiso.trabajo"].search(domain)
		contador_borrador = 0
		contador_solicitado = 0
		contador_autorizado = 0
		contador_aprobado = 0
		contador_cerrado = 0
		contador_observado = 0
		contador_cancelado = 0

		for permiso in permisos:
			if permiso.estado == "1":
				contador_borrador += 1
			elif permiso.estado == "2":
				contador_solicitado += 1
			elif permiso.estado == "3":
				contador_autorizado += 1
			elif permiso.estado == "4":
				contador_aprobado += 1
			elif permiso.estado == "5":
				contador_cerrado += 1
			elif permiso.estado == "6":
				contador_observado += 1
			elif permiso.estado == "7":
				contador_cancelado += 1

		data_graph = [contador_borrador,contador_solicitado,contador_autorizado,contador_aprobado,contador_cerrado,contador_observado,contador_cancelado]
		return data_graph


	def get_data_plantilla(self,fecha_desde=False,fecha_hasta=False):
		domain = [('empresa_id',  '=', self.env.user.empresa_id.id)]
		domain += [('create_date', '>', fecha_desde), ('create_date', '<=', fecha_hasta)]
		permisos = self.env["permiso.trabajo"].search(domain)
		contador_altura = 0
		contador_confinado = 0
		contador_caliente = 0
		contador_frio = 0
		contador_electricos = 0

		for permiso in permisos:
			if permiso.plantilla.name == "Trabajo en Altura":
				contador_altura += 1
			elif permiso.plantilla.name == "Trabajo en Espacios Confinados":
				contador_confinado += 1
			elif permiso.plantilla.name == "Trabajo en Caliente":
				contador_caliente += 1
			elif permiso.plantilla.name == "Trabajo en Frío":
				contador_frio += 1
			elif permiso.plantilla.name == "Trabajo Eléctricos":
				contador_electricos += 1

		data_graph = [contador_altura,contador_confinado,contador_caliente,contador_frio,contador_electricos]
		return data_graph

	def get_data_table(self,fecha_desde=False,fecha_hasta=False):
		domain = [('empresa_id',  '=', self.env.user.empresa_id.id)]
		domain += [('create_date', '>', fecha_desde), ('create_date', '<=', fecha_hasta)]
		permisos = self.env["permiso.trabajo"].search(domain)

		matriz = []
		for permiso in permisos:
			matriz.append([permiso.id,permiso.sequence,permiso.estado])

		return matriz


class UserTransient(models.TransientModel):
	_name = 'user.transient'

	def limites_permisos(self):
		permiso_line = self.env["res.users"].search([('parent_id', '=',  self.env.user.id)])

		if len(permiso_line) < 11:
			return True
		else:
			return False

class Sede(models.Model):
	_name = 'sede.sede'

	name = fields.Char(u'Sede')
	encargado = fields.Many2one("res.users", string="Encargado")
	dni = fields.Char(u'DNI')
	puesto = fields.Char(u'Puesto')
	trabajadores = fields.Integer(u'Numero de trabajadores')
	empresa_id = fields.Many2one("empresa.empresa", string="Empresa")
	area_ids = fields.One2many("area.area", "sede_id", string=" Áreas")

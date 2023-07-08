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
import io  # noqa
from xlwt import easyxf, Workbook  # noqa
from xlwt import Formula  # noqa
from PIL import Image  # noqa
_logger = logging.getLogger(__name__)

import io,binascii,tempfile
from odoo.exceptions import UserError, ValidationError, Warning

try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlrd
except ImportError:
	_logger.debug('Cannot `import xlrd`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')

class TrabajadorConstratista(models.Model):
	_inherit = "trabajador.contratista"


	@api.model
	def default_requisitos(self):
		seguridads_ids = self.env["requisito.estandar"].search([])
		return [(0, 0, {'name': i.name}) for i in seguridads_ids]

	requisito_ids = fields.One2many("requisito.trabajador", "trabajador_contratista_id", string="Requisitos",default=default_requisitos)
	aptitud = fields.Selection(selection=[('1', 'Apto'), ('2', 'No Apto')], index=True, string="Aptitud",compute="_compute_aptitud",store=True)

	@api.depends("requisito_ids")
	def _compute_aptitud(self):
		for record in self:
			record.aptitud = '1'
			for line in record.requisito_ids:
				if not line.cumple:
					record.aptitud = '2'


class UserTransient(models.TransientModel):
	_inherit = 'user.transient'

	def create_users(self,values):
		groups = []

		if not values['name']:
			raise Warning(_("Ingresa el nombre"))
		if not values['dni']:
			raise Warning(_("Ingresa el dni"))
		if not values['correo']:
			raise Warning(_("Ingresa el correo"))
		if not values['codigo']:
			raise Warning(_("Ingresa el codigo"))
		if not (values['tipo'] == 'Planilla' or  values['tipo'] == 'Locación de Servicios'):
			raise Warning(_("Ingresa el tipo de trabajor correctamente"))
		if values['tipo'] == 'Planilla' or values['tipo'] == 'planilla':
			values['tipo'] = '1'
		if values['tipo'] == 'Locacion de Servicios' or values['tipo'] == 'Locación de Servicios':
			values['tipo'] = '2'

		trabajor = self.env['trabajador.trabajador'].sudo().create({
			'name':values['name'],
			'dni':values['dni'],
			'correo':values['correo'],
			'telefono':values['telefono'],
			'codigo':values['codigo'],
			'puesto':values['puesto'],
			'tipo':values['tipo'],
			'empresa_id':values['empresa_id'],
			})

		return trabajor

	def import_user(self,file_imput):
		_logger.info("line[1]")
		xlsfile = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
		xlsfile.write(binascii.a2b_base64(file_imput["file_imput"]))
		xlsfile.seek(0)
		workbook = xlrd.open_workbook(xlsfile.name)
		sheet = workbook.sheet_by_index(0)


		for row_no in range(sheet.nrows):
			if row_no > 0:
				line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
				vals = {
					'name':str(line[0]) ,
					'dni':str(line[1]),
					'correo':str(line[2]),
					'telefono':str(line[3]),
					'codigo':str(line[4]),
					'puesto':str(line[5]),
					'tipo':str(line[6]),
					'empresa_id':self.env.user.empresa_id.id,

				}
				rec = self.create_users(vals)
				if not rec:
					raise Warning(_("Trabajador %s no creado!" %line[0]))
		return True


	def create_users_contratista(self,values):
		groups = []

		if not values['name']:
			raise Warning(_("Ingresa el nombre"))
		if not values['dni']:
			raise Warning(_("Ingresa el dni"))
		if not values['correo']:
			raise Warning(_("Ingresa el correo"))

		trabajor = self.env['trabajador.contratista'].sudo().create({
			'name':values['name'],
			'dni':values['dni'],
			'correo':values['correo'],
			'telefono':values['telefono'],
			'puesto':values['puesto'],
			'contratisa_id':values['contratisa_id'],
			})
		return trabajor

	def import_user_contratista(self,file_imput,contratisa_id):
		_logger.info("line[1]")
		xlsfile = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
		xlsfile.write(binascii.a2b_base64(file_imput["file_imput"]))
		xlsfile.seek(0)
		workbook = xlrd.open_workbook(xlsfile.name)
		sheet = workbook.sheet_by_index(0)


		for row_no in range(sheet.nrows):
			if row_no > 0:
				line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
				vals = {
					'name':str(line[0]) ,
					'dni':str(line[1]),
					'correo':str(line[2]),
					'telefono':str(line[3]),
					'puesto':str(line[4]),
					'contratisa_id':int(contratisa_id),

				}
				rec = self.create_users_contratista(vals)
				if not rec:
					raise Warning(_("Trabajador %s no creado!" %line[0]))
		return True


	def create_requisito(self,values):
		groups = []

		if not values['name']:
			raise Warning(_("Ingresa el nombre"))

		trabajor = self.env['requisito.estandar'].sudo().create({
			'name':values['name'],
			})
		return trabajor

	def import_requisito(self,file_imput):
		_logger.info("line[1]")
		xlsfile = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
		xlsfile.write(binascii.a2b_base64(file_imput["file_imput"]))
		xlsfile.seek(0)
		workbook = xlrd.open_workbook(xlsfile.name)
		sheet = workbook.sheet_by_index(0)


		for row_no in range(sheet.nrows):
			if row_no > 0:
				line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
				vals = {
					'name':str(line[0]) ,
				}
				rec = self.create_requisito(vals)
				if not rec:
					raise Warning(_("Trabajador %s no creado!" %line[0]))
		return True

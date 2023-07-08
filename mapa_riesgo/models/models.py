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

class MapaRiesgo(models.Model):
	_name= "mapa.riesgo"

	name = fields.Char(string="Nombre")
	width_img = fields.Char(string="Nombre")
	height_img = fields.Char(string="Nombre")
	mapa_json = fields.Text(string="Save Json from Canvas")
	have_map = fields.Boolean(string="Tiene mapa de riesgos ?")
	imagen = fields.Binary(string=u'Imagen')


class EditMapaRiesgo(models.TransientModel):
	_name = 'edit.mapa.riesgo'

	@profile
	def limites_permisos(self,plan_id):
		permiso_line = self.env["mapa.riesgo"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		_logger.info("DDDDDDDDDDDDDDDDDDDDDDD")
		_logger.info(plan.limite_registro)
		_logger.info(len(permiso_line))
		_logger.info(plan)
		_logger.info(plan_id)
		if len(permiso_line) < plan.limite_registro:
			_logger.info(plan.limite_registro)
			_logger.info("bbbbbbbbbbbbbbbbbbbbbb")
			return True
		else:
			_logger.info("cccccccccccccccccccc")
			return False

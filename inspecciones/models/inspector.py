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



#plantilla de formato de inspectores
class Inspector(models.Model):
	_name= "inspector"

	name = fields.Char(string="Nombre")
    
class InspectorInspeccion(models.Model):
	_name= "inspector.inspeccion"

	name = fields.Char(string="Nombre",related="inspector_id.name")
	inspeccion_id = fields.Many2one("inspeccion",string="Inspeccion")
	inspector_id = fields.Many2one("inspector",string="inspector")

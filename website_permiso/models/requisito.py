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



class RequisitoTrabajador(models.Model):
	_name = "requisito.trabajador"

	name = fields.Char("Nombre")
	cumple = fields.Boolean("Cumple?",default=False)
	trabajador_id = fields.Many2one("trabajador.trabajador", string="Trabajador")
	trabajador_contratista_id = fields.Many2one("trabajador.contratista", string="Trabajador")

class RequisitoEstandar(models.Model):
	_name = "requisito.estandar"

	name = fields.Char("Nombre")
	tipo = fields.Selection(selection=[('general', 'general'), ('personal', 'personal')], index=True, string="Tipo de requisito")

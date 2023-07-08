# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, content_disposition
import datetime
from datetime import datetime,  timedelta, date
import pytz
import re
import logging
_logger = logging.getLogger(__name__)


class Main(http.Controller):

	"""
	type:  http | json
	"""

	@http.route("/psicosocial-prueba", type="http", method=["GET", "POST"], auth="public", csrf=False, website=True)
	def principal(self):
		registros = request.env["evaluacion.psicosocial.multi"].sudo().search([('id','=', 1)])
		return request.render("psicosocial_multi.form_psicosocial", {"registro": registros[0]})

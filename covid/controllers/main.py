# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import datetime
from datetime import datetime,  timedelta


class Main(http.Controller):

	"""
	type:  http | json
	"""

	@http.route("/covid_anexo_4", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registro(self):
		registros = request.env["covid.4"].sudo().search([('create_uid','=', request.env.uid)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("covid_4.list_covid_4", {"registros": registros,"plan":plan})

	@http.route("/covid_anexo_4/<model('covid.4'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros(self,registro):
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("covid_4.form_covid_4", {"registro": registro,"plan":plan})

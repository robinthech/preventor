from odoo import http
from odoo.http import request
import datetime

from datetime import datetime,  timedelta,date


class Main(http.Controller):

	@http.route("/lista_covid", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def lista_vigilancia_covid(self):
		hoy = date.today()
		fecha_actual= hoy.strftime("%Y-%m-%d")
		empresa = request.env.user.empresa_id
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 1)])
		registros = request.env["covid.anexo"].sudo().search([('create_uid',  '=', request.env.user.id)])
		return request.render("lista_covid.lista_vigilancia_covid",{"registros":registros,"empresa":empresa,"fecha_actual":fecha_actual,"plan":plan})

	@http.route("/lista_covid/<model('covid.anexo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def form_vigilancia_covid(self,registro):
		return request.render("lista_covid.lista_covid_form",{"registro":registro})

	@http.route("/lista_covid/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def vigilancia_covid_guia(self):
		producto = request.env["product.template"].sudo().search([('id',  '=', 1)])
		adjuntos = producto.solve_file_ids
		for line in adjuntos:
			line.public = True
		return request.render("lista_covid.lista_covid_guia", {"producto": producto})

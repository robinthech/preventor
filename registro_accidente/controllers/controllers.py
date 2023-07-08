from odoo import http
from odoo.http import request
import datetime

from datetime import datetime,  timedelta,date


class Main(http.Controller):

	@http.route("/accidentes", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def accidentes(self):
		hoy = date.today()
		fecha_actual= hoy.strftime("%Y-%m-%d")
		empresa = request.env.user.empresa_id
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 3)])
		registros = request.env["registro.accidente"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		return request.render("registro_accidente.lista_accidentes",{"registros":registros,"empresa":empresa,"fecha_actual":fecha_actual,"plan":plan})

	@http.route("/accidentes/<model('registro.accidente'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def accidente(self,registro):
		usuarios = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])
		return request.render("registro_accidente.lista_accidentes_form",{"registro":registro,"usuarios":usuarios})

	@http.route("/accidentes/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def accidente_guia(self):
		producto = request.env["product.template"].sudo().search([('id',  '=', 3)])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if(producto.solve_file_ids[0].id):
			pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("registro_accidente.list_accidentes_guia", {"producto": producto,"pdf":pdf})


	@http.route("/accidentes/reportes", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def accidentes_reportes(self):
		empresa = request.env.user.empresa_id

		return request.render("registro_accidente.report_accidentes",{"empresa":empresa})

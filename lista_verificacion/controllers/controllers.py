from odoo import http,fields
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import Website
import datetime
from datetime import datetime,  timedelta, date
import logging
import xlsxwriter
_logger = logging.getLogger(__name__)

class ListaVerificacion(http.Controller):

	@http.route('/lista-verificacion', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def index(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		# para ello hacer inherit en lista.verificacion el campo sede y campo empresa
		# if usuario es principal filtrar por empresa
		verificaciones = request.env["lista.verificacion"].sudo().search([('create_uid',  '=', request.env.user.id)])
		# if usuario es secundario filtrar por sede
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 4)])
		return request.render('lista_verificacion.lista_verificacion', {"fecha_actual":fecha_actual,"verificaciones":verificaciones,"plan":plan,"grupos":grupos})


	@http.route('/lista-verificacion/<model("lista.verificacion"):verificacion>', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def lista_verificacion(self,verificacion):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		return request.render('lista_verificacion.formulario', {"fecha_actual":fecha_actual,"verificacion":verificacion})

	@http.route('/lista-verificacion/success', type='http', methods=['GET', 'POST'], auth="public", website=True, csrf=False)
	def lista_success(self):
		return request.render('lista_verificacion.success')

	@http.route("/lista-verificacion/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permiso_guia(self):
		producto = request.env["product.template"].sudo().search([('id',  '=', 4)])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if(producto.solve_file_ids[0].id):
			pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("lista_verificacion.lista_verificacion_guia", {"producto": producto,"pdf":pdf})

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

class ProgramaAnual(http.Controller):

	@http.route("/programa_anual", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def programa_anual(self):
		programa_anual = request.env["programa.anual"].sudo().search([('create_uid','=', request.env.uid)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 5)])
		return request.render("programa_anual.vista", {"programa_anual": programa_anual,"plan":plan})

	@http.route("/programa_anual/<model('programa.anual'):programa_anual>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def programas_anuales(self,programa_anual):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		return request.render("programa_anual.principal", {"programa_anual": programa_anual, "fecha_actual":fecha_actual})

	@http.route('/programa_anual/success', type='http', methods=['GET', 'POST'], auth="public", website=True, csrf=False)
	def lista_success(self):
		return request.render('programa_anual.success')

	@http.route("/programa-anual/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def accidente_guia(self):
		producto = request.env["product.template"].sudo().search([('id',  '=', 5)])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if(producto.solve_file_ids[0].id):
			pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("programa_anual.programa_anual_guia", {"producto": producto,"pdf":pdf})

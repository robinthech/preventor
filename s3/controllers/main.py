# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import datetime
from datetime import datetime,  timedelta
import logging
import pytz
import xlsxwriter
_logger = logging.getLogger(__name__)

class Main(http.Controller):

	"""
	type:  http | json
	"""

	@http.route("/registros", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registro(self):
		registros = request.env["registro.monitoreo"].sudo().search([('create_uid','=', request.env.uid)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.list_registros", {"registros": registros,"plan":plan})

	@http.route("/registros/<model('registro.monitoreo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros(self,registro):
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		permiso_line = request.env["registro.monitoreo"].search([('create_uid', '=',  request.env.user.id),('id', '=',  registro.id)])
		return request.render("s3.form_registros", {"registro": registro,"plan":plan,"total_puntos":len(permiso_line.iluminacion_ids)+len(permiso_line.dosimetria_ids)})

	@http.route("/registros/ilu/<model('registro.monitoreo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros_ilu(self,registro):
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.form_ilu", {"registro": registro,"plan":plan})

	@http.route("/registros/dosi/<model('registro.monitoreo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros_dosi(self,registro):
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.form_dosi", {"registro": registro,"plan":plan})

	@http.route("/registros/sono/<model('registro.monitoreo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros_sono(self,registro):
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.form_sono", {"registro": registro,"plan":plan})

	@http.route("/registros/reba/<model('registro.monitoreo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros_reba(self,registro):
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.list_reba", {"registro": registro,"plan":plan})

	@http.route("/registros/reba/form/<model('reba.reba'):reba>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros_reba_form(self,reba):
		registro = request.env["registro.monitoreo"].sudo().search([('id',  '=', reba.riesgo_disergonomico_id.registro_id.id)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.form_reba", {"registro": registro,"reba": reba,"plan":plan,"model":"reba.reba"})

	@http.route("/registros/rosa/<model('registro.monitoreo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros_rosa(self,registro):
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.list_rosa", {"registro": registro,"plan":plan})

	@http.route("/registros/rosa/form/<model('rosa.rosa'):rosa>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros_rosa_form(self,rosa):
		registro = request.env["registro.monitoreo"].sudo().search([('id',  '=', rosa.riesgo_disergonomico_id.registro_id.id)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		return request.render("s3.form_rosa", {"registro": registro,"rosa": rosa,"plan":plan,"model":"rosa.rosa"})





	@http.route("/registros/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def accidente_guia(self):
		producto = request.env["product.template"].sudo().search([('id',  '=', 2)])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if(producto.solve_file_ids[0].id):
			pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("s3.registros_guia", {"producto": producto,"pdf":pdf})


	#guardar reba

	@http.route("/guardar_field_odoo",auth='user', type = 'json')
	def guardar_field_odoo(self,inputs,model,record_id,**kw):
		lineaedit = request.env["{}".format(model)].search([('id', '=', record_id)], limit=1)
		for line in inputs:
			lineaedit.write({'{}'.format(line["name"]): line["value"]})
		return True

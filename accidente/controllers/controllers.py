from odoo import http,fields
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import Website
import datetime
from datetime import datetime,  timedelta, date
import logging
import xlsxwriter
import pytz
_logger = logging.getLogger(__name__)

class ListaVerificacion(http.Controller):

	@http.route('/registro-accidente', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def index(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		verificaciones = request.env["registro.accidente.final"].sudo().search([('create_uid',  '=', request.env.user.id)])
		return request.render('accidente.registro_accidente', {"fecha_actual":fecha_actual,"verificaciones":verificaciones})

	@http.route('/registro-accidente/configuracion', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def responsable(self):
		responsables = request.env["accidente.responsable"].sudo().search([])
		return request.render('accidente.configuracion_registro_accidente', {"responsables":responsables})

	@http.route('/registro-accidente/success', type='http', methods=['GET', 'POST'], auth="public", website=True, csrf=False)
	def lista_success(self):
		return request.render('accidente.success')

	@http.route('/registro-accidente/<model("registro.accidente.final"):accidente>', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def accidente(self,accidente):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		responsables = request.env["accidente.responsable"].sudo().search([])
		usuarios = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])
		
		if accidente.fecha_accidente:
			fecha_dia = accidente.fecha_accidente.strftime("%Y-%m-%d")
			fecha_hora = accidente.fecha_accidente.strftime("%H:%M:%S")
			fecha_accidente = fecha_dia+'T'+fecha_hora
		else:
			today = datetime.now(pytz.timezone('America/Lima'))
			today_dia = today.strftime("%Y-%m-%d")
			today_hora = today.strftime("%H:%M:%S")
			fecha_accidente = today_dia+'T'+today_hora

		return request.render('accidente.formulario_accidente', {"fecha_actual":fecha_actual,"accidente":accidente,"fecha_accidente":fecha_accidente,"responsables":responsables,"usuarios":usuarios})

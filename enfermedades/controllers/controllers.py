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

class RegistroIncidente(http.Controller):

	@http.route('/enfermedades-ocupacionales', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def index(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		verificaciones = request.env["enfermedades.ocupacionales"].sudo().search([('create_uid',  '=', request.env.user.id)])
		return request.render('enfermedades.registro_incidente', {"fecha_actual":fecha_actual,"verificaciones":verificaciones})

	@http.route(["/enfermedades/configuracion"],type="json",auth="public",method=["POST"],website=True)
	def Tipopeligro(self,name):
		type = request.env["tipo.agente"].sudo().search([('agente',  '=', name)])

		datos = [{	"id":p.id,
					"agente":p.agente,
					"name":p.name
					}for p in type]

		return datos

	@http.route('/enfermedades-ocupacionales/configuracion', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def responsable(self):
		responsables = request.env["enfermedades.responsable"].sudo().search([])
		return request.render('enfermedades.configuracion_registro_incidente', {"responsables":responsables})

	@http.route('/enfermedades-ocupacionales/<model("enfermedades.ocupacionales"):accidente>', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def accidente(self,accidente):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		responsables = request.env["enfermedades.responsable"].sudo().search([])
		tipos = request.env["tipo.agente"].sudo().search([])
		if accidente.fecha_accidente:
			fecha_dia = accidente.fecha_accidente.strftime("%Y-%m-%d")
			fecha_hora = accidente.fecha_accidente.strftime("%H:%M:%S")
			fecha_accidente = fecha_dia+'T'+fecha_hora
		else:
			today = datetime.now(pytz.timezone('America/Lima'))
			today_dia = today.strftime("%Y-%m-%d")
			today_hora = today.strftime("%H:%M:%S")
			fecha_accidente = today_dia+'T'+today_hora

		return request.render('enfermedades.formulario_accidente', {"fecha_actual":fecha_actual,"incidente":accidente,"fecha_accidente":fecha_accidente,"responsables":responsables,"tipos":tipos})

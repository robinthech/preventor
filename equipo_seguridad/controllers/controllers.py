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

class EquipoSeguridadLista(http.Controller):

	@http.route('/equipos-seguridad', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def index(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		verificaciones = request.env["equipos.seguridad"].sudo().search([('create_uid',  '=', request.env.user.id)])
		return request.render('equipo_seguridad.registro_incidente', {"fecha_actual":fecha_actual,"verificaciones":verificaciones})

	@http.route('/equipos-seguridad/<model("equipos.seguridad"):accidente>', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def accidente(self,accidente):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		responsables = request.env["seguridad.responsable"].sudo().search([])
		trabajadores = request.env["equipo.trabajadores.trabajadores"].sudo().search([])
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

		return request.render('equipo_seguridad.formulario_accidente', {"fecha_actual":fecha_actual,"incidente":accidente,"fecha_accidente":fecha_accidente,"responsables":responsables,"tipos":tipos,"trabajadores":trabajadores})

	@http.route('/equipos-seguridad/configuracion', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def responsable(self):
		responsables = request.env["equipo.trabajadores.trabajadores"].sudo().search([])
		_logger.info(responsables)
		return request.render('equipo_seguridad.configuracion_registro_incidente', {"responsables":responsables})

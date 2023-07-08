from odoo import http
from odoo.http import request, content_disposition
import datetime
from datetime import datetime,  timedelta, date
from dateutil.relativedelta import relativedelta
import logging
import pytz
import re
_logger = logging.getLogger(__name__)


class Main(http.Controller):

	"""
	type:  http | json
	"""
	@http.route("/trabajador_contratista/requisitos/<model('trabajador.contratista'):trabajador>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def trabajador_contratista_requisitos(self,trabajador):
		usuario = request.env["res.users"].sudo().search(
			[('id',  '=', request.env.user.id)])
		return request.render("website_permiso.form_trabajador_requisitos_contratista",{"trabajador": trabajador,"usuario":usuario})


	@http.route("/guardar_field_odoo_requisito_contratista",auth='user', type = 'json')
	def guardar_field_odoo_requisito_contratista(self,inputs,model,record_id,**kw):
		trabajador = request.env["trabajador.contratista"].search([('id', '=', record_id)], limit=1)
		aptitud = '1'
		for line in inputs:
			lineaedit = request.env["{}".format(model)].search([('id', '=', line["id"])], limit=1)
			lineaedit.write({'{}'.format(line["name"]): line["value"]})
			if not line["value"]:
				aptitud = '2'
		trabajador.write({'aptitud': aptitud})

		return True

	@http.route("/gestion-requisitos", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def gestion_requisito(self):
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		requisito_ids = request.env["requisito.estandar"].sudo().search([])

		return request.render("website_permiso.requisito_estandar",{"usuario":usuario,"requisito_ids":requisito_ids})

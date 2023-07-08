from odoo import http,fields
from odoo.http import request, content_disposition
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import Website
import datetime
from datetime import datetime,  timedelta, date
import logging
import re
import xlsxwriter
_logger = logging.getLogger(__name__)

class MapaRiesgos(http.Controller):


	@http.route('/mapa_riesgo_list', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def mapa_riesgo_list(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		empresa = request.env.user.empresa_id
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		registros = request.env["mapa.riesgo"].sudo().search([('create_uid','=', request.env.uid)])
		_logger.info(plan)
		_logger.info(plan.id)
		return request.render('mapa_riesgo.lista_mapa_riesgo',{"registros":registros,"empresa":empresa,"fecha_actual":fecha_actual,"plan":plan})


	@http.route("/mapa_riesgo_canva/<model('mapa.riesgo'):registro>", type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def mapa_riesgo_canva(self,registro):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		return request.render('mapa_riesgo.template_mapa_riesgo_canva', {"registro": registro})

	@http.route("/template_mapa_riesgo_form", type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def template_mapa_riesgo_form(self):
		registro = request.env["mapa.riesgo"].sudo().search([],limit=1)
		return request.render('mapa_riesgo.template_mapa_riesgo_form', {"registro": registro})


	@http.route(['/pdf/download/mapa_riesgo/<model("mapa.riesgo"):registro>'], type='http', auth="public", website=True)
	def portal_mapa_riesgo_page(self,registro,**kw):
		return self._show_report(model=registro, report_type='pdf', report_ref='mapa_riesgo.action_report_saleorder', download=True)


	def _show_report(self, model, report_type, report_ref, download=False):
		if report_type not in ('html', 'pdf', 'text'):
			raise UserError(_("Invalid report type: %s") % report_type)

		report_sudo = request.env.ref(report_ref).sudo()
		method_name = 'render_qweb_%s' % (report_type)
		report = getattr(report_sudo, method_name)([model.id], data={'report_type': report_type})[0]
		reporthttpheaders = [
			('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
			('Content-Length', len(report)),
		]
		if report_type == 'pdf' and download:
			filename = "%s.pdf" % (re.sub('\W+', '-', 'IPERC Continuo'))
			reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
		return request.make_response(report, headers=reporthttpheaders)

# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, content_disposition
import datetime
from datetime import datetime,  timedelta, date
import pytz
import re
import logging
_logger = logging.getLogger(__name__)


class Main(http.Controller):

	"""
	type:  http | json
	"""

	@http.route("/iperc-continuo", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def principal(self):
		registros = request.env["iperc.continuo"].sudo().search([('create_uid','=', request.env.uid)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 6)])
		return request.render("iperc_continuo.list_iperc_continuo", {"registros": registros,"plan":plan})

	@http.route("/iperc-continuo/configuracion", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def configuracion(self):
		tipos = request.env["type.iperc"].sudo().search([])
		return request.render("iperc_continuo.configuracion_iperc_continuo", {"tipos": tipos})

	@http.route("/iperc-continuo/tablas", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def tablas(self):
		# tipos = request.env["type.iperc"].sudo().search([])
		return request.render("iperc_continuo.tablas_iperc_continuo")

	@http.route("/iperc-continuo/<model('iperc.continuo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros(self,registro):
		fechas = []
		for supervisor in registro.supervisor_ids:
			fecha_dia = supervisor.fecha.strftime("%Y-%m-%d")
			fecha_hora = supervisor.fecha.strftime("%H:%M:%S")
			fecha_inicio = fecha_dia+'T'+fecha_hora
			fechas.append(fecha_inicio)

		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		today_datetime = datetime.now(pytz.timezone('America/Lima'))
		today_dia = today_datetime.strftime("%Y-%m-%d")
		today_hora = today_datetime.strftime("%H:%M:%S")
		today_inicio = today_dia+'T'+today_hora

		# evaluaciones = []
		# for evaluacion in registro.evaluacion_ids:
		# 	descripcion = request.env["descripcion.iperc"].sudo().search([('descripcion_id',  '=', evaluacion.type_id.id)])
		# 	evaluaciones.append(descripcion.id)

		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		riesgos = request.env["descripcion.iperc"].sudo().search([])
		tipos = request.env["type.iperc"].sudo().search([])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 6)])
		return request.render("iperc_continuo.form_iperc_continuo", {"fecha_actual": fecha_actual,"today_inicio":today_inicio,"registro": registro,"plan":plan,'fechas': fechas,'tipos': tipos,'riesgos':riesgos})

	@http.route(["/continuo/descripcion"],type="json",auth="public",method=["POST"],website=True)
	def Tipopeligro(self,name):
		type = request.env["type.iperc"].sudo().search([('name',  '=', name)])
		evaluaciones = request.env["descripcion.iperc"].sudo().search([('descripcion_id',  '=', type.id)])

		datos = [{	"id":p.id,
					"name":p.name
					}for p in evaluaciones]

		return datos
		# sale_order_obj = request.website.sale_get_order(force_create=True)
	@http.route("/iperc-continuo/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def continuo_guia(self):
		producto = request.env["product.template"].sudo().search([('name',  '=', 'Módulo IPERC CONTINUO')])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if(producto.solve_file_ids[0].id):
			pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("iperc_continuo.iperc_continuo_guia", {"producto": producto,"pdf":pdf})

	@http.route(['/pdf/download/<model("iperc.continuo"):registro>'], type='http', auth="public", website=True)
	def portal_order_page(self,registro,**kw):
		# try:
		#     order_sudo = self._document_check_access('iperc.continuo', order_id, access_token=access_token)
		# except (AccessError, MissingError):
		#     return request.redirect('/my')

		# if report_type in ('html', 'pdf', 'text'):

		_logger.info('portal_order_page')
		_logger.info(self)
		# iperc_continuo = request.env.search(["id","=",registro.id])
		_logger.info(registro)
		return self._show_report(model=registro, report_type='pdf', report_ref='iperc_continuo.action_report_saleorder', download=True)

		# use sudo to allow accessing/viewing orders for public user
		# only if he knows the private token
		# Log only once a day


	def _show_report(self, model, report_type, report_ref, download=False):
		_logger.info('_show_report')
		if report_type not in ('html', 'pdf', 'text'):
			raise UserError(_("Invalid report type: %s") % report_type)

		report_sudo = request.env.ref(report_ref).sudo()
		_logger.info(report_sudo)
		# if not isinstance(report_sudo, type(self.env['ir.actions.report'])):
		# 	raise UserError(_("%s is not the reference of a report") % report_ref)

		method_name = 'render_qweb_%s' % (report_type)
		report = getattr(report_sudo, method_name)([model.id], data={'report_type': report_type})[0]
		_logger.info(report)
		reporthttpheaders = [
			('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
			('Content-Length', len(report)),
		]
		if report_type == 'pdf' and download:
			filename = "%s.pdf" % (re.sub('\W+', '-', 'IPERC Continuo'))
			reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
		return request.make_response(report, headers=reporthttpheaders)
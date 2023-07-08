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

	@http.route("/iper", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def principal(self):
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 6)])
		if usuario.perfil == "1":
			sedes = request.env["sede.sede"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		else:
			sedes = request.env["sede.sede"].sudo().search([('encargado',  '=', request.env.user.id)])

		registros = request.env["iper.completo"].sudo().search([('sede',  'in', sedes.ids)])
		return request.render("iperc.list_iper", {"registros": registros,"plan":plan,"sedes":sedes})


	@http.route('/pdfiper/<model("iper.completo"):registro>', type='http', auth="public", website=True)
	def portal_order_page(self,registro,**kw):
		return self._show_report(model=registro, report_type='pdf', report_ref='iperc.action_report_iperc', download=True)

	def _show_report(self, model, report_type, report_ref, download=False):
		if report_type not in ('pdf'):
			raise UserError(_("Invalid report type: %s") % report_type)

		report_sudo = request.env.ref(report_ref).sudo()
		method_name = 'render_qweb_%s' % (report_type)
		report = getattr(report_sudo, method_name)([model.id], data={'report_type': report_type})[0]
		reporthttpheaders = [
			('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
			('Content-Length', len(report)),
		]
		if report_type == 'pdf' and download:
			filename = "%s.pdf" % (re.sub('\W+', '-', 'PERMISO DE TRABAJO'))
			reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
		return request.make_response(report, headers=reporthttpheaders)


	@http.route("/iperc/configuracion", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def configuracion(self):
		tipos = request.env["type.iper"].sudo().search([])
		return request.render("iperc.configuracion_iperc", {"tipos": tipos})

	@http.route("/iperc/tablas", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def tablas(self):
		# tipos = request.env["type.iperc"].sudo().search([])
		return request.render("iperc.tablas_iperc")

	@http.route("/iperc/<model('iper.completo'):registro>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def registros(self,registro):

		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		today_datetime = datetime.now(pytz.timezone('America/Lima'))
		today_dia = today_datetime.strftime("%Y-%m-%d")
		today_hora = today_datetime.strftime("%H:%M:%S")
		today_inicio = today_dia+'T'+today_hora

		# evaluaciones = []
		# for evaluacion in registro.evaluacion_ids:
		# 	descripcion = request.env["descripcion.iper"].sudo().search([('descripcion_id',  '=', evaluacion.type_id.id)])
		# 	evaluaciones.append(descripcion.id)

		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		riesgos = request.env["descripcion.iper"].sudo().search([])
		tipos = request.env["type.iper"].sudo().search([])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 6)])
		responsables = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])

		return request.render("iperc.form_iperc", {"fecha_actual": fecha_actual,"today_inicio":today_inicio,"registro": registro,"plan":plan,'tipos': tipos,'riesgos':riesgos,'responsables':responsables})

	@http.route(["/continuo/descripcion"],type="json",auth="public",method=["POST"],website=True)
	def Tipopeligro(self,name):
		type = request.env["type.iperc"].sudo().search([('name',  '=', name)])
		evaluaciones = request.env["descripcion.iperc"].sudo().search([('descripcion_id',  '=', type.id)])

		datos = [{	"id":p.id,
					"name":p.name
					}for p in evaluaciones]

		return datos
		# sale_order_obj = request.website.sale_get_order(force_create=True)

	@http.route("/iper/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def continuo_guia(self):
		producto = request.env["product.template"].sudo().search([('name',  '=', 'Módulo IPERC')])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if(producto.solve_file_ids[0].id):
			pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("iperc.iper_guia", {"producto": producto,"pdf":pdf})

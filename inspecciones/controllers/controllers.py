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

class Inspecciones(http.Controller):


	@http.route('/inspecciones_list', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def inspecciones_list(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		empresa = request.env.user.empresa_id
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		registros = request.env["inspeccion"].sudo().search([('create_uid','=', request.env.uid)])
		formatos = request.env["formato.inspeccion"].sudo().search([])
		return request.render('inspecciones.lista_inspecciones',{"registros":registros,"empresa":empresa,"fecha_actual":fecha_actual,"plan":plan,"formatos":formatos})


	@http.route("/inspecciones_form/<model('inspeccion'):registro>", type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def inspecciones_form(self,registro):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		condiciones = request.env["formato.condicion"].sudo().search([])
		sub_condiciones = request.env["formato.sub.condicion"].sudo().search([])
		trabajadores = request.env["trabajador.trabajador"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		areas = request.env["area.area"].sudo().search([('create_uid',  '=', request.env.user.id)])
		if registro.fecha:
			fecha= registro.fecha.strftime("%Y-%m-%d")
		else:
			fecha = ""

		if registro.tipo == '1':
			return request.render('inspecciones.template_inspecciones', {"registro": registro,"usuario":usuario,"trabajadores":trabajadores,"fecha":fecha})
		elif registro.tipo == '2':
			return request.render('inspecciones.template_inspecciones_subestandar', {"registro": registro,"usuario":usuario,"trabajadores":trabajadores,"fecha":fecha})
		elif registro.tipo == '3':
			return request.render('inspecciones.template_inspecciones_criticos', {"registro": registro,"usuario":usuario,"trabajadores":trabajadores})

	@http.route(['/pdf/download/inspecciones/<model("inspeccion"):registro>'], type='http', auth="public", website=True)
	def portal_inspecciones_page(self,registro,**kw):
		return self._show_report(model=registro, report_type='pdf', report_ref='inspecciones.action_report_saleorder', download=True)


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

	@http.route("/guardar_field_odoo_inspeccion",auth='user', type = 'json')
	def guardar_field_odoo_requisito_contratista(self,inputs,model,record_id,**kw):
		aptitud = '1'
		for line in inputs:
			_logger.info(line)
			lineaedit = request.env["{}".format(line["model_id"])].search([('id', '=', line["id"])], limit=1)
			lineaedit.write({'{}'.format(line["name"]): line["value"]})
			if not line["value"]:
				aptitud = '2'

	@http.route('/formatos_list', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def formatos_list(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		empresa = request.env.user.empresa_id
		formatos_base = request.env["formato.inspeccion"].sudo().search([('origen',  '=', '1')])
		formatos_creados = request.env["formato.inspeccion"].sudo().search([('create_uid',  '=', request.env.user.id),('origen',  '=', '2')])
		formatos = formatos_creados + formatos_base
		return request.render('inspecciones.lista_formatos',{"empresa":empresa,"fecha_actual":fecha_actual,"formatos":formatos})

	@http.route("/formatos_form/<model('formato.inspeccion'):registro>", type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def formatos_form(self,registro):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		trabajadores = request.env["trabajador.trabajador"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		if registro.tipo == '1':
			return request.render('inspecciones.template_formato_inspecciones', {"registro": registro,"usuario":usuario,"trabajadores":trabajadores})
		elif registro.tipo == '2':
			return request.render('inspecciones.template_formato_inspecciones_subestandar', {"registro": registro,"usuario":usuario,"trabajadores":trabajadores})
		elif registro.tipo == '3':
			return request.render('inspecciones.template_formato_inspecciones_criticos', {"registro": registro,"usuario":usuario,"trabajadores":trabajadores})

	@http.route("/inspeccion/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permiso_guia(self):
		producto = request.env["product.template"].sudo().search([('id',  '=', 1)])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if len(producto.solve_file_ids)>0:
			if(producto.solve_file_ids[0].id):
				pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("website_permiso.list_permiso_guia", {"producto": producto,"pdf":pdf})

	@http.route('/consolidado/inspeccion', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
	def consolidado_inspeccion(self):
		today = date.today()
		fecha_actual = today.strftime("%Y-%m-%d")
		empresa = request.env.user.empresa_id
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 2)])
		registros = request.env["inspeccion"].sudo().search([('create_uid','=', request.env.uid),('tipo','in', ['2','3'])])
		formatos = request.env["formato.inspeccion"].sudo().search([])
		trabajadores = request.env["trabajador.trabajador"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		return request.render('inspecciones.consolidado_inspecciones',{"registros":registros,"empresa":empresa,"fecha_actual":fecha_actual,"plan":plan,"formatos":formatos,"trabajadores":trabajadores})

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
	@http.route("/usuarios-general", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def general(self):
		usuario = request.env["res.users"].sudo().search(
			[('id',  '=', request.env.user.id)])
		trabajadores = request.env["res.users"].sudo().search(
			[('parent_id',  '=', request.env.user.parent_id.id)], order='perfil')
		_logger.info(trabajadores)
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)], order='planes_id')
		if usuario.perfil == "1":
			sedes = request.env["sede.sede"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		else:
			sedes = request.env["sede.sede"].sudo().search([('encargado',  '=', request.env.user.id)])
		usuariosnuevo2 = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])
		planesnuevo = request.env["planes.planes"].sudo().search(
			[('id',  'in', [(rec.planes_id.id) for rec in grupos])])

		matriz = []
		for plannuevo in planesnuevo:
			cuentausernuevo = request.env["res.users.plan"].sudo().search([('user_id', 'in', [(rec.id) for rec in usuariosnuevo2]),('planes_id',  '=', plannuevo.id)])
			res_user_plan_parent = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.parent_id.id),('planes_id',  '=', plannuevo.id)])
			# today = datetime.now(pytz.timezone('America/Lima'))
			if res_user_plan_parent.fecha:
				fecha_parent = res_user_plan_parent.fecha.strftime("%Y-%m-%d %H:%M:%S")
			else:
				fecha_parent = 0
			matriz.append([plannuevo,plannuevo.limite_usuarios-len(cuentausernuevo),len(cuentausernuevo),fecha_parent,cuentausernuevo])

		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 1)])
		fecha_fin = datetime.today()+ relativedelta(months=1)
		# Usuarios secundarios
		secundarios = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil',  '=', '2')])
		return request.render("website_permiso.usuarios",{"usuario":usuario,"trabajadores":trabajadores,"plan":plan,"grupos":grupos,"fecha_fin":fecha_fin,"matriz":matriz,"sedes":sedes,"secundarios":secundarios})

	@http.route("/usuarios-personal", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def personal(self):
		usuario = request.env["res.users"].sudo().search(
			[('id',  '=', request.env.user.id)])
		trabajadores_planilla = request.env["trabajador.trabajador"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id),('tipo',  '=', '1')])
		trabajadores_locacion = request.env["trabajador.trabajador"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id),('tipo',  '=', '2')])
		return request.render("website_permiso.personal",{"trabajadores_planilla":trabajadores_planilla,"trabajadores_locacion":trabajadores_locacion,"usuario":usuario})

	@http.route("/usuarios-contratista", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def contratista(self):
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		contratistas = request.env["contratista.contratista"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		return request.render("website_permiso.contratistas",{"contratistas":contratistas,"usuario":usuario})

	@http.route("/usuarios", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def usuarios(self):
		usuario = request.env["res.users"].sudo().search(
			[('id',  '=', request.env.user.id)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)], order='planes_id')
		usuariosnuevo2 = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])
		planesnuevo = request.env["planes.planes"].sudo().search(
			[('id',  'in', [(rec.planes_id.id) for rec in grupos])])

		matriz = []
		for plannuevo in planesnuevo:
			cuentausernuevo = request.env["res.users.plan"].sudo().search([('user_id', 'in', [(rec.id) for rec in usuariosnuevo2]),('planes_id',  '=', plannuevo.id)])
			res_user_plan_parent = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.parent_id.id),('planes_id',  '=', plannuevo.id)])
			# today = datetime.now(pytz.timezone('America/Lima'))
			if res_user_plan_parent.fecha:
				fecha_parent = res_user_plan_parent.fecha.strftime("%Y-%m-%d %H:%M:%S")
			else:
				fecha_parent = 0
			matriz.append([plannuevo,plannuevo.limite_usuarios-len(cuentausernuevo),len(cuentausernuevo),fecha_parent,cuentausernuevo])

		return request.render("website_permiso.planes",{"matriz":matriz})

	@http.route("/permiso/solicitar", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permiso(self):
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 1)])
		if usuario.perfil == "1":
			sedes = request.env["sede.sede"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		else:
			sedes = request.env["sede.sede"].sudo().search([('encargado',  '=', request.env.user.id)])

		plantillas = request.env["tipo.permiso"].sudo().search([])
		permisos = request.env["permiso.trabajo"].sudo().search(['|',('create_uid',  '=', request.env.user.id),('solicitante_id',  '=', request.env.user.id)])

		return request.render("website_permiso.list_permisos", {"permisos": permisos,"plan":plan,"sedes":sedes,"plantillas":plantillas,"usuario":usuario})


	@http.route("/permiso/plantilla", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def plantillas(self):
		permisos = request.env["tipo.permiso"].sudo().search([])
		return request.render("website_permiso.list_permiso_plantilla", {"permisos": permisos})

	@http.route("/permiso/plantilla/<model('tipo.permiso'):permiso>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def plantillaspermiso(self,permiso):
		requisitos = request.env["tipo.requisito"].sudo().search([])
		return request.render("website_permiso.list_tipo_permiso_plantilla", {"permiso": permiso,"requisitos":requisitos})

	@http.route("/preventor", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def preventor(self):
		# permisos = request.env["permiso.trabajo"].sudo().search([('empresa_uid',  '=',   request.env.user.empresa_id.id)])
		permisos = request.env["permiso.trabajo"].sudo().search([('create_uid',  '=', request.env.user.id)])
		return request.render("website_permiso.preventor", {"permisos": permisos})


	@http.route("/permiso/solicitar/<model('permiso.trabajo'):permiso>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permisos(self,permiso):
		if permiso.fecha_inicio:
			fecha_hora_inicio= permiso.fecha_inicio.strftime("%Y-%m-%d %H:%M:%S")
			fecha_inicio= permiso.fecha_inicio.strftime("%Y-%m-%d")
			hora_inicio= permiso.fecha_inicio.strftime("%H:%M:%S")
		else:
			fecha_hora_inicio = ""
			fecha_inicio = ""
			hora_inicio =""
		if permiso.fecha_fin:
			fecha_hora_fin= permiso.fecha_fin.strftime("%Y-%m-%d %H:%M:%S")
			fecha_fin= permiso.fecha_fin.strftime("%Y-%m-%d")
			hora_fin= permiso.fecha_fin.strftime("%H:%M:%S")
		else:
			fecha_hora_fin = ""
			hora_fin = ""
			fecha_fin =""
		areas = request.env["area.area"].sudo().search([('create_uid',  '=', request.env.user.id)])
		empresas = request.env["contratista.contratista"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		trabajadores = request.env["trabajador.trabajador"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])

		sub_areas = request.env["sub.area"].sudo().search([('create_uid',  '=', request.env.user.id)])
		responsables = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])
		solicitantes = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '1')])
		autorizadores = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '2')])
		aprobadores = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '3')])

		epps = permiso.plantilla.tipos.search([('tipo_requi_id.name',  '=', 'EPP'),('tipo_permiso_id.name',  '=', permiso.plantilla.name)])
		herramientas = permiso.plantilla.tipos.search([('tipo_requi_id.name',  '=', 'Herramientas'),('tipo_permiso_id.name',  '=', permiso.plantilla.name)])
		preparaciones = permiso.plantilla.tipos.search([('tipo_requi_id.name',  '=', 'Preparación'),('tipo_permiso_id.name',  '=', permiso.plantilla.name)])
		aberturas = permiso.plantilla.tipos.search([('tipo_requi_id.name',  '=', 'Cerramiento de Aberturas'),('tipo_permiso_id.name',  '=', permiso.plantilla.name)])
		seguridades = permiso.plantilla.tipos.search([('tipo_requi_id.name',  '=', 'Condiciones de Seguridad'),('tipo_permiso_id.name',  '=', permiso.plantilla.name)])
		desconexiones = permiso.plantilla.tipos.search([('tipo_requi_id.name',  '=', 'Desconexión'),('tipo_permiso_id.name',  '=', permiso.plantilla.name)])
		reconexiones = permiso.plantilla.tipos.search([('tipo_requi_id.name',  '=', 'Reconexión'),('tipo_permiso_id.name',  '=', permiso.plantilla.name)])
		plantillas = request.env["tipo.permiso"].sudo().search([])

		if permiso.estado == "2":
			return request.render("website_permiso.form_solicitado_alert",{"permiso": permiso,"areas":areas,"sub_areas":sub_areas,"trabajadores":trabajadores,"hora_fin":hora_fin,"hora_inicio":hora_inicio,"fecha_fin":fecha_fin,"fecha_inicio":fecha_inicio,"fecha_hora_inicio":fecha_hora_inicio})

		return request.render("website_permiso.form_permisos",{"permiso": permiso,"epps":epps,"herramientas":herramientas,"preparaciones":preparaciones,"aberturas":aberturas,"seguridades":seguridades,"desconexiones":desconexiones,"reconexiones":reconexiones,"areas":areas,"sub_areas":sub_areas,"trabajadores":trabajadores,"solicitantes":solicitantes,"autorizadores":autorizadores,"aprobadores":aprobadores,"responsables":responsables,"empresas":empresas,"hora_fin":hora_fin,"hora_inicio":hora_inicio,"fecha_fin":fecha_fin,"fecha_inicio":fecha_inicio,"fecha_hora_inicio":fecha_hora_inicio,"fecha_hora_fin":fecha_hora_fin,"plantillas":plantillas})

	@http.route("/permiso/grafico", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def graph(self):
		return request.render("website_permiso.list_graph")

	@http.route("/permiso/historial", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def history(self):
		permisos = request.env["permiso.trabajo"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		return request.render("website_permiso.list_history",{"permisos":permisos})

	@http.route("/permiso/guia", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permiso_guia(self):
		producto = request.env["product.template"].sudo().search([('id',  '=', 1)])
		adjuntos = producto.solve_file_ids

		pdf = ''
		if(producto.solve_file_ids[0].id):
			pdf='https://docs.google.com/gview?embedded=true&url=https://preventor.tech/web/content/'+str(producto.solve_file_ids[0].id)

		for line in adjuntos:
			line.public = True
		return request.render("website_permiso.list_permiso_guia", {"producto": producto,"pdf":pdf})

	@http.route("/permiso/autorizar", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permiso_autorizar(self):
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 1)])

		if usuario.perfil == "1":
			sedes = request.env["sede.sede"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		else:
			sedes = request.env["sede.sede"].sudo().search([('encargado',  '=', request.env.user.id)])

		permisos = request.env["permiso.trabajo"].sudo().search(['|',('create_uid',  '=', request.env.user.id),('autorizador_id',  '=', request.env.user.id)])

		return request.render("website_permiso.list_permisos_1", {"permisos": permisos,"plan":plan,"usuario":usuario})

	@http.route("/permiso/aprobar", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permiso_aprobar(self):
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		grupos = request.env["res.users.plan"].sudo().search([('user_id',  '=', request.env.user.id)])
		plan = request.env["planes.planes"].sudo().search([('id', 'in', [(rec.planes_id.id) for rec in grupos]),('product_id',  '=', 1)])

		if usuario.perfil == "1":
			sedes = request.env["sede.sede"].sudo().search([('empresa_id',  '=', request.env.user.empresa_id.id)])
		else:
			sedes = request.env["sede.sede"].sudo().search([('encargado',  '=', request.env.user.id)])

		permisos = request.env["permiso.trabajo"].sudo().search(['|',('create_uid',  '=', request.env.user.id),('aprobador_id',  '=', request.env.user.id)])

		return request.render("website_permiso.list_permisos_2", {"permisos": permisos,"plan":plan,"usuario":usuario})

	@http.route("/permiso/roles", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permiso_roles(self):
		usuarios = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])

		return request.render("website_permiso.list_roles_usuarios", {"usuarios":usuarios})

	@http.route("/permiso/autorizar/<model('permiso.trabajo'):permiso>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permisos_autorizar_line(self,permiso):
		if permiso.fecha_inicio:
			fecha_hora_inicio= permiso.fecha_inicio.strftime("%Y-%m-%d %H:%M:%S")
			fecha_inicio= permiso.fecha_inicio.strftime("%Y-%m-%d")
			hora_inicio= permiso.fecha_inicio.strftime("%H:%M:%S")
		else:
			fecha_hora_inicio = ""
			fecha_inicio = ""
			hora_inicio =""
		if permiso.fecha_fin:
			fecha_hora_fin= permiso.fecha_fin.strftime("%Y-%m-%d %H:%M:%S")
			fecha_fin= permiso.fecha_fin.strftime("%Y-%m-%d")
			hora_fin= permiso.fecha_fin.strftime("%H:%M:%S")
		else:
			fecha_hora_fin = ""
			hora_fin = ""
			fecha_fin =""
		areas = request.env["area.area"].sudo().search([])
		trabajadores = request.env["trabajador.trabajador"].sudo().search([('create_uid',  '=', request.env.user.id)])
		sub_areas = request.env["sub.area"].sudo().search([])
		solicitantes = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '1')])
		autorizadores = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '2')])
		aprobadores = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '3')])

		if permiso.estado == "3":
			return request.render("website_permiso.form_autorizado_alert")
		return request.render("website_permiso.form_permisos_1",{"permiso": permiso,"solicitantes":solicitantes,"autorizadores":autorizadores,"aprobadores":aprobadores,"areas":areas,"sub_areas":sub_areas,"trabajadores":trabajadores,"hora_fin":hora_fin,"hora_inicio":hora_inicio,"fecha_fin":fecha_fin,"fecha_inicio":fecha_inicio,"fecha_hora_inicio":fecha_hora_inicio,"fecha_hora_fin":fecha_hora_fin})

	@http.route("/permiso/aprobar/<model('permiso.trabajo'):permiso>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def permisos_aprobar_line(self,permiso):
		if permiso.fecha_inicio:
			fecha_hora_inicio= permiso.fecha_inicio.strftime("%Y-%m-%d %H:%M:%S")
			fecha_inicio= permiso.fecha_inicio.strftime("%Y-%m-%d")
			hora_inicio= permiso.fecha_inicio.strftime("%H:%M:%S")
		else:
			fecha_hora_inicio = ""
			fecha_inicio = ""
			hora_inicio =""
		if permiso.fecha_fin:
			fecha_hora_fin= permiso.fecha_fin.strftime("%Y-%m-%d %H:%M:%S")
			fecha_fin= permiso.fecha_fin.strftime("%Y-%m-%d")
			hora_fin= permiso.fecha_fin.strftime("%H:%M:%S")
		else:
			fecha_hora_fin = ""
			fecha_fin = ""
			hora_fin =""
		areas = request.env["area.area"].sudo().search([])
		trabajadores = request.env["trabajador.trabajador"].sudo().search([('create_uid',  '=', request.env.user.id)])
		sub_areas = request.env["sub.area"].sudo().search([])
		solicitantes = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '1')])
		autorizadores = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '2')])
		aprobadores = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil_permiso',  '=', '3')])
		if permiso.estado == "4":
			return request.render("website_permiso.form_aprobado_alert")
		return request.render("website_permiso.form_permisos_2",{"permiso": permiso,"solicitantes":solicitantes,"autorizadores":autorizadores,"aprobadores":aprobadores,"areas":areas,"sub_areas":sub_areas,"trabajadores":trabajadores,"hora_fin":hora_fin,"hora_inicio":hora_inicio,"fecha_fin":fecha_fin,"fecha_inicio":fecha_inicio,"fecha_hora_inicio":fecha_hora_inicio,"fecha_hora_fin":fecha_hora_fin})


	@http.route("/trabajadores", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def trabajadores(self):
		empresas = request.env["empresa.empresa"].sudo().search([])
		trabajadores = request.env["trabajador.trabajador"].sudo().search([('create_uid',  '=', request.env.user.id)])
		return request.render("website_permiso.list_trabajador",{"trabajadores":trabajadores,"empresas":empresas})

	@http.route("/contratistas", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def contratistas(self):
		empresas = request.env["empresa.empresa"].sudo().search([('create_uid',  '=', request.env.user.id)])
		return request.render("website_permiso.list_contratistas",{"empresas":empresas})

	@http.route(['/pdfpermiso/<model("permiso.trabajo"):registro>'], type='http', auth="public", website=True)
	def portal_order_page(self,registro,**kw):
		return self._show_report(model=registro, report_type='pdf', report_ref='website_permiso.action_report_permiso', download=True)

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


	@http.route("/trabajador/requisitos/<model('trabajador.trabajador'):trabajador>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def trabajador_requisitos(self,trabajador):
		usuario = request.env["res.users"].sudo().search(
			[('id',  '=', request.env.user.id)])
		return request.render("website_permiso.form_trabajador_requisitos",{"trabajador": trabajador,"usuario":usuario})

	@http.route("/sede/<model('sede.sede'):sede>", type="http", method=["GET", "POST"], auth="user", csrf=False, website=True)
	def sede_area(self,sede):
		secundarios = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id),('perfil',  '=', '2')])
		usuario = request.env["res.users"].sudo().search([('id',  '=', request.env.user.id)])
		return request.render("website_permiso.form_sede_sede",{"sede": sede,"usuario":usuario,"secundarios":secundarios})

	#guardar reba

	@http.route("/guardar_field_odoo_requisito",auth='user', type = 'json')
	def guardar_field_odoo_requisito(self,inputs,model,record_id,**kw):
		trabajador = request.env["trabajador.trabajador"].search([('id', '=', record_id)], limit=1)
		aptitud = '1'
		for line in inputs:
			lineaedit = request.env["{}".format(model)].search([('id', '=', line["id"])], limit=1)
			lineaedit.write({'{}'.format(line["name"]): line["value"]})
			if not line["value"]:
				aptitud = '2'
		trabajador.write({'aptitud': aptitud})

		return True

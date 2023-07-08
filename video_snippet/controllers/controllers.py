from odoo import http,fields
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import Website
from datetime import datetime, timedelta, date
import odoo.addons.decimal_precision as dp
import os
import pytz
import logging
# import culqipy
_logger = logging.getLogger(__name__)

class VideoPreventor(http.Controller):
	@http.route(["/get_videos"],type="json",auth="public",method=["GET", "POST"],website=True)
	def GetVideos(self):
		video_obj = request.env["product.product"].sudo().search([], order='id')
		sale_order_obj = request.website.sale_get_order(force_create=True)

		def get_sale_qty(sale_order,product_id):
			l = list((filter(lambda p:p.product_id.id == product_id,sale_order.order_line)))
			return l[0].product_uom_qty if len(l)>0 else 0


		products = [{   "id":p.id,
						"nombre":p.name,
						"description":p.description,
						"modulo":p.modulo,
						"sale_qty":get_sale_qty(sale_order_obj,p.id),
						"url":p.url,
						"website_url":p.website_url,
						# "imagen":p.imagen
					}for p in video_obj]
		return products

	# @http.route(["/searchplanes"],type="json",auth="public",method=["GET", "POST"],website=True)
	# def getplanes(self,usuario_admin,usuario_creado):
	# 	resultado_planes = request.env["res.users.plan"].sudo().search([('user_id',  '=', usuario_admin)])
	# 	for p in resultado_planes:
	# 		request.env["res.users.plan"].sudo().create({"planes_id":p.planes_id.id,"user_id":usuario_creado})
	# 	return True

	@http.route(["/createuser"],type="json",auth="user",method=["GET", "POST"],website=True)
	def createnewuser(self,name,login,parent_id,planes,empresa_id,perfil):
		user_id = request.env['res.users'].sudo().search([('login','=',login)],limit=1)
		if user_id:
			return False
		else:
			user = request.env["res.users"].sudo().create({\
													"name":name,\
													"login":login,\
													"email":login,\
													"email_formatted":login,\
													"parent_id":parent_id,\
													"sel_groups_1_8_9":8,\
													"perfil":perfil,\
													"empresa_id":empresa_id,\
													'sh_user_from_signup':True
													})

			planes = request.env["planes.planes"].sudo().search([('name',  '=',  'Plan Gratis')])
			for plan in planes:
				request.env["res.users.plan"].sudo().create({"planes_id":plan.id,"user_id":user.id})
			return True



	@http.route(["/searchuser"],type="json",auth="user",method=["GET", "POST"],website=True)
	def searchuser(self,user_id):
		res_user_plan = request.env["res.users.plan"].sudo().search([('user_id',  '=', int(user_id))])
		_logger.info(res_user_plan)

		planes = []
		for plan in res_user_plan.planes_id:
			planes.append(plan.id)
			_logger.info(planes)
		return planes

	@http.route(["/changeuser"],type="json",auth="user",method=["GET", "POST"],website=True)
	def changeuser(self,user_id,matriz):
		res_user_plan = request.env["res.users.plan"].sudo().search([('user_id',  '=', int(user_id))])
		usuariosmismoparent = request.env["res.users"].sudo().search([('parent_id',  '=', request.env.user.parent_id.id)])
		_logger.info(res_user_plan)
		_logger.info(user_id)
		_logger.info(matriz)
		# [[1,iddeplan],[0,iddeplan]]
		respuestas = []
		for tupla in matriz:
			res_user_plan_parent = request.env["res.users.plan"].sudo().search([('planes_id',  '=', int(tupla[1])),('user_id',  '=', request.env.user.parent_id.id)])
			# SI ES NO SE ANALIZA SI EXISTIA, SI EXISTIA UNLINK SINO NO HACER NADA
			plan = request.env["planes.planes"].sudo().search([('id',  '=', int(tupla[1]))])
			cuentauserplan = request.env["res.users.plan"].sudo().search([('user_id', 'in', [(rec.id) for rec in usuariosmismoparent]),('planes_id',  '=', int(tupla[1]))])
			_logger.info(matriz)
			res_user_plan_exist = request.env["res.users.plan"].sudo().search([('planes_id',  '=', int(tupla[1])),('user_id',  '=', int(user_id))])
			# NO COMO INPUT
			if(tupla[0]==1):
				if res_user_plan_exist:
					res_user_plan_exist.unlink()
					respuestas.append([plan.name,plan.product_id.name,1])
			# SI COMO INPUT
			else:
				if not res_user_plan_exist:
					if len(cuentauserplan) < plan.limite_usuarios:
						request.env["res.users.plan"].sudo().create({"planes_id":int(tupla[1]),"user_id":int(user_id),"fecha":res_user_plan_parent.fecha})
						respuestas.append([plan.name,plan.product_id.name,1])
					else:
						respuestas.append([plan.name,plan.product_id.name,0])

		return respuestas

	@http.route(["/shop/payment"],type="http",auth="user",methods=["GET","POST"],website=True,csrf=False)
	def PaymentPage(self):
		sale_order = request.website.sale_get_order(force_create=True)
		credentialsCulqi = request.env.user.company_id.getCredentialsCulqi()
		# context, pricelist = self._get_pricelist_context()
		if len(sale_order.order_line)>0:
			return request.render("video_snippet.shop_payment",{"sale":sale_order,"culqipk":credentialsCulqi["culqi_pk"]})
		else:
			return request.redirect("/")

	@http.route(["/shop/changeplan"],type="json",auth="public",methods=["POST"],website=True)
	def Changeplan(self,product_id,plan_id):
		sale = request.website.sale_get_order(force_create=True)
		# sale._cart_update(
		#             product_id=int(product_id),
		#             add_qty=1,
		#             set_qty=1
		#         )
		plan = request.env["planes.planes"].browse(int(plan_id))
		_logger.info(plan)
		_logger.info(plan.precio)
		for line in sale.order_line:
			if line.product_id.id == int(product_id):
				line.plan_id = plan_id
				line.price_unit = plan.precio
				return [line.price_total,round(sale.amount_total,2)]


		# _logger.info([[line.product_id.name,line.product_uom_qty] for line in sale.order_line])


	@http.route(["/sendpayment"],type="http",auth="public",methods=["GET","POST"],website=True)
	def SendPayment(self,token,email):
		_logger.info("sendpayment")
		sale_order = request.website.sale_get_order(force_create=True)
		credentialsCulqi = request.env.user.company_id.getCredentialsCulqi()
		culqipy.public_key= credentialsCulqi["culqi_pk"]
		culqipy.secret_key= credentialsCulqi["culqi_sk"]
		_logger.info(sale_order)
		_logger.info(credentialsCulqi)
		_logger.info(email)
		_logger.info(token)
		_logger.info(int(sale_order.amount_total*100))
		_logger.info(type(int(sale_order.amount_total*100)))
		_logger.info("SIGUE")
		user = request.env["res.users"].browse(request.session.uid)
		_logger.info(user)


		# for line in sale_order.order_line:
		#     plan = request.env["planes.planes"].browse(int(line.plan_id))
		#     _logger.info(plan.id)
		#     _logger.info(user.id)
		#     _logger.info(type(plan.id))
		#     _logger.info(type(user.id))
		#     request.env["res.users.plan"].sudo().create({"planes_id":plan.id,"user_id":user.id})
		#


		charge = culqipy.Charge.create({
							"amount":int(sale_order.amount_total*100),
							"country_code":"PE",
							"currency_code":sale_order.currency_id.name,
							"email":email,
							"description":request.env.user.company_id.name,
							"source_id":token
						})

		_logger.info(charge)
		user_obj = request.env["res.users"]
		current_user = request.env["res.users"].browse(request.session.uid)
		new_user = False
		if charge["object"]=="charge":
			if charge["outcome"]["type"]=="venta_exitosa":
				# users = user_obj.search([["login","=",email]])
				if not current_user.exists():
					user = current_user.sudo().create({"name":email,"email":email,"login":email})
					user.action_reset_password()
					new_user = True
				else:
					user = current_user


				for line in sale_order.order_line:
					_logger.info("FOR")
					plan = request.env["planes.planes"].sudo().browse(int(line.plan_id))
					planes = request.env["planes.planes"].sudo().search([('product_id',  '=',   plan.product_id.id)])
					for x in planes:
						planesdelete = request.env["res.users.plan"].sudo().search([('planes_id',  '=', x.id),('user_id',  '=', user.id)])
						planesdelete.sudo().unlink()
					_logger.info(line.plan_id)
					_logger.info(user.id)
					# if(planes):
					#     planes.unlink()

					request.env["res.users.plan"].sudo().create({"planes_id":plan.id,"user_id":user.id,"fecha":datetime.now(pytz.timezone('America/Lima')).strftime("%Y-%m-%d %H:%M:%S")})



				_logger.info("venta_exitosa")
				sale_order.partner_id = user.partner_id.id
				sale_order.partner_invoice_id = user.partner_id.id
				sale_order.partner_shipping_id = user.partner_id.id
				sale_order.action_confirm()
				return request.render("video_snippet.shop_payment_message",{"message":charge["outcome"]["user_message"],
																						"state":"venta_exitosa",
																						"new_user":new_user,
																						"user":user})

		if charge["object"] == "error":
			return request.render("video_snippet.shop_payment_message",{"message":charge["user_message"],"state":"error"})

class WebsiteCustom(Website):

	@http.route(['/shop/cart/update_json_v2'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
	def cart_update_json_v2(self, product_id,plan_id,line_id=None, add_qty=None, set_qty=None, display=True):
		"""This route is called when changing quantity from the cart or adding
		a product from the wishlist."""
		order = request.website.sale_get_order(force_create=1)
		if order.state != 'draft':
			request.website.sale_reset()
			return {}

		value = order._cart_update_v2(product_id=product_id,plan_id=plan_id,
									line_id=line_id, add_qty=add_qty, set_qty=set_qty)

		if not order.cart_quantity:
			request.website.sale_reset()
			return value
		_logger.info("sigue")
		order = request.website.sale_get_order()
		value['cart_quantity'] = order.cart_quantity

		if not display:
			return value

		value['website_sale.cart_lines'] = request.env['ir.ui.view'].render_template("website_sale.cart_lines", {
			'website_sale_order': order,
			'date': fields.Date.today(),
			'suggested_products': order._cart_accessories()
		})
		_logger.info(value['website_sale.cart_lines'])
		value['website_sale.short_cart_summary'] = request.env['ir.ui.view'].render_template("website_sale.short_cart_summary", {
			'website_sale_order': order,
		})
		_logger.info(value)
		return value

	def product(self, product, category='', search='', **kwargs):
		if not product.can_access_from_current_website():
			raise NotFound()

		return request.render("website_sale.product", self._prepare_product_values(product, category, search, **kwargs))

	def _prepare_product_values(self, product, category, search, **kwargs):
		add_qty = int(kwargs.get('add_qty', 1))

		product_context = dict(request.env.context, quantity=add_qty,
							   active_id=product.id,
							   partner=request.env.user.partner_id)
		ProductCategory = request.env['product.public.category']

		if category:
			category = ProductCategory.browse(int(category)).exists()

		attrib_list = request.httprequest.args.getlist('attrib')
		attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
		attrib_set = {v[1] for v in attrib_values}

		keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)

		categs = ProductCategory.search([('parent_id', '=', False)])

		pricelist = request.website.get_current_pricelist()

		if not product_context.get('pricelist'):
			product_context['pricelist'] = pricelist.id
			product = product.with_context(product_context)

		# Needed to trigger the recently viewed product rpc
		view_track = request.website.viewref("website_sale.product").track

		return {
			'search': search,
			'category': category,
			'pricelist': pricelist,
			'attrib_values': attrib_values,
			'attrib_set': attrib_set,
			'keep': keep,
			'categories': categs,
			'main_object': product,
			'product': product,
			'add_qty': add_qty,
			'view_track': view_track,
		}

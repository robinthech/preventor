from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class VideosSSTT(models.Model):
	_name = 'preventor.video'

	name = fields.Char("Nombre",related="nombre")
	nombre = fields.Char("Nombre")
	modulo = fields.Many2one("product.template","Modulo")
	url = fields.Char("URL")
	imagen = fields.Binary(string="imagen")

	def all_video(self):
		video_obj = self.env["preventor.video"].sudo().search([])

		products = [{   "id":p.id,
						"nombre":p.nombre,
						"url":p.url,
						"imagen":p.imagen
					}for p in video_obj]
		return products

class productinherit(models.Model):
	_inherit = 'product.template'

	planes = fields.One2many("planes.planes","product_id","Planes")
	url = fields.Char("URL VIDEO")
	modulo = fields.Char("URL MODULO")
	solve_file_ids = fields.Many2many("ir.attachment", "exam_solve_attach_rel", 'solve_file_id', "attachment_id", string="INSTRUCCIONES")

class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	plan_id = fields.Many2one("planes.planes",string="Planes")

class planes(models.Model):
	_name = 'planes.planes'
	_order = "precio asc, id desc"

	name = fields.Char("Nombre")
	product_id = fields.Many2one("product.template", string="Producto relacionado")
	user_ids = fields.Many2many("res.users")
	precio = fields.Float("Precio")
	limite_registro = fields.Integer("Límite de Registros")
	limite_usuarios = fields.Integer("Límite de Usuarios")
	limite_puntos = fields.Integer("Límite de Puntos")
	report_excel = fields.Boolean("Reporte en Excel")
	limite_excel = fields.Integer("Límite de Puntos")

	usuario_ids = fields.One2many("res.users.plan","planes_id",string="Usuarios")

class UsersPlanes(models.Model):
	_name = 'res.users.plan'

	planes_id = fields.Many2one('planes.planes', string='Plan', index=True, required=True)
	user_id = fields.Many2one('res.users', string='Usuarios', index=True, required=True)
	fecha = fields.Datetime("Fecha de asignacion", index=True)

	def cron_plan_gratis(self):
		# cron para asignar a los usuarios antiguos los nuevos planes gratis desarrollados

		_logger.info('CRON')
		planes = self.env["planes.planes"].sudo().search([('name',  '=',  'Plan Gratis')])
		for plan in planes:
			res_user_plan = self.env["res.users.plan"].sudo().search([('user_id','=',user_id.id)])
			self.env["res.users.plan"].sudo().create({"planes_id":plan.id,"user_id":user_id.id})



class Rescompany(models.Model):
	_inherit = 'res.company'

	mode = fields.Selection(selection=[('test','Test'),("live",'Live')],default='test')

	culqi_pk_live = fields.Char(string="Culqi Public Key Live")
	culqi_sk_live = fields.Char(string="Culqi Secret Key Live")

	culqi_pk_test = fields.Char(string="Culqi Public Key Test")
	culqi_sk_test = fields.Char(string="Culqi Secret Key Test")

	def getCredentialsCulqi(self):
		if self.mode == "test" and self.culqi_pk_test and self.culqi_sk_test:
			return {"culqi_pk":self.culqi_pk_test,"culqi_sk":self.culqi_sk_test}
		elif self.mode == "live" and self.culqi_pk_live and self.culqi_sk_live:
			return {"culqi_pk":self.culqi_pk_live,"culqi_sk":self.culqi_sk_live}
		else:
			return False

class SaleOrder(models.Model):
	_inherit = "sale.order"

	def _cart_find_product_line(self, product_id=None, line_id=None,plan_id=None, **kwargs):
		"""Find the cart line matching the given parameters.

		If a product_id is given, the line will match the product only if the
		line also has the same special attributes: `no_variant` attributes and
		`is_custom` values.
		"""
		self.ensure_one()
		product = self.env['product.product'].browse(product_id)

		# split lines with the same product if it has untracked attributes
		if product and (product.product_tmpl_id.has_dynamic_attributes() or product.product_tmpl_id._has_no_variant_attributes()) and not line_id:
			return self.env['sale.order.line']

		domain = [('order_id', '=', self.id), ('product_id', '=', product_id),("plan_id",'=',plan_id)]
		if line_id:
			domain += [('id', '=', line_id)]
		else:
			domain += [('product_custom_attribute_value_ids', '=', False)]

		return self.env['sale.order.line'].sudo().search(domain)

	def _cart_update_v2(self, product_id=None,plan_id=None ,line_id=None, add_qty=0, set_qty=0, **kwargs):
		""" Add or set product quantity, add_qty can be negative """
		_logger.info("cart_update")
		self.ensure_one()
		product_context = dict(self.env.context)
		product_context.setdefault('lang', self.sudo().partner_id.lang)
		SaleOrderLineSudo = self.env['sale.order.line'].sudo().with_context(product_context)
		# change lang to get correct name of attributes/values
		product_with_context = self.env['product.product'].with_context(product_context)
		product = product_with_context.browse(int(product_id))

		try:
			if add_qty:
				add_qty = float(add_qty)
		except ValueError:
			add_qty = 1
		try:
			if set_qty:
				set_qty = float(set_qty)
		except ValueError:
			set_qty = 0
		quantity = 0
		order_line = False
		if self.state != 'draft':
			request.session['sale_order_id'] = None
			raise UserError(_('It is forbidden to modify a sales order which is not in draft status.'))

		if line_id is not False :
			order_line = self._cart_find_product_line(product_id, line_id,plan_id, **kwargs)[:1]
		# Create line if no line with product_id can be located
		if not order_line:
			if not product:
				raise UserError(_("The given product does not exist therefore it cannot be added to cart."))

			no_variant_attribute_values = kwargs.get('no_variant_attribute_values') or []
			received_no_variant_values = product.env['product.template.attribute.value'].browse([int(ptav['value']) for ptav in no_variant_attribute_values])
			received_combination = product.product_template_attribute_value_ids | received_no_variant_values
			product_template = product.product_tmpl_id

			# handle all cases where incorrect or incomplete data are received
			combination = product_template._get_closest_possible_combination(received_combination)

			# get or create (if dynamic) the correct variant
			product = product_template._create_product_variant(combination)

			if not product:
				raise UserError(_("The given combination does not exist therefore it cannot be added to cart."))
			product_id = product.id

			values = self._website_product_id_change_v2(self.id, product_id,plan_id, qty=1)

			# add no_variant attributes that were not received
			for ptav in combination.filtered(lambda ptav: ptav.attribute_id.create_variant == 'no_variant' and ptav not in received_no_variant_values):
				no_variant_attribute_values.append({
					'value': ptav.id,
				})

			# save no_variant attributes values
			if no_variant_attribute_values:
				values['product_no_variant_attribute_value_ids'] = [
					(6, 0, [int(attribute['value']) for attribute in no_variant_attribute_values])
				]

			# add is_custom attribute values that were not received
			custom_values = kwargs.get('product_custom_attribute_values') or []
			received_custom_values = product.env['product.template.attribute.value'].browse([int(ptav['custom_product_template_attribute_value_id']) for ptav in custom_values])
			for ptav in combination.filtered(lambda ptav: ptav.is_custom and ptav not in received_custom_values):
				custom_values.append({
					'custom_product_template_attribute_value_id': ptav.id,
					'custom_value': '',
				})

			# save is_custom attributes values
			if custom_values:
				values['product_custom_attribute_value_ids'] = [(0, 0, {
					'custom_product_template_attribute_value_id': custom_value['custom_product_template_attribute_value_id'],
					'custom_value': custom_value['custom_value']
				}) for custom_value in custom_values]

			# create the line
			order_line = SaleOrderLineSudo.create(values)

			try:
				order_line._compute_tax_id()
			except ValidationError as e:
				# The validation may occur in backend (eg: taxcloud) but should fail silently in frontend
				_logger.debug("ValidationError occurs during tax compute. %s" % (e))
			if add_qty:
				add_qty -= 1

		# compute new quantity
		if set_qty:
			quantity = set_qty
		elif add_qty is not None:
			quantity = order_line.product_uom_qty + (add_qty or 0)

		# Remove zero of negative lines
		if quantity <= 0:
			linked_line = order_line.linked_line_id
			order_line.unlink()
			if linked_line:
				# update description of the parent
				linked_product = product_with_context.browse(linked_line.product_id.id)
				linked_line.name = linked_line.get_sale_order_line_multiline_description_sale(linked_product)
		else:
			# update line
			no_variant_attributes_price_extra = [ptav.price_extra for ptav in order_line.product_no_variant_attribute_value_ids]
			values = self.with_context(no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra))._website_product_id_change(self.id, product_id, qty=quantity)
			if self.pricelist_id.discount_policy == 'with_discount' and not self.env.context.get('fixed_price'):
				order = self.sudo().browse(self.id)
				product_context.update({
					'partner': order.partner_id,
					'quantity': quantity,
					'date': order.date_order,
					'pricelist': order.pricelist_id.id,
					'force_company': order.company_id.id,
				})
				logging.info(product_context)
				product_with_context = self.env['product.product'].with_context(product_context)
				logging.info(product_with_context)
				product = product_with_context.browse(product_id)
				values['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
					order_line._get_display_price(product),
					order_line.product_id.taxes_id,
					order_line.tax_id,
					self.company_id
				)
			logging.info(values)
			order_line.write(values)

			# link a product to the sales order
			if kwargs.get('linked_line_id'):
				linked_line = SaleOrderLineSudo.browse(kwargs['linked_line_id'])
				order_line.write({
					'linked_line_id': linked_line.id,
				})
				linked_product = product_with_context.browse(linked_line.product_id.id)
				linked_line.name = linked_line.get_sale_order_line_multiline_description_sale(linked_product)
			# Generate the description with everything. This is done after
			# creating because the following related fields have to be set:
			# - product_no_variant_attribute_value_ids
			# - product_custom_attribute_value_ids
			# - linked_line_id
			order_line.name = order_line.get_sale_order_line_multiline_description_sale(product)

		option_lines = self.order_line.filtered(lambda l: l.linked_line_id.id == order_line.id)

		return {'line_id': order_line.id, 'quantity': quantity, 'option_ids': list(set(option_lines.ids))}

	def _website_product_id_change_v2(self, order_id, product_id,plan_id, qty=0):
		order = self.sudo().browse(order_id)
		product_context = dict(self.env.context)
		product_context.setdefault('lang', order.partner_id.lang)
		product_context.update({
			'partner': order.partner_id,
			'quantity': qty,
			'date': order.date_order,
			'pricelist': order.pricelist_id.id,
			'force_company': order.company_id.id,
		})
		product = self.env['product.product'].with_context(product_context).browse(product_id)
		discount = 0

		if order.pricelist_id.discount_policy == 'without_discount':
			# This part is pretty much a copy-paste of the method '_onchange_discount' of
			# 'sale.order.line'.
			price, rule_id = order.pricelist_id.with_context(product_context).get_product_price_rule(product, qty or 1.0, order.partner_id)
			pu, currency = request.env['sale.order.line'].with_context(product_context)._get_real_price_currency(product, rule_id, qty, product.uom_id, order.pricelist_id.id)
			if pu != 0:
				if order.pricelist_id.currency_id != currency:
					# we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
					date = order.date_order or fields.Date.today()
					pu = currency._convert(pu, order.pricelist_id.currency_id, order.company_id, date)
				discount = (pu - price) / pu * 100
				if discount < 0:
					# In case the discount is negative, we don't want to show it to the customer,
					# but we still want to use the price defined on the pricelist
					discount = 0
					pu = price
		else:
			pu = product.price
			if order.pricelist_id and order.partner_id:
				order_line = order._cart_find_product_line(product.id,plan_id=plan_id)
				if order_line:
					pu = self.env['account.tax']._fix_tax_included_price_company(pu, product.taxes_id, order_line[0].tax_id, self.company_id)

		return {
			'product_id': product_id,
			'product_uom_qty': qty,
			'order_id': order_id,
			'product_uom': product.uom_id.id,
			'price_unit': pu,
			'discount': discount,
			'plan_id':plan_id,
		}

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class Resuserinherit(models.Model):
	_inherit = 'res.users'

	parent_id = fields.Many2one('res.users',string="Agregado por")
	perfil = fields.Selection(selection=[('1', 'Principal'),('2', 'Secundario')], string='Perfil', default='1')
	signature = fields.Text('firma')
	signature_binary = fields.Binary(string=u'Imagen de firma')

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class Resuserinherit(models.Model):
	_inherit = 'res.users'

	perfil_permiso = fields.Selection(selection=[('1', 'Solicitante'),('2', 'Autorizador'),('3', 'Aprobador')], string='Perfil para permiso de trabajo', default='1')

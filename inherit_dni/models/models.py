from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class Resuserinherit(models.Model):
    _inherit = 'res.users'

    dni = fields.Char(string="DNI")

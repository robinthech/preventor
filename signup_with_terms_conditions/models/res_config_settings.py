# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_terms_of_service = fields.Boolean("Show Terms of Service on Sign up", config_parameter='signup.enable_terms_of_service')
    enable_privacy_policy = fields.Boolean("Show Privacy Policy on Sign up", config_parameter='signup.enable_privacy_policy')

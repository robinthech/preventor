# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class AuthSignupHome(AuthSignupHome):

    @http.route()
    def web_auth_signup(self, *args, **kw):
        response = super(AuthSignupHome, self).web_auth_signup(*args, **kw)

        enable_terms_of_service = request.env['ir.config_parameter'].sudo().get_param('signup.enable_terms_of_service')
        enable_privacy_policy = request.env['ir.config_parameter'].sudo().get_param('signup.enable_privacy_policy')
        response.qcontext.update({
            'enable_terms_of_service': enable_terms_of_service,
            'enable_privacy_policy': enable_privacy_policy
        })
        return response

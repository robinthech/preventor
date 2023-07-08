# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo.http import request
from odoo import http, _
from urllib import parse
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.main import ensure_db, Home
import logging
import werkzeug
from odoo.addons.auth_signup.models.res_users import SignupError

from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

from odoo.addons.auth_signup.controllers.main import Home
import json
import random
import werkzeug

class WebHome(Home):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):

                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)

                        return super(AuthSignupHome, self).web_login(*args, **kw)
                qcontext['success'] = _("Your registration successfully! Please wait for account approval.")
                email = qcontext.get('login')
                user_id = request.env['res.users'].sudo().search([('login','=',email)],limit=1)
                url = "/web/signup/verify/"+str(user_id.id)
                return werkzeug.utils.redirect(url)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values)
        user_id = request.env['res.users'].sudo().search([('login','=',values.get('login'))],limit=1)
        user_email_template = request.env.ref('sh_signup_email_approval.sh_user_mail_template', raise_if_not_found=False)
        if user_id and user_email_template:
            verification_number = random.randrange(1000, 9999)
            print("\n\n\n\n\nverification_number",verification_number)
            user_id.sudo().write({'verification_code':str(verification_number),'sh_password':qcontext.get('password')})
            user_email_template.sudo().send_mail(user_id.id, force_send=True)
        request.env.cr.commit()

    @http.route('/web/signup/verify/<int:user_id>', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
    def web_auth_signup_verify(self,user_id, *args, **kw):
        return request.render('sh_signup_email_approval.sh_signup_verfiy_template',{})

    @http.route('/web/signup/verify', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
    def web_auth_signup_verify_page(self,**kw):
        dic={}
        u_id = ''
        code = ''
        if kw.get('url'):
            url = str(kw.get('url'))
            split_url = url.split("/")
            u_id = split_url[-1]
        if kw.get('code'):
            code=kw.get('code')
        user_id = request.env['res.users'].sudo().search([('id','=',int(u_id))],limit=1)
        if user_id and code!='':
            if user_id.verification_code == code:
                user_id.sudo().write({
                    'sh_user_from_signup':True,
                    'parent_id':user_id.id,
                    'perfil':'1'
                    })
                planes = request.env["planes.planes"].sudo().search([('name',  '=',  'Plan Gratis')])
                for plan in planes:
                    request.env["res.users.plan"].sudo().create({"planes_id":plan.id,"user_id":user_id.id})

                redirect='/'
                uid = request.session.authenticate(request.session.db, user_id.login, user_id.sh_password)
                a = http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
                dic.update({
                    'success':'1',
                    })
            else:
                dic.update({
                    'error':'0',
                    'user_id':user_id.id,
                    })
        return json.dumps(dic)

    @http.route('/web/signup/error/verify', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
    def web_auth_signup_error_verify_page(self,**kw):
        dic={}
        u_id = ''
        code = ''
        if kw.get('url'):
            url = str(kw.get('url'))
            split_url = url.split("/")
            u_id = split_url[-1]
        user_id = request.env['res.users'].sudo().search([('id','=',int(u_id))],limit=1)
        if user_id:
            dic.update({
                'success':'1',
                'user_id':user_id.id,
                })
        return json.dumps(dic)

    @http.route('/web/signup/error/<int:user_id>', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
    def web_auth_signup_error(self,user_id,**kw):
        return request.render('sh_signup_email_approval.email_approval_sorry',{})

    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction

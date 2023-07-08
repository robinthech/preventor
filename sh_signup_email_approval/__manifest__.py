# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name' : 'Signup Email Verification',
    'author' : 'Softhealer Technologies',
    'website': 'http://www.softhealer.com',
    "support": "support@softhealer.com",
    'category': 'Website',
    'summary': """
Verify Email Signup, Email Verification Module, Sign-up Email Confirmation, Account Activate By Email, Log-in Email Verification,Sign-in Mail Verification, Signup Verification App, Log-in Verification, Email OTP Verification,Odoo E-mail Verification
                    """,
    'description': """
Whenever any user sign up, that will pass to the email verification process, the user can log in after email verification. For email, verification users have to verify with the verification code that sent in a user email address. It shows alert if you entered an invalid verification code. Only verified users can access the system.
 Signup Email Verification Odoo
 Verify Email At Signup Module, Email Verification, Email Confirmation On Sign-up, Account Activate By Email, Log-in Email Verification, Sign-in Mail Verification, Signup Verification Odoo
Verify Email At Signup, Email Verification  Module, Sign-up Email Confirmation, Account Activate By Email, Log-in Email Verification, Sign-in Mail Verification, Signup Verification App, Log-in Verification, Email OTP Verification, Odoo Email Verification, Odoo E-mail Verification, Mail OTP Odoo

                    """,
    'version':'13.0.1',
    'depends' : ['base', 'website','web','auth_signup','inherit_users'],
    'application' : True,
    'data' : [
            "data/user_mail_template.xml",
            'views/user_signup_approve_view.xml',
            "views/user_signup_template.xml",
            ],
    'images': ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/AUuwbuCwgGY",
    'auto_install':False,
    'installable' : True,
	"price": 35,
    "currency": "EUR"
}

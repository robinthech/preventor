# -*- coding: utf-8 -*-
{
    'name': "Signup With Terms & Conditions",

    'summary': """
        """,
    'version': '1.0',
    'description': """
        This module force new user to accept signup terms & conditions.
    """,
    'author': "Caretechr",
    'website': "https://caretechr.com",
    'category': 'Website',

    # any module necessary for this one to work correctly
    'depends': ['auth_signup', 'website'],

    # always loaded
    'data': [
        'views/res_config_settings_views.xml',
        'views/signup_template.xml',
        'views/terms_of_service.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': ['static/description/banner.png'],
    'price': 10,
    'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': '',
    'installable': True,
    'auto_install': False,
    'application': False,
}

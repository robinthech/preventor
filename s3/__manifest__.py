# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo S3',
    'version': '13.0.1.0.0',
    'author': 'HSE Golden Solution',
    'license': '',
    'category': 'Service',
    'depends': ['base'],
    'website': 'https://www.hsegoldensolution.com',
    'description': """  """,
    'summary': '',
    'depends': ['base',"website","website_permiso"],
    'data': [
        'security/security.xml',
        'views/sidebar.xml',
        'views/views.xml',
        'data/sequence.xml',
        'views/template.xml',
        'views/web_ilu.xml',
        'views/web_dosi.xml',
        'views/web_sono.xml',
        'views/web_site.xml',
        'views/web_reba.xml',
        'views/web_rosa.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}

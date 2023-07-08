# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo S3',
    'version': '13.0.1.0.0',
    'author': 'HSE Golden Solution',
    'license': '',
    'category': 'Service',
    'depends': ['base','website',],
    'website': 'https://www.hsegoldensolution.com',
    'description': """  """,
    'summary': '',
    'data': [
        'security/interno.xml',
        'security/portal.xml',
        'data/sequence.xml',
        'views/template.xml',
        'views/web_rosa.xml',
        'views/web_niosh.xml',
        'views/assets.xml',
    ],
    'installable': True,
    'auto_install': False,
}

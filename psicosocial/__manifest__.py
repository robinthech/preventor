# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Psicosocial',
    'version': '13.0.1.0.0',
    'author': 'HSE Golden Solution',
    'license': '',
    'category': 'Service',
    'website': 'https://www.hsegoldensolution.com',
    'description': """  """,
    'summary': '',
    'depends': ['base',"website","web"],
    'data': [
        'views/views.xml',
        'views/assets.xml',
        'views/templates.xml',
        'data/sequence.xml',
        'security/portal.xml',
        'security/registrador.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
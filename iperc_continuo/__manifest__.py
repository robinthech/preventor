# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'iperc_continuo',
    'version': '13.0.1.0.0',
    'author': 'HSE Golden Solution',
    'license': '',
    'category': 'Service',
    'website': 'https://www.hsegoldensolution.com',
    'description': """  """,
    'summary': '',
    'depends': ['base',"website"],
    'data': [
        'security/security.xml',
        'views/sidebar.xml',
        'views/templates.xml',
        'views/assets.xml',
        'views/views.xml',
        'reports/report.xml',
        'reports/iperc_continuo_report.xml',
        'data/data.xml',
        'data/sequence.xml',
    ],
    'installable': True,
    'auto_install': False,
}
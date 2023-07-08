# -*- coding: utf-8 -*-
{
    'name': "Auditoria Interna",
    'summary': """
        Website Auditoria Interna""",

    'description': """
        Para preventor
    """,
    'author': "PREVENTOR",
    'website': "http://preventor.tech",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base',"website","website_permiso"],
    'data': [
        'security/auditoria.xml',
        'data/secuencia.xml',
        'views/templates.xml',
        'views/assets.xml',
    ],
}

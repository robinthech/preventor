# -*- coding: utf-8 -*-
{
    'name': "lista_covid",
    'summary': """
        Website lista de vigilancia covid""",

    'description': """
        Lista de vigilancia covid
    """,
    'author': "APRENTECH",
    'website': "http://aprentech.tech",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','mail','board',"website","website_permiso"],
    'data': [
        'assets.xml',
        'data/data.xml',
        'security/security.xml',
        # 'security/permiso.xml',
        'views/views.xml',
        'templates/website.xml',
    ],
}

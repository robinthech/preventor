# -*- coding: utf-8 -*-
{
    'name': "registro_accidente",
    'summary': """
        Website Permisos de trabajo""",

    'description': """
        Permisos de trabajo
    """,
    'author': "APRENTECH",
    'website': "http://aprentech.tech",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','mail','board',"website","website_permiso"],
    'data': [
        'assets.xml',
        'security/security.xml',
        'security/permiso.xml',
        'data/secuencia.xml',
        'views/views.xml',
        'templates/sidebar.xml',
        'templates/website.xml',
        'templates/graph.xml',
    ],
    'qweb': [
        "static/src/xml/xml.xml",

    ],
}

# -*- coding: utf-8 -*-
{
    'name': "website_permiso",
    'summary': """
        Website Permisos de trabajo""",

    'description': """
        Permisos de trabajo
    """,
    'author': "APRENTECH",
    'website': "http://aprentech.tech",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','web','mail','board',"website","video_snippet","inherit_users"],
    'data': [
        'assets.xml',
        'security/security.xml',
        'security/permiso.xml',
        'security/portal.xml',
        'data/data.xml',
        'data/secuencia.xml',
        'views/views.xml',
        'views/requisitos.xml',
        'templates/website.xml',
        'templates/trabajador.xml',
        'templates/preventor.xml',
        'templates/sidebar.xml',
        'templates/requisitos.xml',
        'templates/sede_area.xml',
        'reports/report.xml',
        'reports/iperc_continuo_report.xml',
    ],
    'qweb': [
        "static/src/xml/xml.xml",

    ],
}

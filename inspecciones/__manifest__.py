# -*- coding: utf-8 -*-
{
    'name': "Inspecciones",

    'summary': """
        Inspecciones""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ROBINSON TORRES ",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sitio web',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website','web','website_permiso'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'templates/templates.xml',
        'templates/list.xml',
        'templates/substandar.xml',
        'templates/consolidado.xml',
        'templates/criticos.xml',
        'views/views.xml',
        'views/assets.xml',
        'reports/report.xml',
        'reports/inspecciones_report.xml',
    ],
    "qweb":[
        'inspecciones/static/src/xml/reporte_consolidado.xml',

    ],
}

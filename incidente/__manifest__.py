# -*- coding: utf-8 -*-
{
    'name': "Registro de incidentes de trabajo",

    'summary': """
        Registro de incidente de trabajo""",

    'author': "Preventor",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'data/secuencia.xml',
        'security/interno.xml',
        'security/portal.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/assets.xml',
    ],
}

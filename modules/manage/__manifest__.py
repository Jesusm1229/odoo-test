# -*- coding: utf-8 -*-
{
    'name': "manage module",

    'summary': "This is a module to manage",

    'description': """
Long description of module's purpose
    """,

    'author': "JesuS Medina",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # es importante el orden: primero el views y luego los propios
        'views/views.xml',
        'views/project_view.xml',
        'views/history_view.xml',
        'views/sprint_view.xml',
        'views/task.xml'
        'views/bug_view.xml',
        'views/improvement_view.xml',
        'views/dev_view.xml',
        'views/techonology_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}


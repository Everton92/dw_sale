# -*- coding: utf-8 -*-
{
    'name': "DW Sale",
    'license': 'AGPL-3', # TODO: Verificar se a licensa desejada será essa
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Everton Silva",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Vendas',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale',],

    # always loaded
    'data': [
        'data/cron.xml',
        'views/views.xml',
        # 'security/ir.model.access.csv',
        'report/dw_report_views.xml',
        # 'report/dw_report.xml',
        # 'report/dw_report_templates.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE SALE',
    'summary': '',
    'category': 'Sales',
    'version': '15.0.0.1',
    'sequence': -97,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'sales_team',
        'cgm_purchase',
        'sale_management',
        'sale_delivery_state',
        'currency_rate_live',
    ],
    'data': [
        # security
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        # report
        'report/stock_state_template.xml',
        'report/sale_report.xml',
        'report/sale_report_templates.xml',
        # views
        'views/sale_order_views.xml',
        'views/report_sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/sale_order_template_views.xml',
        'views/product_move_report_views.xml',
        'views/ir_ui_menu.xml',
        # data
        'data/mail_template_data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
